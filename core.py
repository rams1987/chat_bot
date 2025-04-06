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
def call_gemini_api(user_input):
    api_key = os.getenv("GEMINI_API_KEY")  # Load the API key from the environment

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=user_input
    )

    return response.text


