#!/usr/bin/env python3
"""
Railway Deployment Helper Script
This script helps prepare your project for Railway deployment
"""

import os
import shutil
import sys

def prepare_railway_deployment():
    """Prepare the project for Railway deployment"""
    print("🚀 Preparing Emergency Agent System for Railway Deployment...")
    
    # Step 1: Backup original requirements
    if os.path.exists("requirements.txt"):
        shutil.copy("requirements.txt", "requirements-original.txt")
        print("✅ Backed up original requirements.txt")
    
    # Step 2: Use Railway-optimized requirements
    if os.path.exists("requirements-railway-minimal.txt"):
        shutil.copy("requirements-railway-minimal.txt", "requirements.txt")
        print("✅ Using Railway-optimized requirements.txt")
    else:
        print("❌ requirements-railway-minimal.txt not found!")
        return False
    
    # Step 3: Check for required Railway files
    required_files = [
        "railway.json",
        "railway.toml", 
        "Procfile",
        "start_railway.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing Railway configuration files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All Railway configuration files present")
    
    # Step 4: Check for environment variables
    print("\n🔐 Environment Variables Check:")
    print("Make sure to set these in Railway dashboard:")
    print("- GEMINI_API_KEY=your_gemini_api_key_here")
    print("- PORT=8000 (Railway sets this automatically)")
    print("- PYTHON_VERSION=3.11")
    
    # Step 5: Display deployment instructions
    print("\n📋 Next Steps:")
    print("1. Commit all changes to GitHub")
    print("2. Go to railway.app and create new project")
    print("3. Connect your GitHub repository")
    print("4. Set environment variables in Railway dashboard")
    print("5. Deploy!")
    
    print("\n✅ Project is ready for Railway deployment!")
    return True

def restore_original_files():
    """Restore original files after deployment"""
    print("🔄 Restoring original files...")
    
    if os.path.exists("requirements-original.txt"):
        shutil.copy("requirements-original.txt", "requirements.txt")
        print("✅ Restored original requirements.txt")
    
    print("✅ Files restored!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "restore":
        restore_original_files()
    else:
        prepare_railway_deployment()
