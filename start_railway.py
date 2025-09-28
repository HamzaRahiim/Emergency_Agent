#!/usr/bin/env python3
"""
Railway startup script for Emergency Agent System
This script ensures proper initialization and handles startup gracefully
"""

import os
import sys
import time
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ['GEMINI_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {missing_vars}")
        logger.warning("Some features may not work properly")
    else:
        logger.info("All required environment variables are set")

def wait_for_dependencies():
    """Wait for any external dependencies to be ready"""
    logger.info("Checking dependencies...")
    time.sleep(2)  # Give time for any external services
    logger.info("Dependencies check complete")

def main():
    """Main startup function"""
    logger.info("Starting Emergency Agent System...")
    
    # Check environment
    check_environment()
    
    # Wait for dependencies
    wait_for_dependencies()
    
    # Get port from environment
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting server on port {port}")
    
    # Import and run the FastAPI app
    try:
        import uvicorn
        from main import app
        
        logger.info("FastAPI app imported successfully")
        
        # Start the server
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info",
            access_log=True
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()