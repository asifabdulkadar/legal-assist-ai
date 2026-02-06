# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_lg

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"

# Copy application code
COPY . .

# Make startup script executable
RUN chmod +x start.sh

# Create necessary directories
RUN mkdir -p data/storage data/templates logs

# Expose Streamlit port (Railway will set PORT env var)
EXPOSE 8501

# Health check (uses PORT env var or defaults to 8501)
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD sh -c 'curl --fail http://localhost:${PORT:-8501}/_stcore/health || exit 1'

# Run Streamlit using startup script (handles PORT env var)
CMD ["./start.sh"]

