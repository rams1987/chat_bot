import streamlit as st
import random
import time

from core import load_local_model, call_gemini_api


st.set_page_config(page_title="Chat App with History", layout="wide")

# --- Sidebar ---
st.sidebar.title("🗂️ Chat Sessions")

# Initialize chat_sessions dictionary
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {"Default": [{"role": "assistant", "content": "Let's start chatting! 👇"}]}
    st.session_state.current_session = "Default"

# Select chat session
session_names = list(st.session_state.chat_sessions.keys())
selected_session = st.sidebar.selectbox("Select a session", session_names)

# Switch session if selected
if selected_session != st.session_state.get("current_session"):
    st.session_state.current_session = selected_session

# Button to start a new chat session
if st.sidebar.button("➕ New Chat"):
    new_name = f"Chat {len(session_names) + 1}"
    st.session_state.chat_sessions[new_name] = [{"role": "assistant", "content": "New chat started 👇"}]
    st.session_state.current_session = new_name

# Get current session messages
current_session = st.session_state.current_session
st.session_state.messages = st.session_state.chat_sessions[current_session]



# --- Main Chat Interface ---
st.title("🧠 Streamlit loves LLMs!")

st.caption("Note that this demo app isn't actually connected to any LLMs. Those are expensive ;)")


st.markdown("---")

# Default context and form submission flag
if "user_context" not in st.session_state:
    st.session_state.user_context = {}

if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

with st.form("finance_form", clear_on_submit=False):
    age = st.number_input("Age", min_value=1, max_value=120, step=1)
    income = st.number_input("Monthly Income (in USD)", min_value=0.0, step=100.0)
    expenses = st.radio("Monthly Expenses", options=["Low", "Medium", "High"])
    goals = st.text_input("Your Financial Goals")
    country = st.selectbox("Country", options=["United States", "India", "United Kingdom", "Canada", "Australia", "Other"])
    
    submitted = st.form_submit_button("Submit")

if submitted:

    st.session_state.user_context = {
        "age": age,
        "income": income,
        "expenses": expenses,
        "goals": goals,
        "country": country,
    }

    st.session_state.form_submitted = True  # <-- Important line to enable chat


    st.success("✅ Form Submitted!")
    st.write("**Here’s what you submitted:**")
    st.markdown(f"""
    - **Age:** {age}  
    - **Income:** ${income:,.2f}  
    - **Expenses:** {expenses}  
    - **Goals:** {goals}  
    - **Country:** {country}
    """)

# Default empty context if not submitted
if "user_context" not in st.session_state:
    st.session_state.user_context = {}

# Only show chat if the form is submitted
if st.session_state.form_submitted:

    # Display messages from current session
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Say something"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # call the gemini api
        response = call_gemini_api(prompt, st.session_state.user_context)

        # Simulate assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown(response)

        # Add assistant message
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Update chat_sessions with new message
        st.session_state.chat_sessions[current_session] = st.session_state.messages

else:
    st.write("Please fill out the form to start chatting.")