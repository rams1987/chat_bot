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
    response = call_gemini_api(prompt)

    # Simulate assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown(response)
    #     assistant_response = random.choice([
    #         "Hello there! How can I assist you today?",
    #         "Hi, human! Is there anything I can help you with?",
    #         "Do you need help?",
    #     ])
    #     for word in assistant_response.split():
    #         full_response += word + " "
    #         time.sleep(0.05)
    #         message_placeholder.markdown(full_response + "▌")
         

    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Update chat_sessions with new message
    st.session_state.chat_sessions[current_session] = st.session_state.messages
