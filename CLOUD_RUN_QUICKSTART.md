# Cloud Run Setup Instructions

## Quick Setup (5 Minutes)

### 1. Enable Required APIs
```bash
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

### 2. Store API Key in Secret Manager
```bash
echo -n "YOUR_PERPLEXITY_API_KEY" | \
  gcloud secrets create perplexity-api-key --data-file=-

# Grant Cloud Run access
gcloud secrets add-iam-policy-binding perplexity-api-key \
  --member="serviceAccount:sacred-evening-477817-c1@appspot.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### 3. Deploy
```bash
./deploy-cloud-run.sh production
```

---

## GitHub Actions Setup (Optional)

### 1. Create Service Account
```bash
gcloud iam service-accounts create github-actions \
  --display-name="GitHub Actions Deployer"

gcloud projects add-iam-policy-binding sacred-evening-477817-c1 \
  --member="serviceAccount:github-actions@sacred-evening-477817-c1.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding sacred-evening-477817-c1 \
  --member="serviceAccount:github-actions@sacred-evening-477817-c1.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding sacred-evening-477817-c1 \
  --member="serviceAccount:github-actions@sacred-evening-477817-c1.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

gcloud iam service-accounts keys create key.json \
  --iam-account=github-actions@sacred-evening-477817-c1.iam.gserviceaccount.com
```

### 2. Add GitHub Secrets
Go to GitHub repo → Settings → Secrets → Actions:

- `GCP_PROJECT_ID`: `sacred-evening-477817-c1`
- `GCP_SA_KEY`: (paste contents of key.json)

### 3. Push Code
```bash
git add .
git commit -m "Add Cloud Run CI/CD"
git push origin main
```

GitHub Actions will automatically deploy!

---

## Quick Commands

### View Service
```bash
gcloud run services describe math-agent --region=us-central1
```

### View Logs
```bash
gcloud run services logs read math-agent --region=us-central1 --limit=50
```

### Update Configuration
```bash
gcloud run services update math-agent \
  --region=us-central1 \
  --memory=4Gi \
  --cpu=4 \
  --min-instances=2
```

### Rollback
```bash
PREV=$(gcloud run revisions list --service=math-agent --region=us-central1 --format="value(name)" --limit=2 | tail -1)
gcloud run services update-traffic math-agent --region=us-central1 --to-revisions=$PREV=100
```

---

## Cost Optimization

### Development (Scale to Zero)
```bash
gcloud run services update math-agent \
  --region=us-central1 \
  --min-instances=0 \
  --memory=1Gi \
  --cpu=1
```

### Production (Always Warm)
```bash
gcloud run services update math-agent \
  --region=us-central1 \
  --min-instances=1 \
  --memory=2Gi \
  --cpu=2 \
  --cpu-boost
```

---

## Troubleshooting

### Container Won't Start
```bash
# Check logs
gcloud run services logs read math-agent --region=us-central1 --limit=100

# Common fixes:
# 1. Increase timeout: --timeout 600
# 2. Increase memory: --memory 4Gi
# 3. Check secret permissions
```

### Slow Responses
```bash
# Keep instance warm
gcloud run services update math-agent --min-instances=1

# Enable CPU boost
gcloud run services update math-agent --cpu-boost
```

### 503 Errors
```bash
# Increase capacity
gcloud run services update math-agent \
  --max-instances=20 \
  --concurrency=100
```

---

**That's it!** Your Math Agent is now on Cloud Run with automatic scaling, CI/CD, and zero-downtime deployments.

