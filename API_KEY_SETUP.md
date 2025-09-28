# 🔑 API Key Setup Guide

## The Error Explained
```
ValueError: GEMINI_API_KEY environment variable is required
```

This error occurs because the application needs a Google Gemini API key to function.

## How to Fix This

### **Step 1: Get Your Gemini API Key**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

### **Step 2: Set Up Environment Variable**

#### **Option A: Using the Setup Script (Recommended)**
```bash
# Create .env file
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env

# Run the setup script
python setup_api_key.py
```

#### **Option B: Manual Setup**
1. Create a `.env` file in your project root:
```bash
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
```

2. Replace `your_actual_api_key_here` with your real API key

#### **Option C: Set Environment Variable Directly (Windows)**
```cmd
set GEMINI_API_KEY=your_actual_api_key_here
python main.py
```

#### **Option D: Set Environment Variable Directly (PowerShell)**
```powershell
$env:GEMINI_API_KEY="your_actual_api_key_here"
python main.py
```

### **Step 3: For Railway Deployment**
1. Go to your Railway project dashboard
2. Click on "Variables" tab
3. Add a new environment variable:
   - **Name**: `GEMINI_API_KEY`
   - **Value**: Your actual API key
4. Redeploy your application

### **Step 4: Test the Setup**
```bash
python main.py
```

You should see:
```
[OK] Using model: gemini-2.0-flash
INFO: Uvicorn running on http://0.0.0.0:8000
```

## Security Notes
- Never commit your `.env` file to git
- Keep your API key secure
- The `.env` file is already in `.gitignore`

## Troubleshooting
- Make sure there are no spaces around the `=` sign
- Make sure the API key is valid and active
- Check that the `.env` file is in the project root directory
