import streamlit as st
from core import call_gemini_api
from typing import Dict

def initialize_session_state():
    """Initialize session state variables."""
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {
            "Default": [{"role": "assistant", "content": "Let's start chatting! 👇"}]
        }
        st.session_state.current_session = "Default"
    
    if "user_context" not in st.session_state:
        st.session_state.user_context = {}
    
    if "form_submitted" not in st.session_state:
        st.session_state.form_submitted = False

def render_financial_form():
    """Render and handle the financial information form."""
    with st.form("finance_form", clear_on_submit=False):
        age = st.number_input("Age", min_value=1, max_value=120, step=1)
        income = st.number_input("Monthly Income (in USD)", min_value=0.0, step=100.0)
        expenses = st.radio("Monthly Expenses", options=["Low", "Medium", "High"])
        goals = st.text_input("Your Financial Goals")
        country = st.selectbox(
            "Country", 
            options=["United States", "India", "United Kingdom", "Canada", "Australia", "Other"]
        )
        
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            st.session_state.user_context = {
                "age": age,
                "income": income,
                "expenses": expenses,
                "goals": goals,
                "country": country,
            }
            st.session_state.form_submitted = True
            return True
    return False

def render_chat_interface():
    """Render the chat interface."""
    # Display current chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask your financial question"):
        handle_chat_input(prompt)

def handle_chat_input(prompt: str):
    """Handle chat input and generate response."""
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = call_gemini_api(prompt, st.session_state.user_context)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.chat_sessions[st.session_state.current_session] = st.session_state.messages

def main():
    st.set_page_config(page_title="Financial Advisor Chat", layout="wide")
    
    initialize_session_state()
    
    # Sidebar
    st.sidebar.title("🗂️ Chat Sessions")
    
    # New chat button
    if st.sidebar.button("➕ New Chat"):
        new_name = f"Chat {len(st.session_state.chat_sessions) + 1}"
        st.session_state.chat_sessions[new_name] = [
            {"role": "assistant", "content": "New chat started 👇"}
        ]
        st.session_state.current_session = new_name
    
    # Session selector
    session_names = list(st.session_state.chat_sessions.keys())
    selected_session = st.sidebar.selectbox("Select a session", session_names)
    
    if selected_session != st.session_state.current_session:
        st.session_state.current_session = selected_session
    
    # Main content
    st.title("🧠 Financial Advisor Chat")
    st.markdown("---")
    
    # Get current session messages
    st.session_state.messages = st.session_state.chat_sessions[st.session_state.current_session]
    
    # Show financial profile if form has been submitted
    if st.session_state.form_submitted:
        with st.expander("Your Financial Profile", expanded=False):
            st.markdown(f"""
            - **Age:** {st.session_state.user_context['age']}  
            - **Income:** ${st.session_state.user_context['income']:,.2f}  
            - **Expenses:** {st.session_state.user_context['expenses']}  
            - **Goals:** {st.session_state.user_context['goals']}  
            - **Country:** {st.session_state.user_context['country']}
            """)
    
    # Handle form submission and chat interface
    if not st.session_state.form_submitted:
        if render_financial_form():
            st.success("✅ Form Submitted!")
            st.rerun()  # Rerun the app to show the chat interface
    else:
        render_chat_interface()

if __name__ == "__main__":
    main()