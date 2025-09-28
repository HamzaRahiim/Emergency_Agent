#!/usr/bin/env python3
"""
Railway deployment startup script for Emergency Agent System
"""

import os
import uvicorn
from main import app

if __name__ == "__main__":
    # Get port from Railway environment variable
    port = int(os.environ.get("PORT", 8000))
    
    # Run the application
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        workers=1,  # Railway handles scaling
        log_level="info"
    )

