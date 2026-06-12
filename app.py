import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- Configuration ---
st.set_page_config(page_title="S&P 500 Financial Health Scorecard", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    project_root = os.path.dirname(os.path.abspath(__file__))
    health_scores_path = os.path.join(project_root, "data", "processed", "sp500_health_scores.csv")
    cleaned_ratios_path = os.path.join(project_root, "data", "processed", "sp500_cleaned_ratios.csv")
    
    df_scores = pd.read_csv(health_scores_path)
    df_ratios = pd.read_csv(cleaned_ratios_path)
    
    # Merge them so we have all raw ratios, percentiles, and sub-scores in one place
    # Avoid duplicate columns
    cols_to_use = df_ratios.columns.difference(df_scores.columns).tolist() + ['Symbol']
    df_merged = pd.merge(df_scores, df_ratios[cols_to_use], on='Symbol', how='left')
    return df_merged

try:
    df = load_data()
except FileNotFoundError:
    st.error("Data not found. Please ensure the backend scoring engine has been run.")
    st.stop()

st.title("S&P 500 Financial Health Scorecard 📊")

tab1, tab2, tab3 = st.tabs(["Sector Overview", "Company Drill-down", "Full Universe Table"])

# --- VIEW 1: SECTOR OVERVIEW ---
with tab1:
    st.header("Sector Overview")
    sectors = sorted(df['GICS Sector'].dropna().unique())
    selected_sector = st.selectbox("Select Sector", sectors)
    
    sector_df = df[df['GICS Sector'] == selected_sector]
    
    # Summary Stats
    median_score = sector_df['Health Score'].median()
    at_risk_pct = (len(sector_df[sector_df['Health Label'] == 'At risk']) / len(sector_df)) * 100
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Companies in Sector", len(sector_df))
    col2.metric("Median Health Score", f"{median_score:.1f}/100")
    col3.metric("% At Risk", f"{at_risk_pct:.1f}%")
    
    st.markdown("---")
    
    # Top 10 and Bottom 10 Bar Charts
    col_bar1, col_bar2 = st.columns(2)
    
    with col_bar1:
        top_10 = sector_df.nlargest(10, 'Health Score').sort_values('Health Score', ascending=True)
        fig_top = px.bar(top_10, x='Health Score', y='Security', orientation='h', title='Top 10 Healthiest Companies', color='Health Score', color_continuous_scale='Greens')
        fig_top.update_layout(yaxis_title=None)
        st.plotly_chart(fig_top, use_container_width=True)
        
    with col_bar2:
        bottom_10 = sector_df.nsmallest(10, 'Health Score').sort_values('Health Score', ascending=True)
        fig_bottom = px.bar(bottom_10, x='Health Score', y='Security', orientation='h', title='Bottom 10 Companies (Most Distressed)', color='Health Score', color_continuous_scale='Reds_r')
        fig_bottom.update_layout(yaxis_title=None)
        st.plotly_chart(fig_bottom, use_container_width=True)
        
    st.markdown("---")
    
    # Heatmap: all companies x 5 dimensions
    st.subheader("Sector Dimension Heatmap")
    dim_cols = ["Profitability Score", "Leverage Score", "Liquidity Score", "Efficiency Score", "Growth Score"]
    
    heatmap_data = sector_df.sort_values("Health Score", ascending=False).set_index("Security")[dim_cols]
    fig_heatmap = px.imshow(heatmap_data, 
                            labels=dict(x="Dimension", y="Company", color="Score (0-100)"),
                            x=["Profitability", "Leverage", "Liquidity", "Efficiency", "Growth"],
                            aspect="auto",
                            color_continuous_scale='RdYlGn')
    # Dynamically scale the height of the heatmap based on how many companies are in the sector
    fig_heatmap.update_layout(height=max(400, len(sector_df) * 15)) 
    st.plotly_chart(fig_heatmap, use_container_width=True)

# --- VIEW 2: COMPANY DRILL-DOWN ---
with tab2:
    st.header("Company Drill-down")
    
    # Search box for ticker
    search_list = df.apply(lambda row: f"{row['Symbol']} - {row['Security']}", axis=1).tolist()
    
    selected_search = st.selectbox("Search for a Company", search_list)
    selected_ticker = selected_search.split(" - ")[0]
    
    comp_data = df[df['Symbol'] == selected_ticker].iloc[0]
    
    st.subheader(f"{comp_data['Security']} ({comp_data['Symbol']})")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Sector", comp_data['GICS Sector'])
    col_m2.metric("Health Score", f"{comp_data['Health Score']:.1f}/100")
    
    # Color code health label
    label_color = "green" if comp_data['Health Label'] == "Strong" else "orange" if comp_data['Health Label'] == "Moderate" else "red"
    col_m3.markdown(f"**Health Label:** <span style='color:{label_color}; font-size:24px'>{comp_data['Health Label']}</span>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    col_radar, col_table = st.columns([1, 1])
    
    with col_radar:
        st.write("**Dimension Balance (0-100)**")
        categories = ['Profitability', 'Leverage', 'Liquidity', 'Efficiency', 'Growth']
        scores = [comp_data['Profitability Score'], comp_data['Leverage Score'], 
                  comp_data['Liquidity Score'], comp_data['Efficiency Score'], comp_data['Growth Score']]
        
        # Close the radar loop
        scores = [0 if pd.isna(s) else s for s in scores] # handle NaNs
        scores.append(scores[0])
        cat_loop = categories + [categories[0]]
        
        fig_radar = go.Figure(data=go.Scatterpolar(
          r=scores,
          theta=cat_loop,
          fill='toself',
          line_color='#2ca02c'
        ))
        
        fig_radar.update_layout(
          polar=dict(
            radialaxis=dict(
              visible=True,
              range=[0, 100]
            )),
          showlegend=False
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        
    with col_table:
        st.write("**15-Ratio Benchmark (vs Sector)**")
        
        metrics_list = [
            "Gross Margin", "Operating Margin", "Net Margin", "ROE", "ROA",
            "Current Ratio", "Quick Ratio",
            "Debt-to-Equity", "Debt-to-Assets", "Interest Coverage Ratio",
            "Asset Turnover", "Receivables Turnover",
            "Revenue Growth (YoY)", "EPS Growth (YoY)", "Free Cash Flow Margin"
        ]
        
        table_data = []
        for m in metrics_list:
            raw_val = comp_data.get(m, float('nan'))
            pct_val = comp_data.get(f"{m} (Pct)", float('nan'))
            
            # Formatting
            if pd.isna(raw_val):
                raw_str = "N/A"
            elif "Margin" in m or "Growth" in m or "RO" in m:
                raw_str = f"{raw_val*100:.1f}%"
            else:
                raw_str = f"{raw_val:.2f}"
                
            pct_str = f"{pct_val*100:.1f}th" if pd.notna(pct_val) else "N/A"
            
            table_data.append({
                "Metric": m,
                "Raw Value": raw_str,
                "Sector Percentile": pct_str
            })
            
        st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)


# --- VIEW 3: FULL UNIVERSE TABLE ---
with tab3:
    st.header("Full Universe Data")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    
    all_sectors = ["All"] + sorted(df['GICS Sector'].dropna().unique().tolist())
    filter_sector = col_f1.selectbox("Filter by Sector", all_sectors)
    
    filter_label = col_f2.selectbox("Filter by Health Label", ["All", "Strong", "Moderate", "At risk"])
    
    filter_score = col_f3.slider("Minimum Health Score", 0, 100, 0)
    
    # Apply filters
    filtered_df = df.copy()
    if filter_sector != "All":
        filtered_df = filtered_df[filtered_df['GICS Sector'] == filter_sector]
    if filter_label != "All":
        filtered_df = filtered_df[filtered_df['Health Label'] == filter_label]
        
    filtered_df = filtered_df[filtered_df['Health Score'] >= filter_score]
    
    display_cols = ["Symbol", "Security", "GICS Sector", "Health Score", "Health Label", 
                    "Profitability Score", "Leverage Score", "Liquidity Score", "Efficiency Score", "Growth Score"]
    
    # Display table
    st.dataframe(
        filtered_df[display_cols].sort_values("Health Score", ascending=False),
        use_container_width=True, 
        hide_index=True
    )
    
    # Download Button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name='sp500_health_scores_filtered.csv',
        mime='text/csv',
    )
