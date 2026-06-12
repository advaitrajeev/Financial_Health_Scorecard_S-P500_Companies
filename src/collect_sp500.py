"""
collect_sp500.py
----------------
Fetches the current S&P 500 constituent list from Wikipedia and saves it
to data/processed/sp500_tickers.csv.

Usage:
    python -m src.collect_sp500
"""

import os
import io
import pandas as pd
import requests


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")


def fetch_sp500_tickers() -> pd.DataFrame:
    """
    Scrape the S&P 500 constituent table from Wikipedia.

    Returns a DataFrame with columns: Symbol, Security, GICS Sector,
    GICS Sub-Industry, Headquarters Location, Date Added, CIK, Founded.
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    tables = pd.read_html(io.StringIO(response.text))
    # The first table on the page is the current constituents
    sp500_table = tables[0]

    # Clean the ticker symbols (some have dots, e.g. BRK.B → BRK-B for yfinance)
    sp500_table["Symbol"] = (
        sp500_table["Symbol"].str.strip().str.replace(".", "-", regex=False)
    )

    return sp500_table


def save_tickers(df: pd.DataFrame) -> str:
    """Save the tickers DataFrame to CSV and return the file path."""
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    output_path = os.path.join(PROCESSED_DIR, "sp500_tickers.csv")
    df.to_csv(output_path, index=False)
    return output_path


def main():
    print("Fetching S&P 500 constituent list from Wikipedia...")
    df = fetch_sp500_tickers()
    path = save_tickers(df)
    print(f"Saved {len(df)} tickers to {path}")
    print(f"\nSample tickers: {df['Symbol'].head(10).tolist()}")
    print(f"Sectors found:  {df['GICS Sector'].nunique()} unique sectors")
    return df


if __name__ == "__main__":
    main()
