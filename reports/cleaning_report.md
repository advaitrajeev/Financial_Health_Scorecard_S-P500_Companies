# Phase 3 — Data Cleaning & Processing Report

This report documents the cleaning decisions and ratio calculation rules applied to the S&P 500 fundamentals dataset.

## Summary Stats
- **Total Companies Processed:** 15
- **Financial Sector Companies:** 1 (leverage ratios excluded/modified)
- **Companies with Negative Equity:** 1 (ROE and Debt-to-Equity adjusted)
- **REITs with Missing Gross Profit:** 0 (gross profit is structurally not reported)

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
| Symbol   | Security   | GICS Sector   |   Stockholders Equity |
|:---------|:-----------|:--------------|----------------------:|
| ABBV     | AbbVie     | Health Care   |             -3.27e+09 |
