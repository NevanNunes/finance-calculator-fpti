import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Finance Calculators - FPTI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #2E4BC7;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        background: linear-gradient(90deg, #2E4BC7 0%, #7B68EE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .main-description {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .calculator-header {
        text-align: center;
        color: #2E4BC7;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .calculator-description {
        text-align: center;
        color: #555;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        padding: 0.5rem;
    }
    
    .result-container {
        background: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: linear-gradient(90deg, #2E4BC7 0%, #7B68EE 100%);
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        z-index: 999;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #2E4BC7 0%, #7B68EE 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        font-size: 1rem;
        transition: all 0.3s;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.95);
    }
</style>
""", unsafe_allow_html=True)

# Main title and description
st.markdown('<h1 class="main-title">📊 Finance Calculators – FPTI</h1>', unsafe_allow_html=True)
st.markdown('<p class="main-description">Your comprehensive toolkit for financial calculations and planning</p>', unsafe_allow_html=True)

# Sidebar menu
st.sidebar.title("🔧 Finance Toolkit")
st.sidebar.markdown("---")

menu_option = st.sidebar.selectbox(
    "Choose a Calculator:",
    ["💰 Simple Interest Calculator", "📉 Inflation Impact Calculator", "🧾 Simple Income Tax Estimator"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ About")
st.sidebar.info("This toolkit provides essential financial calculators to help you make informed financial decisions.")

# Simple Interest Calculator
if menu_option == "💰 Simple Interest Calculator":
    st.markdown('<div class="calculator-header">💰 Simple Interest Calculator</div>', unsafe_allow_html=True)
    st.markdown('<p class="calculator-description">Calculate simple interest and total amount for your investments</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        principal = st.number_input("💵 Principal Amount (₹)", min_value=0.0, value=10000.0, step=1000.0)
    
    with col2:
        rate = st.number_input("📈 Annual Interest Rate (%)", min_value=0.0, value=5.0, step=0.1)
    
    with col3:
        time = st.number_input("📅 Time Period (years)", min_value=0.0, value=1.0, step=0.5)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🧮 Calculate Interest", key="si_calc"):
            if principal > 0 and rate > 0 and time > 0:
                simple_interest = (principal * rate * time) / 100
                total_amount = principal + simple_interest
                
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                st.success(f"💰 **Simple Interest:** ₹{simple_interest:,.2f}")
                st.success(f"💸 **Total Amount:** ₹{total_amount:,.2f}")
                st.info(f"📊 **Growth:** Your investment will grow by ₹{simple_interest:,.2f} ({((simple_interest/principal)*100):.2f}%)")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("⚠️ Please enter valid positive values for all fields!")

# Inflation Impact Calculator
elif menu_option == "📉 Inflation Impact Calculator":
    st.markdown('<div class="calculator-header">📉 Inflation Impact Calculator</div>', unsafe_allow_html=True)
    st.markdown('<p class="calculator-description">Understand how inflation affects your money\'s purchasing power over time</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        current_value = st.number_input("💰 Current Value (₹)", min_value=0.0, value=100000.0, step=5000.0)
    
    with col2:
        inflation_rate = st.number_input("📈 Annual Inflation Rate (%)", min_value=0.0, value=6.0, step=0.1)
    
    with col3:
        years = st.number_input("📅 Time Period (years)", min_value=1, value=10, step=1)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("📊 Calculate Impact", key="inflation_calc"):
            if current_value > 0 and inflation_rate >= 0 and years > 0:
                # Calculate future purchasing power
                future_purchasing_power = current_value / ((1 + inflation_rate/100) ** years)
                purchasing_power_loss = current_value - future_purchasing_power
                loss_percentage = (purchasing_power_loss / current_value) * 100
                
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                st.warning(f"💸 **Future Purchasing Power:** ₹{future_purchasing_power:,.2f}")
                st.error(f"📉 **Purchasing Power Loss:** ₹{purchasing_power_loss:,.2f} ({loss_percentage:.2f}%)")
                st.info(f"📊 **Today's ₹{current_value:,.0f} will be worth ₹{future_purchasing_power:,.2f} after {years} years**")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Create chart data
                chart_years = list(range(0, int(years) + 1))
                chart_values = [current_value / ((1 + inflation_rate/100) ** year) for year in chart_years]
                
                chart_data = pd.DataFrame({
                    'Year': chart_years,
                    'Purchasing Power (₹)': chart_values
                })
                
                st.markdown("### 📈 Purchasing Power Over Time")
                st.line_chart(data=chart_data.set_index('Year'))
                
                # Additional insights
                st.markdown("### 💡 Insights")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Annual Loss Rate", f"{inflation_rate}%", f"-₹{(current_value * inflation_rate/100):,.0f}")
                with col2:
                    required_return = inflation_rate + 2  # Beat inflation by 2%
                    st.metric("Required Return to Beat Inflation", f"{required_return}%", f"+2%")
            else:
                st.error("⚠️ Please enter valid positive values for all fields!")

# Simple Income Tax Estimator
elif menu_option == "🧾 Simple Income Tax Estimator":
    st.markdown('<div class="calculator-header">🧾 Simple Income Tax Estimator</div>', unsafe_allow_html=True)
    st.markdown('<p class="calculator-description">Estimate your income tax based on progressive tax slabs</p>', unsafe_allow_html=True)
    
    # Tax slab information
    st.info("""
    📋 **Progressive Tax Slabs:**
    - ₹0 - ₹10,000: 10% tax rate
    - ₹10,001 - ₹30,000: 12% tax rate  
    - Above ₹30,000: 20% tax rate
    
    💡 Progressive taxation means you pay different rates on different portions of your income.
    """)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        annual_income = st.number_input("💰 Annual Income (₹)", min_value=0.0, value=50000.0, step=5000.0)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🧮 Calculate Tax", key="tax_calc"):
            if annual_income >= 0:
                tax_amount = 0
                tax_breakdown = []
                
                # Calculate progressive tax
                if annual_income > 30000:
                    # 20% on amount above 30,000
                    tax_on_high = (annual_income - 30000) * 0.20
                    tax_amount += tax_on_high
                    tax_breakdown.append(f"₹{tax_on_high:,.2f} (20% on ₹{annual_income - 30000:,.2f})")
                    
                    # 12% on 10,001 to 30,000
                    tax_on_mid = 20000 * 0.12
                    tax_amount += tax_on_mid
                    tax_breakdown.append(f"₹{tax_on_mid:,.2f} (12% on ₹20,000)")
                    
                    # 10% on 0 to 10,000
                    tax_on_low = 10000 * 0.10
                    tax_amount += tax_on_low
                    tax_breakdown.append(f"₹{tax_on_low:,.2f} (10% on ₹10,000)")
                    
                elif annual_income > 10000:
                    # 12% on amount above 10,000
                    tax_on_mid = (annual_income - 10000) * 0.12
                    tax_amount += tax_on_mid
                    tax_breakdown.append(f"₹{tax_on_mid:,.2f} (12% on ₹{annual_income - 10000:,.2f})")
                    
                    # 10% on 0 to 10,000
                    tax_on_low = 10000 * 0.10
                    tax_amount += tax_on_low
                    tax_breakdown.append(f"₹{tax_on_low:,.2f} (10% on ₹10,000)")
                    
                else:
                    # 10% on entire amount
                    tax_amount = annual_income * 0.10
                    tax_breakdown.append(f"₹{tax_amount:,.2f} (10% on ₹{annual_income:,.2f})")
                
                effective_tax_rate = (tax_amount / annual_income * 100) if annual_income > 0 else 0
                net_income = annual_income - tax_amount
                
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                st.error(f"💸 **Total Tax Amount:** ₹{tax_amount:,.2f}")
                st.success(f"💰 **Net Income:** ₹{net_income:,.2f}")
                st.info(f"📊 **Effective Tax Rate:** {effective_tax_rate:.2f}%")
                
                # Tax breakdown
                st.markdown("### 📋 Tax Breakdown:")
                for breakdown in reversed(tax_breakdown):
                    st.write(f"• {breakdown}")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Visual representation
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Gross Income", f"₹{annual_income:,.0f}")
                with col2:
                    st.metric("Tax Paid", f"₹{tax_amount:,.0f}", f"-{effective_tax_rate:.1f}%")
                with col3:
                    st.metric("Net Income", f"₹{net_income:,.0f}")
                    
            else:
                st.error("⚠️ Please enter a valid income amount!")

# Footer
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    Made with ❤️ using Streamlit | FPTI Project
</div>
""", unsafe_allow_html=True)