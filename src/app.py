import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from forecaster import run_forecast
from llm_explainer import generate_friendly_warning
from datetime import datetime

# --- UI Configuration ---
st.set_page_config(page_title="CashFlow Radar", layout="wide")
st.title("🌊 CashFlow Radar")
st.subheader("Personal Liquidity Forecaster & Early Warning System")

# --- Sidebar Controls ---
st.sidebar.header("Scenario Testing")
st.sidebar.write("Simulate a sudden expense today to see how it impacts your forecast.")
simulated_expense = st.sidebar.number_input("Simulated Expense ($)", min_value=0, max_value=5000, value=0, step=50)

# --- Run the Engine ---
with st.spinner("Analyzing historical data and forecasting next 30 days..."):
    # We pass the real file, and ask Prophet to predict
    forecast_df, baseline = run_forecast(file_path='data/historical_balances.csv', days_ahead=30)

if forecast_df is not None:
    # --- Scenario Logic ---
    # If the user simulates an expense, we shift the whole future prediction down
    if simulated_expense > 0:
        forecast_df.loc[forecast_df['ds'] >= datetime.now(), 'yhat'] -= simulated_expense
        forecast_df.loc[forecast_df['ds'] >= datetime.now(), 'yhat_lower'] -= simulated_expense
        forecast_df.loc[forecast_df['ds'] >= datetime.now(), 'yhat_upper'] -= simulated_expense

    # --- Anomaly Detection for UI ---
    future_only = forecast_df[forecast_df['ds'] >= datetime.now()]
    trouble_spots = future_only[future_only['yhat_lower'] < 0]

    # --- Display AI Warning ---
    if not trouble_spots.empty:
        first_drop = trouble_spots.iloc[0]
        drop_date = first_drop['ds'].strftime('%B %d, %Y')
        
        # Call our LLM Explainer 
        warning_msg = generate_friendly_warning(
            date=drop_date, 
            expected_balance=first_drop['yhat'], 
            worst_case=first_drop['yhat_lower']
        )
        st.error(f"**AI Insight:** {warning_msg}")
    else:
        st.success("**AI Insight:** Your account looks healthy for the next 30 days! No overdraft risk detected.")

    # --- The Interactive Chart ---
    st.write("### 30-Day Balance Forecast")
    
    fig = go.Figure()

    # 1. Plot the historical baseline (Simple Average)
    fig.add_trace(go.Scatter(
        x=forecast_df['ds'], y=[baseline] * len(forecast_df),
        mode='lines', name='Baseline (30-Day Avg)',
        line=dict(color='gray', dash='dash')
    ))

    # 2. Plot the uncertainty bounds (The shaded area)
    fig.add_trace(go.Scatter(
        x=pd.concat([forecast_df['ds'], forecast_df['ds'][::-1]]),
        y=pd.concat([forecast_df['yhat_upper'], forecast_df['yhat_lower'][::-1]]),
        fill='toself',
        fillcolor='rgba(0,176,246,0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=True,
        name='Uncertainty Range (90%)'
    ))

    # 3. Plot the central prediction
    fig.add_trace(go.Scatter(
        x=forecast_df['ds'], y=forecast_df['yhat'],
        mode='lines', name='Expected Balance',
        line=dict(color='blue', width=2)
    ))

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Account Balance ($)",
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # --- Show the Raw Data (Transparency Rule) ---
    with st.expander("View Raw Forecast Data (Transparency)"):
        st.dataframe(future_only[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].rename(
            columns={'ds': 'Date', 'yhat': 'Expected', 'yhat_lower': 'Worst Case', 'yhat_upper': 'Best Case'}
        ))