# 🌊 CashFlow Radar

## i. Overview
**CashFlow Radar** is a lightweight, predictive personal liquidity forecaster. 
Many retail banking customers rely solely on past data and lack accessible tools to look ahead, leading to unexpected overdrafts. This tool solves that by transforming historical account balances into a visual 30-day forecast. It empowers users to understand their future financial health, view uncertainty ranges, and simulate upcoming expenses—all translated into friendly, non-jargon insights by an AI assistant.

## ii. Features
* **Predictive 30-Day Forecasting:** Uses machine learning to project future daily balances based on historical spending patterns (salary, rent, weekends).
* **Uncertainty Visualization:** Displays a 90% confidence interval to show a range of likely outcomes rather than overconfident single-number predictions.
* **Baseline Comparison:** Visually compares the AI forecast against a simple 30-day moving average to prove model efficacy and avoid over-fitting.
* **Early Anomaly Detection:** Continuously monitors the "worst-case scenario" lower bounds. If the model predicts a drop below $0, it triggers an early warning.
* **AI-Powered "Non-Expert" Explanations:** Integrates Google's Gemini LLM to translate raw mathematical anomalies into friendly, actionable 1-sentence warnings.
* **Scenario Testing:** Allows users to simulate a sudden, unexpected expense today to see how it shifts their financial runway for the next month.

## iii. Install and Run Instructions

**Prerequisites:**
* Python 3.9+
* Git

**1. Clone the repository:**
```bash
git clone [https://github.com/aryankk073/cashflow-radar.git](https://github.com/aryankk073/cashflow-radar.git)
cd cashflow-radar