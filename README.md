# Financial Advisor Chatbot

An AI-powered financial advisor chatbot built with Streamlit and Google's Gemini API that provides personalized financial advice, budget planning, and generates PDF reports.

## Features

- 🤖 AI-powered financial advice using Google Gemini API
- 💰 Personalized budget planning with 50/30/20 rule
- 📊 PDF report generation
- 💬 Interactive chat interface
- 📱 Responsive web interface
- 🗂️ Multiple chat sessions

## Quick Start

### Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

## Streamlit Cloud Deployment

### Step 1: Prepare Your Code

1. **Ensure your code is in a GitHub repository**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Verify your repository structure**
   ```
   chat_bot/
   ├── app.py              # Main Streamlit application
   ├── core.py             # Financial advisor logic
   ├── pdf_utils.py        # PDF generation utilities
   ├── requirements.txt    # Python dependencies
   └── .streamlit/         # Streamlit configuration
   ```

### Step 2: Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Create New App**
   - Click "New app"
   - Select your repository from the dropdown
   - Set the main file path to: `app.py`
   - Choose your branch (usually `main`)

3. **Configure Secrets**
   - In the "Secrets" section, add your Gemini API key:
   ```
   GEMINI_API_KEY = "your_actual_api_key_here"
   ```

4. **Deploy**
   - Click "Deploy!"
   - Wait for the build to complete
   - Your app will be available at a URL like: `https://your-app-name.streamlit.app`

### Step 3: Get Your API Key

1. **Visit Google AI Studio**
   - Go to [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account

2. **Create API Key**
   - Click "Create API Key"
   - Copy the generated key
   - Add it to your Streamlit Cloud secrets

## Troubleshooting

### Common Issues

1. **Build fails due to missing dependencies**
   - Ensure all packages are listed in `requirements.txt`
   - Check that package names are correct

2. **API key not working**
   - Verify the key is correctly added to Streamlit secrets
   - Ensure the key has proper permissions

3. **App loads but doesn't respond**
   - Check the logs in Streamlit Cloud dashboard
   - Verify your API key is valid

### Performance Tips

- Streamlit Cloud has memory limits, so the app is optimized for cloud deployment
- Large model downloads are handled efficiently
- PDF generation is optimized for cloud environment

## Support

If you encounter issues:
1. Check the Streamlit Cloud logs
2. Verify your API key is working
3. Test locally first to isolate issues

## License

MIT License 