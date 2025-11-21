# Deploy Frontend (Firebase) & Backend (Cloud Run)

## Prerequisites
- Google Cloud project: sacred-evening-477817-c1
- Firebase project created (web app) named math-focused-assistant
- Installed CLIs:
  - gcloud
  - firebase-tools (npm install -g firebase-tools)

## 1. Backend → Cloud Run
```bash
export PERPLEXITY_API_KEY="your_key_here"
./deploy_cloud_run.sh
```
Outputs a URL like:
```
https://math-focused-backend-xxxxx-uc.a.run.app
```
Test health:
```bash
curl https://math-focused-backend-xxxxx-uc.a.run.app/health
```

## 2. Frontend → Firebase Hosting
```bash
./deploy_firebase.sh
```
After deploy you get a Hosting URL like:
```
https://math-focused-assistant.web.app
```

## 3. Point Frontend to Backend
Edit `frontend/src/App.js` and set:
```js
const API_URL = "https://math-focused-backend-xxxxx-uc.a.run.app";
```
Or build with env var:
```bash
cd frontend
REACT_APP_API_URL="https://math-focused-backend-xxxxx-uc.a.run.app" npm run build
```
Redeploy frontend:
```bash
firebase deploy --only hosting
```

## 4. Verification Checklist
- [ ] Backend health endpoint returns status ok
- [ ] Cloud Run logs show requests
- [ ] Frontend loads via Firebase URL
- [ ] Browser network tab shows calls to Cloud Run URL
- [ ] Queries return answers

## 5. Troubleshooting
| Issue | Fix |
|-------|-----|
| 403 on Cloud Run | Enable Cloud Run API, re-deploy |
| PERPLEXITY_API_KEY missing | export and redeploy |
| Frontend still calls localhost | Hard-coded old bundle; rebuild with REACT_APP_API_URL |
| Firebase deploy fails | Run firebase login, then firebase init hosting |

## 6. Next Steps
- Add CI/CD with GitHub Actions for both deploys
- Add custom domain (Firebase + Cloud Run Cloud DNS)
- Add monitoring (Cloud Logging + Error Reporting)

