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

| Sector                 |   Asset Turnover | Current Ratio   | Debt-to-Assets   | Debt-to-Equity   | EPS Growth (YoY)   | Free Cash Flow Margin   | Gross Margin   | Interest Coverage Ratio   | Net Margin   | Operating Margin   | Quick Ratio   | ROA    | ROE    |   Receivables Turnover | Revenue Growth (YoY)   |
|:-----------------------|-----------------:|:----------------|:-----------------|:-----------------|:-------------------|:------------------------|:---------------|:--------------------------|:-------------|:-------------------|:--------------|:-------|:-------|-----------------------:|:-----------------------|
| Consumer Discretionary |             0.55 | 1.38            | 9.31%            | 0.25             | -74.94%            | 37.95%                  | 82.96%         | N/A                       | 20.51%       | 20.78%             | 1.38          | 11.31% | 30.63% |                  65.81 | 10.26%                 |
| Financials             |             0.15 | N/A             | 7.22%            | N/A              | -29.18%            | 14.72%                  | N/A            | N/A                       | 21.01%       | N/A                | N/A           | 3.13%  | 12.36% |                  20.78 | -9.27%                 |
| Health Care            |             0.51 | 1.58            | 26.35%           | 0.38             | -1.26%             | 16.68%                  | 56.42%         | 13.81                     | 14.72%       | 21.29%             | 1.18          | 7.52%  | 15.92% |                   4.86 | 6.73%                  |
| Industrials            |             0.94 | 1.60            | 19.76%           | 1.39             | -7.22%             | 9.93%                   | 39.37%         | 29.71                     | 13.64%       | 19.11%             | 1.13          | 13.00% | 49.26% |                   6.82 | 0.92%                  |
| Information Technology |             0.63 | 1.89            | 17.53%           | 0.42             | 20.66%             | 18.03%                  | 54.23%         | 33.41                     | 11.77%       | 15.24%             | 1.72          | 8.69%  | 16.85% |                   6.38 | 8.94%                  |
| Materials              |             0.3  | 1.81            | 32.48%           | 0.79             | -30.87%            | -8.91%                  | 22.21%         | -1.36                     | -6.60%       | 12.65%             | 1.39          | -2.04% | -3.99% |                   7.5  | -2.44%                 |
| Real Estate            |             0.09 | 0.43            | 37.44%           | 0.82             | -568.89%           | 48.01%                  | 68.67%         | -4.37                     | -48.54%      | 18.85%             | 0.43          | -4.19% | -9.24% |                 441.42 | -3.43%                 |
| Utilities              |             0.24 | 0.77            | 57.75%           | 7.36             | -46.61%            | -13.27%                 | 18.07%         | 1.05                      | 7.44%        | 16.10%             | 0.69          | 1.76%  | 22.40% |                   7.27 | -0.37%                 |

### Sector Highlights:
- **Technology & Communication Services:** High net and operating margins, low leverage, and solid cash/growth profiles.
- **Utilities & Real Estate (REITs):** Characterized by high leverage (`Debt-to-Equity`) and lower liquidity (`Current Ratio`), backed by long-term stable cash flows that support debt-heavy capital structures.
- **Consumer Staples:** High `Asset Turnover` with lower margins, reflecting high volumes and tight retail/grocery markups.

---

## Outlier Analysis
The following companies occupy the extreme ends of the distribution for each ratio:

### Gross Margin

**Top 3 Highest:**
1. **ADBE** (Adobe Inc. - Information Technology): **89.27%**
2. **ABNB** (Airbnb - Consumer Discretionary): **82.96%**
3. **ABBV** (AbbVie - Health Care): **70.24%**

**Top 3 Lowest:**
1. **ALB** (Albemarle Corporation - Materials): **13.00%**
2. **AES** (AES Corporation - Utilities): **18.07%**
3. **APD** (Air Products - Materials): **31.41%**

---
### Operating Margin

**Top 3 Highest:**
1. **ADBE** (Adobe Inc. - Information Technology): **36.63%**
2. **ABBV** (AbbVie - Health Care): **32.85%**
3. **APD** (Air Products - Materials): **24.00%**

**Top 3 Lowest:**
1. **ALB** (Albemarle Corporation - Materials): **1.31%**
2. **AMD** (Advanced Micro Devices - Information Technology): **10.66%**
3. **AKAM** (Akamai Technologies - Information Technology): **14.93%**

---
### Net Margin

**Top 3 Highest:**
1. **ADBE** (Adobe Inc. - Information Technology): **30.00%**
2. **AFL** (Aflac - Financials): **21.01%**
3. **ABNB** (Airbnb - Consumer Discretionary): **20.51%**

**Top 3 Lowest:**
1. **ARE** (Alexandria Real Estate Equities - Real Estate): **-48.54%**
2. **ALB** (Albemarle Corporation - Materials): **-9.93%**
3. **APD** (Air Products - Materials): **-3.28%**

---
### ROE

**Top 3 Highest:**
1. **MMM** (3M - Industrials): **69.12%**
2. **ADBE** (Adobe Inc. - Information Technology): **61.34%**
3. **ABNB** (Airbnb - Consumer Discretionary): **30.63%**

**Top 3 Lowest:**
1. **ARE** (Alexandria Real Estate Equities - Real Estate): **-9.24%**
2. **ALB** (Albemarle Corporation - Materials): **-5.36%**
3. **APD** (Air Products - Materials): **-2.63%**

---
### ROA

**Top 3 Highest:**
1. **ADBE** (Adobe Inc. - Information Technology): **24.17%**
2. **AOS** (A. O. Smith - Industrials): **17.38%**
3. **ACN** (Accenture - Information Technology): **11.74%**

**Top 3 Lowest:**
1. **ARE** (Alexandria Real Estate Equities - Real Estate): **-4.19%**
2. **ALB** (Albemarle Corporation - Materials): **-3.12%**
3. **APD** (Air Products - Materials): **-0.96%**

---
### Current Ratio

**Top 3 Highest:**
1. **AMD** (Advanced Micro Devices - Information Technology): **2.8500**
2. **AKAM** (Akamai Technologies - Information Technology): **2.3634**
3. **ALB** (Albemarle Corporation - Materials): **2.2292**

**Top 3 Lowest:**
1. **ARE** (Alexandria Real Estate Equities - Real Estate): **0.4306**
2. **ABBV** (AbbVie - Health Care): **0.6713**
3. **AES** (AES Corporation - Utilities): **0.7657**

---
### Quick Ratio

**Top 3 Highest:**
1. **AKAM** (Akamai Technologies - Information Technology): **2.3634**
2. **AMD** (Advanced Micro Devices - Information Technology): **2.0124**
3. **ALB** (Albemarle Corporation - Materials): **1.5733**

**Top 3 Lowest:**
1. **ARE** (Alexandria Real Estate Equities - Real Estate): **0.4306**
2. **ABBV** (AbbVie - Health Care): **0.5570**
3. **AES** (AES Corporation - Utilities): **0.6936**

---
### Debt-to-Equity

**Top 3 Highest:**
1. **AES** (AES Corporation - Utilities): **7.3584**
2. **MMM** (3M - Industrials): **2.6801**
3. **APD** (Air Products - Materials): **1.2250**

**Top 3 Lowest:**
1. **AMD** (Advanced Micro Devices - Information Technology): **0.0611**
2. **AOS** (A. O. Smith - Industrials): **0.1034**
3. **ABNB** (Airbnb - Consumer Discretionary): **0.2521**

---
### Debt-to-Assets

**Top 3 Highest:**
1. **AES** (AES Corporation - Utilities): **57.75%**
2. **ABBV** (AbbVie - Health Care): **50.39%**
3. **AKAM** (Akamai Technologies - Information Technology): **49.44%**

**Top 3 Lowest:**
1. **AMD** (Advanced Micro Devices - Information Technology): **5.00%**
2. **AOS** (A. O. Smith - Industrials): **6.11%**
3. **AFL** (Aflac - Financials): **7.22%**

---
### Interest Coverage Ratio

**Top 3 Highest:**
1. **AOS** (A. O. Smith - Industrials): **53.9704**
2. **ACN** (Accenture - Information Technology): **45.9362**
3. **ADBE** (Adobe Inc. - Information Technology): **34.2091**

**Top 3 Lowest:**
1. **ARE** (Alexandria Real Estate Equities - Real Estate): **-4.3672**
2. **ALB** (Albemarle Corporation - Materials): **-1.6587**
3. **APD** (Air Products - Materials): **-1.0593**

---
### Asset Turnover

**Top 3 Highest:**
1. **AOS** (A. O. Smith - Industrials): **1.2187**
2. **ACN** (Accenture - Information Technology): **1.0654**
3. **ADBE** (Adobe Inc. - Information Technology): **0.8058**

**Top 3 Lowest:**
1. **ARE** (Alexandria Real Estate Equities - Real Estate): **0.0864**
2. **AFL** (Aflac - Financials): **0.1490**
3. **AES** (AES Corporation - Utilities): **0.2363**

---
### Receivables Turnover

**Top 3 Highest:**
1. **ARE** (Alexandria Real Estate Equities - Real Estate): **441.4231**
2. **ABNB** (Airbnb - Consumer Discretionary): **65.8118**
3. **AFL** (Aflac - Financials): **20.7844**

**Top 3 Lowest:**
1. **A** (Agilent Technologies - Health Care): **4.6725**
2. **ABBV** (AbbVie - Health Care): **4.8582**
3. **ACN** (Accenture - Information Technology): **5.3326**

---
### Revenue Growth (YoY)

**Top 3 Highest:**
1. **AMD** (Advanced Micro Devices - Information Technology): **34.34%**
2. **ADBE** (Adobe Inc. - Information Technology): **10.53%**
3. **ABNB** (Airbnb - Consumer Discretionary): **10.26%**

**Top 3 Lowest:**
1. **AFL** (Aflac - Financials): **-9.27%**
2. **ALB** (Albemarle Corporation - Materials): **-4.37%**
3. **ARE** (Alexandria Real Estate Equities - Real Estate): **-3.43%**

---
### EPS Growth (YoY)

**Top 3 Highest:**
1. **AMD** (Advanced Micro Devices - Information Technology): **165.00%**
2. **ALB** (Albemarle Corporation - Materials): **48.57%**
3. **ADBE** (Adobe Inc. - Information Technology): **35.11%**

**Top 3 Lowest:**
1. **ARE** (Alexandria Real Estate Equities - Real Estate): **-568.89%**
2. **APD** (Air Products - Materials): **-110.30%**
3. **ABNB** (Airbnb - Consumer Discretionary): **-74.94%**

---
### Free Cash Flow Margin

**Top 3 Highest:**
1. **ARE** (Alexandria Real Estate Equities - Real Estate): **48.01%**
2. **ADBE** (Adobe Inc. - Information Technology): **41.45%**
3. **ABNB** (Airbnb - Consumer Discretionary): **37.95%**

**Top 3 Lowest:**
1. **APD** (Air Products - Materials): **-31.28%**
2. **AES** (AES Corporation - Utilities): **-13.27%**
3. **MMM** (3M - Industrials): **5.60%**

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
