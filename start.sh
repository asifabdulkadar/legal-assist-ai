#!/bin/bash
# Startup script for Railway deployment
# Sets Streamlit port from Railway's PORT environment variable

set -e  # Exit on error

# Get port from Railway's PORT env var or default to 8501
PORT=${PORT:-8501}

# Export Streamlit configuration via environment variables
export STREAMLIT_SERVER_PORT=$PORT
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true

# Print configuration for debugging
echo "Starting Streamlit on port: $PORT"
echo "Server address: $STREAMLIT_SERVER_ADDRESS"
echo "Headless mode: $STREAMLIT_SERVER_HEADLESS"

# Run Streamlit
exec streamlit run app.py

