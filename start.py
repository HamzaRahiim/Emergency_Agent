#!/usr/bin/env python3
"""
Startup script for the Emergency Medical Agent System
"""

import os
import sys
import uvicorn
from pathlib import Path

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking system requirements...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  Warning: .env file not found")
        print("   Please copy env_example.txt to .env and add your GEMINI_API_KEY")
        print("   Get your API key from: https://makersuite.google.com/app/apikey")
    
    # Check if data files exist
    required_files = ['hospiatl_dataset.json', 'hospital data 2.json']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Missing required data files: {', '.join(missing_files)}")
        return False
    
    print("✅ All requirements met")
    return True

def main():
    """Main startup function"""
    print("🚑 Emergency Medical Agent System")
    print("=" * 50)
    
    if not check_requirements():
        print("\n❌ Please fix the issues above before starting the system")
        sys.exit(1)
    
    print("\n🚀 Starting Emergency Medical Agent System...")
    print("📍 Focused on Karachi, Pakistan")
    print("🤖 Powered by Google Gemini AI")
    print("\n🌐 Web Interface: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("\n💡 To test without web interface, run: python test_system.py")
    print("\n" + "=" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Emergency Medical Agent System stopped")
    except Exception as e:
        print(f"\n❌ Error starting system: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

