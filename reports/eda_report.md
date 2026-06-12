# Phase 4 — Exploratory Data Analysis (EDA) Report

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

| Sector                 |   Asset Turnover |   Current Ratio | Debt-to-Assets   | Debt-to-Equity   | EPS Growth (YoY)   | Free Cash Flow Margin   | Gross Margin   | Interest Coverage Ratio   | Net Margin   | Operating Margin   |   Quick Ratio | ROA    | ROE    |   Receivables Turnover | Revenue Growth (YoY)   |
|:-----------------------|-----------------:|----------------:|:-----------------|:-----------------|:-------------------|:------------------------|:---------------|:--------------------------|:-------------|:-------------------|--------------:|:-------|:-------|-----------------------:|:-----------------------|
| Communication Services |             0.55 |            1.19 | 31.53%           | 0.84             | 30.19%             | 15.55%                  | 58.92%         | 4.88                      | 13.14%       | 17.63%             |          1.12 | 6.28%  | 17.84% |                   8.48 | 3.35%                  |
| Consumer Discretionary |             0.97 |            1.34 | 44.51%           | 1.32             | 0.12%              | 9.21%                   | 39.95%         | 5.97                      | 9.37%        | 15.84%             |          1.07 | 10.18% | 31.83% |                  20.72 | 4.91%                  |
| Consumer Staples       |             0.83 |            0.95 | 38.54%           | 1.00             | -4.87%             | 9.36%                   | 36.01%         | 6.40                      | 6.61%        | 14.29%             |          0.54 | 6.43%  | 17.77% |                  14.1  | 1.73%                  |
| Energy                 |             0.5  |            1.15 | 21.21%           | 0.49             | -8.55%             | 9.00%                   | 29.39%         | 8.02                      | 11.15%       | 19.24%             |          0.86 | 5.98%  | 12.92% |                   9.06 | -0.34%                 |
| Financials             |             0.19 |            1.16 | 10.26%           | N/A              | 14.29%             | 22.60%                  | 53.46%         | N/A                       | 19.33%       | 27.15%             |          1.16 | 2.48%  | 13.74% |                   3.64 | 7.37%                  |
| Health Care            |             0.56 |            1.55 | 28.74%           | 0.70             | 6.46%              | 15.25%                  | 59.37%         | 6.69                      | 12.42%       | 18.86%             |          1.19 | 6.11%  | 12.90% |                   5.85 | 6.99%                  |
| Industrials            |             0.71 |            1.24 | 28.20%           | 0.74             | 6.74%              | 12.28%                  | 36.10%         | 9.24                      | 12.41%       | 17.16%             |          1.01 | 8.27%  | 23.78% |                   6.93 | 4.45%                  |
| Information Technology |             0.51 |            1.6  | 24.58%           | 0.48             | 15.59%             | 22.38%                  | 57.96%         | 11.89                     | 16.31%       | 21.53%             |          1.37 | 7.57%  | 19.18% |                   5.67 | 13.39%                 |
| Materials              |             0.56 |            1.68 | 30.50%           | 0.74             | -1.98%             | 6.66%                   | 29.18%         | 6.87                      | 6.73%        | 13.18%             |          1.17 | 4.82%  | 11.50% |                   8.42 | 3.30%                  |
| Real Estate            |             0.15 |            0.8  | 44.86%           | 0.89             | 13.90%             | 37.88%                  | 63.14%         | 3.31                      | 21.54%       | 28.11%             |          0.8  | 3.37%  | 7.75%  |                  14.62 | 5.06%                  |
| Utilities              |             0.19 |            0.77 | 44.78%           | 1.74             | 4.19%              | -9.93%                  | 47.20%         | 2.56                      | 13.70%       | 23.03%             |          0.6  | 2.65%  | 10.45% |                   7.75 | 9.74%                  |

### Sector Highlights:
- **Technology & Communication Services:** High net and operating margins, low leverage, and solid cash/growth profiles.
- **Utilities & Real Estate (REITs):** Characterized by high leverage (`Debt-to-Equity`) and lower liquidity (`Current Ratio`), backed by long-term stable cash flows that support debt-heavy capital structures.
- **Consumer Staples:** High `Asset Turnover` with lower margins, reflecting high volumes and tight retail/grocery markups.

---

## Outlier Analysis
The following companies occupy the extreme ends of the distribution for each ratio:

### Gross Margin

**Top 3 Highest:**
1. **VICI** (Vici Properties - Real Estate): **99.33%**
2. **APO** (Apollo Global Management - Financials): **95.50%**
3. **INCY** (Incyte - Health Care): **92.76%**

**Top 3 Lowest:**
1. **F** (Ford Motor Company - Consumer Discretionary): **0.90%**
2. **COR** (Cencora - Health Care): **3.57%**
3. **MCK** (McKesson Corporation - Health Care): **3.61%**

---
### Operating Margin

**Top 3 Highest:**
1. **VICI** (Vici Properties - Real Estate): **91.24%**
2. **IBKR** (Interactive Brokers - Financials): **85.98%**
3. **APP** (AppLovin - Information Technology): **75.75%**

**Top 3 Lowest:**
1. **MRNA** (Moderna - Health Care): **-159.94%**
2. **LITE** (Lumentum - Information Technology): **-11.68%**
3. **IVZ** (Invesco - Financials): **-10.91%**

---
### Net Margin

**Top 3 Highest:**
1. **SPG** (Simon Property Group - Real Estate): **72.71%**
2. **VICI** (Vici Properties - Real Estate): **69.28%**
3. **CME** (CME Group - Financials): **62.45%**

**Top 3 Lowest:**
1. **MRNA** (Moderna - Health Care): **-146.83%**
2. **SATS** (EchoStar - Communication Services): **-96.62%**
3. **ARE** (Alexandria Real Estate Equities - Real Estate): **-48.54%**

---
### ROE

**Top 3 Highest:**
1. **CL** (Colgate-Palmolive - Consumer Staples): **3948.15%**
2. **GDDY** (GoDaddy - Information Technology): **406.79%**
3. **VRSK** (Verisk Analytics - Industrials): **293.95%**

**Top 3 Lowest:**
1. **SATS** (EchoStar - Communication Services): **-251.43%**
2. **HAS** (Hasbro - Consumer Discretionary): **-59.87%**
3. **PSKY** (Paramount Skydance Corporation - Communication Services): **-52.94%**

---
### ROA

**Top 3 Highest:**
1. **VRSN** (Verisign - Information Technology): **62.27%**
2. **NVDA** (Nvidia - Information Technology): **58.06%**
3. **APP** (AppLovin - Information Technology): **45.92%**

**Top 3 Lowest:**
1. **SATS** (EchoStar - Communication Services): **-33.70%**
2. **MRNA** (Moderna - Health Care): **-22.87%**
3. **PSKY** (Paramount Skydance Corporation - Communication Services): **-14.28%**

---
### Current Ratio

**Top 3 Highest:**
1. **VICI** (Vici Properties - Real Estate): **26.6768**
2. **DHI** (D. R. Horton - Consumer Discretionary): **17.3940**
3. **BLK** (BlackRock - Financials): **15.7609**

**Top 3 Lowest:**
1. **MAA** (Mid-America Apartment Communities - Real Estate): **0.0902**
2. **CPT** (Camden Property Trust - Real Estate): **0.1013**
3. **EQR** (Equity Residential - Real Estate): **0.1532**

---
### Quick Ratio

**Top 3 Highest:**
1. **VICI** (Vici Properties - Real Estate): **26.6768**
2. **BLK** (BlackRock - Financials): **15.7609**
3. **IVZ** (Invesco - Financials): **12.0020**

**Top 3 Lowest:**
1. **MAA** (Mid-America Apartment Communities - Real Estate): **0.0902**
2. **CPT** (Camden Property Trust - Real Estate): **0.1013**
3. **ORLY** (O’Reilly Automotive - Consumer Discretionary): **0.1154**

---
### Debt-to-Equity

**Top 3 Highest:**
1. **CL** (Colgate-Palmolive - Consumer Staples): **158.4074**
2. **LYV** (Live Nation Entertainment - Communication Services): **38.3916**
3. **GDDY** (GoDaddy - Information Technology): **17.9572**

**Top 3 Lowest:**
1. **MPWR** (Monolithic Power Systems - Information Technology): **0.0057**
2. **INCY** (Incyte - Health Care): **0.0078**
3. **ODFL** (Old Dominion - Industrials): **0.0093**

---
### Debt-to-Assets

**Top 3 Highest:**
1. **DPZ** (Domino's - Consumer Discretionary): **294.11%**
2. **FICO** (Fair Isaac - Information Technology): **164.60%**
3. **YUM** (Yum! Brands - Consumer Discretionary): **160.90%**

**Top 3 Lowest:**
1. **IBKR** (Interactive Brokers - Financials): **0.01%**
2. **MPWR** (Monolithic Power Systems - Information Technology): **0.48%**
3. **INCY** (Incyte - Health Care): **0.58%**

---
### Interest Coverage Ratio

**Top 3 Highest:**
1. **PHM** (PulteGroup - Consumer Discretionary): **4813.1008**
2. **ODFL** (Old Dominion - Industrials): **4600.0135**
3. **WST** (West Pharmaceutical Services - Health Care): **1202.8000**

**Top 3 Lowest:**
1. **MRNA** (Moderna - Health Care): **-275.8000**
2. **SNDK** (Sandisk - Information Technology): **-22.4762**
3. **SATS** (EchoStar - Communication Services): **-11.4158**

---
### Asset Turnover

**Top 3 Highest:**
1. **MCK** (McKesson Corporation - Health Care): **4.9006**
2. **COR** (Cencora - Health Care): **4.1955**
3. **CAH** (Cardinal Health - Health Care): **4.1899**

**Top 3 Lowest:**
1. **C** (Citigroup - Financials): **0.0321**
2. **GS** (Goldman Sachs - Financials): **0.0322**
3. **CME** (CME Group - Financials): **0.0329**

---
### Receivables Turnover

**Top 3 Highest:**
1. **VICI** (Vici Properties - Real Estate): **1699.6674**
2. **EVRG** (Evergy - Utilities): **596.1600**
3. **ARE** (Alexandria Real Estate Equities - Real Estate): **441.4231**

**Top 3 Lowest:**
1. **IBKR** (Interactive Brokers - Financials): **0.1130**
2. **SCHW** (Charles Schwab Corporation - Financials): **0.2224**
3. **HOOD** (Robinhood Markets - Financials): **0.2428**

---
### Revenue Growth (YoY)

**Top 3 Highest:**
1. **EXE** (Expand Energy - Energy): **188.77%**
2. **APP** (AppLovin - Information Technology): **69.99%**
3. **KEY** (KeyCorp - Financials): **65.72%**

**Top 3 Lowest:**
1. **MRNA** (Moderna - Health Care): **-39.92%**
2. **PCAR** (Paccar - Industrials): **-15.50%**
3. **ON** (ON Semiconductor - Information Technology): **-15.35%**

---
### EPS Growth (YoY)

**Top 3 Highest:**
1. **TKO** (TKO Group Holdings - Communication Services): **11200.00%**
2. **INCY** (Incyte - Health Care): **4173.33%**
3. **MCHP** (Microchip Technology - Information Technology): **2300.00%**

**Top 3 Lowest:**
1. **SATS** (EchoStar - Communication Services): **-11356.82%**
2. **CRL** (Charles River Laboratories - Health Care): **-1555.00%**
3. **CRWD** (CrowdStrike - Information Technology): **-983.33%**

---
### Free Cash Flow Margin

**Top 3 Highest:**
1. **IBKR** (Interactive Brokers - Financials): **154.02%**
2. **STT** (State Street Corporation - Financials): **77.64%**
3. **APP** (AppLovin - Information Technology): **71.94%**

**Top 3 Lowest:**
1. **MRNA** (Moderna - Health Care): **-107.96%**
2. **C** (Citigroup - Financials): **-87.02%**
3. **JPM** (JPMorgan Chase - Financials): **-81.27%**

---


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
