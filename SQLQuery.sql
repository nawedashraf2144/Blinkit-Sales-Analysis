-- 1. Display all records from Blinkit dataset
SELECT * FROM blinkit_data;


-- 2. Clean the Item_Fat_Content column
-- Replace LF and low fat with Low Fat
-- Replace reg with Regular

UPDATE blinkit_data
SET Item_Fat_Content =
CASE 
    WHEN Item_Fat_Content IN ('LF', 'low fat') THEN 'Low Fat'
    WHEN Item_Fat_Content = 'reg' THEN 'Regular'
    ELSE Item_Fat_Content
END;


-- 3. Check distinct values after data cleaning
SELECT DISTINCT Item_Fat_Content
FROM blinkit_data;


-- 4. Calculate total sales in millions
SELECT
    CAST(SUM(Total_Sales) / 1000000.0 AS DECIMAL(10,2))
    AS Total_Sales_Million
FROM blinkit_data;


-- 5. Calculate average sales
SELECT
    CAST(AVG(Total_Sales) AS INT) AS Avg_Sales
FROM blinkit_data;


-- 6. Calculate total number of orders/items
SELECT
    COUNT(*) AS No_of_Orders
FROM blinkit_data;


-- 7. Calculate average rating
SELECT
    CAST(AVG(Rating) AS DECIMAL(10,1)) AS Avg_Rating
FROM blinkit_data;


-- 8. Calculate total sales, average sales, number of items
-- and average rating for each fat content category
SELECT Item_Fat_Content,
       CAST(SUM(Total_Sales)/1000 AS DECIMAL(10,2))
       AS Total_Sales_Thousands,
       CAST(AVG(Total_Sales) AS DECIMAL(10,1))
       AS Avg_Sales,
       COUNT(*) AS No_Of_Items,
       CAST(AVG(Rating) AS DECIMAL(10,1))
       AS Avg_Rating
FROM blinkit_data
GROUP BY Item_Fat_Content
ORDER BY Total_Sales_Thousands DESC;


-- 9. Calculate total sales, average sales, number of items, and average rating for each Item Type, grouping by Item_Type and displaying the highest sales first.

SELECT Item_Type,
       CAST(SUM(Total_Sales) AS DECIMAL(10,2)) AS Total_Sales,
       CAST(AVG(Total_Sales) AS DECIMAL(10,1)) AS Avg_Sales,
       COUNT(*) AS No_Of_Items,
       CAST(AVG(Rating) AS DECIMAL(10,1)) AS Avg_Rating
FROM blinkit_data
GROUP BY Item_Type
ORDER BY Total_Sales DESC;

-- 10. Calculate total sales for Low Fat and Regular items across each Outlet Location Type using PIVOT, replace NULL values with 0, and sort by Outlet Location Type.

SELECT Outlet_Location_Type,
       ISNULL([Low Fat], 0) AS Low_Fat,
       ISNULL([Regular], 0) AS Regular
FROM
(
    SELECT Outlet_Location_Type, Item_Fat_Content,
           CAST(SUM(Total_Sales) AS DECIMAL(10,2)) AS Total_Sales
    FROM blinkit_data
    GROUP BY Outlet_Location_Type, Item_Fat_Content
) AS SourceTable
PIVOT
(
    SUM(Total_Sales)
    FOR Item_Fat_Content IN ([Low Fat], [Regular])
) AS PivotTable
ORDER BY Outlet_Location_Type;

 -- 11. Calculate total sales, average sales, number of items, and average rating for each Outlet Establishment Year, and display the highest sales first.

SELECT Outlet_Establishment_Year,
       CAST(SUM(Total_Sales) AS DECIMAL(10,2)) AS Total_Sales,
       CAST(AVG(Total_Sales) AS DECIMAL(10,1)) AS Avg_Sales,
       COUNT(*) AS No_Of_Items,
       CAST(AVG(Rating) AS DECIMAL(10,2)) AS Avg_Rating
FROM blinkit_data
GROUP BY Outlet_Establishment_Year
ORDER BY Total_Sales DESC;

-- 12. Calculate total sales and sales percentage for each Outlet Size, and display the highest sales first.

SELECT
       Outlet_Size,
       CAST(SUM(Total_Sales) AS DECIMAL(10,2)) AS Total_Sales,
       CAST((SUM(Total_Sales) * 100.0 / SUM(SUM(Total_Sales)) OVER()) AS DECIMAL(10,2)) AS Sales_Percentage
FROM blinkit_data
GROUP BY Outlet_Size
ORDER BY Total_Sales DESC;

-- 13. Calculate total sales, sales percentage, average sales, number of items, and average rating for each Outlet Location Type, and display the highest sales first.

SELECT Outlet_Location_Type,
       CAST(SUM(Total_Sales) AS DECIMAL(10,2)) AS Total_Sales,
       CAST((SUM(Total_Sales) * 100.0 / SUM(SUM(Total_Sales)) OVER()) AS DECIMAL(10,2)) AS Sales_Percentage,
       CAST(AVG(Total_Sales) AS DECIMAL(10,1)) AS Avg_Sales,
       COUNT(*) AS No_Of_Items,
       CAST(AVG(Rating) AS DECIMAL(10,2)) AS Avg_Rating
FROM blinkit_data
GROUP BY Outlet_Location_Type
ORDER BY Total_Sales DESC;

-- 14. Calculate total sales, sales percentage, average sales, number of items, and average rating for each Outlet Type, and display the highest sales first.

SELECT Outlet_Type,
       CAST(SUM(Total_Sales) AS DECIMAL(10,2)) AS Total_Sales,
       CAST((SUM(Total_Sales) * 100.0 / SUM(SUM(Total_Sales)) OVER()) AS DECIMAL(10,2)) AS Sales_Percentage,
       CAST(AVG(Total_Sales) AS DECIMAL(10,1)) AS Avg_Sales,
       COUNT(*) AS No_Of_Items,
       CAST(AVG(Rating) AS DECIMAL(10,2)) AS Avg_Rating
FROM blinkit_data
GROUP BY Outlet_Type
ORDER BY Total_Sales DESC;





