# Blinkit Grocery Sales Analysis

A data analysis project on Blinkit's grocery sales data, covering SQL-based KPI reporting, Python-based outlet and item segmentation, a simulated experimentation framework, and an interactive Power BI dashboard.

## Overview

This project analyzes 8,500+ records of grocery sales across 10 outlets and 16 item types to uncover sales drivers, segment performance tiers, and test whether item visibility meaningfully impacts sales. It combines three layers of analysis:

1. **SQL layer**: KPI reporting and granular breakdowns (sales by outlet, item type, fat content, location, and establishment year)
2. **Python layer**: K-Means clustering for segmentation, a simulated A/B test on item visibility, and correlation analysis
3. **Power BI layer**: An interactive dashboard for exploring sales, products, and outlet performance

## 📊 Dataset Overview

The dataset contains **8,523 grocery sales records** across **10 outlets** and **16 item types**, with product details, outlet information, sales, and ratings.

**Dataset file:** `BlinkIT-Grocery-Data.csv.csv`

### 📋 Dataset Columns

| No. | Column Name | Description |
|:---:|-------------|-------------|
| 1 | **Item Fat Content** | Fat category of the product, such as Low Fat or Regular |
| 2 | **Item Identifier** | Identifier assigned to each product |
| 3 | **Item Type** | Product category, such as Dairy or Fruits and Vegetables |
| 4 | **Outlet Establishment Year** | Year in which the outlet was established |
| 5 | **Outlet Identifier** | Identifier assigned to each outlet |
| 6 | **Outlet Location Type** | Location tier of the outlet: Tier 1, Tier 2, or Tier 3 |
| 7 | **Outlet Size** | Size category of the outlet |
| 8 | **Outlet Type** | Type of outlet, such as Grocery Store or Supermarket |
| 9 | **Item Visibility** | Measure of the product's visibility in the outlet |
| 10 | **Item Weight** | Weight of the product |
| 11 | **Total Sales** | Sales value associated with the record |
| 12 | **Rating** | Rating associated with the record |

### 🔢 Dataset Summary

| Metric | Value |
|--------|------:|
| 📦 Total Records | **8,523** |
| 🏬 Total Outlets | **10** |
| 🛒 Item Types | **16** |
| 📑 Columns | **12** |

## Part 1: SQL Analysis (`SQLQuery.sql`)

Cleans inconsistent fat content labels and computes core KPIs (total sales, average sales, item count, average rating), then breaks each down by fat content, item type, outlet location, outlet size, outlet establishment year, and outlet type.

## Part 2: Advanced Analytics (`blinkit_advanced_analytics(1).py`)

### 1. K-Means Clustering: Outlet Segmentation
Outlets were grouped into three performance tiers (High-Performer, Mid-Tier, Underperforming) using average sales, visibility, and rating as features. The elbow method was used to select k=3.

### 2. K-Means Clustering: Item Segmentation
Individual items were clustered into four groups based on sales, visibility, and rating, separating consistently high-performing items from low-performing and niche ones.

### 3. A/B Test Simulation: Item Visibility vs Sales
Items were split into a high-visibility group (at or above the median) and a low-visibility group (below the median), then compared using an independent t-test. This is an observational comparison, not a randomized experiment, so it does not establish causation.

- Test group mean sales: 142.94
- Control group mean sales: 139.05
- t-statistic: 2.886, p-value: 0.0039 (statistically significant)
- Cohen's d: 0.063 (negligible effect size)

**Takeaway**: the difference is statistically significant due to the large sample size, but the practical effect is very small. Visibility alone is not a strong lever for sales.

### 4. Correlation and Feature Driver Analysis
Correlation of Sales with item visibility, item weight, rating, and outlet establishment year was close to zero across the board, meaning no single numeric feature is a strong linear driver of sales on its own. Categorical breakdowns (outlet type, fat content) show only minor variation in average sales.

## Part 3: Power BI Dashboard (`Blinkit-Sales-Dashboard.pbix`)

The interactive dashboard brings the key sales and outlet measures together in one view.



### Dashboard KPIs

- **Total sales:** $1.20M
- **Average sales:** $141
- **Number of items:** 8,523
- **Average rating:** 3.9

### Dashboard Features

- Filters for **outlet location type**, **outlet size**, and **item type**.
- Sales breakdowns by **fat content**, **item type**, **outlet size**, and **outlet location**.
- Sales by **outlet establishment year** and fat content by outlet location.
- An outlet-type comparison showing total sales, item count, average sales, average rating, and item visibility.
- Metric selection for total sales, average sales, item count, and average rating.

Open `Blinkit-Sales-Dashboard.pbix` in Power BI Desktop to explore the dashboard and apply filters. The figures above reflect the dashboard shown with all filters selected.

## Key Insights

- Outlet-level sales differences are small in absolute terms but clear enough to support a 3-tier segmentation.
- Item visibility has a statistically detectable but practically negligible relationship with sales.
- No individual numeric feature strongly predicts sales, although this does not establish which factors cause sales differences.
- Supermarket Type2 and Type1 outlets slightly outperform Grocery Store and Type3 outlets on average sales.

## Tech Stack

- **SQL**: data cleaning, KPI aggregation, grouped reporting
- **Python**: pandas, NumPy, scikit-learn (K-Means, StandardScaler), SciPy (t-test), Matplotlib
- **Power BI**: interactive dashboard, KPI cards, filters, and visualizations

## Files

```text
SQLQuery.sql                         SQL cleaning and KPI queries
blinkit_advanced_analytics(1).py     K-Means clustering, visibility comparison, correlation analysis
BlinkIT-Grocery-Data.csv.csv         Source dataset
Blinkit Objectives.txt              Project objectives
Blinkit-Sales-Dashboard.pbix        Power BI dashboard file
Blinkit-sales-Dashboard(1).png      Dashboard preview
requirements.txt                    Python dependencies
output/                             Charts generated when the Python script runs
  outlet_elbow.png                  Elbow plot for outlet clustering
  item_clusters.png                 Item segmentation scatter plot
  ab_test_visibility.png            Visibility group box plot
  correlation_heatmap.png           Feature correlation heatmap
```

## How to Run

```bash
pip install -r requirements.txt
python "blinkit_advanced_analytics(1).py"
```

Keep the Python script and CSV file in the same folder. Run `SQLQuery.sql` in a compatible SQL environment after importing the dataset as `blinkit_data` with the column names used in the script. Open the `.pbix` file in Power BI Desktop; if prompted, update the data source path to your local dataset.

## Author

Nawed Ashraf


[def]: Blinkit-sales-Dashboard%281%29.png