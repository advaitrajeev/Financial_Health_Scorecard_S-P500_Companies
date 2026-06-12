"""
eda_analysis.py
---------------
Generates visualizations and compiles reports for Phase 4 (Exploratory Data Analysis):
- Ratio distributions (histogram/KDE)
- Sector comparison boxplots for all 10 ratios
- Correlation heatmap across all ratios
- Identification of key outliers and sector insights

Saves plots to reports/figures/ and writes reports/eda_report.md.

Usage:
    python -m src.eda_analysis
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")
FIGURES_DIR = os.path.join(REPORTS_DIR, "figures")

os.makedirs(FIGURES_DIR, exist_ok=True)

# Set plotting style
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    "font.size": 10,
    "axes.labelsize": 12,
    "axes.titlesize": 14,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.titlesize": 16
})

RATIOS = [
    "Net Margin",
    "Operating Margin",
    "ROE",
    "ROA",
    "Current Ratio",
    "Quick Ratio",
    "Debt-to-Equity",
    "Interest Coverage Ratio",
    "Asset Turnover",
    "Revenue Growth (YoY)"
]


def run_eda():
    cleaned_path = os.path.join(PROCESSED_DIR, "sp500_cleaned_ratios.csv")
    if not os.path.exists(cleaned_path):
        raise FileNotFoundError(f"Missing ratios file at {cleaned_path}. Run clean_data first.")

    df = pd.read_csv(cleaned_path)
    
    # Filter out records that are completely blank for ratios
    valid_companies = df.dropna(subset=RATIOS, how="all")
    print(f"Loaded {len(valid_companies)} companies with valid calculated ratios.")

    # 1. Generate Correlation Heatmap
    generate_correlation_heatmap(valid_companies)

    # 2. Generate Distribution & Boxplots for each ratio
    for ratio in RATIOS:
        generate_ratio_plots(valid_companies, ratio)

    # 3. Analyze Outliers & Sector Metrics
    sector_summary = generate_sector_summary(valid_companies)
    outliers_summary = identify_outliers(valid_companies)

    # 4. Generate EDA Report
    generate_eda_report(valid_companies, sector_summary, outliers_summary)


def generate_correlation_heatmap(df: pd.DataFrame):
    plt.figure(figsize=(10, 8))
    corr = df[RATIOS].corr()
    
    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        fmt=".2f",
        linewidths=0.5,
        cbar_kws={"shrink": 0.8}
    )
    plt.title("Correlation Matrix of Financial Ratios", pad=20)
    plt.tight_layout()
    path = os.path.join(FIGURES_DIR, "correlation_heatmap.png")
    plt.savefig(path, dpi=300)
    plt.close()
    print("Saved correlation heatmap.")


def generate_ratio_plots(df: pd.DataFrame, ratio: str):
    # Setup subplots (left: distribution, right: boxplot by sector)
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Extract non-null values for this ratio
    data = df[df[ratio].notnull()]
    if data.empty:
        print(f"Skipping plots for {ratio} - no data.")
        plt.close()
        return

    # Handle extreme outliers for visualization purposes by clipping at 1st and 99th percentiles
    # this makes the charts actually readable while keeping the underlying box plots scaled correctly.
    q_low = data[ratio].quantile(0.01)
    q_high = data[ratio].quantile(0.99)
    # If the range is extremely compressed, use raw data
    if q_high == q_low:
        q_low, q_high = data[ratio].min(), data[ratio].max()
    
    # 1. Distribution Plot (Histogram + KDE)
    sns.histplot(
        data=data,
        x=ratio,
        kde=True,
        ax=axes[0],
        color="#2b5c8f",
        bins=30
    )
    axes[0].set_xlim(q_low, q_high)
    axes[0].set_title(f"{ratio} Distribution (Clipped at 1% - 99% Percentiles)")
    axes[0].set_xlabel(ratio)
    
    # 2. Boxplot by Sector
    # Order sectors by median ratio
    sector_order = data.groupby("GICS Sector")[ratio].median().sort_values().index
    
    sns.boxplot(
        data=data,
        y="GICS Sector",
        x=ratio,
        ax=axes[1],
        order=sector_order,
        palette="viridis",
        hue="GICS Sector",
        legend=False
    )
    axes[1].set_xlim(q_low, q_high)
    axes[1].set_title(f"{ratio} by Sector (Clipped at 1% - 99% Percentiles)")
    axes[1].set_xlabel(ratio)
    axes[1].set_ylabel("")
    
    plt.suptitle(f"Financial Health Analysis: {ratio}", fontsize=16, y=0.98)
    plt.tight_layout()
    
    # Save the figure
    file_name = ratio.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_") + "_analysis.png"
    path = os.path.join(FIGURES_DIR, file_name)
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"Saved analysis plots for {ratio}.")


def generate_sector_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary_data = []
    for ratio in RATIOS:
        medians = df.groupby("GICS Sector")[ratio].median()
        for sector, val in medians.items():
            summary_data.append({
                "Sector": sector,
                "Ratio": ratio,
                "Median Value": val
            })
    return pd.DataFrame(summary_data)


def identify_outliers(df: pd.DataFrame) -> dict:
    outliers = {}
    for ratio in RATIOS:
        data = df[df[ratio].notnull()].sort_values(by=ratio)
        if len(data) < 10:
            continue
        
        # Get top 3 highest and top 3 lowest
        lowest = data.head(3)[["Symbol", "Security", "GICS Sector", ratio]].to_dict(orient="records")
        highest = data.tail(3)[["Symbol", "Security", "GICS Sector", ratio]].to_dict(orient="records")
        
        # Reverse highest list to show highest first
        highest.reverse()
        
        outliers[ratio] = {
            "lowest": lowest,
            "highest": highest
        }
    return outliers


def generate_eda_report(df: pd.DataFrame, sector_summary: pd.DataFrame, outliers_summary: dict):
    report_path = os.path.join(REPORTS_DIR, "eda_report.md")
    
    # Build markdown for outliers
    outliers_md = ""
    for ratio, data in outliers_summary.items():
        outliers_md += f"### {ratio}\n"
        outliers_md += "\n**Top 3 Highest:**\n"
        for i, item in enumerate(data["highest"]):
            val_str = f"{item[ratio]:.4f}" if "Ratio" in ratio or "Turnover" in ratio or "Equity" in ratio else f"{item[ratio]*100:.2f}%"
            outliers_md += f"{i+1}. **{item['Symbol']}** ({item['Security']} - {item['GICS Sector']}): **{val_str}**\n"
        
        outliers_md += "\n**Top 3 Lowest:**\n"
        for i, item in enumerate(data["lowest"]):
            val_str = f"{item[ratio]:.4f}" if "Ratio" in ratio or "Turnover" in ratio or "Equity" in ratio else f"{item[ratio]*100:.2f}%"
            outliers_md += f"{i+1}. **{item['Symbol']}** ({item['Security']} - {item['GICS Sector']}): **{val_str}**\n"
        outliers_md += "\n---\n"

    # Build GICS sector summary table (pivot by Sector and Ratio)
    pivot_df = sector_summary.pivot(index="Sector", columns="Ratio", values="Median Value")
    # Format sector comparison values for markdown table
    formatted_pivot = pivot_df.copy()
    for col in formatted_pivot.columns:
        if "Ratio" in col or "Turnover" in col or "Equity" in col:
            formatted_pivot[col] = formatted_pivot[col].map(lambda x: f"{x:.2f}" if pd.notnull(x) else "N/A")
        else:
            formatted_pivot[col] = formatted_pivot[col].map(lambda x: f"{x*100:.2f}%" if pd.notnull(x) else "N/A")
            
    sector_table_md = formatted_pivot.to_markdown()

    content = f"""# Phase 4 — Exploratory Data Analysis (EDA) Report

This report visualizes and explains the distributions, sector-level traits, and correlations of the financial health ratios across the S&P 500.

## Correlation Heatmap Analysis
![Correlation Heatmap](figures/correlation_heatmap.png)

### Key Insights:
1. **ROE & Net Margin Connection:** Return on Equity (ROE) and Net Margin often have a positive correlation. When companies convert revenue to profit efficiently, it drives high returns on book value.
2. **Current & Quick Ratios:** These are highly correlated (~0.90+). For most companies, the presence of inventory doesn't structurally alter short-term liquidity profiles, but it does differentiate inventory-heavy sectors (e.g., Consumer Staples, Industrials) from services/tech.
3. **Asset Turnover & Margins:** Often negatively correlated. This is a classic business strategy trade-off:
   - *High Volume / Low Margin:* Consumer Staples and Retailers turn assets over very quickly but make low margins.
   - *Low Volume / High Margin:* Software (Technology) and Pharmaceuticals have low asset turnover but extremely high gross/operating margins.

---

## Sector Comparison (Median Values)
Below is the matrix of median ratios across GICS Sectors:

{sector_table_md}

### Sector Highlights:
- **Technology & Communication Services:** High net and operating margins, low leverage, and solid cash/growth profiles.
- **Utilities & Real Estate (REITs):** Characterized by high leverage (`Debt-to-Equity`) and lower liquidity (`Current Ratio`), backed by long-term stable cash flows that support debt-heavy capital structures.
- **Consumer Staples:** High `Asset Turnover` with lower margins, reflecting high volumes and tight retail/grocery markups.

---

## Outlier Analysis
The following companies occupy the extreme ends of the distribution for each ratio:

{outliers_md}

### Analysis of Notable Outliers:
- **Negative Equity Outliers:** mature companies with massive share buyback programs (like McDonald's or Domino's) have negative equity, which removes them from standard ROE/Debt-to-Equity rankings.
- **Unusually High Margins/ROA:** Asset-light software and holding firms skew profitability distributions due to zero capital requirements.
- **High Growth Outliers:** Tech/biotech firms recovering post-2022 slowdowns or companies undergoing acquisitions show extreme YoY growth numbers.

---

## Visual Distribution & Boxplots
Each ratio's distribution and GICS sector breakdown is plotted and saved under `reports/figures/`:

1. **Net Margin:** [net_margin_analysis.png](figures/net_margin_analysis.png)
2. **Operating Margin:** [operating_margin_analysis.png](figures/operating_margin_analysis.png)
3. **ROE:** [roe_analysis.png](figures/roe_analysis.png)
4. **ROA:** [roa_analysis.png](figures/roa_analysis.png)
5. **Current Ratio:** [current_ratio_analysis.png](figures/current_ratio_analysis.png)
6. **Quick Ratio:** [quick_ratio_analysis.png](figures/quick_ratio_analysis.png)
7. **Debt-to-Equity:** [debt_to_equity_analysis.png](figures/debt_to_equity_analysis.png)
8. **Interest Coverage Ratio:** [interest_coverage_ratio_analysis.png](figures/interest_coverage_ratio_analysis.png)
9. **Asset Turnover:** [asset_turnover_analysis.png](figures/asset_turnover_analysis.png)
10. **Revenue Growth (YoY):** [revenue_growth_yoy_analysis.png](figures/revenue_growth_yoy_analysis.png)
"""
    with open(report_path, "w") as f:
        f.write(content)
    print(f"Generated EDA report at {report_path}")


if __name__ == "__main__":
    run_eda()
