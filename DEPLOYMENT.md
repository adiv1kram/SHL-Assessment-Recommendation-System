# Deployment Guide - SHL Assessment Recommendation System

## Backend Deployment (Render.com - FREE)

### Step 1: Prepare Backend
Your backend is ready! Files needed:
- ✅ `Dockerfile` 
- ✅ `requirements-ultra-minimal.txt`
- ✅ Code in `backend/data/app/`

### Step 2: Create start.sh Script
```bash
#!/bin/bash
cd data
python -m app.main
```

### Step 3: Deploy to Render.com

1. **Go to** https://render.com and sign up/login

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Or use "Deploy from Git URL"

3. **Configure Service**:
   ```
   Name: shl-recommendation-api
   Region: Choose closest to you
   Branch: main
   Root Directory: backend
   
   Build Command: pip install -r requirements-ultra-minimal.txt
   Start Command: cd data && python -m app.main
   
   Instance Type: Free
   ```

4. **Environment Variables** (if needed):
   ```
   GEMINI_API_KEY=your_key_here  (optional)
   ```

5. **Click "Create Web Service"**

6. **Wait 5-10 minutes** for deployment

7. **Your API URL**: `https://shl-recommendation-api.onrender.com`

### Step 4: Test Deployed API
```bash
# Test health endpoint
curl https://your-app.onrender.com/health

# Test recommend endpoint
curl -X POST https://your-app.onrender.com/recommend \
  -H "Content-Type: application/json" \
  -d '{"query":"Python developer"}'
```

---

## Frontend Deployment (Vercel - FREE)

### Step 1: Update API URL
Edit `frontend/src/App.jsx`:
```javascript
// Change this line:
const API_URL = 'http://localhost:8000';

// To your deployed backend:
const API_URL = 'https://your-app.onrender.com';
```

### Step 2: Build Frontend
```bash
cd frontend
npm run build
```

### Step 3: Deploy to Vercel

1. **Install Vercel CLI** (optional):
   ```bash
   npm i -g vercel
   cd frontend
   vercel
   ```

2. **Or use Vercel Dashboard**:
   - Go to https://vercel.com
   - Click "Add New" → "Project"
   - Import your GitHub repository
   - Select `frontend` folder
   - Framework: Vite
   - Click "Deploy"

3. **Your Frontend URL**: `https://your-project.vercel.app`

---

## Alternative: Railway.app

If Render doesn't work, try Railway.app:

1. Go to https://railway.app
2. "New Project" → "Deploy from GitHub"
3. Select repository and `backend` folder
4. Railway auto-detects Dockerfile
5. Deploy!

---

## Troubleshooting

### Backend won't start
- Check logs in Render dashboard
- Verify all files are committed to Git
- Ensure `shl_catalog.json` exists in `backend/data/`

### Frontend can't connect to backend
- Check CORS is enabled in `main.py` (✅ Already done)
- Verify API URL is correct in `App.jsx`
- Check backend is actually running

### Free tier limitations
- Render free tier: Sleeps after 15 min inactivity (first request takes ~30s)
- Vercel free tier: 100GB bandwidth/month

---

## Quick Commands Reference

```bash
# Test local backend
curl http://localhost:8000/health

# Test deployed backend  
curl https://YOUR-APP.onrender.com/health

# Build frontend
cd frontend && npm run build

# Deploy frontend with Vercel CLI
cd frontend && vercel --prod
```
