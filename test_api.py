#!/usr/bin/env python3
"""
Simple API test script to debug Gemini API issues
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

def test_api():
    """Test the Gemini API connection."""
    print("🔍 Testing Gemini API Connection...")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ No API key found!")
        print("Please set GEMINI_API_KEY in your environment or .env file")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    # Test API configuration
    try:
        genai.configure(api_key=api_key)
        print("✅ API configured successfully")
    except Exception as e:
        print(f"❌ API configuration failed: {e}")
        return False
    
    # Test model creation
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        print("✅ Model created successfully")
    except Exception as e:
        print(f"❌ Model creation failed: {e}")
        return False
    
    # Test simple generation
    try:
        print("🔄 Testing simple generation...")
        response = model.generate_content("Say 'Hello World'")
        print(f"✅ Generation successful!")
        print(f"Response: {response.text}")
        return True
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        return False

def test_financial_advisor():
    """Test the financial advisor functionality."""
    print("\n🧠 Testing Financial Advisor...")
    print("=" * 50)
    
    try:
        from core import call_gemini_api
        
        # Test with simple context
        context = {
            "age": 30,
            "income": 5000,
            "expenses": "Medium",
            "goals": "Save for retirement",
            "country": "United States"
        }
        
        response = call_gemini_api("Give me budgeting advice", context)
        print("✅ Financial advisor test successful!")
        print(f"Response length: {len(response)} characters")
        print(f"First 100 chars: {response[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Financial advisor test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Financial Advisor API Test")
    print("=" * 50)
    
    # Test basic API
    api_works = test_api()
    
    if api_works:
        # Test financial advisor
        advisor_works = test_financial_advisor()
        
        if advisor_works:
            print("\n🎉 All tests passed! Your setup is working correctly.")
        else:
            print("\n⚠️ API works but financial advisor has issues.")
    else:
        print("\n❌ API test failed. Please check your API key and configuration.") 