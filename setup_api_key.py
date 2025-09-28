#!/usr/bin/env python3
"""
Simple script to help set up your Gemini API key
"""

import os

def setup_api_key():
    """Interactive setup for API key"""
    print("🔑 Gemini API Key Setup")
    print("=" * 40)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        return False
    
    # Read current .env content
    with open('.env', 'r') as f:
        content = f.read()
    
    if 'your_gemini_api_key_here' in content:
        print("📝 Current .env file contains placeholder API key")
        print("🔗 Get your API key from: https://makersuite.google.com/app/apikey")
        print()
        
        api_key = input("Enter your Gemini API key: ").strip()
        
        if not api_key:
            print("❌ No API key provided!")
            return False
        
        # Update .env file
        new_content = content.replace('your_gemini_api_key_here', api_key)
        
        with open('.env', 'w') as f:
            f.write(new_content)
        
        print("✅ API key updated in .env file!")
        print("🧪 Testing the connection...")
        
        # Test the connection
        try:
            import google.generativeai as genai
            from dotenv import load_dotenv
            
            load_dotenv()
            api_key = os.getenv("GEMINI_API_KEY")
            
            if api_key and api_key != "your_gemini_api_key_here":
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content("Hello! Test message.")
                print("✅ API connection successful!")
                print(f"🤖 Response: {response.text}")
                return True
            else:
                print("❌ API key not loaded properly")
                return False
                
        except Exception as e:
            print(f"❌ API test failed: {e}")
            return False
    else:
        print("✅ .env file already has an API key configured")
        return True

if __name__ == "__main__":
    success = setup_api_key()
    if success:
        print("\n🎉 Setup complete! You can now run your emergency agent system.")
        print("🚀 Run: python main.py")
        print("🌐 Then visit: http://localhost:8000")
    else:
        print("\n⚠️ Setup incomplete. Please try again.")
