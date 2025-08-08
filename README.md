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

3. **Test the setup**
   ```bash
   python test_deployment.py
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## Streamlit Cloud Deployment

### Step 1: Prepare Your Code

1. **Ensure your code is in a GitHub repository**
   ```bash
   git add .
   git commit -m "Ready for Streamlit Cloud deployment"
   git push origin main
   ```

2. **Verify your repository structure**
   ```
   chat_bot/
   ├── app.py              # Main Streamlit application
   ├── app_debug.py        # Debug version for troubleshooting
   ├── core.py             # Financial advisor logic
   ├── pdf_utils.py        # PDF generation utilities
   ├── requirements.txt    # Python dependencies
   ├── test_deployment.py  # Deployment test script
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

### Chat Not Responding (API Key Configured)

If you see "✅ API Key Configured" but chat isn't responding:

1. **Deploy Debug App**
   - Create a new Streamlit Cloud app using `app_debug.py` as the main file
   - This will show you exactly what's wrong with the API calls

2. **Check API Key Format**
   - Ensure your API key starts with "AI" (for Google AI Studio keys)
   - Make sure there are no extra spaces or characters

3. **Test API Key Locally**
   ```bash
   # Create a simple test
   python -c "
   import os
   from dotenv import load_dotenv
   import google.generativeai as genai
   
   load_dotenv()
   api_key = os.getenv('GEMINI_API_KEY')
   print(f'API Key found: {api_key[:10]}...' if api_key else 'No API key')
   
   if api_key:
       genai.configure(api_key=api_key)
       model = genai.GenerativeModel('gemini-2.0-flash')
       response = model.generate_content('Hello')
       print(f'Response: {response.text}')
   "
   ```

4. **Common Issues**
   - **API Quota Exceeded**: Check your Google AI Studio usage
   - **Invalid Model**: The app uses 'gemini-2.0-flash', ensure it's available
   - **Network Issues**: Try refreshing the page or waiting a moment

### Common Issues

1. **Import errors during build**
   - Run `python test_deployment.py` locally to verify imports
   - Ensure all packages in `requirements.txt` are correct

2. **API key not working**
   - Verify the key is correctly added to Streamlit secrets
   - Ensure the key has proper permissions
   - Check the format: `GEMINI_API_KEY = "your_key_here"`

3. **App loads but doesn't respond**
   - Check the logs in Streamlit Cloud dashboard
   - Verify your API key is valid
   - Test locally first to isolate issues

### Performance Tips

- The app is optimized for Streamlit Cloud deployment
- No heavy model downloads required (uses Google Gemini API)
- PDF generation is optimized for cloud environment

## Support

If you encounter issues:
1. Run `python test_deployment.py` to check imports
2. Deploy `app_debug.py` to identify API issues
3. Check the Streamlit Cloud logs
4. Verify your API key is working
5. Test locally first to isolate issues

## License

MIT License 