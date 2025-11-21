#!/bin/bash
set -e
SERVICE_NAME="math-focused-backend"
REGION="us-central1"
PROJECT_ID="sacred-evening-477817-c1"

if ! command -v gcloud &>/dev/null; then
  echo "gcloud CLI not installed"; exit 1;
fi

echo "Building and deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --source . \
  --region $REGION \
  --project $PROJECT_ID \
  --allow-unauthenticated \
  --memory 1Gi \
  --timeout 300 \
  --set-env-vars PERPLEXITY_API_KEY=${PERPLEXITY_API_KEY:-PLACEHOLDER}

