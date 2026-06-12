"""
ratios.py
---------
Contains individual functions to calculate financial health ratios
across 5 dimensions: Profitability, Liquidity, Leverage, Efficiency, Growth.

These functions handle missing data and edge cases using numpy and pandas.
"""

import pandas as pd
import numpy as np

# =============================================================================
# PROFITABILITY
# =============================================================================

def calc_gross_margin(gross_profit: pd.Series, revenue: pd.Series) -> pd.Series:
    """
    Gross Margin
    
    Formula: Gross Profit / Total Revenue
    
    Measures how efficiently a company produces its goods or services. 
    It represents the portion of each dollar of revenue that the company retains as gross profit.
    """
    return np.where(revenue > 0, gross_profit / revenue, np.nan)

def calc_operating_margin(operating_income: pd.Series, revenue: pd.Series) -> pd.Series:
    """
    Operating Margin
    
    Formula: Operating Income / Total Revenue
    
    Measures a company's pricing strategy and operating efficiency. 
    It indicates how much profit a company makes after paying for variable costs of production.
    """
    return np.where(revenue > 0, operating_income / revenue, np.nan)

def calc_net_profit_margin(net_income: pd.Series, revenue: pd.Series) -> pd.Series:
    """
    Net Profit Margin
    
    Formula: Net Income / Total Revenue
    
    The percentage of revenue left after all expenses have been deducted from sales.
    It is a strong indicator of the company's overall bottom-line profitability.
    """
    return np.where(revenue > 0, net_income / revenue, np.nan)

def calc_return_on_equity(net_income: pd.Series, equity: pd.Series) -> pd.Series:
    """
    Return on Equity (ROE)
    
    Formula: Net Income / Shareholders' Equity
    
    Measures a corporation's profitability by revealing how much profit a company generates 
    with the money shareholders have invested. (Note: meaningful only when Equity > 0).
    """
    return np.where(equity > 0, net_income / equity, np.nan)

def calc_return_on_assets(net_income: pd.Series, total_assets: pd.Series) -> pd.Series:
    """
    Return on Assets (ROA)
    
    Formula: Net Income / Total Assets
    
    An indicator of how profitable a company is relative to its total assets. 
    It gives an idea as to how efficient management is at using its assets to generate earnings.
    """
    return np.where(total_assets > 0, net_income / total_assets, np.nan)


# =============================================================================
# LIQUIDITY
# =============================================================================

def calc_current_ratio(current_assets: pd.Series, current_liabilities: pd.Series) -> pd.Series:
    """
    Current Ratio
    
    Formula: Current Assets / Current Liabilities
    
    Measures a company's ability to pay short-term obligations or those due within one year.
    A ratio under 1 suggests potential liquidity problems.
    """
    return np.where(current_liabilities > 0, current_assets / current_liabilities, np.nan)

def calc_quick_ratio(current_assets: pd.Series, inventory: pd.Series, current_liabilities: pd.Series) -> pd.Series:
    """
    Quick Ratio
    
    Formula: (Current Assets - Inventory) / Current Liabilities
    
    A more conservative measure of liquidity than the current ratio. It excludes inventory 
    because it is generally more difficult to turn into cash quickly.
    """
    # If inventory is missing, treat it as 0 for calculation purposes
    inv = inventory.fillna(0)
    return np.where(current_liabilities > 0, (current_assets - inv) / current_liabilities, np.nan)


# =============================================================================
# LEVERAGE / SOLVENCY
# =============================================================================

def calc_debt_to_equity(total_debt: pd.Series, equity: pd.Series) -> pd.Series:
    """
    Debt-to-Equity Ratio
    
    Formula: Total Debt / Shareholders' Equity
    
    Evaluates a company's financial leverage. A high ratio indicates that a company 
    is largely using debt to finance its growth, increasing its risk profile.
    """
    return np.where(equity > 0, total_debt / equity, np.nan)

def calc_debt_to_assets(total_debt: pd.Series, total_assets: pd.Series) -> pd.Series:
    """
    Debt-to-Assets Ratio
    
    Formula: Total Debt / Total Assets
    
    Shows the degree to which a company has used debt to finance its assets. 
    A higher ratio implies a higher degree of leverage and financial risk.
    """
    return np.where(total_assets > 0, total_debt / total_assets, np.nan)

def calc_interest_coverage(ebit: pd.Series, interest_expense: pd.Series) -> pd.Series:
    """
    Interest Coverage Ratio
    
    Formula: EBIT / Interest Expense
    
    Measures how easily a company can pay interest on its outstanding debt. 
    A lower ratio indicates a higher burden of debt expenses on the company.
    """
    return np.where(interest_expense > 0, ebit / interest_expense, np.nan)


# =============================================================================
# EFFICIENCY
# =============================================================================

def calc_asset_turnover(revenue: pd.Series, total_assets: pd.Series) -> pd.Series:
    """
    Asset Turnover Ratio
    
    Formula: Total Revenue / Total Assets
    
    Measures the value of a company's sales or revenues relative to the value of its assets.
    It indicates how efficiently a company is using its assets to generate sales.
    """
    return np.where(total_assets > 0, revenue / total_assets, np.nan)

def calc_receivables_turnover(revenue: pd.Series, accounts_receivable: pd.Series) -> pd.Series:
    """
    Receivables Turnover Ratio
    
    Formula: Total Revenue / Accounts Receivable
    
    Quantifies a firm's effectiveness in extending credit and in collecting debts on that credit.
    A higher ratio indicates the company operates largely on a cash basis or its collection methods are highly efficient.
    """
    return np.where(accounts_receivable > 0, revenue / accounts_receivable, np.nan)


# =============================================================================
# GROWTH
# =============================================================================

def extract_revenue_growth(yoy_growth: pd.Series) -> pd.Series:
    """
    Revenue Growth (YoY)
    
    Formula: (Current Year Revenue - Previous Year Revenue) / Previous Year Revenue
    
    Measures the rate of increase in a company's sales year-over-year. 
    Consistent revenue growth is a primary indicator of a healthy, expanding business.
    """
    return yoy_growth

def extract_eps_growth(eps_growth: pd.Series) -> pd.Series:
    """
    EPS Growth (YoY)
    
    Formula: (Current Year Diluted EPS - Previous Year Diluted EPS) / |Previous Year Diluted EPS|
    
    Indicates how much a company's bottom-line profitability on a per-share basis is growing.
    It factors in both net income growth and share buybacks/dilution.
    """
    return eps_growth

def calc_free_cash_flow_margin(fcf: pd.Series, revenue: pd.Series) -> pd.Series:
    """
    Free Cash Flow Margin
    
    Formula: Free Cash Flow / Total Revenue
    
    Measures what percentage of revenue is converted into free cash flow. 
    High FCF margins indicate a company is highly efficient at converting sales into actual cash.
    """
    return np.where(revenue > 0, fcf / revenue, np.nan)
