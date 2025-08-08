#!/usr/bin/env python3
"""
Simple test script to verify deployment setup
"""

def test_imports():
    """Test that all required imports work correctly."""
    try:
        import streamlit as st
        print("✅ streamlit imported successfully")
        
        import google.generativeai as genai
        print("✅ google.generativeai imported successfully")
        
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
        
        import fpdf
        print("✅ fpdf imported successfully")
        
        import requests
        print("✅ requests imported successfully")
        
        # Test core module imports
        from core import call_gemini_api, prepare_report
        print("✅ core module imported successfully")
        
        from pdf_utils import generate_pdf
        print("✅ pdf_utils imported successfully")
        
        print("\n🎉 All imports successful! Ready for deployment.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_imports() 