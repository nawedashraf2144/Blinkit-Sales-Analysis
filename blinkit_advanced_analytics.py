"""
Author: Nawed Ashraf
"""

# %% Setup and imports
import os
from pathlib import Path

os.environ.setdefault('OMP_NUM_THREADS', '1')

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy import stats
import matplotlib.pyplot as plt

pd.set_option('display.width', 120)

# %% Load and clean data
# ------------------------------------------------------------------------------------------------------------------ #
#                                                  Load & Clean                                                      #
# ------------------------------------------------------------------------------------------------------------------ #
script_dir = Path(__file__).resolve().parent
csv_path = script_dir / 'BlinkIT-Grocery-Data.csv.csv'
df = pd.read_csv(csv_path)

# This workspace's CSV names the sales column "Total Sales".
if 'Sales' not in df.columns and 'Total Sales' in df.columns:
    df = df.rename(columns={'Total Sales': 'Sales'})

output_dir = script_dir / 'output'
output_dir.mkdir(parents=True, exist_ok=True)

# Same cleaning logic as the SQL script (standardize Fat Content labels)
df['Item Fat Content'] = df['Item Fat Content'].replace({
    'reg': 'Regular',
    'LF': 'Low Fat',
    'low fat': 'Low Fat'
})

# Item Weight has ~1.4K missing values — impute with the item-type median so the
# clustering/correlation steps don't silently drop ~17% of rows
df['Item Weight'] = df.groupby('Item Type')['Item Weight'].transform(
    lambda x: x.fillna(x.median())
)

print(f"Rows: {len(df)} | Outlets: {df['Outlet Identifier'].nunique()} | Item Types: {df['Item Type'].nunique()}")


# ==================================================================================================================== #
# %%
#  1. K-MEANS CLUSTERING — OUTLET SEGMENTATION                                                                        #
#     Objective: Segment the 10 outlets into performance tiers using Sales, Visibility, and Rating —                 #
#     mirrors real-world "high performer / underperforming / niche" audience-segmentation logic.                     #
# ==================================================================================================================== #

outlet_agg = df.groupby('Outlet Identifier').agg(
    Avg_Sales=('Sales', 'mean'),
    Total_Sales=('Sales', 'sum'),
    Avg_Visibility=('Item Visibility', 'mean'),
    Avg_Rating=('Rating', 'mean'),
    Item_Count=('Item Identifier', 'count')
).reset_index()

features = ['Avg_Sales', 'Avg_Visibility', 'Avg_Rating']
X = StandardScaler().fit_transform(outlet_agg[features])

# Elbow method to justify k
inertias = []
for k in range(1, 7):
    km = KMeans(n_clusters=k, random_state=42, n_init=10).fit(X)
    inertias.append(km.inertia_)

plt.figure(figsize=(6, 4))
plt.plot(range(1, 7), inertias, marker='o')
plt.title('Elbow Method — Outlet Segmentation')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.tight_layout()
plt.savefig(output_dir / 'outlet_elbow.png', dpi=120)
plt.show()
plt.close()

# k=3 chosen from elbow: High-Performer / Mid-Tier / Underperforming
kmeans_outlet = KMeans(n_clusters=3, random_state=42, n_init=10)
outlet_agg['Cluster'] = kmeans_outlet.fit_predict(X)

# Label clusters by their average sales rank (data-driven, not hardcoded)
cluster_rank = outlet_agg.groupby('Cluster')['Avg_Sales'].mean().sort_values(ascending=False)
labels = {cluster_rank.index[0]: 'High-Performer', cluster_rank.index[1]: 'Mid-Tier', cluster_rank.index[2]: 'Underperforming'}
outlet_agg['Segment'] = outlet_agg['Cluster'].map(labels)

print("\n=== Outlet Segmentation (K-Means, k=3) ===")
print(outlet_agg[['Outlet Identifier', 'Avg_Sales', 'Avg_Visibility', 'Avg_Rating', 'Segment']]
      .sort_values('Avg_Sales', ascending=False).to_string(index=False))


# ==================================================================================================================== #
# %%
#  2. K-MEANS CLUSTERING — ITEM SEGMENTATION                                                                          #
#     Objective: Cluster individual items by Sales + Visibility + Rating into performance tiers,                     #
#     useful for prioritizing which item types to promote / de-prioritize.                                           #
# ==================================================================================================================== #

item_features = ['Sales', 'Item Visibility', 'Rating']
Xi = StandardScaler().fit_transform(df[item_features])

kmeans_item = KMeans(n_clusters=4, random_state=42, n_init=10)
df['Item_Cluster'] = kmeans_item.fit_predict(Xi)

item_cluster_summary = df.groupby('Item_Cluster').agg(
    Avg_Sales=('Sales', 'mean'),
    Avg_Visibility=('Item Visibility', 'mean'),
    Avg_Rating=('Rating', 'mean'),
    Count=('Item Identifier', 'count')
).sort_values('Avg_Sales', ascending=False)

print("\n=== Item Segmentation (K-Means, k=4) ===")
print(item_cluster_summary.to_string())

# Scatter plot: Sales vs Visibility colored by cluster
plt.figure(figsize=(7, 5))
scatter = plt.scatter(df['Item Visibility'], df['Sales'], c=df['Item_Cluster'], cmap='viridis', alpha=0.5, s=10)
plt.xlabel('Item Visibility')
plt.ylabel('Sales')
plt.title('Item Segmentation — Sales vs Visibility (K-Means, k=4)')
plt.colorbar(scatter, label='Cluster')
plt.tight_layout()
plt.savefig(output_dir / 'item_clusters.png', dpi=120)
plt.show()
plt.close()


# ==================================================================================================================== #
# %%
#  3. A/B TESTING SIMULATION — DOES HIGH VISIBILITY SIGNIFICANTLY INCREASE SALES?                                     #
#     Objective: Simulate an experimentation framework by treating items above/below median visibility               #
#     as "Test" (High Visibility) vs "Control" (Low Visibility) groups, then run an independent t-test.              #
# ==================================================================================================================== #

median_vis = df['Item Visibility'].median()
group_high = df[df['Item Visibility'] >= median_vis]['Sales']
group_low = df[df['Item Visibility'] < median_vis]['Sales']

t_stat, p_value = stats.ttest_ind(group_high, group_low, equal_var=False)

# Effect size (Cohen's d) so the result isn't just "significant" but also sized
pooled_std = np.sqrt((group_high.std() ** 2 + group_low.std() ** 2) / 2)
cohens_d = (group_high.mean() - group_low.mean()) / pooled_std

print("\n=== A/B Test Simulation: High vs Low Item Visibility ===")
print(f"Test group  (High Visibility, n={len(group_high)}): Mean Sales = {group_high.mean():.2f}")
print(f"Control group (Low Visibility, n={len(group_low)}): Mean Sales = {group_low.mean():.2f}")
print(f"t-statistic = {t_stat:.3f} | p-value = {p_value:.4f} | Cohen's d = {cohens_d:.3f}")

if p_value < 0.05:
    direction = "LOWER" if group_high.mean() < group_low.mean() else "HIGHER"
    print(f"Result: Statistically significant (p < 0.05). High-visibility items show {direction} average sales.")
else:
    print("Result: No statistically significant difference at the 95% confidence level.")

# Box plot for the write-up / dashboard
plt.figure(figsize=(6, 4))
plt.boxplot([group_low, group_high], tick_labels=['Low Visibility (Control)', 'High Visibility (Test)'], showfliers=False)
plt.ylabel('Sales')
plt.title('A/B Test: Sales by Visibility Group')
plt.tight_layout()
plt.savefig(output_dir / 'ab_test_visibility.png', dpi=120)
plt.show()
plt.close()


# ==================================================================================================================== #
# %%
#  4. CORRELATION / FEATURE-DRIVER ANALYSIS — WHAT ACTUALLY DRIVES SALES?                                             #
#     Objective: Quantify which numeric features correlate with Sales, and how Sales varies                          #
#     across key categorical drivers (Outlet Type, Fat Content).                                                     #
# ==================================================================================================================== #

numeric_cols = ['Sales', 'Item Visibility', 'Item Weight', 'Rating', 'Outlet Establishment Year']
corr_matrix = df[numeric_cols].corr()

print("\n=== Correlation Matrix (numeric features vs Sales) ===")
print(corr_matrix['Sales'].sort_values(ascending=False).to_string())

plt.figure(figsize=(6, 5))
plt.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
plt.xticks(range(len(numeric_cols)), numeric_cols, rotation=45, ha='right')
plt.yticks(range(len(numeric_cols)), numeric_cols)
for i in range(len(numeric_cols)):
    for j in range(len(numeric_cols)):
        plt.text(j, i, f"{corr_matrix.iloc[i, j]:.2f}", ha='center', va='center', fontsize=8)
plt.colorbar(label='Correlation')
plt.title('Feature Correlation with Sales')
plt.tight_layout()
plt.savefig(output_dir / 'correlation_heatmap.png', dpi=120)
plt.show()
plt.close()

# Categorical driver: Sales by Outlet Type
outlet_type_sales = df.groupby('Outlet Type')['Sales'].mean().sort_values(ascending=False)
print("\n=== Avg Sales by Outlet Type ===")
print(outlet_type_sales.to_string())

# Categorical driver: Sales by Fat Content
fat_sales = df.groupby('Item Fat Content')['Sales'].mean().sort_values(ascending=False)
print("\n=== Avg Sales by Fat Content ===")
print(fat_sales.to_string())

print("\nCharts saved to /output: outlet_elbow.png, item_clusters.png, ab_test_visibility.png, correlation_heatmap.png")
