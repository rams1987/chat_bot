import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Financial Advisor Debug", layout="wide")

st.title("🔧 Financial Advisor Debug Mode")

# Check environment variables
st.header("Environment Check")
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    st.success(f"✅ API Key found: {api_key[:10]}...")
else:
    st.error("❌ No API Key found! Please set GEMINI_API_KEY in Streamlit secrets.")

# Test imports
st.header("Import Check")
try:
    import google.generativeai as genai
    st.success("✅ google.generativeai imported successfully")
except ImportError as e:
    st.error(f"❌ Import error: {e}")

# Test API connection
st.header("API Connection Test")
if api_key:
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content("Say 'Hello World'")
        st.success(f"✅ API working! Response: {response.text}")
    except Exception as e:
        st.error(f"❌ API error: {e}")
else:
    st.warning("⚠️ Cannot test API without API key")

# Simple chat interface for testing
st.header("Simple Chat Test")
if api_key:
    user_input = st.text_input("Enter a message:")
    if st.button("Send") and user_input:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(user_input)
            st.write("**Response:**")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.warning("Please set GEMINI_API_KEY to test chat functionality")

# Show all environment variables (for debugging)
st.header("Environment Variables")
env_vars = {k: v for k, v in os.environ.items() if 'GEMINI' in k or 'STREAMLIT' in k}
if env_vars:
    for key, value in env_vars.items():
        st.text(f"{key}: {value[:20]}..." if len(value) > 20 else f"{key}: {value}")
else:
    st.text("No relevant environment variables found") 