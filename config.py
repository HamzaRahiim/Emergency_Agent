import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your_gemini_api_key_here")

# Instructions for setting up the API key:
# 1. Get your API key from: https://makersuite.google.com/app/apikey
# 2. Set the environment variable: export GEMINI_API_KEY="your_actual_api_key"
# 3. Or create a .env file with: GEMINI_API_KEY=your_actual_api_key

if GEMINI_API_KEY == "your_gemini_api_key_here":
    print("⚠️  WARNING: Please set your GEMINI_API_KEY environment variable")
    print("📝 Instructions:")
    print("   1. Get API key from: https://makersuite.google.com/app/apikey")
    print("   2. Set environment variable: export GEMINI_API_KEY='your_actual_api_key'")
    print("   3. Or create .env file with: GEMINI_API_KEY=your_actual_api_key")