import os
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd

warnings.filterwarnings("ignore")

CLEAN_CSV = os.path.join("data", "superstore_clean.csv")
CHARTS_DIR = "charts"
ACCENT_COLOR = "#2563EB"

sns.set_theme(style="whitegrid", font_scale=1.1)
plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.bbox": "tight",
    "savefig.facecolor": "white",
})


def save_chart(fig, filename):
    os.makedirs(CHARTS_DIR, exist_ok=True)
    filepath = os.path.join(CHARTS_DIR, filename)
    fig.savefig(filepath)
    plt.close(fig)
    print(f"Saved → {filepath}")


def fmt_millions(x, _pos=None):
    if x >= 1_000_000:
        return f"${x / 1_000_000:.1f}M"
    if x >= 1_000:
        return f"${x / 1_000:.0f}K"
    return f"${x:.0f}"


def chart_sales_by_region(df):
    region_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(
        region_sales.index,
        region_sales.values,
        color=sns.color_palette("Blues_d", len(region_sales)),
        edgecolor="white",
        height=0.55,
    )
    for bar, val in zip(bars, region_sales.values):
        ax.text(
            val * 0.98, bar.get_y() + bar.get_height() / 2,
            fmt_millions(val), va="center", ha="right",
            fontsize=11, fontweight="bold", color="white",
        )
    ax.set_xlabel("Total Sales (USD)", fontsize=12)
    ax.set_title("Total Sales by Region", fontsize=15, fontweight="bold", pad=14)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_millions))
    ax.set_xlim(0, region_sales.max() * 1.12)
    ax.spines[["top", "right"]].set_visible(False)
    save_chart(fig, "01_sales_by_region.png")


def chart_top10_products(df):
    top10 = df.groupby("Product Name")["Sales"].sum().nlargest(10).sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(11, 6))
    bars = ax.barh(
        [name[:55] + "…" if len(name) > 55 else name for name in top10.index],
        top10.values,
        color=sns.color_palette("Blues_d", 10),
        edgecolor="white",
        height=0.65,
    )
    for bar, val in zip(bars, top10.values):
        ax.text(
            val + top10.max() * 0.01, bar.get_y() + bar.get_height() / 2,
            fmt_millions(val), va="center", ha="left", fontsize=10, fontweight="bold",
        )
    ax.set_xlabel("Total Sales (USD)", fontsize=12)
    ax.set_title("Top 10 Products by Sales", fontsize=15, fontweight="bold", pad=14)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_millions))
    ax.set_xlim(0, top10.max() * 1.22)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    save_chart(fig, "02_top10_products.png")


def chart_monthly_sales_trend(df):
    df = df.copy()
    df["YearMonth"] = df["Order Date"].dt.to_period("M")
    monthly = df.groupby("YearMonth")["Sales"].sum().reset_index()
    monthly["YearMonth"] = monthly["YearMonth"].dt.to_timestamp()

    fig, ax = plt.subplots(figsize=(13, 5))
    ax.plot(
        monthly["YearMonth"], monthly["Sales"],
        color=ACCENT_COLOR, linewidth=2.2, marker="o",
        markersize=4, markerfacecolor="white", markeredgewidth=1.5,
    )
    ax.fill_between(monthly["YearMonth"], monthly["Sales"], alpha=0.12, color=ACCENT_COLOR)
    ax.set_xlabel("Month", fontsize=12)
    ax.set_ylabel("Sales (USD)", fontsize=12)
    ax.set_title("Monthly Sales Trend", fontsize=15, fontweight="bold", pad=14)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_millions))
    ax.spines[["top", "right"]].set_visible(False)
    fig.autofmt_xdate(rotation=45, ha="right")
    plt.tight_layout()
    save_chart(fig, "03_monthly_sales_trend.png")


def chart_heatmap_category_subcategory(df):
    pivot = (
        df.groupby(["Category", "Sub-Category"])["Sales"]
        .sum()
        .unstack(level=0)
        .fillna(0)
    )
    pivot_k = pivot / 1_000

    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(
        pivot_k, annot=True, fmt=".1f", cmap="Blues",
        linewidths=0.5, linecolor="white", ax=ax,
        cbar_kws={"label": "Sales ($000s)", "shrink": 0.8},
    )
    ax.set_title("Sales by Category and Sub-Category ($000s)", fontsize=14, fontweight="bold", pad=14)
    ax.set_xlabel("Category", fontsize=12)
    ax.set_ylabel("Sub-Category", fontsize=12)
    plt.tight_layout()
    save_chart(fig, "04_heatmap_category_subcategory.png")


def chart_profit_by_segment(df):
    seg_profit = df.groupby("Segment")["Profit"].sum().sort_values(ascending=False).reset_index()
    colors = ["#1D4ED8" if v >= 0 else "#DC2626" for v in seg_profit["Profit"]]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(seg_profit["Segment"], seg_profit["Profit"], color=colors, edgecolor="white", width=0.5)
    for bar, val in zip(bars, seg_profit["Profit"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            val + abs(seg_profit["Profit"].max()) * 0.015,
            fmt_millions(val), ha="center", va="bottom", fontsize=12, fontweight="bold",
        )
    ax.set_xlabel("Customer Segment", fontsize=12)
    ax.set_ylabel("Total Profit (USD)", fontsize=12)
    ax.set_title("Total Profit by Customer Segment", fontsize=15, fontweight="bold", pad=14)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_millions))
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    save_chart(fig, "05_profit_by_segment.png")


def main():
    if not os.path.exists(CLEAN_CSV):
        raise FileNotFoundError(f"'{CLEAN_CSV}' not found. Run data_cleaning.py first.")

    df = pd.read_csv(CLEAN_CSV, parse_dates=["Order Date", "Ship Date"])
    print(f"Loaded {len(df):,} rows.")

    chart_sales_by_region(df)
    chart_top10_products(df)
    chart_monthly_sales_trend(df)
    chart_heatmap_category_subcategory(df)
    chart_profit_by_segment(df)

    print(f"All charts saved to '{CHARTS_DIR}/'.")


if __name__ == "__main__":
    main()
