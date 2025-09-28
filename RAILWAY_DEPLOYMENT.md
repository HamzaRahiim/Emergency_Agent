# 🚀 Railway Deployment Guide for Emergency Agent System

## 📋 Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Environment Variables**: Prepare your API keys

## 🔧 Deployment Steps

### Step 1: Prepare Your Repository

1. **Use the Railway-optimized requirements file**:
   ```bash
   # Rename the minimal requirements file
   mv requirements-railway-minimal.txt requirements.txt
   ```

2. **Ensure all Railway config files are present**:
   - `railway.json` ✅
   - `railway.toml` ✅
   - `Procfile` ✅
   - `start_railway.py` ✅

### Step 2: Deploy to Railway

1. **Connect GitHub to Railway**:
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your Emergency Agent repository

2. **Configure Environment Variables**:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   PORT=8000
   PYTHON_VERSION=3.11
   ```

3. **Deploy**:
   - Railway will automatically detect the Python project
   - It will use the `requirements.txt` file
   - The `Procfile` will be used for startup

### Step 3: Verify Deployment

1. **Check the deployment logs** in Railway dashboard
2. **Test the endpoints**:
   - `https://your-app.railway.app/` - Main interface
   - `https://your-app.railway.app/hub` - Multi-agent hub
   - `https://your-app.railway.app/fire` - Fire emergency
   - `https://your-app.railway.app/police` - Police emergency

## 🛠️ Troubleshooting

### Common Issues and Solutions:

#### 1. **Pydantic Build Error**
```
ERROR: Failed building wheel for pydantic-core
```
**Solution**: Use `requirements-railway-minimal.txt` which avoids problematic dependencies.

#### 2. **Python Version Issues**
```
Python 3.13 compatibility issues
```
**Solution**: Railway will use Python 3.11 as specified in `railway.toml`.

#### 3. **Port Binding Issues**
```
Error: Port already in use
```
**Solution**: Railway automatically sets the `PORT` environment variable.

#### 4. **Health Check Error** ⭐ **FIXED**
```
The health check endpoint didn't respond as expected
```
**Solution**: Added proper health check endpoints:
- `/status` - Simple status check
- `/health` - Detailed health information
- Updated Railway config to use `/status` endpoint

#### 5. **Memory Issues**
```
Out of memory during build
```
**Solution**: Railway provides sufficient memory, but you can optimize by removing unused dependencies.

## 📁 Railway Configuration Files

### `railway.json`
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100
  }
}
```

### `Procfile`
```
web: gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

### `railway.toml`
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT"
healthcheckPath = "/"
healthcheckTimeout = 100

[environments.production]
PYTHON_VERSION = "3.11"
```

## 🔐 Environment Variables

Set these in Railway dashboard:

| Variable | Description | Example |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Your Google Gemini API key | `AIzaSy...` |
| `PORT` | Port number (Railway sets this) | `8000` |
| `PYTHON_VERSION` | Python version | `3.11` |

## 🚀 Post-Deployment

1. **Test all endpoints** to ensure they work
2. **Monitor logs** for any errors
3. **Set up custom domain** (optional)
4. **Configure auto-deploy** from GitHub (optional)

## 📞 Support

If you encounter issues:
1. Check Railway deployment logs
2. Verify environment variables are set
3. Ensure all files are committed to GitHub
4. Try redeploying with the minimal requirements

## ✅ Success Indicators

Your deployment is successful when:
- ✅ Build completes without errors
- ✅ Application starts successfully
- ✅ Health check passes
- ✅ All endpoints respond correctly
- ✅ Multi-agent system works
- ✅ Gemini API integration works

---

**🎉 Your Emergency Agent System is now live on Railway!**

