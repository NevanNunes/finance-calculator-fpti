import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Finance Tools",
    page_icon="💰",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; font-weight:bold; color:#1f77b4; text-align:center; margin-bottom:2rem;}
    .metric-card {background-color:#f0f2f6; padding:1rem; border-radius:10px; border-left:5px solid #1f77b4;}
    .alert-card {background-color:#ff4c4c; color:white; padding:0.75rem; border-radius:8px; margin:0.25rem 0; font-weight:bold;}
    .success-card {background-color:#4caf50; color:white; padding:0.75rem; border-radius:8px; margin:0.25rem 0; font-weight:bold;}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">💰 Finance Tools Dashboard</h1>', unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs(["💵 Simple Interest Calculator", "📊 Investment Diversification Analyzer"])

# ---------------------- Simple Interest ----------------------
with tab1:
    st.subheader("Simple Interest Calculator")

    principal = st.number_input("Principal Amount (₹)", min_value=0.0, step=1000.0, value=10000.0)
    rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, max_value=100.0, step=0.1, value=5.0)
    time = st.number_input("Time (Years)", min_value=0.1, step=0.1, value=3.0)

    if st.button("Calculate Simple Interest"):
        interest = principal * (rate/100) * time
        total_amount = principal + interest

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Interest Earned (₹)", f"{interest:,.2f}")
        with col2:
            st.metric("Total Amount (₹)", f"{total_amount:,.2f}")

# ---------------------- Investment Diversification ----------------------
with tab2:
    st.subheader("Advanced Investment Diversification Analyzer")

    num_assets = st.number_input("Number of Assets", min_value=1, step=1, value=3)
    
    asset_data = []
    for i in range(int(num_assets)):
        st.markdown(f"### Asset {i+1}")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(f"Asset Name {i+1}", key=f"name_{i}")
        with col2:
            value = st.number_input(f"Asset Value (₹) {i+1}", min_value=0.0, step=100.0, key=f"value_{i}")
        asset_data.append({"Name": name, "Value": value})
    
    threshold = st.slider("Alert if any asset exceeds (%) of portfolio", min_value=1, max_value=100, value=20)

    if st.button("Analyze Portfolio"):
        df = pd.DataFrame(asset_data)
        df['Percentage'] = (df['Value'] / df['Value'].sum()) * 100

        # Alert if exceeds threshold
        over_threshold = df[df['Percentage'] > threshold]

        # Display summary
        st.subheader("Portfolio Summary")
        st.dataframe(df.sort_values('Percentage', ascending=False).reset_index(drop=True))

        # Pie chart
        fig = px.pie(df, names='Name', values='Value', title="Portfolio Allocation", color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True)

        # Alerts
        if not over_threshold.empty:
            st.subheader("⚠️ Assets Exceeding Threshold")
            for idx, row in over_threshold.iterrows():
                st.markdown(f'<div class="alert-card">Asset **{row["Name"]}** is **{row["Percentage"]:.2f}%** of portfolio (> {threshold}%)</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="success-card">All assets are within the defined threshold ✅</div>', unsafe_allow_html=True)

        # Diversification score
        st.subheader("Diversification Score")
        diversification_score = 100 - df['Percentage'].max()
        st.metric("Diversification Score", f"{diversification_score:.1f}%")
