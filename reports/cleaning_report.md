# Phase 3 — Data Cleaning & Processing Report

This report documents the cleaning decisions and ratio calculation rules applied to the S&P 500 fundamentals dataset.

## Summary Stats
- **Total Companies Processed:** 503
- **Financial Sector Companies:** 76 (leverage ratios excluded/modified)
- **Companies with Negative Equity:** 31 (ROE and Debt-to-Equity adjusted)
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
| Symbol   | Security                    | GICS Sector            |   Stockholders Equity |
|:---------|:----------------------------|:-----------------------|----------------------:|
| ABBV     | AbbVie                      | Health Care            |          -3.27e+09    |
| MO       | Altria                      | Consumer Staples       |          -3.502e+09   |
| AZO      | AutoZone                    | Consumer Discretionary |          -3.41431e+09 |
| BKNG     | Booking Holdings            | Consumer Discretionary |          -5.578e+09   |
| CAH      | Cardinal Health             | Health Care            |          -2.781e+09   |
| CCI      | Crown Castle                | Real Estate            |          -1.635e+09   |
| DVA      | DaVita                      | Health Care            |          -6.51082e+08 |
| DELL     | Dell Technologies           | Information Technology |          -2.47e+09    |
| DPZ      | Domino's                    | Consumer Discretionary |          -3.90114e+09 |
| FICO     | Fair Isaac                  | Information Technology |          -1.74578e+09 |
| HCA      | HCA Healthcare              | Health Care            |          -6.027e+09   |
| HLT      | Hilton Worldwide            | Consumer Discretionary |          -5.388e+09   |
| HPQ      | HP Inc.                     | Information Technology |          -3.46e+08    |
| IRM      | Iron Mountain               | Real Estate            |          -9.81007e+08 |
| LOW      | Lowe's                      | Consumer Discretionary |          -9.917e+09   |
| MAR      | Marriott International      | Consumer Discretionary |          -3.771e+09   |
| MAS      | Masco                       | Industrials            |          -1.86e+08    |
| MCD      | McDonald's                  | Consumer Discretionary |          -1.79e+09    |
| MCK      | McKesson Corporation        | Health Care            |          -2.172e+09   |
| MTD      | Mettler Toledo              | Health Care            |          -2.3636e+07  |
| MSCI     | MSCI Inc.                   | Financials             |          -2.65454e+09 |
| ORLY     | O’Reilly Automotive         | Consumer Discretionary |          -7.63352e+08 |
| OTIS     | Otis Worldwide              | Industrials            |          -5.392e+09   |
| PM       | Philip Morris International | Consumer Staples       |          -9.994e+09   |
| SBAC     | SBA Communications          | Real Estate            |          -4.85352e+09 |
| STX      | Seagate Technology          | Information Technology |          -4.53e+08    |
| SBUX     | Starbucks                   | Consumer Discretionary |          -8.0966e+09  |
| TDG      | TransDigm Group             | Industrials            |          -9.686e+09   |
| VRSN     | Verisign                    | Information Technology |          -2.1542e+09  |
| WYNN     | Wynn Resorts                | Consumer Discretionary |          -2.75492e+08 |
| YUM      | Yum! Brands                 | Consumer Discretionary |          -7.325e+09   |
