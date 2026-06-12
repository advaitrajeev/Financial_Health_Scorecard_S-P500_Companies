"""
scorecard.py
------------
The methodological heart of the Financial Health Scorecard.
Transforms raw financial ratios into sector-relative percentiles, computes 
weighted dimension sub-scores, and generates a final composite Health Score.

Usage:
    python -m src.scorecard
"""

import os
import pandas as pd
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

# Weighting Schema Design
DIMENSION_WEIGHTS = {
    "Profitability": 0.30,
    "Leverage": 0.25,
    "Liquidity": 0.20,
    "Efficiency": 0.15,
    "Growth": 0.10
}

# (Metric Name, Higher-is-better flag)
DIMENSION_METRICS = {
    "Profitability": [
        ("Gross Margin", True),
        ("Operating Margin", True),
        ("Net Margin", True),
        ("ROE", True),
        ("ROA", True)
    ],
    "Liquidity": [
        ("Current Ratio", True),
        ("Quick Ratio", True)
    ],
    "Leverage": [
        ("Debt-to-Equity", False), # False = higher debt is worse
        ("Debt-to-Assets", False),
        ("Interest Coverage Ratio", True)
    ],
    "Efficiency": [
        ("Asset Turnover", True),
        ("Receivables Turnover", True)
    ],
    "Growth": [
        ("Revenue Growth (YoY)", True),
        ("EPS Growth (YoY)", True),
        ("Free Cash Flow Margin", True)
    ]
}

def compute_health_scores():
    input_path = os.path.join(PROCESSED_DIR, "sp500_cleaned_ratios.csv")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Missing {input_path}. Please run clean_data.py first.")
        
    df = pd.read_csv(input_path)
    print(f"Loaded {len(df)} companies from {input_path}")
    print("Computing sector-relative percentiles and sub-scores...")
    
    # Helper to calculate percentile within sector
    # Using rank(pct=True). If ascending=False, the highest raw value gets the lowest percentile.
    def rank_within_sector(series, ascending):
        return series.groupby(df['GICS Sector']).rank(pct=True, ascending=ascending)
        
    for dimension, metrics in DIMENSION_METRICS.items():
        percentile_cols = []
        for metric, ascending in metrics:
            if metric in df.columns:
                pct_col_name = f"{metric} (Pct)"
                df[pct_col_name] = rank_within_sector(df[metric], ascending)
                percentile_cols.append(pct_col_name)
            
        # Compute the sub-score for the dimension (average of the available percentiles * 100)
        # We use mean() across columns so if a single metric is missing, it averages the rest.
        if percentile_cols:
            df[f"{dimension} Score"] = df[percentile_cols].mean(axis=1) * 100
        else:
            df[f"{dimension} Score"] = np.nan
            
    print("Calculating composite Health Scores...")
    
    # Calculate composite score gracefully handling missing dimensions
    def calculate_composite(row):
        score = 0
        weight_sum = 0
        for dim, w in DIMENSION_WEIGHTS.items():
            val = row.get(f"{dim} Score", np.nan)
            if pd.notna(val):
                score += val * w
                weight_sum += w
        
        # If the company is completely missing all data, return NaN
        if weight_sum == 0:
            return np.nan
            
        # Rescale score in case a dimension was missing (e.g. if a company had no Growth metrics at all)
        return score / weight_sum

    df["Health Score"] = df.apply(calculate_composite, axis=1)
    
    # Assign Health Label based on predefined thresholds
    def get_health_label(score):
        if pd.isna(score):
            return "Unknown"
        elif score >= 70:
            return "Strong"
        elif score >= 40:
            return "Moderate"
        else:
            return "At risk"
            
    df["Health Label"] = df["Health Score"].apply(get_health_label)
    
    # Sort the dataframe from best to worst
    df = df.sort_values(by="Health Score", ascending=False).reset_index(drop=True)
    
    # Save the output
    output_path = os.path.join(PROCESSED_DIR, "sp500_health_scores.csv")
    df.to_csv(output_path, index=False)
    
    print(f"\nSuccessfully computed health scores for {len(df)} companies.")
    print(f"Saved definitive results to {output_path}")

    print("\n--- Health Label Distribution ---")
    print(df["Health Label"].value_counts().to_string())
    
    print("\n--- Top 5 Healthiest Companies ---")
    top_5 = df[["Symbol", "Security", "GICS Sector", "Health Score", "Health Label"]].head(5)
    print(top_5.to_string(index=False))

if __name__ == "__main__":
    compute_health_scores()
