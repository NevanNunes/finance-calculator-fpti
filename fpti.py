import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Advanced Portfolio Analyzer", page_icon="📊", layout="wide")

# Custom CSS for colorful UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4B0082;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        color: #FF4500;
        font-weight: bold;
        margin-top: 1rem;
    }
    .stButton>button {
        background-color: #4B0082;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">📊 Advanced Investment Diversification Analyzer</h1>', unsafe_allow_html=True)

# Tabs for clean separation
tab1, tab2 = st.tabs(["💼 Portfolio Input", "📈 Analysis & Charts"])

with tab1:
    st.subheader("Enter Your Assets")

    # Form for clean input
    with st.form("asset_form", clear_on_submit=False):
        num_assets = st.number_input("Number of different assets:", min_value=1, value=4, step=1)
        asset_names = []
        asset_values = []

        for i in range(num_assets):
            st.markdown(f"**Asset {i+1}**")
            name = st.text_input(f"Name of Asset {i+1}", key=f"name_{i}", placeholder=f"Asset {i+1}")
            value = st.number_input(f"Value of {name or 'Asset'} (₹)", min_value=0.0, value=1000.0, key=f"value_{i}")
            asset_names.append(name)
            asset_values.append(value)

        threshold = st.slider("Alert if any asset exceeds (%) of portfolio", 0, 100, 20)

        submitted = st.form_submit_button("Analyze Portfolio")

with tab2:
    if submitted:
        assets = {name: val for name, val in zip(asset_names, asset_values) if name.strip() != ""}
        if not assets:
            st.error("Please enter at least one asset name and value.")
        else:
            # Risk levels
            risk_dict = {'Stocks':'High', 'Bonds':'Low', 'Crypto':'Very High', 'Real Estate':'Medium'}
            asset_risks = {k: risk_dict.get(k, 'Unknown') for k in assets.keys()}

            total_value = sum(assets.values())
            allocation = {k: (v / total_value * 100) for k, v in assets.items()}

            df_alloc = pd.DataFrame({
                'Asset': list(allocation.keys()),
                'Percentage': list(allocation.values()),
                'Risk': [asset_risks[k] for k in allocation.keys()]
            })

            st.subheader("📋 Portfolio Allocation Table")
            st.dataframe(df_alloc.style.format({"Percentage": "{:.2f}%"}))

            # Highlight over-allocated assets
            over_allocated = df_alloc[df_alloc['Percentage'] > threshold]
            if not over_allocated.empty:
                st.warning("⚠️ Assets exceeding threshold:")
                st.table(over_allocated)

                st.subheader("🔧 Suggested Rebalancing")
                adjustments = df_alloc.copy()
                adjustments['Suggested (%)'] = adjustments['Percentage'].apply(lambda x: threshold if x > threshold else x)
                st.dataframe(adjustments.style.format({"Percentage": "{:.2f}%", "Suggested (%)": "{:.2f}%"}))
            else:
                st.success("✅ All assets are within the diversification threshold.")

            # Pie chart
            fig_pie = px.pie(
                df_alloc, names='Asset', values='Percentage',
                title='Portfolio Allocation Pie Chart',
                color='Risk',
                color_discrete_map={'Low':'green', 'Medium':'orange', 'High':'red', 'Very High':'darkred', 'Unknown':'grey'}
            )
            fig_pie.update_traces(textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)

            # Bar chart
            fig_bar = px.bar(
                df_alloc, x='Asset', y='Percentage', color='Risk',
                title='Portfolio Allocation Bar Chart',
                text='Percentage',
                color_discrete_map={'Low':'green', 'Medium':'orange', 'High':'red', 'Very High':'darkred', 'Unknown':'grey'}
            )
            fig_bar.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
            st.plotly_chart(fig_bar, use_container_width=True)

            # Download CSV
            csv_data = df_alloc.to_csv(index=False)
            st.download_button("📥 Download Portfolio Summary", data=csv_data, file_name="portfolio_summary.csv", mime="text/csv")
