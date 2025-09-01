from flask import Flask, request, jsonify
import pandas as pd
import io
from flask_cors import CORS
import google.generativeai as genai

# --- CONFIGURATION ---
GOOGLE_API_KEY="AIzaSyDd3lDVujzvAAtQTIMvnyqzIZF8n9WQgzY" # Make sure your key is pasted here
genai.configure(api_key=GOOGLE_API_KEY)

app = Flask(__name__)
CORS(app)

# --- AI PROMPT FUNCTION (Unchanged) ---
def get_gemini_response(data):
    total = data['total_expenses']
    summary_items = [f"- {category}: ₹{amount}" for category, amount in data['summary'].items()]
    summary_str = "\n".join(summary_items)
    prompt = f"""
    You are a friendly and helpful personal finance assistant. A user has uploaded their monthly expense report. Here is the data:
    Total Monthly Expenses: ₹{total}
    Spending Breakdown by Category:
    {summary_str}
     Based on this data, please do the following:
    1. Provide a short, encouraging summary of their spending (2-3 sentences).
    2. Print all of their expenses stating your expenses.
    3. Highlight their top 2-3 spending categories (give them as list).
    4. Offer one clear, actionable saving tip based on their highest controllable spending category (avoid suggesting cuts to 'Rent' or 'Bills & Utilities' if possible).
    5. Add emojis.
    6. After doing all these, leave some space and ask do you need help with anything else.
    Keep the entire response concise, friendly, and easy to understand.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred with the AI model: {str(e)}"

# --- DATA ANALYSIS LOGIC (Updated for chart) ---
def categorize_expense(description):
    # This function is the same as before
    description = description.lower()
    if 'zomato' in description or 'swiggy' in description or 'dinner' in description: return 'Food & Dining'
    elif 'rent' in description: return 'Rent'
    elif 'groceries' in description or 'dmart' in description: return 'Groceries'
    elif 'bill' in description or 'recharge' in description: return 'Bills & Utilities'
    elif 'uber' in description: return 'Transport'
    elif 'netflix' in description or 'movie' in description: return 'Entertainment'
    elif 'myntra' in description or 'shopping' in description: return 'Shopping'
    else: return 'Other'

def analyze_expenses(file):
    try:
        df = pd.read_csv(file)
        df['Category'] = df['Description'].apply(categorize_expense)
        total_expenses = int(df['Amount'].sum())
        summary_raw = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
        summary_dict = {key: int(value) for key, value in summary_raw.to_dict().items()}
        
        # NEW: Prepare data for the chart
        chart_labels = list(summary_raw.index)
        chart_data = [int(value) for value in summary_raw.values]

        return {
            'total_expenses': total_expenses,
            'summary': summary_dict,
            'chart_labels': chart_labels, # Add labels list
            'chart_data': chart_data,     # Add data list
            'status': 'success'
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

# --- FLASK ROUTE (Unchanged) ---
@app.route('/analyze', methods=['POST'])
def handle_analysis():
    if 'expense_file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'}), 400
    file = request.files['expense_file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'}), 400
    if file:
        analysis_results = analyze_expenses(file)
        if analysis_results['status'] == 'success':
            gemini_response = get_gemini_response(analysis_results)
            analysis_results['llm_response'] = gemini_response
            return jsonify(analysis_results)
        else:
            return jsonify(analysis_results)

if __name__ == '__main__':
    app.run(debug=True)
