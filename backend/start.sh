#!/bin/bash
# Render start script
PORT=${PORT:-8000}
echo "Starting application on port $PORT"
uvicorn app.main:app --host 0.0.0.0 --port $PORT
