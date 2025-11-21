# Backend-only Dockerfile for Math-Focused Assistant
# Build with:
#   docker build -f backend/Dockerfile -t math-backend .
# Run with:
#   docker run -p 8080:8080 -e PERPLEXITY_API_KEY=your_key math-backend

FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# System dependencies (add more if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for better caching
COPY backend/requirements.txt ./backend/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt \
    && pip install --no-cache-dir gunicorn

# Copy backend source code
COPY backend/app ./backend/app
COPY backend/kb ./backend/kb
COPY backend/data ./backend/data

# (Optional) Pre-download models to reduce cold start
# RUN python - <<'EOF'
# from sentence_transformers import SentenceTransformer
# SentenceTransformer('all-MiniLM-L6-v2')
# print('Model pre-downloaded')
# EOF

# Create non-root user for security
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Environment variables
ENV PYTHONPATH=/app \
    PORT=8080 \
    PYTHONUNBUFFERED=1 \
    WORKERS=1 \
    THREADS=4

# Expose service port
EXPOSE 8080

# Healthcheck (expects /health endpoint; add one to FastAPI if not present)
# To add a health endpoint, you can put this in backend/app/main.py:
#   @app.get('/health')
#   def health():
#       return {'status': 'ok'}
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD curl -fs http://localhost:$PORT/health || exit 1

# Start the FastAPI app via gunicorn + uvicorn worker
CMD exec gunicorn \
    --bind 0.0.0.0:$PORT \
    --workers $WORKERS \
    --worker-class uvicorn.workers.UvicornWorker \
    --threads $THREADS \
    --timeout 0 \
    backend.app.main:app

