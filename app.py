import streamlit as st
from core import call_gemini_api
from typing import Dict
from fpdf import FPDF
import base64
import unicodedata

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

def sanitize_text(text: str) -> str:
    # Replace special dash-like characters with regular dash
    text = text.replace('\u2013', '-').replace('\u2014', '-')
    # Normalize and strip other special characters
    return unicodedata.normalize("NFKD", text).encode("latin1", "ignore").decode("latin1")

def generate_pdf(user_context, insights):
    """Generate a PDF report with user context and latest insights."""
    from fpdf import FPDF
    
    # Create PDF object
    pdf = FPDF()
    pdf.add_page()
    
    # Set font
    pdf.set_font('Arial', 'B', 16)
    
    # Title
    pdf.cell(190, 10, 'Financial Advisory Report', 0, 1, 'C')
    pdf.ln(10)
    
    # User Context Section
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(190, 10, 'Your Financial Profile', 0, 1, 'L')
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 12)
    context_items = [
        f"Age: {user_context['age']}",
        f"Income: ${user_context['income']:,.2f}",
        f"Expenses: {sanitize_text(user_context['expenses'])}",
        f"Goals: {sanitize_text(user_context['goals'])}",
        f"Country: {sanitize_text(user_context['country'])}"
    ]
    
    for item in context_items:
        pdf.cell(190, 10, sanitize_text(item), 0, 1, 'L')
    pdf.ln(10)
    
    # Latest Insights Section
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(190, 10, 'Latest Financial Insights', 0, 1, 'L')
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 12)
    # Split insights into lines that fit the page width
    sanitized_insights = sanitize_text(insights)
    lines = []
    words = sanitized_insights.split()
    current_line = []
    
    for word in words:
        current_line.append(word)
        if len(' '.join(current_line)) > 80:  # Approximate characters that fit in line
            lines.append(' '.join(current_line[:-1]))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    
    for line in lines:
        pdf.cell(190, 10, line, 0, 1, 'L')
    
    # Return PDF as bytes
    return pdf.output(dest='S').encode('latin-1')

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
    
    # Download PDF Button in sidebar
    if st.session_state.form_submitted:
        if st.sidebar.button("📥 Download PDF Report"):
            pdf_data = generate_pdf(
                st.session_state.user_context, 
                st.session_state.messages[-1]["content"]
            )
            st.sidebar.download_button(
                label="Download PDF",
                data=pdf_data,
                file_name="Financial_Advisor_Report.pdf",
                mime="application/pdf"
            )
    
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
            insights = render_initial_insights()
            st.rerun()
    else:
        render_chat_interface()

if __name__ == "__main__":
    main()