# Emergency Agent System - Deployment Guide

## Based on Working Todo Project Structure

Your working `todo/` project uses a simple, reliable approach. Here's what we've applied to your Emergency Agent System:

### Key Changes Made:

1. **Dockerfile Approach** (like your working project)
   - Uses `python:3.11-slim` base image
   - Simple, clean Dockerfile
   - Proper health checks
   - Non-root user for security

2. **Simplified Requirements** (like your working project)
   - Minimal dependencies
   - No complex build requirements
   - Based on your working `requirements.txt`

3. **Railway Configuration** (like your working project)
   - Uses `dockerfile` builder instead of `nixpacks`
   - Simple start command: `python main.py`
   - Proper health check configuration

### Files Created/Updated:

- ✅ `Dockerfile` - Clean, simple Docker configuration
- ✅ `requirements-simple.txt` - Minimal dependencies
- ✅ `.dockerignore` - Optimized build context
- ✅ `railway.json` - Updated to use dockerfile builder
- ✅ `railway.toml` - Updated configuration
- ✅ `main.py` - Updated port default to 8000

### Deployment Steps:

1. **Use the simplified requirements:**
   ```bash
   cp requirements-simple.txt requirements.txt
   ```

2. **Commit and push to your repository**

3. **Deploy on Railway:**
   - Railway will automatically detect the Dockerfile
   - Use the dockerfile builder (already configured)
   - Health check will use `/status` endpoint

### Environment Variables Required:
- `GEMINI_API_KEY` - Your Google Gemini API key
- `PORT` - Railway sets this automatically

### Why This Should Work:

Your `todo/` project works because it:
- Uses simple dependencies
- Has a clean Dockerfile
- Uses dockerfile builder on Railway
- Has minimal complexity

We've applied the same approach to your Emergency Agent System.

### Testing Locally:

```bash
# Build and run with Docker
docker build -t emergency-agent .
docker run -p 8000:8000 -e GEMINI_API_KEY=your_key emergency-agent

# Or run directly
python main.py
```

The deployment should now work reliably like your todo project! 🚀
