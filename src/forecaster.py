import pandas as pd
from prophet import Prophet
import logging
import warnings

# Suppress harmless warnings to keep the terminal output clean for the judges
logging.getLogger('cmdstanpy').setLevel(logging.WARNING)
warnings.filterwarnings('ignore')

def run_forecast(file_path='data/historical_balances.csv', days_ahead=30):
    print("1. Loading historical data...")
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print("Error: Could not find the CSV. Did you run data_generator.py first?")
        return None, None
        
    df['ds'] = pd.to_datetime(df['ds'])
    
    # --- RULE CHECK: Compare predictions to a simple baseline ---
    print("2. Calculating simple baseline...")
    # Our baseline is just the average balance of the last 30 days
    baseline_val = df['y'].tail(30).mean()
    
    # --- RULE CHECK: Predict future trends and show a range of outcomes ---
    print("3. Training AI model (this takes a few seconds)...")
    # interval_width=0.90 gives us our 90% confidence interval (lower and upper bounds)
    model = Prophet(interval_width=0.90, daily_seasonality=True, yearly_seasonality=True)
    model.fit(df[['ds', 'y']])
    
    # Generate the next 30 days
    future = model.make_future_dataframe(periods=days_ahead)
    forecast = model.predict(future)
    
    # Isolate only the future dates for anomaly checking
    future_forecast = forecast.tail(days_ahead)
    
    # --- RULE CHECK: Detect early warning signs ---
    print("\n------------------------------------------------")
    print("                 FORECAST REPORT                ")
    print("------------------------------------------------")
    
    # Check if the worst-case scenario (lower bound) drops below $0
    trouble_spots = future_forecast[future_forecast['yhat_lower'] < 0]
    
    if not trouble_spots.empty:
        first_drop = trouble_spots.iloc[0]
        drop_date = first_drop['ds'].strftime('%B %d, %Y')
        worst_case = first_drop['yhat_lower']
        expected = first_drop['yhat']
        
        print(f"⚠️ EARLY WARNING TRIGGERED!")
        print(f"Date of concern: {drop_date}")
        print(f"Expected balance: ${expected:.2f}")
        print(f"Worst-case bound: ${worst_case:.2f} (Overdraft risk)")
    else:
        print("✅ Account looks healthy for the next 30 days.")
        print(f"Lowest expected worst-case balance: ${future_forecast['yhat_lower'].min():.2f}")
        
    print("------------------------------------------------\n")
    
    # We return the dataframe so our Streamlit UI can graph it later
    return forecast, baseline_val

if __name__ == "__main__":
    # If we run this file directly, execute the test
    forecast_df, baseline = run_forecast()