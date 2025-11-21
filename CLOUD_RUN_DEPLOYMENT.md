# Cloud Run Deployment Guide

## 🚀 Quick Deploy to Google Cloud Run

This guide covers deploying the Math-Focused Assistant to Google Cloud Run with CI/CD automation.

---

## 📋 Prerequisites

1. **Google Cloud Project**
   - Active GCP project with billing enabled
   - Project ID: `sacred-evening-477817-c1` (or your project)

2. **Required APIs** (Enable these):
   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable secretmanager.googleapis.com
   ```

3. **Service Account** for GitHub Actions:
   ```bash
   # Create service account
   gcloud iam service-accounts create github-actions \
     --display-name="GitHub Actions Deployer"
   
   # Grant necessary roles
   gcloud projects add-iam-policy-binding sacred-evening-477817-c1 \
     --member="serviceAccount:github-actions@sacred-evening-477817-c1.iam.gserviceaccount.com" \
     --role="roles/run.admin"
   
   gcloud projects add-iam-policy-binding sacred-evening-477817-c1 \
     --member="serviceAccount:github-actions@sacred-evening-477817-c1.iam.gserviceaccount.com" \
     --role="roles/storage.admin"
   
   gcloud projects add-iam-policy-binding sacred-evening-477817-c1 \
     --member="serviceAccount:github-actions@sacred-evening-477817-c1.iam.gserviceaccount.com" \
     --role="roles/iam.serviceAccountUser"
   
   # Create key
   gcloud iam service-accounts keys create key.json \
     --iam-account=github-actions@sacred-evening-477817-c1.iam.gserviceaccount.com
   ```

4. **Store Perplexity API Key** in Secret Manager:
   ```bash
   echo -n "YOUR_PERPLEXITY_API_KEY" | gcloud secrets create perplexity-api-key \
     --data-file=- \
     --replication-policy="automatic"
   
   # Grant access to Cloud Run service account
   gcloud secrets add-iam-policy-binding perplexity-api-key \
     --member="serviceAccount:sacred-evening-477817-c1@appspot.gserviceaccount.com" \
     --role="roles/secretmanager.secretAccessor"
   ```

---

## 🔧 GitHub Repository Setup

### 1. Add Repository Secrets

Go to **GitHub repo → Settings → Secrets and variables → Actions** and add:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `GCP_PROJECT_ID` | `sacred-evening-477817-c1` | Your GCP project ID |
| `GCP_SA_KEY` | Contents of `key.json` | Service account JSON key |

### 2. Push Code to GitHub

```bash
git add .
git commit -m "Add Cloud Run deployment with CI/CD"
git push origin main
```

The GitHub Actions workflow will automatically:
1. Run tests
2. Build Docker image (multi-stage)
3. Push to Google Container Registry
4. Deploy to Cloud Run
5. Run health checks

---

## 🐳 Manual Deployment (Without CI/CD)

### Option 1: Deploy from Local Machine

```bash
# Authenticate
gcloud auth login
gcloud config set project sacred-evening-477817-c1

# Build and submit to Cloud Build
gcloud builds submit --tag gcr.io/sacred-evening-477817-c1/math-agent

# Deploy to Cloud Run
gcloud run deploy math-agent \
  --image gcr.io/sacred-evening-477817-c1/math-agent \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-secrets="PERPLEXITY_API_KEY=perplexity-api-key:latest" \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --min-instances 0 \
  --max-instances 10
```

### Option 2: Deploy with Docker + GCR

```bash
# Build multi-stage image
docker build -f Dockerfile.multistage -t gcr.io/sacred-evening-477817-c1/math-agent:latest .

# Authenticate Docker to GCR
gcloud auth configure-docker

# Push image
docker push gcr.io/sacred-evening-477817-c1/math-agent:latest

# Deploy
gcloud run deploy math-agent \
  --image gcr.io/sacred-evening-477817-c1/math-agent:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-secrets="PERPLEXITY_API_KEY=perplexity-api-key:latest"
```

---

## 🧪 Testing the Deployment

### 1. Get Service URL
```bash
gcloud run services describe math-agent \
  --region us-central1 \
  --format 'value(status.url)'
```

### 2. Health Check
```bash
SERVICE_URL=$(gcloud run services describe math-agent --region us-central1 --format 'value(status.url)')
curl $SERVICE_URL/health
```

### 3. Test Query Endpoint
```bash
curl -X POST $SERVICE_URL/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Find the derivative of x^x",
    "difficulty": "JEE_Advanced"
  }' | jq '.confidence, .mcp_used'
```

### 4. View Logs
```bash
gcloud run services logs read math-agent --region us-central1 --limit 50
```

---

## 📊 Cloud Run Configuration

### Current Settings (from CI/CD):
- **Memory**: 2 GiB
- **CPU**: 2 vCPU
- **Timeout**: 300 seconds (5 minutes)
- **Min Instances**: 0 (scales to zero)
- **Max Instances**: 10
- **Concurrency**: 80 requests per instance
- **Region**: us-central1

### Cost Optimization:
```bash
# Production with always-warm instance
gcloud run services update math-agent \
  --region us-central1 \
  --min-instances 1 \
  --cpu-throttling \
  --cpu-boost

# Development (scale to zero)
gcloud run services update math-agent \
  --region us-central1 \
  --min-instances 0 \
  --memory 1Gi \
  --cpu 1
```

---

## 🔄 CI/CD Workflow Details

### Trigger Events:
- **Push to `main`**: Full deploy to production
- **Push to `develop`**: Build only (no deploy)
- **Pull Request**: Run tests only
- **Manual**: Workflow dispatch button

### Workflow Jobs:

1. **Test** (`test` job)
   - Runs pytest with coverage
   - Uploads coverage to Codecov
   - Gates deployment

2. **Build** (`build` job)
   - Multi-stage Docker build
   - Push to GCR with tags: `latest`, `branch-name`, `git-sha`
   - Uses layer caching for speed

3. **Deploy** (`deploy` job)
   - Deploys to Cloud Run
   - Injects secrets from Secret Manager
   - Runs health check
   - Creates deployment summary

4. **Rollback** (`rollback` job)
   - Automatic rollback on deployment failure
   - Reverts to previous revision

---

## 🔐 Security Best Practices

### Secrets Management:
- ✅ API keys stored in Google Secret Manager
- ✅ No secrets in environment variables
- ✅ Automatic rotation support

### Container Security:
- ✅ Non-root user (`appuser`)
- ✅ Minimal base image (python:3.11-slim)
- ✅ No unnecessary packages
- ✅ Multi-stage build (no build tools in production)

### Network Security:
```bash
# Restrict to authenticated users only
gcloud run services update math-agent \
  --region us-central1 \
  --no-allow-unauthenticated

# Add Cloud Armor for DDoS protection
gcloud compute security-policies create math-agent-policy \
  --description "Rate limiting for Math Agent"

gcloud compute security-policies rules create 1000 \
  --security-policy math-agent-policy \
  --expression "true" \
  --action "rate-based-ban" \
  --rate-limit-threshold-count 100 \
  --rate-limit-threshold-interval-sec 60
```

---

## 📈 Monitoring & Observability

### View Metrics:
```bash
# Open Cloud Run dashboard
gcloud run services describe math-agent \
  --region us-central1 \
  --format 'value(status.url)' | xargs -I {} open "https://console.cloud.google.com/run/detail/us-central1/math-agent"
```

### Custom Alerts:
```bash
# Alert on high error rate
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="Math Agent Error Rate" \
  --condition-display-name="Error rate > 5%" \
  --condition-threshold-value=0.05 \
  --condition-threshold-duration=300s
```

### Structured Logging:
The app logs are automatically collected. View in Cloud Logging:
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=math-agent" \
  --limit 50 \
  --format json
```

---

## 🚀 Advanced Deployment Patterns

### Blue-Green Deployment:
```bash
# Deploy new version without traffic
gcloud run deploy math-agent \
  --image gcr.io/sacred-evening-477817-c1/math-agent:v2 \
  --no-traffic \
  --tag blue

# Test blue version
curl https://blue---math-agent-abc123-uc.a.run.app/health

# Shift traffic gradually
gcloud run services update-traffic math-agent \
  --to-revisions blue=10  # 10% canary
  
# Full cutover
gcloud run services update-traffic math-agent \
  --to-latest
```

### Multi-Region Deployment:
```bash
# Deploy to multiple regions
for region in us-central1 europe-west1 asia-southeast1; do
  gcloud run deploy math-agent \
    --image gcr.io/sacred-evening-477817-c1/math-agent \
    --region $region \
    --platform managed
done

# Add global load balancer (requires Cloud Load Balancing)
```

---

## 🛠️ Troubleshooting

### Issue: Container crashes on startup
```bash
# Check logs
gcloud run services logs read math-agent --region us-central1 --limit 100

# Common fixes:
# 1. Increase memory: --memory 4Gi
# 2. Increase timeout: --timeout 600
# 3. Check secret access permissions
```

### Issue: Slow cold starts
```bash
# Solution 1: Keep 1 instance warm
gcloud run services update math-agent --min-instances 1

# Solution 2: Enable CPU boost
gcloud run services update math-agent --cpu-boost

# Solution 3: Pre-download models (already in Dockerfile.multistage)
```

### Issue: 503 Service Unavailable
```bash
# Increase concurrency and instances
gcloud run services update math-agent \
  --concurrency 100 \
  --max-instances 20
```

---

## 💰 Cost Estimation

### Pricing (as of 2025):
- **CPU**: $0.00002400 per vCPU-second
- **Memory**: $0.00000250 per GiB-second
- **Requests**: $0.40 per million
- **Free tier**: 2 million requests/month

### Example Monthly Cost:
```
Assumptions:
- 100,000 requests/month
- Avg 2 seconds per request
- 2 vCPU, 2 GiB memory

Cost = (100K requests × 2s × $0.000024 × 2 CPU) + 
       (100K requests × 2s × $0.0000025 × 2 GiB) + 
       (100K requests × $0.40 / 1M)
     = $9.60 + $1.00 + $0.04
     = ~$10.64/month
```

With free tier: **~$0/month** for moderate usage!

---

## 📚 Additional Resources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Build Pricing](https://cloud.google.com/build/pricing)
- [Secret Manager Guide](https://cloud.google.com/secret-manager/docs)
- [GitHub Actions for GCP](https://github.com/google-github-actions)

---

## ✅ Deployment Checklist

Before going to production:

- [ ] Enable required GCP APIs
- [ ] Create service account with correct permissions
- [ ] Store secrets in Secret Manager
- [ ] Configure GitHub secrets
- [ ] Update CORS origins in `backend/app/main.py`
- [ ] Set up custom domain (optional)
- [ ] Configure Cloud CDN (optional)
- [ ] Set up monitoring alerts
- [ ] Test rollback procedure
- [ ] Document API endpoints
- [ ] Create runbook for incidents

---

**Need help?** Check logs, adjust resource limits, or contact GCP support.

Generated: November 19, 2025
Status: Production Ready

