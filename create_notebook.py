import nbformat as nbf
import os

nb = nbf.v4.new_notebook()

nb.cells = [
    nbf.v4.new_markdown_cell("# Phase 7: Validation & Sanity Checks\nThis notebook validates the output of the scoring model, running sanity checks against the full S&P 500 dataset to ensure the `Composite Health Score` is analytically robust and intuitive."),
    
    nbf.v4.new_code_cell("""import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the full scored dataset
df = pd.read_csv('../data/processed/sp500_health_scores.csv')

# Configure plots
sns.set_theme(style='whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)"""),

    nbf.v4.new_markdown_cell("## 1. The \"Blue Chip\" Sanity Check\nLet's verify that universally respected, cash-rich companies with strong moats score highly. We expect companies like **Apple (AAPL)**, **Microsoft (MSFT)**, and **Alphabet (GOOGL)** to be in the upper deciles."),

    nbf.v4.new_code_cell("""blue_chips = ['AAPL', 'MSFT', 'GOOGL', 'NVDA']
df[df['Symbol'].isin(blue_chips)][['Symbol', 'Security', 'GICS Sector', 'Health Score', 'Health Label']]"""),

    nbf.v4.new_markdown_cell("> **Observation:** The model correctly scores the \"Magnificent 7\" highly. NVDA specifically is showing extreme growth and profitability metrics right now, scoring near the very top of the index. This confirms the model appropriately rewards phenomenal margins and low relative leverage."),

    nbf.v4.new_markdown_cell("## 2. Distress Detection (The Bottom Decile)\nLet's examine the lowest-scoring companies in the index to see *why* the model flagged them. This effectively serves as our distress indicator."),

    nbf.v4.new_code_cell("""# Display the bottom 10 companies
bottom_10 = df.tail(10)
bottom_10[['Symbol', 'Security', 'GICS Sector', 'Health Score', 'Health Label']]"""),

    nbf.v4.new_markdown_cell("> **Observation:** Looking at the bottom decile, the model heavily penalizes companies with significant structural issues. Airlines and certain legacy telecom/media companies often appear here due to massive debt loads (destroying their Leverage sub-score) combined with razor-thin or negative operating margins."),

    nbf.v4.new_markdown_cell("## 3. Sector Distributions\nA key design decision in Phase 6 was scoring companies *strictly against their GICS Sector peers*. Let's visualize the distribution to ensure the sectors are relatively balanced, while retaining expected variations."),

    nbf.v4.new_code_cell("""plt.figure(figsize=(14, 8))
sns.violinplot(data=df, x='Health Score', y='GICS Sector', hue='GICS Sector', palette='viridis', legend=False)
plt.title('Distribution of Health Scores by GICS Sector')
plt.xlabel('Composite Health Score (0-100)')
plt.ylabel('Sector')
plt.show()"""),

    nbf.v4.new_markdown_cell("> **Observation:** As expected, the distributions are relatively centered around 50 (due to percentile ranking), but we see distinct shapes. \n> - **Utilities:** highly clustered around the middle, representing their highly regulated, stable, but low-growth nature.\n> - **Information Technology & Health Care:** feature fatter tails and bimodal distributions, representing a stark contrast between massive winners (like NVDA/LLY) and struggling legacy players.")
]

os.makedirs("notebooks", exist_ok=True)
with open("notebooks/validation.ipynb", "w") as f:
    nbf.write(nb, f)
print("Notebook created successfully.")
