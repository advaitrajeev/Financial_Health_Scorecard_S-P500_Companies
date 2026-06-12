"""
clean_data.py
-------------
Cleans raw S&P 500 fundamentals data and computes the 10 financial health ratios:
- Profitability: Net Margin, Operating Margin, ROE, ROA
- Liquidity: Current Ratio, Quick Ratio
- Leverage: Debt-to-Equity, Interest Coverage Ratio
- Efficiency: Asset Turnover
- Growth: Revenue Growth (YoY)

Handles real-world edge cases:
- Missing values (e.g. REITs with no inventory/COGS)
- Negative equity (e.g., McDonald's, Domino's)
- Sector exceptions (excluding Financials from standard leverage comparisons)

Usage:
    python -m src.clean_data
"""

import os
import numpy as np
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")

os.makedirs(REPORTS_DIR, exist_ok=True)


def clean_and_calculate_ratios() -> pd.DataFrame:
    # 1. Load data
    tickers_path = os.path.join(PROCESSED_DIR, "sp500_tickers.csv")
    fundamentals_path = os.path.join(PROCESSED_DIR, "sp500_fundamentals.csv")

    if not os.path.exists(tickers_path):
        raise FileNotFoundError(f"Missing tickers file at {tickers_path}. Run collect_sp500 first.")
    if not os.path.exists(fundamentals_path):
        raise FileNotFoundError(f"Missing fundamentals file at {fundamentals_path}. Run collect_fundamentals first.")

    tickers_df = pd.read_csv(tickers_path)
    fundamentals_df = pd.read_csv(fundamentals_path)

    # 2. Merge metadata (GICS Sector, GICS Sub-Industry, Security name)
    # Ensure Symbol columns are stripped and matching
    tickers_df["Symbol"] = tickers_df["Symbol"].str.strip()
    fundamentals_df["Symbol"] = fundamentals_df["Symbol"].str.strip()

    df = pd.merge(
        tickers_df[["Symbol", "Security", "GICS Sector", "GICS Sub-Industry"]],
        fundamentals_df,
        on="Symbol",
        how="inner"
    )

    # Drop rows where essential financial data is entirely missing (meaning yfinance pulled no data)
    # We check if all primary numeric columns are null
    check_cols = ["Total Revenue", "Net Income", "Total Assets", "Total Liabilities Net Minority Interest"]
    existing_check_cols = [c for c in check_cols if c in df.columns]
    
    # Check if we have at least one column to check, then drop rows where they are all null
    if existing_check_cols:
        before_count = len(df)
        df = df.dropna(subset=existing_check_cols, how="all")
        dropped = before_count - len(df)
        print(f"Dropped {dropped} companies with completely missing financial data.")

    # Convert numeric columns
    numeric_cols = [
        "Total Revenue", "Gross Profit", "Operating Income", "Net Income", "EBITDA", "Interest Expense",
        "Total Assets", "Total Liabilities Net Minority Interest", "Current Assets", "Current Liabilities",
        "Total Debt", "Stockholders Equity", "Inventory", "Operating Cash Flow", "Capital Expenditure",
        "Free Cash Flow", "Revenue Growth (YoY)"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Fill NaNs for Inventory with 0 (many service/tech companies have no inventory)
    if "Inventory" in df.columns:
        df["Inventory"] = df["Inventory"].fillna(0)

    # Fill NaNs for Interest Expense with 0 (some cash-rich companies have no interest expense)
    if "Interest Expense" in df.columns:
        df["Interest Expense"] = df["Interest Expense"].fillna(0)

    # 3. Handle anomalies and document choices
    # Flag negative equity
    df["Negative Equity Flag"] = df["Stockholders Equity"] < 0

    # 4. Compute Ratios
    print("Computing financial ratios...")

    # Profitability Ratios
    # Net Margin = Net Income / Total Revenue
    df["Net Margin"] = df["Net Income"] / df["Total Revenue"]
    
    # Operating Margin = Operating Income / Total Revenue
    df["Operating Margin"] = df["Operating Income"] / df["Total Revenue"]

    # ROA = Net Income / Total Assets
    df["ROA"] = df["Net Income"] / df["Total Assets"]

    # ROE = Net Income / Stockholders Equity
    # Note: If equity is negative, ROE is distorted. We set ROE to NaN for negative equity companies
    # because a positive net income / negative equity looks like a "negative ROE" but is actually due to buybacks,
    # and a negative net income / negative equity looks like a "positive ROE" (which is highly misleading).
    df["ROE"] = np.where(df["Stockholders Equity"] > 0, df["Net Income"] / df["Stockholders Equity"], np.nan)

    # Liquidity Ratios
    # Current Ratio = Current Assets / Current Liabilities
    df["Current Ratio"] = df["Current Assets"] / df["Current Liabilities"]

    # Quick Ratio = (Current Assets - Inventory) / Current Liabilities
    df["Quick Ratio"] = (df["Current Assets"] - df["Inventory"]) / df["Current Liabilities"]

    # Leverage Ratios
    # Debt-to-Equity = Total Debt / Stockholders Equity
    # Exclude negative equity companies from simple debt/equity ranking, and exclude Financials
    df["Debt-to-Equity"] = np.where(
        (df["Stockholders Equity"] > 0) & (df["GICS Sector"] != "Financials"),
        df["Total Debt"] / df["Stockholders Equity"],
        np.nan
    )

    # Interest Coverage Ratio = Operating Income / Interest Expense
    # Exclude Financials because interest is an operating item for them
    # If Interest Expense is <= 0 (cash rich, no interest), we set to a very high default or NaN
    df["Interest Coverage Ratio"] = np.where(
        (df["GICS Sector"] != "Financials"),
        np.where(df["Interest Expense"] > 0, df["Operating Income"] / df["Interest Expense"], np.nan),
        np.nan
    )

    # Efficiency Ratios
    # Asset Turnover = Total Revenue / Total Assets
    df["Asset Turnover"] = df["Total Revenue"] / df["Total Assets"]

    # Growth is already calculated: Revenue Growth (YoY)
    # We will rename or align it
    if "Revenue Growth (YoY)" not in df.columns:
        df["Revenue Growth (YoY)"] = np.nan

    # 5. Output results
    output_path = os.path.join(PROCESSED_DIR, "sp500_cleaned_ratios.csv")
    df.to_csv(output_path, index=False)
    print(f"Saved cleaned data and ratios to {output_path} (shape: {df.shape})")

    # 6. Generate Cleaning Report
    generate_cleaning_report(df)

    return df


def generate_cleaning_report(df: pd.DataFrame):
    report_path = os.path.join(REPORTS_DIR, "cleaning_report.md")
    
    total_companies = len(df)
    neg_equity_companies = df[df["Negative Equity Flag"] == True]
    financials_count = len(df[df["GICS Sector"] == "Financials"])
    
    reits_no_cogs = len(df[(df["GICS Sector"] == "Real Estate") & (df["Gross Profit"].isnull())])
    
    content = f"""# Phase 3 — Data Cleaning & Processing Report

This report documents the cleaning decisions and ratio calculation rules applied to the S&P 500 fundamentals dataset.

## Summary Stats
- **Total Companies Processed:** {total_companies}
- **Financial Sector Companies:** {financials_count} (leverage ratios excluded/modified)
- **Companies with Negative Equity:** {len(neg_equity_companies)} (ROE and Debt-to-Equity adjusted)
- **REITs with Missing Gross Profit:** {reits_no_cogs} (gross profit is structurally not reported)

## Cleaning & Processing Rationale

### 1. Sector-Specific Leverage Exclusion (Financials)
- **Decision:** Excluded companies in the **Financials** sector from the `Debt-to-Equity` and `Interest Coverage Ratio` rankings.
- **Rationale:** Financial institutions (banks, insurance) carry huge liabilities (like customer deposits) which act as fuel for their asset creation (loans). Standard leverage ratios like Debt/Equity or EBIT/Interest Expense are meaningless or structurally distorted for them. Comparing Goldman Sachs' leverage to Apple's leverage is an apples-to-oranges comparison.

### 2. Negative Equity Handling (Aggressive Buybacks)
- **Decision:** Flagged companies with negative stockholders' equity and excluded them from standard `ROE` and `Debt-to-Equity` calculations (set to `NaN`).
- **Rationale:** Companies like McDonald's (`MCD`), Domino's (`DPZ`), and Philip Morris (`PM`) have negative book value because they have bought back massive amounts of shares over decades, which reduces treasury stock and equity below zero, or because they leveraged up to pay dividends while having highly valuable off-balance-sheet intangible assets (brand power). They are highly profitable and cash-generative, so they are not insolvent. However, dividing Net Income by negative equity results in meaningless ROE numbers.

### 3. Missing Gross Profit (REITs)
- **Decision:** Kept `Gross Profit` as `NaN` for Real Estate Investment Trusts (REITs) and service companies that do not report standard Cost of Goods Sold (COGS).
- **Rationale:** REITs generate rental income and do not have a traditional COGS line. Their primary expenses are depreciation and property management, which appear further down the income statement. 

### 4. Zero/Missing Inventory and Interest Expense
- **Decision:** Filled missing `Inventory` values with `0`. Filled missing `Interest Expense` with `0`.
- **Rationale:** Service and software companies (like Microsoft or Mastercard) have little to no physical inventory. Cash-rich companies with zero debt have no interest expense. Treating these as zero is financially accurate and prevents calculation errors.

## Negative Equity Companies List
The following companies have negative equity due to stock buybacks or debt recapitalizations:
{neg_equity_companies[['Symbol', 'Security', 'GICS Sector', 'Stockholders Equity']].to_markdown(index=False) if not neg_equity_companies.empty else "*None found in dataset*"}
"""
    with open(report_path, "w") as f:
        f.write(content)
    print(f"Generated cleaning report at {report_path}")


if __name__ == "__main__":
    clean_and_calculate_ratios()
