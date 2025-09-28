# Railway Deployment Fixes

## Common Railway Health Check Issues & Solutions

### 1. **Health Check Timeout (Most Common)**
**Problem**: Health check fails with "service unavailable"
**Solutions**:
- ✅ Reduced health check timeout from 300s to 60s
- ✅ Reduced worker count from 4 to 2 (less memory usage)
- ✅ Added proper startup script with dependency checks
- ✅ Added timeout and keep-alive settings

### 2. **Port Configuration**
**Problem**: App not binding to Railway's PORT
**Solutions**:
- ✅ Using `$PORT` environment variable
- ✅ Default fallback to port 8000
- ✅ Proper host binding to `0.0.0.0`

### 3. **Application Startup Time**
**Problem**: App takes too long to initialize
**Solutions**:
- ✅ Created `start_railway.py` with proper initialization
- ✅ Added dependency checks and logging
- ✅ Reduced worker count for faster startup

### 4. **Memory Issues**
**Problem**: App runs out of memory during startup
**Solutions**:
- ✅ Reduced gunicorn workers from 4 to 2
- ✅ Added memory-efficient settings
- ✅ Optimized startup process

## Updated Configuration Files

### railway.json
```json
{
  "deploy": {
    "startCommand": "python start_railway.py",
    "healthcheckPath": "/status",
    "healthcheckTimeout": 60,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 5
  }
}
```

### railway.toml
```toml
[deploy]
startCommand = "python start_railway.py"
healthcheckPath = "/status"
healthcheckTimeout = 60
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 5

[environments.production]
PYTHON_VERSION = "3.11"
PORT = "8000"
```

## Environment Variables Required
Make sure these are set in Railway:
- `GEMINI_API_KEY` - Your Google Gemini API key
- `PORT` - Railway will set this automatically

## Testing Locally
```bash
# Test the startup script
python start_railway.py

# Test health endpoints
curl http://localhost:8000/status
curl http://localhost:8000/health
```

## If Still Failing
1. Check Railway logs for specific error messages
2. Verify all environment variables are set
3. Test the startup script locally first
4. Consider using Railway's built-in Python runtime instead of custom startup
