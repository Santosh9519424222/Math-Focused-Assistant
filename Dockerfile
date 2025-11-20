# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (curl needed for healthcheck & debugging)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements first for better layer caching
COPY backend/requirements.txt /app/backend/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/backend/requirements.txt \
    && pip install --no-cache-dir gunicorn

# Pre-download sentence-transformers model to avoid cold start latency
# (Temporarily disabled to speed up container build in constrained environments)
# RUN python - <<'EOF'
# from sentence_transformers import SentenceTransformer
# SentenceTransformer('all-MiniLM-L6-v2')
# print('Model pre-downloaded successfully')
# EOF

# Copy backend code (includes app, guardrails, workflow, feedback system)
COPY backend/ /app/backend/

# Optionally copy frontend build artifacts (if present) for static serving
# This step is disabled to avoid build failures when frontend/build is not present or excluded by .dockerignore.
# To include a pre-built React app, uncomment the next line and ensure frontend/build is in the build context.
# COPY frontend/build /app/frontend/build

# Ensure data & kb directories exist (already copied within backend but explicit for clarity)
COPY backend/kb/ /app/backend/kb/
COPY backend/data/ /app/backend/data/

# Create non-root user for security best practices
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Expose port (FastAPI will be served by gunicorn/uvicorn on $PORT)
EXPOSE 8080

# Environment configuration
ENV PYTHONPATH=/app \
    PORT=8080 \
    PYTHONUNBUFFERED=1 \
    WORKERS=1 \
    THREADS=8

# Healthcheck to ensure container readiness
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD curl -fs http://localhost:$PORT/health || exit 1

# Run the application (single worker; adjust WORKERS env for horizontal concurrency)
# Use exec form so signals are properly forwarded
CMD cd backend && exec gunicorn \
    --bind :$PORT \
    --workers $WORKERS \
    --worker-class uvicorn.workers.UvicornWorker \
    --threads $THREADS \
    --timeout 0 \
    app.main:app
