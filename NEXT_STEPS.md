# Next Steps - Quick Reference

## 🚀 What You Need to Do Now

### 1. Add Your Gemini API Key (2 minutes)
```bash
nano backend/data/.env
# Replace with your actual key:
GEMINI_API_KEY=AIzaSy...your_key_here
```

### 2. Test Backend (5 minutes)
```bash
cd backend
./setup.sh
source venv/bin/activate
cd data
python -m app.main
```

**Verify**: Open http://localhost:8000/health should return `{"status":"healthy"}`

### 3. Test Frontend (5 minutes)
Open new terminal:
```bash
cd frontend
./setup.sh
npm run dev
```

**Verify**: Open http://localhost:3000 and test with:
- "Java developer with collaboration skills"
- Should see both technical AND behavioral assessments

### 4. Run Evaluation (5 minutes)
```bash
cd backend/data
python -m app.evaluation
```

**Note the scores** for your approach document:
- Mean Recall@5: ____
- Mean Recall@10: ____

### 5. Generate Submission CSV (5 minutes)
```bash
# Make sure backend is running!
cd submission
python genetate_csv.py
```

**Verify**: `submission.csv` created with correct format

### 6. Deploy Backend (15 minutes)
1. Go to [Render.com](https://render.com)
2. New → Web Service
3. Connect your GitHub repo
4. Configure:
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend/data && python -m app.main`
   - Add Environment Variable: `GEMINI_API_KEY=your_key`
5. Deploy
6. **Save your URL**: `https://your-app.onrender.com`

### 7. Deploy Frontend (10 minutes)
1. Update `frontend/src/App.jsx`:
   ```javascript
   const API_URL = 'https://your-app.onrender.com';
   ```
2. Go to [Vercel.com](https://vercel.com)
3. Import your GitHub repo
4. Configure:
   - Framework: Vite
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
5. Deploy
6. **Save your URL**: `https://your-app.vercel.app`

### 8. Create Approach Document (30 minutes)
Use this outline for your 2-page PDF:

**Page 1:**
- Problem understanding
- Technical approach (semantic search + AI classification)
- Technology stack (FastAPI, React, Gemini, ChromaDB)
- System architecture diagram (use ARCHITECTURE.md)

**Page 2:**
- Balancing algorithm explanation
- Evaluation results (your Mean Recall scores)
- Optimization iterations
- Deployment details

### 9. GitHub Repository (5 minutes)
```bash
cd "SHL Assessment Recommendation System"
git init
git add .
git commit -m "Initial commit - SHL Assessment Recommender"
git remote add origin your_github_url
git push -u origin main
```

Make sure repository is public or grant access to SHL reviewers.

### 10. Submit! (5 minutes)
Go to submission form and provide:

1. **API Endpoint URL**: `https://your-app.onrender.com`
2. **GitHub URL**: `https://github.com/your-username/shl-assessment-recommender`
3. **Frontend URL**: `https://your-app.vercel.app`
4. **Upload**: `submission.csv`
5. **Upload**: `approach.pdf`

---

## ⏱️ Total Time: ~90 minutes

## ✅ Pre-Submission Checklist

- [ ] Backend health endpoint responds with 200
- [ ] Frontend displays and allows searching
- [ ] Results include BOTH technical and behavioral assessments
- [ ] Evaluation script runs successfully
- [ ] Submission CSV generated
- [ ] Both deployments accessible publicly
- [ ] Approach document created (PDF, 2 pages)
- [ ] GitHub repository accessible
- [ ] All URLs tested from different device/network

## 🎯 You're Ready!

Everything has been built for you. Just follow these steps and you'll have a complete, professional submission!

**Good luck! 🚀**
