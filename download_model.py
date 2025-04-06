import os
from transformers import AutoModelForCausalLM, AutoTokenizer

# Define the model directory
MODEL_DIR = "models/gpt2"

def download_model():
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR, exist_ok=True)
        # Download the model and tokenizer
        model = AutoModelForCausalLM.from_pretrained("gpt2")
        tokenizer = AutoTokenizer.from_pretrained("gpt2")
        model.save_pretrained(MODEL_DIR)
        tokenizer.save_pretrained(MODEL_DIR)
        print(f"Model and tokenizer downloaded and saved to {MODEL_DIR}")
    else:
        print(f"Model already exists in {MODEL_DIR}")

if __name__ == "__main__":
    download_model() 