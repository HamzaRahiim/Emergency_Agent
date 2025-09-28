#!/usr/bin/env python3
"""
Test script to check Gemini API key status
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

def test_api_key():
    """Test the Gemini API key"""
    print("Testing Gemini API Key...")
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key or api_key == "your_gemini_api_key_here":
        print("[ERROR] API key not set or still using placeholder")
        print("Please set your real API key in the .env file")
        return False
    
    print(f"[INFO] API key found: {api_key[:10]}...")
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # List available models first
        print("[INFO] Checking available models...")
        models = genai.list_models()
        available_models = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                available_models.append(model.name)
        
        print(f"[INFO] Available models: {available_models}")
        
        # Try the first available model
        if available_models:
            model_name = available_models[0]
            print(f"[INFO] Testing with model: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Hello, this is a test message.")
            
            print("[SUCCESS] API key is working!")
            print(f"[RESPONSE] {response.text}")
            return True
        else:
            print("[ERROR] No models available for content generation")
            return False
        
    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR] API test failed: {error_msg}")
        
        if "quota" in error_msg.lower():
            print("\n[QUOTA ISSUE] Your API key has exceeded its quota")
            print("Solutions:")
            print("1. Wait for quota to reset (usually 24 hours)")
            print("2. Upgrade your Google AI Studio plan")
            print("3. Create a new API key")
            print("4. Check your billing settings")
        elif "permission" in error_msg.lower():
            print("\n[PERMISSION ISSUE] API key doesn't have proper permissions")
            print("Solutions:")
            print("1. Check API key permissions in Google AI Studio")
            print("2. Enable the Generative AI API")
        elif "invalid" in error_msg.lower():
            print("\n[INVALID KEY] API key is invalid")
            print("Solutions:")
            print("1. Generate a new API key")
            print("2. Check if the key was copied correctly")
        
        return False

if __name__ == "__main__":
    success = test_api_key()
    if success:
        print("\n[SUCCESS] Your API key is working! You can now run the main application.")
    else:
        print("\n[FAILED] Please fix the API key issue before running the main application.")
