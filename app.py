import streamlit as st
from core import call_gemini_api
from typing import Dict
import base64
import datetime
from pdf_utils import generate_pdf



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

    # State for managing the dynamic download button
    if "pdf_data_to_download" not in st.session_state:
        st.session_state.pdf_data_to_download = None
    if "pdf_ready_for_download" not in st.session_state:
        st.session_state.pdf_ready_for_download = False
    # Store the content of the message the PDF was generated for
    if "pdf_generated_for_message_content" not in st.session_state:
        st.session_state.pdf_generated_for_message_content = None

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

def render_initial_insights():
    """Generate and display initial insights based on the user's financial profile."""
    initial_insights = call_gemini_api(
        "Provide initial financial insights based on the user's profile.",
        st.session_state.user_context
    )
    st.session_state.messages.append({"role": "assistant", "content": initial_insights})
    st.markdown("### Initial Financial Insights")
    st.markdown(initial_insights)
    return initial_insights

def download_pdf_link(pdf_data: bytes, filename: str) -> str:
    """Generate a download link for the PDF file."""
    b64 = base64.b64encode(pdf_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download PDF Report</a>'
    return href

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

    # PDF Download Logic
    if st.session_state.form_submitted:
        st.sidebar.markdown("---")
        st.sidebar.markdown("**PDF Report**")

        latest_message_content = None
        try:
            latest_message_content = st.session_state.messages[-1]["content"]
            # Extract and display the first sentence from the latest content
            # first_sentence = latest_message_content.split('.')[0] + '.' if '.' in latest_message_content else latest_message_content
            # st.sidebar.markdown(f"*Latest insight:* {first_sentence[:100]}...") # Limit length
        except IndexError:
            st.sidebar.warning("No messages yet.")

        # Determine if the current ready PDF matches the latest message
        pdf_matches_latest = (
            st.session_state.pdf_ready_for_download and 
            st.session_state.pdf_generated_for_message_content == latest_message_content
        )

        # --- Conditional Button Rendering ---
        if pdf_matches_latest and st.session_state.pdf_data_to_download:
            # State: PDF is ready and matches the latest message -> Show Download Button
            st.sidebar.download_button(
                label="📥 Download Report",
                data=st.session_state.pdf_data_to_download,
                file_name="Financial_Advisor_Report.pdf",
                mime="application/pdf",
                key="pdf_download_active",
                # When download button is clicked, reset the state so it becomes "Prepare" again
                on_click=lambda: setattr(st.session_state, 'pdf_ready_for_download', False) 
            )
        elif latest_message_content: 
            # State: PDF not ready, or doesn't match latest -> Show Prepare Button
            if st.sidebar.button("⚙️ Prepare Report", key="pdf_prepare"):
                try:
                    # Generate PDF and update state
                    st.session_state.pdf_data_to_download = generate_pdf(
                        st.session_state.user_context,
                        latest_message_content
                    )
                    st.session_state.pdf_generated_for_message_content = latest_message_content
                    st.session_state.pdf_ready_for_download = True
                    # Use st.rerun() to immediately re-render the sidebar with the download button
                    st.rerun() 
                except Exception as e:
                    st.sidebar.error(f"Error generating PDF: {e}")
                    st.session_state.pdf_ready_for_download = False
                    st.session_state.pdf_data_to_download = None
                    st.session_state.pdf_generated_for_message_content = None
        # else: # Case where there are no messages yet - do nothing for buttons

    # New chat button
    if st.sidebar.button("➕ New Chat"):
        new_name = f"Chat {len(st.session_state.chat_sessions) + 1}"
        st.session_state.chat_sessions[new_name] = [
            {"role": "assistant", "content": "New chat started 👇"}
        ]
        st.session_state.current_session = new_name
        # Reset PDF state
        st.session_state.pdf_ready_for_download = False
        st.session_state.pdf_data_to_download = None
        st.session_state.pdf_generated_for_message_content = None

    # Session selector
    session_names = list(st.session_state.chat_sessions.keys())
    selected_session = st.sidebar.selectbox("Select a session", session_names)
    
    if selected_session != st.session_state.current_session:
        st.session_state.current_session = selected_session
         # Reset PDF state
        st.session_state.pdf_ready_for_download = False
        st.session_state.pdf_data_to_download = None
        st.session_state.pdf_generated_for_message_content = None
    
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
            insights = render_initial_insights()
            st.rerun()
    else:
        render_chat_interface()

if __name__ == "__main__":
    main()