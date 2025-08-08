import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai
from typing import Dict, Optional
from pdf_utils import generate_pdf

# Load environment variables from .env file
load_dotenv()

class FinancialAdvisor:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
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

    def _build_prompt(self, user_input: str, context: Optional[Dict] = None, chat_history=None) -> str:
        """Build the complete prompt including system prompt, context, chat history, and user input."""
        system_prompt = self._get_system_prompt()
        
        if not context:
            return f"{system_prompt}\n\nQuestion: {user_input}"
        
        monthly_income = float(context.get('income', 0))
        budget = self._calculate_budget_allocation(monthly_income)
        
        prompt = f"""
        {system_prompt}

        {self._format_user_profile(context)}

        Suggested Monthly Budget Breakdown (50/30/20 Rule):
        {self._format_budget_categories(budget)}
        """

        # Add chat history if available
        if chat_history and len(chat_history) > 1:
            prompt += "\nPrevious Conversation:\n"
            for message in chat_history[:-1]:  # Exclude the current message
                role = "User" if message["role"] == "user" else "Assistant"
                prompt += f"{role}: {message['content']}\n"

        prompt += f"\nCurrent Question: {user_input}\n"
        prompt += """
        Please provide specific financial advice considering the user's profile, budget breakdown, and previous conversation context. Include:
        1. Specific recommendations for their situation
        2. Dollar amounts and percentages where relevant
        3. Action items they can implement immediately
        4. Long-term financial planning suggestions
        5. Any relevant warnings or areas of concern
        """
        
        return prompt

    def get_response(self, user_input: str, context: Optional[Dict] = None, chat_history=None) -> str:
        """Generate a response using the Gemini model."""
        try:
            prompt = self._build_prompt(user_input, context, chat_history)

            response = self.model.generate_content(prompt)
            
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"

# Initialize the financial advisor
financial_advisor = FinancialAdvisor()

def call_gemini_api(user_input: str, context: Optional[Dict] = None, chat_history=None) -> str:
    """Main function to call the Gemini API with financial context and chat history."""
    return financial_advisor.get_response(user_input, context, chat_history)

def prepare_report(user_context, latest_message_content):
    """
    Prepare a financial report by calling the Gemini API and generating a PDF.
    """
    # Define the prompt for the Gemini API
    prompt = """
    Generate a financial report with the following structure:
    1. **Initial Financial Insights and Recommendations**
       - Provide a brief overview of the client's financial situation.
    2. **Evaluating Your Current Situation**
       - Discuss income, expenses, and financial goals.
    3. **Detailed Budget Analysis & Recommendations**
       - Break down the budget using the 50/30/20 rule.
    4. **Actionable Steps & Long-Term Planning**
       - List immediate actions and long-term strategies.
    5. **Warnings and Areas of Concern**
       - Highlight potential risks and areas for improvement.
    6. **Next Steps**
       - Summarize the key actions the client should take next.
    """

    # Call the Gemini API
    #insights = call_gemini_api(prompt, user_context)

    # Generate the PDF using the structured insights
    pdf_bytes = generate_pdf(user_context, latest_message_content)

    return pdf_bytes


