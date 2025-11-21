# Google Cloud Deployment Guide

This guide will help you deploy the Math-Focused Assistant to Google Cloud.

## Prerequisites

1. **Google Cloud Account** with billing enabled
2. **gcloud CLI** installed and authenticated
3. **API Keys**:
   - PERPLEXITY_API_KEY (get from https://www.perplexity.ai/settings/api)
   - GEMINI_API_KEY (optional, get from Google AI Studio)

## Option 1: Deploy to Google Cloud Run (Recommended)

Cloud Run is serverless, cheaper, and scales automatically.

### Step 1: Authenticate and Set Project

```bash
# Login to Google Cloud
gcloud auth login

# Set your project ID
gcloud config set project sacred-evening-477817-c1

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### Step 2: Set Environment Variables

```bash
# Set your API keys
export PERPLEXITY_API_KEY="your_perplexity_api_key_here"
export GEMINI_API_KEY="your_gemini_api_key_here"
```

### Step 3: Build and Deploy

```bash
# Navigate to project root
cd /home/santoshyadav_951942/Math-Focused-Assistant

# Build the Docker image
gcloud builds submit --tag gcr.io/sacred-evening-477817-c1/math-focused-assistant

# Deploy to Cloud Run
gcloud run deploy math-focused-assistant \
  --image gcr.io/sacred-evening-477817-c1/math-focused-assistant \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 2Gi \
  --cpu 2 \
  --max-instances 10 \
  --set-env-vars PERPLEXITY_API_KEY=$PERPLEXITY_API_KEY,GEMINI_API_KEY=$GEMINI_API_KEY
```

### Step 4: Get Your Service URL

After deployment, you'll receive a URL like:
```
https://math-focused-assistant-xxxxx-uc.a.run.app
```

## Option 2: Deploy to Google App Engine

App Engine is a fully managed platform, but less flexible and potentially more expensive.

### Step 1: Update app.yaml

Edit `/home/santoshyadav_951942/Math-Focused-Assistant/app.yaml` and replace:
- `your_perplexity_api_key_here` with your actual API key
- `your_gemini_api_key_here` with your actual API key

### Step 2: Deploy

```bash
# Navigate to project root
cd /home/santoshyadav_951942/Math-Focused-Assistant

# Install gunicorn in your virtual environment
source backend/venv/bin/activate
pip install gunicorn

# Deploy to App Engine
gcloud app deploy app.yaml --project sacred-evening-477817-c1
```

### Step 3: Access Your App

```bash
gcloud app browse
```

## Testing Your Deployment

### Test the API

```bash
# Replace with your actual URL
curl -X POST https://your-service-url/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Solve x² + 5x + 6 = 0",
    "difficulty": "JEE_Main"
  }'
```

### Test Health Endpoint

```bash
curl https://your-service-url/health
```

## Monitoring and Logs

### View Logs (Cloud Run)

```bash
gcloud run services logs read math-focused-assistant --region us-central1
```

### View Logs (App Engine)

```bash
gcloud app logs tail -s default
```

## Cost Optimization

### Cloud Run Pricing (Pay per use)
- **Free Tier**: 2 million requests/month
- **Memory**: ~$0.0000025 per GB-second
- **CPU**: ~$0.00002400 per vCPU-second
- **Estimated**: $5-20/month for moderate use

### App Engine Pricing
- **F2 instance**: ~$0.10/hour when active
- **Estimated**: $30-70/month

## Troubleshooting

### Build Fails
```bash
# Check Docker build locally
docker build -t test-image .
docker run -p 8080:8080 -e PERPLEXITY_API_KEY=$PERPLEXITY_API_KEY test-image
```

### Deployment Fails
```bash
# Check deployment status
gcloud run services describe math-focused-assistant --region us-central1

# Check logs
gcloud run services logs read math-focused-assistant --region us-central1 --limit 50
```

### API Key Issues
Make sure your API keys are properly set as environment variables:
```bash
gcloud run services update math-focused-assistant \
  --region us-central1 \
  --set-env-vars PERPLEXITY_API_KEY=$PERPLEXITY_API_KEY
```

## Frontend Deployment (Optional)

To deploy the React frontend separately:

### Build Frontend
```bash
cd frontend
npm install
npm run build
```

### Deploy to Firebase Hosting or Cloud Storage
```bash
# Firebase (recommended for React apps)
npm install -g firebase-tools
firebase login
firebase init hosting
firebase deploy

# Or Cloud Storage (static hosting)
gsutil mb gs://your-bucket-name
gsutil -m cp -r build/* gs://your-bucket-name
gsutil iam ch allUsers:objectViewer gs://your-bucket-name
```

## Update Backend URL in Frontend

Edit `frontend/src/App.js` and update the API endpoint:
```javascript
const API_URL = 'https://your-cloud-run-url';
```

## Security Best Practices

1. **Use Secret Manager** for API keys:
```bash
# Store secrets
echo -n "your_api_key" | gcloud secrets create perplexity-api-key --data-file=-

# Grant access to Cloud Run
gcloud secrets add-iam-policy-binding perplexity-api-key \
  --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Update Cloud Run to use secrets
gcloud run services update math-focused-assistant \
  --region us-central1 \
  --set-secrets PERPLEXITY_API_KEY=perplexity-api-key:latest
```

2. **Enable Authentication** (if needed):
```bash
gcloud run services update math-focused-assistant \
  --region us-central1 \
  --no-allow-unauthenticated
```

## Continuous Deployment

Use Cloud Build for automatic deployments:

```bash
# Connect your GitHub repository
gcloud builds triggers create github \
  --repo-name=Math-Focused-Assistant \
  --repo-owner=your-github-username \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml
```

## Next Steps

1. ✅ Test all API endpoints
2. ✅ Monitor logs and performance
3. ✅ Set up alerts and monitoring
4. ✅ Configure custom domain (optional)
5. ✅ Enable HTTPS (automatic with Cloud Run)
6. ✅ Set up CI/CD pipeline

## Support

For issues, check:
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- Project README.md

