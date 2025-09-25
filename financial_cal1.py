import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import io

# Page configuration
st.set_page_config(
    page_title="Personal Finance Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .category-expense {
        background-color: #ffebee;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.25rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'transactions_df' not in st.session_state:
    st.session_state.transactions_df = None
if 'net_worth_data' not in st.session_state:
    st.session_state.net_worth_data = []

def create_sample_data():
    """Create sample transaction data for demonstration"""
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    
    # Transaction categories and typical amounts
    expense_categories = {
        'Groceries': (-50, -200),
        'Utilities': (-80, -150),
        'Transportation': (-30, -100),
        'Entertainment': (-20, -80),
        'Restaurants': (-25, -75),
        'Shopping': (-40, -200),
        'Healthcare': (-50, -300),
        'Insurance': (-100, -400)
    }
    
    income_categories = {
        'Salary': (2000, 5000),
        'Freelance': (200, 1000),
        'Investment': (50, 500)
    }
    
    transactions = []
    
    # Generate transactions
    for date in dates:
        # Random number of transactions per day (0-5)
        num_transactions = np.random.poisson(1.5)
        
        for _ in range(num_transactions):
            # 80% chance of expense, 20% chance of income
            if np.random.random() < 0.8:
                category = np.random.choice(list(expense_categories.keys()))
                amount_range = expense_categories[category]
                amount = np.random.uniform(amount_range[0], amount_range[1])
                transaction_type = 'Expense'
            else:
                category = np.random.choice(list(income_categories.keys()))
                amount_range = income_categories[category]
                amount = np.random.uniform(amount_range[0], amount_range[1])
                transaction_type = 'Income'
            
            transactions.append({
                'Date': date,
                'Description': f"{category} transaction",
                'Category': category,
                'Amount': round(amount, 2),
                'Type': transaction_type
            })
    
    return pd.DataFrame(transactions).sort_values('Date')

def categorize_transaction(description, amount):
    """Automatically categorize transactions based on description and amount"""
    description = description.lower()
    
    # Income categories
    if any(word in description for word in ['salary', 'paycheck', 'wage', 'income', 'freelance']):
        return 'Income', 'Income'
    if any(word in description for word in ['dividend', 'investment', 'interest']):
        return 'Investment', 'Income'
    
    # Expense categories (negative amounts)
    if amount < 0:
        if any(word in description for word in ['grocery', 'food', 'supermarket', 'walmart', 'costco']):
            return 'Groceries', 'Expense'
        elif any(word in description for word in ['gas', 'fuel', 'uber', 'taxi', 'metro', 'bus']):
            return 'Transportation', 'Expense'
        elif any(word in description for word in ['restaurant', 'cafe', 'pizza', 'mcdonalds', 'starbucks']):
            return 'Restaurants', 'Expense'
        elif any(word in description for word in ['electric', 'water', 'internet', 'phone', 'utility']):
            return 'Utilities', 'Expense'
        elif any(word in description for word in ['movie', 'netflix', 'spotify', 'entertainment', 'game']):
            return 'Entertainment', 'Expense'
        elif any(word in description for word in ['amazon', 'shopping', 'store', 'mall']):
            return 'Shopping', 'Expense'
        elif any(word in description for word in ['doctor', 'hospital', 'pharmacy', 'medical']):
            return 'Healthcare', 'Expense'
        elif any(word in description for word in ['insurance', 'premium']):
            return 'Insurance', 'Expense'
        else:
            return 'Other', 'Expense'
    else:
        return 'Other Income', 'Income'

def process_transactions(df):
    """Process and categorize transactions"""
    if df is None or df.empty:
        return df
    
    # Ensure Date column is datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Auto-categorize if Category column doesn't exist or is empty
    if 'Category' not in df.columns or df['Category'].isnull().any():
        df[['Category', 'Type']] = df.apply(
            lambda row: categorize_transaction(
                row.get('Description', ''), 
                row['Amount']
            ), axis=1, result_type='expand'
        )
    
    # Ensure Type column exists
    if 'Type' not in df.columns:
        df['Type'] = df['Amount'].apply(lambda x: 'Income' if x > 0 else 'Expense')
    
    # Add month-year for grouping
    df['Month_Year'] = df['Date'].dt.to_period('M')
    
    return df

def calculate_metrics(df):
    """Calculate key financial metrics"""
    if df is None or df.empty:
        return {
            'total_income': 0,
            'total_expenses': 0,
            'net_income': 0,
            'monthly_avg_income': 0,
            'monthly_avg_expenses': 0
        }
    
    total_income = df[df['Amount'] > 0]['Amount'].sum()
    total_expenses = abs(df[df['Amount'] < 0]['Amount'].sum())
    net_income = total_income - total_expenses
    
    # Monthly averages - create Month_Year if it doesn't exist
    if 'Month_Year' not in df.columns:
        df['Month_Year'] = df['Date'].dt.to_period('M')
    
    months = df['Month_Year'].nunique() if df['Month_Year'].nunique() > 0 else 1
    monthly_avg_income = total_income / months
    monthly_avg_expenses = total_expenses / months
    
    return {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_income': net_income,
        'monthly_avg_income': monthly_avg_income,
        'monthly_avg_expenses': monthly_avg_expenses
    }

def main():
    # Header
    st.markdown('<h1 class="main-header">💰 Personal Finance Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.header("📊 Dashboard Controls")
    
    # File upload
    uploaded_file = st.sidebar.file_uploader(
        "Upload Transaction CSV", 
        type=['csv'],
        help="Upload a CSV file with columns: Date, Description, Amount (and optionally Category, Type)"
    )
    
    # Sample data option
    if st.sidebar.button("📝 Load Sample Data"):
        st.session_state.transactions_df = create_sample_data()
        st.sidebar.success("Sample data loaded!")
    
    # Clear/Reset button
    if st.sidebar.button("🔄 Start Fresh", type="secondary"):
        st.session_state.transactions_df = None
        st.session_state.net_worth_data = []
        st.sidebar.success("Dashboard reset! Ready for new data.")
        st.rerun()
    
    # Process uploaded file
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.transactions_df = process_transactions(df)
            st.sidebar.success("File uploaded successfully!")
        except Exception as e:
            st.sidebar.error(f"Error reading file: {str(e)}")
    
    # Main content
    if st.session_state.transactions_df is not None:
        df = st.session_state.transactions_df
        
        # Ensure the dataframe is properly processed
        df = process_transactions(df)
        st.session_state.transactions_df = df
        
        # Date filter
        st.sidebar.subheader("📅 Date Filter")
        min_date = df['Date'].min().date()
        max_date = df['Date'].max().date()
        
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            df_filtered = df[(df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)]
        else:
            df_filtered = df
        
        # Calculate metrics
        metrics = calculate_metrics(df_filtered)
        
        # Display key metrics
        st.subheader("📈 Key Financial Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="💵 Total Income",
                value=f"${metrics['total_income']:,.2f}",
                delta=f"${metrics['monthly_avg_income']:,.2f}/month"
            )
        
        with col2:
            st.metric(
                label="💸 Total Expenses",
                value=f"${metrics['total_expenses']:,.2f}",
                delta=f"${metrics['monthly_avg_expenses']:,.2f}/month"
            )
        
        with col3:
            st.metric(
                label="💰 Net Income",
                value=f"${metrics['net_income']:,.2f}",
                delta="Profit" if metrics['net_income'] > 0 else "Loss",
                delta_color="normal" if metrics['net_income'] > 0 else "inverse"
            )
        
        with col4:
            savings_rate = (metrics['net_income'] / metrics['total_income'] * 100) if metrics['total_income'] > 0 else 0
            st.metric(
                label="📊 Savings Rate",
                value=f"{savings_rate:.1f}%",
                delta="Good" if savings_rate > 20 else "Improve"
            )
        
        # Charts section
        st.subheader("📊 Financial Analysis")
        
        # Create tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["💳 Cash Flow", "🏷️ Categories", "📅 Trends", "📋 Transactions"])
        
        with tab1:
            # Monthly cash flow
            monthly_data = df_filtered.groupby(['Month_Year', 'Type'])['Amount'].sum().unstack(fill_value=0)
            if 'Income' not in monthly_data.columns:
                monthly_data['Income'] = 0
            if 'Expense' not in monthly_data.columns:
                monthly_data['Expense'] = 0
                
            monthly_data['Expense'] = abs(monthly_data['Expense'])
            monthly_data['Net'] = monthly_data['Income'] - monthly_data['Expense']
            
            fig_cashflow = go.Figure()
            fig_cashflow.add_trace(go.Bar(
                x=monthly_data.index.astype(str),
                y=monthly_data['Income'],
                name='Income',
                marker_color='green'
            ))
            fig_cashflow.add_trace(go.Bar(
                x=monthly_data.index.astype(str),
                y=monthly_data['Expense'],
                name='Expenses',
                marker_color='red'
            ))
            fig_cashflow.add_trace(go.Scatter(
                x=monthly_data.index.astype(str),
                y=monthly_data['Net'],
                name='Net Cash Flow',
                line=dict(color='blue', width=3),
                mode='lines+markers'
            ))
            
            fig_cashflow.update_layout(
                title="Monthly Cash Flow Analysis",
                xaxis_title="Month",
                yaxis_title="Amount (₹)",
                hovermode='x unified'
            )
            st.plotly_chart(fig_cashflow, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Expense breakdown
                expenses_df = df_filtered[df_filtered['Type'] == 'Expense']
                if not expenses_df.empty:
                    expense_by_category = expenses_df.groupby('Category')['Amount'].sum().abs()
                    
                    fig_pie = px.pie(
                        values=expense_by_category.values,
                        names=expense_by_category.index,
                        title="Expense Breakdown by Category"
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Top expense categories
                if not expenses_df.empty:
                    top_expenses = expense_by_category.sort_values(ascending=True).tail(10)
                    
                    fig_bar = px.bar(
                        x=top_expenses.values,
                        y=top_expenses.index,
                        orientation='h',
                        title="Top Expense Categories",
                        labels={'x': 'Amount (₹)', 'y': 'Category'}
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
        
        with tab3:
            # Weekly spending trend
            df_filtered['Week'] = df_filtered['Date'].dt.to_period('W')
            weekly_expenses = df_filtered[df_filtered['Type'] == 'Expense'].groupby('Week')['Amount'].sum().abs()
            
            fig_trend = px.line(
                x=weekly_expenses.index.astype(str),
                y=weekly_expenses.values,
                title="Weekly Spending Trend",
                labels={'x': 'Week', 'y': 'Expenses (₹)'}
            )
            st.plotly_chart(fig_trend, use_container_width=True)
            
            # Daily spending pattern
            df_filtered['Day_of_Week'] = df_filtered['Date'].dt.day_name()
            daily_pattern = df_filtered[df_filtered['Type'] == 'Expense'].groupby('Day_of_Week')['Amount'].mean().abs()
            
            # Reorder days
            days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            daily_pattern = daily_pattern.reindex(days_order, fill_value=0)
            
            fig_daily = px.bar(
                x=daily_pattern.index,
                y=daily_pattern.values,
                title="Average Daily Spending Pattern",
                labels={'x': 'Day of Week', 'y': 'Average Expenses (₹)'}
            )
            st.plotly_chart(fig_daily, use_container_width=True)
        
        with tab4:
            # Transaction table with filters
            st.subheader("Transaction Details")
            
            # Additional filters
            col1, col2, col3 = st.columns(3)
            with col1:
                type_filter = st.selectbox("Filter by Type", ['All', 'Income', 'Expense'])
            with col2:
                categories = ['All'] + sorted(df_filtered['Category'].unique().tolist())
                category_filter = st.selectbox("Filter by Category", categories)
            with col3:
                min_amount = st.number_input("Minimum Amount", value=0.0)
            
            # Apply filters
            filtered_transactions = df_filtered.copy()
            if type_filter != 'All':
                filtered_transactions = filtered_transactions[filtered_transactions['Type'] == type_filter]
            if category_filter != 'All':
                filtered_transactions = filtered_transactions[filtered_transactions['Category'] == category_filter]
            if min_amount > 0:
                filtered_transactions = filtered_transactions[abs(filtered_transactions['Amount']) >= min_amount]
            
            # Display transactions
            st.dataframe(
                filtered_transactions[['Date', 'Description', 'Category', 'Amount', 'Type']].sort_values('Date', ascending=False),
                use_container_width=True
            )
            
            # Summary statistics
            st.subheader("Summary Statistics")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Total Transactions:** {len(filtered_transactions)}")
                st.write(f"**Date Range:** {filtered_transactions['Date'].min().strftime('%Y-%m-%d')} to {filtered_transactions['Date'].max().strftime('%Y-%m-%d')}")
            with col2:
                st.write(f"**Average Transaction:** ${filtered_transactions['Amount'].mean():.2f}")
                st.write(f"**Largest Expense:** ${filtered_transactions[filtered_transactions['Amount'] < 0]['Amount'].min():.2f}")
        
        # Net Worth Tracking Section
        st.subheader("💎 Net Worth Tracking")
        
        with st.expander("Add Net Worth Entry"):
            col1, col2, col3 = st.columns(3)
            with col1:
                nw_date = st.date_input("Date", value=datetime.now().date())
            with col2:
                assets = st.number_input("Total Assets ($)", min_value=0.0, step=1000.0)
            with col3:
                liabilities = st.number_input("Total Liabilities ($)", min_value=0.0, step=1000.0)
            
            if st.button("Add Net Worth Entry"):
                net_worth = assets - liabilities
                st.session_state.net_worth_data.append({
                    'Date': nw_date,
                    'Assets': assets,
                    'Liabilities': liabilities,
                    'Net_Worth': net_worth
                })
                st.success(f"Added net worth entry: ${net_worth:,.2f}")
        
        # Display net worth chart if data exists
        if st.session_state.net_worth_data:
            nw_df = pd.DataFrame(st.session_state.net_worth_data)
            
            fig_nw = px.line(
                nw_df, 
                x='Date', 
                y='Net_Worth',
                title="Net Worth Over Time",
                labels={'Net_Worth': 'Net Worth ($)', 'Date': 'Date'}
            )
            st.plotly_chart(fig_nw, use_container_width=True)
            
            # Show net worth table
            st.dataframe(nw_df.sort_values('Date', ascending=False), use_container_width=True)
        
        # Export functionality
        st.subheader("💾 Export Data")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Export Summary Report"):
                report = f"""
Personal Finance Summary Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

=== KEY METRICS ===
Total Income: ${metrics['total_income']:,.2f}
Total Expenses: ${metrics['total_expenses']:,.2f}
Net Income: ${metrics['net_income']:,.2f}
Savings Rate: {savings_rate:.1f}%

=== TOP EXPENSE CATEGORIES ===
"""
                if not expenses_df.empty:
                    for cat, amount in expense_by_category.sort_values(ascending=False).head().items():
                        report += f"{cat}: ${amount:,.2f}\n"
                
                st.download_button(
                    label="📄 Download Report",
                    data=report,
                    file_name=f"finance_report_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
        
        with col2:
            # Export processed transactions
            csv_buffer = io.StringIO()
            df_filtered.to_csv(csv_buffer, index=False)
            
            st.download_button(
                label="📊 Download Transactions CSV",
                data=csv_buffer.getvalue(),
                file_name=f"transactions_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    else:
        # Welcome screen
        st.info("👆 Upload a CSV file or load sample data to get started!")
        
        st.markdown("""
        ### 📝 CSV Format Requirements
        Your CSV file should have the following columns:
        - **Date**: Transaction date (YYYY-MM-DD format)
        - **Description**: Transaction description
        - **Amount**: Transaction amount (positive for income, negative for expenses)
        - **Category** (optional): Transaction category
        - **Type** (optional): 'Income' or 'Expense'
        
        ### 🚀 Features
        - 📊 **Cash Flow Analysis**: Monthly income vs expenses
        - 🏷️ **Category Breakdown**: Spending by category
        - 📈 **Trends**: Weekly and daily spending patterns
        - 💰 **Net Worth Tracking**: Track assets and liabilities over time
        - 📋 **Transaction Management**: Filter and search transactions
        - 📄 **Export Reports**: Download summaries and processed data
        
        ### 🎯 Getting Started
        1. Click "Load Sample Data" to see the dashboard in action
        2. Or upload your own CSV file of bank/credit card transactions
        3. Use the date filters and category breakdowns to analyze your finances
        4. Track your net worth over time
        5. Export reports for record keeping
        """)

if __name__ == "__main__":
    main()