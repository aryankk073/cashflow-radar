import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load the hidden .env file
load_dotenv()

def generate_friendly_warning(date, expected_balance, worst_case):
    print("🤖 Asking AI to translate financial data into plain English...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    # Fallback just in case the API key isn't working
    if not api_key or api_key == "your_actual_api_key_here":
        print("(Using fallback text because API key isn't detected)")
        return f"Heads up! Your balance might dip to around ${worst_case:.2f} by {date}, so you might want to delay any big purchases."

    # Configure Gemini
    genai.configure(api_key=api_key)
    
    # We use gemini-1.5-flash because it is lightning fast and free
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # This is the "Prompt Engineering"
    prompt = f"""
    You are a friendly, helpful banking assistant inside a mobile app.
    Our predictive AI model has flagged a potential low-balance warning for a user. 
    
    Date of concern: {date}
    Expected Balance: ${expected_balance:.2f}
    Worst-case scenario (Lower bound): ${worst_case:.2f}
    
    Write a single, 1-sentence friendly warning for the user's dashboard. 
    Do not use financial jargon. Be helpful, not scary. Suggest they check their upcoming expenses.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Heads up! Your balance might dip to around ${worst_case:.2f} by {date}. Consider reviewing your upcoming expenses."

if __name__ == "__main__":
    # Test the function directly
    test_warning = generate_friendly_warning("November 15", 50.00, -25.50)
    print("\nFINAL DASHBOARD TEXT:")
    print(f"\"{test_warning}\"")