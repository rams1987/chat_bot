import os
import requests
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from dotenv import load_dotenv
from google import genai
from typing import Dict, Optional

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

class FinancialAdvisor:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.0-flash"
        
    def _get_system_prompt(self) -> str:
        """Returns the system prompt defining the financial advisor's role and capabilities."""
        return """You are an experienced financial advisor with expertise in:
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

    def _calculate_budget_allocation(self, monthly_income: float) -> Dict[str, float]:
        """Calculate budget allocations based on the 50/30/20 rule."""
        return {
            'needs': monthly_income * 0.5,
            'wants': monthly_income * 0.3,
            'savings': monthly_income * 0.2
        }

    def _format_budget_categories(self, budget: Dict[str, float]) -> str:
        """Format budget categories with specific examples."""
        return f"""
        1. Needs (50%): ${budget['needs']:,.2f}
           - Rent/Housing
           - Utilities
           - Groceries
           - Transportation
           - Insurance
           - Minimum Debt Payments

        2. Wants (30%): ${budget['wants']:,.2f}
           - Entertainment
           - Dining Out
           - Shopping
           - Hobbies
           - Subscriptions

        3. Savings/Debt (20%): ${budget['savings']:,.2f}
           - Emergency Fund
           - Retirement Savings
           - Investment
           - Extra Debt Payments
           - Financial Goals
        """

    def _format_user_profile(self, context: Dict) -> str:
        """Format user's financial profile."""
        return f"""
        User's Financial Profile:
        - Age: {context.get('age', 'Not specified')}
        - Monthly Income: ${float(context.get('income', 0)):,.2f}
        - Monthly Expenses Level: {context.get('expenses', 'Not specified')}
        - Financial Goals: {context.get('goals', 'Not specified')}
        - Country: {context.get('country', 'Not specified')}
        """

    def _build_prompt(self, user_input: str, context: Optional[Dict] = None) -> str:
        """Build the complete prompt including system prompt, context, and user input."""
        system_prompt = self._get_system_prompt()
        
        if not context:
            return f"{system_prompt}\n\nQuestion: {user_input}"
        
        monthly_income = float(context.get('income', 0))
        budget = self._calculate_budget_allocation(monthly_income)
        
        return f"""
        {system_prompt}

        {self._format_user_profile(context)}

        Suggested Monthly Budget Breakdown (50/30/20 Rule):
        {self._format_budget_categories(budget)}

        Current Question: {user_input}

        Please provide specific financial advice considering the user's profile and the suggested budget breakdown above. Include:
        1. Specific recommendations for their situation
        2. Dollar amounts and percentages where relevant
        3. Action items they can implement immediately
        4. Long-term financial planning suggestions
        5. Any relevant warnings or areas of concern
        """

    def get_response(self, user_input: str, context: Optional[Dict] = None) -> str:
        """Generate a response using the Gemini model."""
        try:
            prompt = self._build_prompt(user_input, context)

            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"

# Initialize the financial advisor
financial_advisor = FinancialAdvisor()

def call_gemini_api(user_input: str, context: Optional[Dict] = None) -> str:
    """Main function to call the Gemini API with financial context."""
    return financial_advisor.get_response(user_input, context)


