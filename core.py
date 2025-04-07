import os
import requests
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

# Define the model directory
MODEL_DIR = "models/gpt2"

def load_local_model():
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR, exist_ok=True)
        model = AutoModelForCausalLM.from_pretrained("gpt2")
        tokenizer = AutoTokenizer.from_pretrained("gpt2")
        model.save_pretrained(MODEL_DIR)
        tokenizer.save_pretrained(MODEL_DIR)
    else:
        model = AutoModelForCausalLM.from_pretrained(MODEL_DIR)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    
    return pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=100,
        truncation=True,
        do_sample=True,
        temperature=0.7
    )


# --- API Call Function (Keep as is, remember to replace placeholder) ---
def call_gemini_api(user_input, context=None):
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # Create a comprehensive system prompt for financial expertise
    system_prompt = """You are an experienced financial advisor with expertise in:
    1. Personal budgeting and financial planning
    2. Investment strategies
    3. Debt management
    4. Retirement planning
    5. Emergency fund planning
    
    When providing budget advice:
    - Break down expenses into essential and non-essential categories
    - Use the 50/30/20 rule (50% needs, 30% wants, 20% savings)
    - Provide specific dollar amounts based on the user's income
    - Suggest practical ways to reduce expenses
    - Recommend savings goals and investment options
    - Consider local cost of living based on the user's country
    
    Always provide actionable, specific advice with numbers and percentages."""

    # Create a detailed context-aware prompt
    if context:
        monthly_income = float(context.get('income', 0))
        
        # Calculate suggested budget allocations
        needs = monthly_income * 0.5
        wants = monthly_income * 0.3
        savings = monthly_income * 0.2
        
        context_prompt = f"""
        {system_prompt}

        User's Financial Profile:
        - Age: {context.get('age', 'Not specified')}
        - Monthly Income: ${monthly_income:,.2f}
        - Monthly Expenses Level: {context.get('expenses', 'Not specified')}
        - Financial Goals: {context.get('goals', 'Not specified')}
        - Country: {context.get('country', 'Not specified')}

        Suggested Monthly Budget Breakdown (50/30/20 Rule):
        1. Needs (50%): ${needs:,.2f}
           - Rent/Housing
           - Utilities
           - Groceries
           - Transportation
           - Insurance
           - Minimum Debt Payments

        2. Wants (30%): ${wants:,.2f}
           - Entertainment
           - Dining Out
           - Shopping
           - Hobbies
           - Subscriptions

        3. Savings/Debt (20%): ${savings:,.2f}
           - Emergency Fund
           - Retirement Savings
           - Investment
           - Extra Debt Payments
           - Financial Goals

        Current Question: {user_input}

        Please provide specific financial advice considering the user's profile and the suggested budget breakdown above. Include:
        1. Specific recommendations for their situation
        2. Dollar amounts and percentages where relevant
        3. Action items they can implement immediately
        4. Long-term financial planning suggestions
        5. Any relevant warnings or areas of concern
        """
    else:
        context_prompt = f"{system_prompt}\n\nQuestion: {user_input}"

    # Generate response with context
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=context_prompt
    )

    return response.text


