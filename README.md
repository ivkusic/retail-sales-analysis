# Superstore Sales Analysis

A beginner-friendly end-to-end data analysis project using the classic
**Sample Superstore** dataset. The project covers data cleaning, SQL-based
exploration, and Python visualizations — ideal for building a portfolio or
learning the data analytics workflow.

---

## Dataset

| Property | Detail |
|---|---|
| **Name** | Sample Superstore |
| **Source** | [leonism/sample-superstore on GitHub](https://github.com/leonism/sample-superstore) |
| **Direct URL** | `https://raw.githubusercontent.com/leonism/sample-superstore/master/data/superstore.csv` |
| **Rows** | ~9,994 orders |
| **Columns** | 21 (Row ID, Order ID, Order Date, Ship Date, Ship Mode, Customer ID, Customer Name, Segment, Country, City, State, Postal Code, Region, Product ID, Category, Sub-Category, Product Name, Sales, Quantity, Discount, Profit) |

The dataset represents four years of US retail orders across three product
categories: **Furniture**, **Office Supplies**, and **Technology**.

---

## Project Structure

```
superstore-sales-project/
│
├── data_cleaning.py          # Download, clean, and feature-engineer the data
├── analysis.sql              # Six SQLite-compatible analytical queries
├── visualizations.py         # Five matplotlib/seaborn charts
├── requirements.txt          # Python package dependencies
├── README.md                 # This file
│
├── data/
│   ├── superstore_raw.csv    # Downloaded automatically by data_cleaning.py
│   └── superstore_clean.csv  # Output of data_cleaning.py (used by charts)
│
└── charts/
    ├── 01_sales_by_region.png
    ├── 02_top10_products.png
    ├── 03_monthly_sales_trend.png
    ├── 04_heatmap_category_subcategory.png
    └── 05_profit_by_segment.png
```

---

## How to Run

### 1. Prerequisites

- Python 3.8 or higher
- pip

### 2. Clone or download the project

```bash
git clone https://github.com/your-username/superstore-sales-project.git
cd superstore-sales-project
```

Or simply copy the project folder to your machine.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Clean the data

This step downloads the CSV, cleans it, adds engineered columns, and saves
the result.

```bash
python data_cleaning.py
```

Expected output:
```
Downloading dataset...
Loaded 9,994 rows and 21 columns.
No null values found.
DUPLICATE ROWS: 0
Converting date columns...
Adding 'Profit Margin %' column...
Adding 'Days to Ship' column...
Cleaned data saved to: data/superstore_clean.csv
```

### 5. Generate charts

```bash
python visualizations.py
```

Five PNG files will appear in the `charts/` folder.

### 6. Run SQL queries (optional)

**Option A — SQLite CLI**

```bash
sqlite3 superstore.db
```

Inside the SQLite shell:

```sql
.mode csv
.headers on
.import data/superstore_clean.csv superstore
-- then paste any query from analysis.sql
```

**Option B — Python (pandas + sqlite3)**

```python
import pandas as pd
import sqlite3

df = pd.read_csv("data/superstore_clean.csv")
con = sqlite3.connect("superstore.db")
df.to_sql("superstore", con, if_exists="replace", index=False)

result = pd.read_sql("""
    SELECT region, ROUND(SUM(sales),2) AS total_sales
    FROM superstore
    GROUP BY region
    ORDER BY total_sales DESC
""", con)
print(result)
```

---

## What Each Script Does

### `data_cleaning.py`

| Step | Action |
|---|---|
| Download | Fetches CSV from GitHub using `urllib` |
| Load | Reads into a pandas DataFrame |
| Inspect | Reports null counts and duplicate rows |
| Parse dates | Converts `Order Date` and `Ship Date` from string to `datetime` |
| Feature: Profit Margin % | `Profit / Sales * 100`, rounded to 2 decimal places |
| Feature: Days to Ship | `Ship Date - Order Date` in calendar days |
| De-duplicate | Drops exact duplicate rows |
| Save | Writes `data/superstore_clean.csv` |

### `analysis.sql`

| Query | Description |
|---|---|
| 1 | Total sales and profit by **Region** |
| 2 | Top 10 **Products** by sales |
| 3 | **Monthly** sales trend |
| 4 | Sales by **Category** and **Sub-Category** |
| 5 | Average **discount** by customer Segment |
| 6 | Top 5 **States** by profit |

### `visualizations.py`

| Chart | Type | Insight |
|---|---|---|
| 01 | Horizontal bar | Which region generates the most revenue? |
| 02 | Horizontal bar | Which products are the top sellers? |
| 03 | Line + fill | How do sales fluctuate month over month? |
| 04 | Heatmap | Where is revenue concentrated across categories? |
| 05 | Vertical bar | Which customer segment is most profitable? |

---

## Charts Preview

After running `visualizations.py`, you will find these charts in the
`charts/` folder:

| File | Description |
|---|---|
| `01_sales_by_region.png` | Total Sales by Region |
| `02_top10_products.png` | Top 10 Products by Sales |
| `03_monthly_sales_trend.png` | Monthly Sales Trend (2014–2017) |
| `04_heatmap_category_subcategory.png` | Sales Heatmap — Category × Sub-Category |
| `05_profit_by_segment.png` | Total Profit by Customer Segment |

---

## Tools Used

| Tool | Purpose |
|---|---|
| Python 3 | Core scripting language |
| pandas | Data loading, cleaning, and transformation |
| matplotlib | Chart rendering |
| seaborn | Statistical chart styling |
| SQLite | Lightweight SQL database for queries |
| urllib (stdlib) | Downloading the dataset (no extra install) |

---

## Author

**[Your Name]**
[your.email@example.com](mailto:your.email@example.com)
[GitHub](https://github.com/your-username) | [LinkedIn](https://linkedin.com/in/your-profile)

---

*Dataset originally sourced from the Tableau Sample Superstore workbook and
hosted publicly on GitHub.*
