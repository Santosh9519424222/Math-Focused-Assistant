# 🚀 How to Access Your Math-Focused Assistant

## ✅ Server Status
Your FastAPI server is **RUNNING** on the VM!
- **VM IP**: 34.31.83.248
- **Port**: 8000
- **Status**: Active (PID 327173)

---

## 🌐 Option 1: Direct Browser Access (Requires Firewall Rule)

### Step 1: Create Firewall Rule (Run from your local machine)
```bash
gcloud compute firewall-rules create allow-port-8000 \
  --allow tcp:8000 \
  --source-ranges 0.0.0.0/0 \
  --description "Allow access to FastAPI app on port 8000" \
  --project=sacred-evening-477817-c1
```

### Step 2: Access in Browser
Once firewall rule is created, open:
- **Health Check**: http://34.31.83.248:8000/health
- **Main API**: http://34.31.83.248:8000/
- **API Docs**: http://34.31.83.248:8000/docs
- **Test Query**: http://34.31.83.248:8000/docs#/default/query_rag_pipeline_query_post

---

## 🔒 Option 2: SSH Tunnel (Most Secure - No Firewall Changes)

### From Your Local Machine:
```bash
# Create SSH tunnel (replace with your SSH key path)
gcloud compute ssh instance-20251112-111252 \
  --zone=YOUR_ZONE \
  --project=sacred-evening-477817-c1 \
  -- -L 8000:localhost:8000 -N -f
```

Or if you have direct SSH access:
```bash
ssh -L 8000:localhost:8000 -N -f santoshyadav_951942@34.31.83.248
```

### Then Access in Browser:
- **Health Check**: http://localhost:8000/health
- **Main API**: http://localhost:8000/
- **API Docs**: http://localhost:8000/docs

---

## 🌈 Option 3: Google Cloud Console Tunnel (GUI Method)

1. Go to: https://console.cloud.google.com/compute/instances
2. Find your instance: `instance-20251112-111252`
3. Click **SSH** → Opens in browser
4. In the SSH window, run:
```bash
curl http://localhost:8000/health
```
5. Use Cloud Shell tunnel (if available in your project)

---

## 🧪 Option 4: Test with curl (From VM)

Already working! Run these commands in your VM SSH session:

```bash
# Health check
curl http://localhost:8000/health

# Root endpoint
curl http://localhost:8000/

# KB Status
curl http://localhost:8000/kb/status

# Test a math query (triggers lazy init)
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Solve x^2 + 5x + 6 = 0",
    "difficulty": "JEE_Main"
  }'
```

---

## 📊 Check Server Status

```bash
# View server logs
tail -f /home/santoshyadav_951942/Math-Focused-Assistant/backend/server.log

# Check if server is running
ps aux | grep uvicorn

# Test health endpoint
curl http://localhost:8000/health
```

---

## 🔥 Restart Server

If you need to restart:
```bash
# Kill existing server
pkill -f uvicorn

# Start fresh
cd /home/santoshyadav_951942/Math-Focused-Assistant
source .venv/bin/activate
cd backend
PYTHONPATH=. nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &
```

---

## 🎯 Recommended: SSH Tunnel Method

**Best for development** - No firewall changes needed:

### macOS/Linux:
```bash
ssh -i ~/.ssh/YOUR_KEY \
  -L 8000:localhost:8000 \
  santoshyadav_951942@34.31.83.248
```

### Windows (PowerShell):
```powershell
ssh -i C:\path\to\YOUR_KEY `
  -L 8000:localhost:8000 `
  santoshyadav_951942@34.31.83.248
```

Then browse to: http://localhost:8000

---

## 🚨 Important Notes

1. **Server is running on VM** - Check with: `curl http://localhost:8000/health`
2. **Firewall rule needed** for direct external access (Option 1)
3. **SSH tunnel** is safer and doesn't require firewall changes (Option 2)
4. **First /query request** will take ~10-20 seconds (loads ML models)
5. **API Key is set** - Your Perplexity API is configured and ready

---

## 📱 Quick Test (From Your Local Machine)

After setting up tunnel or firewall:

### Browser Test:
```
http://YOUR_ACCESS_URL/docs
```

### curl Test:
```bash
curl -X POST http://YOUR_ACCESS_URL/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the derivative of x^x?",
    "difficulty": "JEE_Advanced"
  }'
```

---

## 🎉 Your App is Ready!

The Math-Focused Assistant is running with:
- ✅ Perplexity API configured
- ✅ Knowledge base with 5 sample problems
- ✅ LangGraph workflow
- ✅ Input/Output guardrails
- ✅ Feedback system
- ✅ Health monitoring

Choose your access method and enjoy! 🚀

