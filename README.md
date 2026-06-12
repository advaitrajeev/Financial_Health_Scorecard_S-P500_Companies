# 📊 Financial Health Scorecard — S&P 500 Companies

A standardized, automated, and reproducible financial health assessment tool designed to analyze, score, and screen S&P 500 companies for investment, credit risk, and research purposes.

---

## 🔍 Executive summary:

This project answers a question every equity analyst, portfolio manager, and finance student asks constantly: "Which companies are financially healthy and which are quietly distressed?" You pull real S&P 500 fundamental data, engineer the same ratios a Goldman Sachs analyst would use in a morning briefing, build a composite health score, and wrap it in a clean dashboard with sector filtering and company-level drill-down. The output looks and feels like something a real investment team would use.

---

## 📈 Industry context:

Financial health analysis is the foundation of equity research, credit analysis, and investment due diligence. Analysts at every tier — from junior associates at boutique advisory firms to portfolio managers at BlackRock — spend significant time assessing whether a company can sustain its operations, service its debt, and generate returns. What they don't have is a standardised, reproducible, automated version of that analysis across 500+ companies simultaneously. That's what you're building.The timing matters too. With rising interest rates, higher refinancing costs, and slowing revenue growth in several sectors post-2022, a tool that quickly surfaces financially stressed companies is directly relevant to real decisions being made right now.

---

## 👥 Stakeholder analysis:
The people who would actually use this tool, and what they'd use it for:

*   **Equity research analysts** — screening for distressed companies before initiating coverage
*   **Portfolio managers** — monitoring existing holdings for deteriorating fundamentals
*   **Credit risk teams** — early warning for potential covenant breaches
*   **Investment banking associates** — quick comp table construction for pitch books
*   **Students and junior analysts** — learning what healthy vs unhealthy looks like across sectors

---

## 🎯 Defining Financial Health (Phase 1)

A financially healthy company has **five core properties** working in harmony. No single metric tells the full story — a company can look profitable but be drowning in debt, or have great liquidity but be shrinking. To evaluate health accurately, we must look through all five lenses:

1. **Profitability** — *"Does the business actually make money?"*
   * A company is profitable when it converts revenue into earnings efficiently. 
   * *Example:* Microsoft has a ~35% net margin (for every $100 of revenue, $35 becomes profit). Snap Inc. has a negative net margin (it spends more than it earns). Both are "tech companies" but lie in completely different health categories.
2. **Liquidity** — *"Can it pay its bills in the next 12 months?"*
   * This is short-term survival. A current ratio above 1.5 means the company has $1.50 in short-term assets for every $1 of short-term obligations. 
   * *Example:* SVB in early 2023 had a liquidity mismatch (assets were locked in long-term bonds it couldn't sell quickly). Liquidity crises can kill even asset-rich companies.
3. **Leverage** — *"How much debt is it carrying?"*
   * Debt amplifies returns but also amplifies risk. The debt-to-equity ratio tells you how levered the capital structure is; the interest coverage ratio tells you how easily the company can make interest payments.
   * *Example:* Amazon carries significant debt but generates enough free cash flow to service it comfortably. A retailer with the same debt load and declining revenue is at high risk.
4. **Efficiency** — *"How well does it use its assets?"*
   * Asset turnover measures how much revenue a company generates per dollar of assets. Efficiency ratios are most meaningful when compared within a specific sector.
   * *Example:* A supermarket like Walmart turns over its asset base 2–3x per year (high velocity, thin margins). A capital-intensive manufacturer might turn over assets once every two years.
5. **Growth** — *"Is the business expanding or contracting?"*
   * A company can score well on all four dimensions above but be slowly dying if revenue is declining year-over-year. Growth is the leading indicator; the other four are lagging.
   * *Example:* Netflix in 2022 had shrinking subscriber growth; its historical financials looked fine, but the trajectory was a clear warning signal.

### 📋 Concrete Examples Across the Health Spectrum

| Company | Why "Strong" or "At Risk" |
| :--- | :--- |
| **Microsoft (MSFT)** | 35%+ net margins, minimal debt relative to cash, growing revenue — strong across all 5 dimensions. |
| **Apple (AAPL)** | Negative book equity (buybacks) but exceptional profitability and FCF — requires ratio interpretation. |
| **Bed Bath & Beyond (2022)** | Revenue declining, high leverage, burning cash — bottom decile before bankruptcy. |
| **SVB (2022)** | Appeared profitable but liquidity mismatch + duration risk — collapsed despite "decent" reported ratios. |
| **Snap (SNAP)** | Negative margins, no FCF, cash burn — at risk despite revenue growth. |

---

## 🛠️ Key Architectural Pillars

### 1. Financial Ratio & Score Engineering
The scoring engine evaluates companies across five distinct dimensions of financial health:
*   **Solvency & Bankruptcy Risk:** Altman Z-Score implementation to quantify default probabilities.
*   **Liquidity Profile:** Current Ratio & Quick Ratio to evaluate short-term obligation coverage.
*   **Financial Leverage:** Debt-to-Equity (D/E) ratio & Interest Coverage Ratio (ICR) to monitor debt load safety margins.
*   **Profitability & Returns:** Return on Equity (ROE), Return on Assets (ROA), and Operating Margin to isolate quality earnings.
*   **Operational Efficiency:** Asset Turnover and Cash Conversion Cycle metrics to track capital utilization.

### 2. Sector Benchmarking & Norms
Financial metrics vary wildly by sector (e.g., a healthy leverage ratio for a Utility company would spell disaster for a Software company). The scorecard normalizes scoring based on **sector-relative performance** rather than applying blunt absolute thresholds.

### 3. Interactive Visualization
A sleek, modern interface allowing:
*   **Macro Heatmaps:** Fast sector-by-sector health comparisons.
*   **Ranked Screening:** Sorting the S&P 500 index by overall score, solvency risk, or individual ratios.
*   **Drill-down Analytics:** Dedicated dashboard for each company detailing historical trends and peer comparisons.

---

## 🚀 Getting Started

*(Placeholder sections for installation and configuration, ready to be customized as the codebase develops.)*

### Prerequisites
*   Node.js (v18+) or Python (v3.9+) depending on project runtime
*   S&P 500 API Keys (or local CSV fundamental data dump)

### Installation
```bash
# Clone the repository
git clone git@github.com:advaitrajeev/my_react_app.git
cd "Financial Health Scorecard — S&P 500 companies"

# Install dependencies
npm install  # For web dashboard
# OR
pip install -r requirements.txt  # For computation backend
```

### Running the App
```bash
npm run dev
# OR
python main.py
```

---

## 🧮 Phase 5: Financial Ratios Dictionary

The following 15 financial ratios form the core of the scorecard feature engineering. They are grouped into five key dimensions: Profitability, Liquidity, Leverage, Efficiency, and Growth.

### Profitability Ratios

*   **Gross Margin:** `Gross Profit / Total Revenue`
    Measures how efficiently a company produces its goods or services. It represents the portion of each dollar of revenue that the company retains as gross profit.
*   **Operating Margin:** `Operating Income / Total Revenue`
    Measures a company's pricing strategy and operating efficiency. It indicates how much profit a company makes after paying for variable costs of production.
*   **Net Profit Margin:** `Net Income / Total Revenue`
    The percentage of revenue left after all expenses have been deducted from sales. It is a strong indicator of the company's overall bottom-line profitability.
*   **Return on Equity (ROE):** `Net Income / Shareholders' Equity`
    Measures a corporation's profitability by revealing how much profit a company generates with the money shareholders have invested.
*   **Return on Assets (ROA):** `Net Income / Total Assets`
    An indicator of how profitable a company is relative to its total assets. It gives an idea as to how efficient management is at using its assets to generate earnings.

### Liquidity Ratios

*   **Current Ratio:** `Current Assets / Current Liabilities`
    Measures a company's ability to pay short-term obligations or those due within one year. A ratio under 1 suggests potential liquidity problems.
*   **Quick Ratio:** `(Current Assets - Inventory) / Current Liabilities`
    A more conservative measure of liquidity than the current ratio. It excludes inventory because it is generally more difficult to turn into cash quickly.

### Leverage / Solvency Ratios

*   **Debt-to-Equity Ratio:** `Total Debt / Shareholders' Equity`
    Evaluates a company's financial leverage. A high ratio indicates that a company is largely using debt to finance its growth, increasing its risk profile.
*   **Debt-to-Assets Ratio:** `Total Debt / Total Assets`
    Shows the degree to which a company has used debt to finance its assets. A higher ratio implies a higher degree of leverage and financial risk.
*   **Interest Coverage Ratio:** `EBIT / Interest Expense`
    Measures how easily a company can pay interest on its outstanding debt. A lower ratio indicates a higher burden of debt expenses on the company.

### Efficiency Ratios

*   **Asset Turnover Ratio:** `Total Revenue / Total Assets`
    Measures the value of a company's sales or revenues relative to the value of its assets. It indicates how efficiently a company is using its assets to generate sales.
*   **Receivables Turnover Ratio:** `Total Revenue / Accounts Receivable`
    Quantifies a firm's effectiveness in extending credit and in collecting debts on that credit. A higher ratio indicates the company operates largely on a cash basis or its collection methods are highly efficient.

### Growth Ratios

*   **Revenue Growth (YoY):** `(Current Year Revenue - Previous Year Revenue) / Previous Year Revenue`
    Measures the rate of increase in a company's sales year-over-year. Consistent revenue growth is a primary indicator of a healthy, expanding business.
*   **EPS Growth (YoY):** `(Current Year Diluted EPS - Previous Year Diluted EPS) / |Previous Year Diluted EPS|`
    Indicates how much a company's bottom-line profitability on a per-share basis is growing. It factors in both net income growth and share buybacks/dilution.
*   **Free Cash Flow Margin:** `Free Cash Flow / Total Revenue`
    Measures what percentage of revenue is converted into free cash flow. High FCF margins indicate a company is highly efficient at converting sales into actual cash.

---

## ⚖️ Phase 6: Scoring Methodology

The heart of the project is the composite health score. Generating a unified 0-100 score across 500 deeply heterogeneous companies requires handling vast differences in capital structure and business models. 

### 1. Sector-Relative Percentile Ranking
Comparing the `Debt-to-Equity` ratio of a software company (like Adobe) to an industrial manufacturer (like Boeing) is mathematically valid but analytically useless. To correct for this, **every company is ranked exclusively against its GICS Sector peers**. 
- A 90th percentile `Current Ratio` means the company is more liquid than 90% of companies in its specific sector.
- **Directional Scoring:** Positive indicators (like `Gross Margin`) are scored normally. Negative indicators (like `Debt-to-Assets`) are inverted (`1 - percentile`) so that higher debt translates to a lower score.

### 2. Dimension Weights
The 15 ratios are aggregated into five dimension sub-scores, which are then weighted to produce the final `Composite Health Score`.

| Dimension | Weight | Rationale |
| :--- | :--- | :--- |
| **Profitability** | `30%` | *The ultimate engine of value.* Without consistent earnings, all other metrics eventually degrade. We assign the highest weight here because a company that can consistently generate cash can usually buy time to fix other issues. |
| **Leverage** | `25%` | *The primary cause of death.* Excessive debt combined with poor interest coverage is the most common catalyst for bankruptcy. This is weighted heavily as a "survival" indicator. |
| **Liquidity** | `20%` | *Short-term survival.* A company can be profitable but still go bankrupt if it cannot meet its near-term obligations (e.g., SVB). |
| **Efficiency** | `15%` | *Operational discipline.* Measures how well management is deploying its capital base. It's important, but less existentially critical than profitability or leverage. |
| **Growth** | `10%` | *The future trajectory.* Growth is highly prized by equity markets, but a company can be "financially healthy" while shrinking (e.g., a mature cash-cow paying high dividends). Therefore, it receives the lowest weight in a pure *health* assessment. |

### 3. Final Health Labels
Based on the final 0-100 score, companies are categorized into actionable brackets:
- 🟢 **Strong (70 - 100):** Best-in-class balance sheet and margins within their sector.
- 🟡 **Moderate (40 - 69):** Average performers; surviving but may have specific dimension weaknesses.
- 🔴 **At risk (0 - 39):** Bottom-decile sector performers exhibiting significant distress, high leverage, or collapsing margins.

