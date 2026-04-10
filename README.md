

# 🌊 CashFlow Radar

## i. Overview
**CashFlow Radar** is a lightweight, predictive personal liquidity forecaster built for the NatWest Hackathon. 
Many retail banking customers experience "balance anxiety"—the fear of making a purchase today and hitting an overdraft before payday. This tool transforms historical transaction data into a visual 30-day forecast. It empowers users to look ahead, understand financial uncertainty, and test spending scenarios, all translated into friendly, non-jargon insights by an AI assistant.

## ii. Features
* **Predictive 30-Day Forecasting:** Uses machine learning (Meta Prophet) to project future daily balances based on historical patterns like salary cycles and weekend spending.
* **Uncertainty Visualization:** Displays a 90% confidence interval (shaded "fan") to show a range of likely outcomes, helping users prepare for the "worst-case."
* **Baseline Comparison:** Visually compares the AI forecast against a 30-day moving average baseline to prove model reliability.
* **Early Anomaly Detection:** Automatically flags potential overdraft risks if the lower bound of the forecast dips below $0.
* **AI-Powered "Non-Expert" Explanations:** Integrates Google's Gemini LLM to translate raw data into friendly, actionable 1-sentence dashboard warnings.
* **Scenario Testing:** An interactive sidebar allows users to simulate a sudden large expense and instantly see its impact on their 30-day financial runway.

## iii. Install and Run Instructions

**Prerequisites:**
* Python 3.9+
* Git

**1. Clone the repository:**
```bash
git clone https://github.com/aryankk073/cashflow-radar.git
cd cashflow-radar
```

**2. Create a virtual environment:**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables:**
Rename `.env.example` to `.env` and add your Google Gemini API key:
```text
GEMINI_API_KEY=your_actual_key_here
```

**5. Generate the synthetic training data:**
```bash
python src/data_generator.py
```

**6. Run the Streamlit Dashboard:**
```bash
streamlit run src/app.py
```

## iv. Tech Stack
* **Programming Language:** Python 3.10
* **Frontend Framework:** Streamlit
* **Data Manipulation:** Pandas & NumPy
* **Forecasting Engine:** Meta Prophet (Time-series with seasonality)
* **LLM / AI Explainer:** Google Gemini 1.5 Flash
* **Charting:** Plotly Graph Objects

## v. Usage Examples
1. **Financial Health Check:** Open the app to see the "AI Insight" banner. If green, your account is healthy; if red, a risk has been detected.
2. **"What-If" Planning:** Use the sidebar to enter a value (e.g., 500). The chart will instantly drop, showing you if that purchase will cause an overdraft later in the month.

## vi. Architecture & Limitations
* **Architecture:** `Data Generator` -> `Prophet Model` -> `Anomaly Logic` -> `Gemini API` -> `Streamlit UI`.
* **Limitations:** This project uses synthetic data via `src/data_generator.py` to simulate a 2-year banking history. Real-world implementation would require a secure connection to a Core Banking API.

---

## vii. Hackathon Use Cases Addressed
This project strictly follows the **Theme 2: AI Predictive Forecasting** guidelines:
1. **Plan Ahead (Short-term forecasting):** Forecasts exactly 30 days ahead to help users plan their monthly budget.
2. **Understand Uncertainty:** Uses uncertainty bands to provide a range (low, likely, high) rather than a single misleading number.
3. **Compare Plans (Scenario forecasting):** Interactive "What-if" spending slider allows users to test the impact of big purchases.
4. **Spot Trouble Early (Anomaly detection):** Detects and flags sudden dips in the worst-case forecast range before they happen.
5. **Transparency & Trust:** Includes a "Raw Data" expander so users can see the exact math behind the AI's prediction.

## viii. Team Contributions
While the final codebase was compiled and pushed via a single repository manager to maintain strict Git DCO and Single-Email compliance, this project was a full collaborative effort by a team of 4:
* **Aditya:** Data Engineering & Synthetic Data Generation.
* **Omkar:** Machine Learning (Meta Prophet integration & Logic).
* **[Teammate 3 Name]:** UI/UX Design & LLM Prompt Engineering.
* **Aryan:** Repository Architecture, Code Integration, & Open-Source Compliance.