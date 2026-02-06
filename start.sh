#!/bin/bash
# Startup script for Railway deployment
# Sets Streamlit port from Railway's PORT environment variable

export STREAMLIT_SERVER_PORT=${PORT:-8501}
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true

streamlit run app.py

