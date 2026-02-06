# LegalAssist AI: GenAI Powered Legal Assistant for Indian SMEs

**LegalAssist AI** is a sophisticated generative AI platform designed specifically to empower Indian Small and Medium Enterprise (SME) owners. It bridges the gap between complex legal jargon and actionable business intelligence, allowing owners to understand contracts, identify risks, and negotiate better terms without immediate legal overhead.

## 🚀 The Problem
Indian SMEs often operate with limited legal resources. Managing diverse contracts—from employment to vendor agreements—poses significant risks. Complex legal language, hidden "penalty" clauses, and unfavorable termination terms can lead to severe business disruptions and financial loss.

## ✨ The Solution
LegalAssist AI provides an end-to-end contract intelligence layer:
- **Simplified Explanations**: Uses LLMs (GPT-4) to break down complex clauses into plain business language.
- **Multilingual Analysis**: Supports both English and Hindi contracts, ensuring inclusivity for regional business owners.
- **Deep Risk Scoring**: Calculates risk at both the clause and document level (Low/Medium/High).
- **Compliance Guardrails**: Identify issues with Indian laws such as the Indian Contract Act, Stamp Act, and Labour Laws.
- **Actionable Alternatives**: Suggests SME-friendly clause wordings to facilitate renegotiation.

## 🛠️ Technical Architecture & Stack
- **Web UI**: Streamlit (Responsive and interactive dashboard)
- **Language Models**: OpenAI GPT-4 (Legal reasoning, simplification, and entity extraction)
- **NLP Pipeline**: spaCy (`en_core_web_lg`) & NLTK (Preprocessing, NER, and text segmentation)
- **Multilingual Support**: Google Translate API (`googletrans`) for Hindi-to-English normalization.
- **Document Processing**: `pdfplumber` (High-fidelity PDF parsing) and `python-docx`.
- **Data Management**: JSON-based audit logging and local storage for historical analysis.

## 🌟 Key Features
1. **Contract Classifier**: Automatically identifies agreement types (Employment, Vendor, Lease, etc.).
2. **Entity Extractor**: Automatically pulls Parties, Dates, Jurisdictions, and Financial Obligations.
3. **Risk Dashboard**: Visualizes risk via interactive gauges and metrics.
4. **Clause-by-Clause Analysis**: Categorizes sections as Rights, Obligations, or Prohibitions.
5. **SME Template Library**: Provides standardized, SME-friendly templates for immediate use.
6. **Audit Trail**: Maintains a complete history of all contract analyses for legal transparency.

## 📦 Installation & Setup

1. **Navigate to project directory**:
   ```bash
   cd d:/guvi/legal-assistant
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Download spaCy models**:
   ```bash
   python -m spacy download en_core_web_lg
   ```
4. **Environment Variables**:
   Create a `.env` file and add:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

## 🖥️ Running Locally
```bash
streamlit run app.py
```

## ☁️ Deployment Guide

This application is deployment-ready and can be deployed to various platforms. The application uses Streamlit which serves both frontend (UI) and backend (Python processing) in a single service.

### Prerequisites
- GitHub repository (for cloud deployments)
- OpenAI API key
- Python 3.11+ (for local deployments)

### Environment Variables
Create a `.env` file or set these environment variables in your deployment platform:
```env
OPENAI_API_KEY=your_openai_api_key_here
LLM_MODEL=gpt-4  # Optional, defaults to gpt-4
```

### Option 1: Railway.app (Recommended)

Railway automatically detects the Dockerfile and deploys your application.

**Steps:**
1. Push your code to a GitHub repository
2. Sign up at [Railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will automatically detect the Dockerfile and start building
6. Go to "Variables" tab and add:
   - `OPENAI_API_KEY` = your OpenAI API key
   - `LLM_MODEL` = gpt-4 (optional)
7. Your app will be live at `https://your-app-name.up.railway.app`

**Note:** Railway will automatically use the `Dockerfile` for deployment. If you prefer non-Docker deployment, Railway can use the `Procfile` which uses a startup script to handle the PORT environment variable correctly.

### Option 2: Render.com

**Steps:**
1. Push your code to a GitHub repository
2. Sign up at [Render.com](https://render.com)
3. Click "New" → "Web Service"
4. Connect your GitHub repository
5. Render will automatically detect `render.yaml` configuration
6. Add environment variables:
   - `OPENAI_API_KEY` = your OpenAI API key
   - `LLM_MODEL` = gpt-4 (optional)
7. Click "Create Web Service"
8. Your app will be live at `https://your-app-name.onrender.com`

**Note:** Free tier has cold starts. Consider upgrading for production use.

### Option 3: Streamlit Cloud (Simplest)

**Steps:**
1. Push your code to a public GitHub repository (or private with Streamlit Cloud access)
2. Go to [Share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository and branch
6. Set Main file path to: `app.py`
7. Click "Advanced settings" and add secrets:
   ```
   OPENAI_API_KEY=your_openai_api_key
   LLM_MODEL=gpt-4
   ```
8. Click "Deploy"
9. Your app will be live at `https://your-app-name.streamlit.app`

**Note:** Streamlit Cloud has limitations on file uploads and processing time.

### Option 4: Docker Compose (Local/Cloud VPS)

**Steps:**
1. Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   LLM_MODEL=gpt-4
   ```
2. Run the application:
   ```bash
   docker-compose up -d
   ```
3. Access the application at `http://localhost:8501`

**For production on a VPS:**
- Use a reverse proxy (nginx) with SSL
- Set up proper firewall rules
- Configure automatic restarts
- Set up log rotation

### Option 5: Manual Docker Deployment

**Steps:**
1. Build the Docker image:
   ```bash
   docker build -t legal-assist-ai .
   ```
2. Run the container:
   ```bash
   docker run -d \
     -p 8501:8501 \
     -e OPENAI_API_KEY=your_openai_api_key \
     -e LLM_MODEL=gpt-4 \
     -v $(pwd)/data:/app/data \
     -v $(pwd)/logs:/app/logs \
     --name legal-assist-ai \
     legal-assist-ai
   ```
3. Access at `http://localhost:8501`

### Troubleshooting

**Common Issues:**

1. **spaCy model not found:**
   - The Dockerfile automatically downloads the model
   - For manual deployment, run: `python -m spacy download en_core_web_lg`

2. **NLTK data missing:**
   - The Dockerfile automatically downloads required NLTK data
   - For manual deployment, run the NLTK download commands from the Dockerfile

3. **OpenAI API errors:**
   - Verify your API key is correct
   - Check your OpenAI account has sufficient credits
   - Ensure the API key has proper permissions

4. **Port conflicts:**
   - Change the port in `docker-compose.yml` or use `--server.port` flag
   - Railway and Render use `PORT` environment variable automatically
   - The `start.sh` script handles PORT variable expansion for Railway deployments
   - If you see "$PORT is not a valid integer" error, ensure you're using the startup script

5. **Build timeouts:**
   - spaCy model download can take time
   - Consider using a pre-built image or caching layers

6. **502 Bad Gateway errors:**
   - Check Railway logs for startup errors
   - Ensure `OPENAI_API_KEY` is set in Railway environment variables
   - Verify the application is starting correctly (check logs)
   - The health check may take up to 60 seconds on first start
   - Ensure all dependencies are installed (spaCy model, NLTK data)
   - Check if the port is correctly configured (should use Railway's PORT env var)

**Health Check:**
The application includes a health check endpoint at `/_stcore/health` for monitoring. The health check waits 60 seconds before starting to allow the app to fully initialize.

### Data Persistence

For production deployments:
- **Railway/Render:** Use their volume/storage services for persistent data
- **Docker:** Mount volumes for `data/` and `logs/` directories
- **Streamlit Cloud:** Limited persistence, consider external storage

### Security Notes

- Never commit `.env` files to version control
- Use environment variables for all secrets
- Enable HTTPS in production (most platforms provide this automatically)
- Regularly update dependencies for security patches
#   l e g a l - a s s i s t - a i 
 
 