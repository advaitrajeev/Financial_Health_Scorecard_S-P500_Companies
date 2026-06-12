"""
collect_fundamentals.py
-----------------------
Pulls fundamental financial data (income statement, balance sheet, cash flow)
for every S&P 500 ticker using yfinance. Saves raw data per-ticker to data/raw/
and merges everything into data/processed/sp500_fundamentals.csv.

Implements caching: if a ticker's raw files already exist on disk, it is skipped
so we never re-hit the API unnecessarily.

Usage:
    python -m src.collect_fundamentals
"""

import os
import sys
import time
import warnings

import pandas as pd
import yfinance as yf
from tqdm import tqdm

warnings.filterwarnings("ignore", category=FutureWarning)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Core function: pull one ticker
# ---------------------------------------------------------------------------
def pull_ticker_fundamentals(symbol: str) -> dict[str, pd.DataFrame | None]:
    """
    Pull income statement, balance sheet, and cash flow for a single ticker.

    Returns a dict with keys 'income', 'balance', 'cashflow'. Each value is
    a DataFrame (periods as columns, line items as rows) or None on failure.

    Catches all API/network errors gracefully and returns None for failed pulls.
    """
    result = {"income": None, "balance": None, "cashflow": None}

    try:
        ticker = yf.Ticker(symbol)

        # Income statement (annual)
        income = ticker.income_stmt
        if income is not None and not income.empty:
            result["income"] = income

        # Balance sheet (annual)
        balance = ticker.balance_sheet
        if balance is not None and not balance.empty:
            result["balance"] = balance

        # Cash flow (annual)
        cashflow = ticker.cashflow
        if cashflow is not None and not cashflow.empty:
            result["cashflow"] = cashflow

    except Exception as e:
        print(f"  [ERROR] {symbol}: {e}")

    return result


# ---------------------------------------------------------------------------
# Save raw data to disk (caching layer)
# ---------------------------------------------------------------------------
def save_raw_ticker(symbol: str, data: dict[str, pd.DataFrame | None]) -> bool:
    """
    Save raw DataFrames to CSV files in data/raw/.

    Files: {SYMBOL}_income.csv, {SYMBOL}_balance.csv, {SYMBOL}_cashflow.csv.
    Returns True if at least one file was saved.
    """
    saved_any = False
    for key in ("income", "balance", "cashflow"):
        df = data.get(key)
        if df is not None and not df.empty:
            path = os.path.join(RAW_DIR, f"{symbol}_{key}.csv")
            df.to_csv(path)
            saved_any = True
    return saved_any


def ticker_already_cached(symbol: str) -> bool:
    """Check if all three raw files for a ticker already exist on disk."""
    for key in ("income", "balance", "cashflow"):
        path = os.path.join(RAW_DIR, f"{symbol}_{key}.csv")
        if not os.path.exists(path):
            return False
    return True


# ---------------------------------------------------------------------------
# Extract the specific fields we need from raw data
# ---------------------------------------------------------------------------

# Fields we extract from each statement (yfinance row labels)
INCOME_FIELDS = [
    "Total Revenue",
    "Gross Profit",
    "Operating Income",
    "Net Income",
    "EBITDA",
    "Interest Expense",
    "EBIT",
    "Diluted EPS",
]

BALANCE_FIELDS = [
    "Total Assets",
    "Total Liabilities Net Minority Interest",
    "Current Assets",
    "Current Liabilities",
    "Total Debt",
    "Stockholders Equity",
    "Inventory",
    "Accounts Receivable",
]

CASHFLOW_FIELDS = [
    "Operating Cash Flow",
    "Capital Expenditure",
    "Free Cash Flow",
]


def extract_latest_values(df: pd.DataFrame, fields: list[str]) -> dict:
    """
    From a raw yfinance statement DataFrame, extract the most recent period's
    values for the requested fields.

    yfinance returns periods as columns (most recent first) and line items as
    the index.
    """
    if df is None or df.empty:
        return {f: None for f in fields}

    # Take the most recent period (first column)
    latest_col = df.columns[0]
    values = {}
    for field in fields:
        if field in df.index:
            val = df.loc[field, latest_col]
            values[field] = val
        else:
            values[field] = None
    return values


def build_ticker_row(symbol: str) -> dict | None:
    """
    Read cached raw files for one ticker and return a flat dict of all
    the fields we need, or None if files are missing.
    """
    try:
        income_path = os.path.join(RAW_DIR, f"{symbol}_income.csv")
        balance_path = os.path.join(RAW_DIR, f"{symbol}_balance.csv")
        cashflow_path = os.path.join(RAW_DIR, f"{symbol}_cashflow.csv")

        income_df = pd.read_csv(income_path, index_col=0) if os.path.exists(income_path) else None
        balance_df = pd.read_csv(balance_path, index_col=0) if os.path.exists(balance_path) else None
        cashflow_df = pd.read_csv(cashflow_path, index_col=0) if os.path.exists(cashflow_path) else None

        row = {"Symbol": symbol}
        row.update(extract_latest_values(income_df, INCOME_FIELDS))
        row.update(extract_latest_values(balance_df, BALANCE_FIELDS))
        row.update(extract_latest_values(cashflow_df, CASHFLOW_FIELDS))

        # Calculate Revenue Growth (YoY)
        yoy_growth = None
        eps_growth = None
        if income_df is not None and not income_df.empty:
            try:
                # Find Total Revenue row
                rev_idx = income_df.index == "Total Revenue"
                if rev_idx.any():
                    # Get the row values (first match if duplicate)
                    rev_row = income_df.loc[rev_idx].iloc[0]
                    cols = list(income_df.columns)
                    if len(cols) >= 2:
                        rev_latest = float(rev_row[cols[0]])
                        rev_prev = float(rev_row[cols[1]])
                        if rev_prev > 0:
                            yoy_growth = (rev_latest - rev_prev) / rev_prev
                
                # Find Diluted EPS row
                eps_idx = income_df.index == "Diluted EPS"
                if eps_idx.any():
                    eps_row = income_df.loc[eps_idx].iloc[0]
                    cols = list(income_df.columns)
                    if len(cols) >= 2:
                        eps_latest = float(eps_row[cols[0]])
                        eps_prev = float(eps_row[cols[1]])
                        if eps_prev != 0:
                            # Use abs(eps_prev) to correctly calculate growth if EPS was negative
                            eps_growth = (eps_latest - eps_prev) / abs(eps_prev)
            except Exception:
                pass
        row["Revenue Growth (YoY)"] = yoy_growth
        row["EPS Growth (YoY)"] = eps_growth

        return row

    except Exception as e:
        print(f"  [ERROR reading cached data] {symbol}: {e}")
        return None


# ---------------------------------------------------------------------------
# Main collection loop
# ---------------------------------------------------------------------------
def collect_all(tickers: list[str]) -> pd.DataFrame:
    """
    Loop over all tickers, pull fundamentals, cache to disk, and build
    the merged processed DataFrame.

    Skips tickers that are already cached.
    """
    total = len(tickers)
    pulled = 0
    cached = 0
    failed = 0

    print(f"\n{'='*60}")
    print(f"  Collecting fundamentals for {total} S&P 500 tickers")
    print(f"  Raw data cached to: {RAW_DIR}")
    print(f"{'='*60}\n")

    for symbol in tqdm(tickers, desc="Pulling data", unit="ticker"):
        if ticker_already_cached(symbol):
            cached += 1
            continue

        data = pull_ticker_fundamentals(symbol)

        if save_raw_ticker(symbol, data):
            pulled += 1
        else:
            failed += 1

        # Small delay to be respectful to the API
        time.sleep(0.3)

    print(f"\n--- Collection summary ---")
    print(f"  Already cached: {cached}")
    print(f"  Newly pulled:   {pulled}")
    print(f"  Failed:         {failed}")
    print(f"  Total:          {total}")

    # Build the merged dataset from cached raw files
    print(f"\nBuilding merged fundamentals dataset...")
    rows = []
    for symbol in tqdm(tickers, desc="Merging", unit="ticker"):
        row = build_ticker_row(symbol)
        if row is not None:
            rows.append(row)

    fundamentals_df = pd.DataFrame(rows)

    # Save processed output
    output_path = os.path.join(PROCESSED_DIR, "sp500_fundamentals.csv")
    fundamentals_df.to_csv(output_path, index=False)
    print(f"\nSaved {len(fundamentals_df)} companies to {output_path}")

    return fundamentals_df


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    # Load ticker list (must run collect_sp500.py first)
    tickers_path = os.path.join(PROCESSED_DIR, "sp500_tickers.csv")

    if not os.path.exists(tickers_path):
        print("Ticker list not found. Running S&P 500 list collection first...")
        from src.collect_sp500 import main as collect_sp500_main
        collect_sp500_main()

    tickers_df = pd.read_csv(tickers_path)
    tickers = tickers_df["Symbol"].tolist()

    # Support a test flag to run a subset of tickers quickly
    if "--test" in sys.argv:
        print("\n*** RUNNING IN TEST MODE (First 15 tickers only) ***\n")
        tickers = tickers[:15]

    fundamentals = collect_all(tickers)

    # Print a quick summary
    print(f"\n{'='*60}")
    print(f"  DATA COLLECTION COMPLETE")
    print(f"{'='*60}")
    print(f"\nDataset shape: {fundamentals.shape}")
    print(f"\nColumns: {list(fundamentals.columns)}")
    print(f"\nSample (first 5 rows):")
    print(fundamentals.head().to_string())
    print(f"\nNull counts per column:")
    print(fundamentals.isnull().sum().to_string())


if __name__ == "__main__":
    main()
