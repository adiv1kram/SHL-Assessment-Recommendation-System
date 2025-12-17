# SHL Assessment Recommendation System - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### Step 1: Add Your Gemini API Key

```bash
# Edit the .env file
nano backend/data/.env

# Add your API key:
GEMINI_API_KEY=your_actual_api_key_here
```

### Step 2: Setup Backend

```bash
cd backend
./setup.sh

# Activate virtual environment and start server
source venv/bin/activate
cd data
python -m app.main
```

Backend runs at: **http://localhost:8000**

### Step 3: Setup Frontend (in a new terminal)

```bash
cd frontend
./setup.sh

# Start development server
npm run dev
```

Frontend runs at: **http://localhost:3000**

## 🧪 Testing the System

### Test the API

```bash
# Health check
curl http://localhost:8000/health

# Get recommendations
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Java developer with collaboration skills"}'
```

### Test Sample Queries from Assignment

1. "I am hiring for Java developers who can also collaborate effectively with my business teams."
2. "Looking to hire mid-level professionals who are proficient in Python, SQL and Java Script."
3. "Here is a JD text, can you recommend some assessment that can help me screen applications. I am hiring for an analyst and wants applications to screen using Cognitive and personality tests"

## 📊 Run Evaluation

```bash
cd backend
source venv/bin/activate
cd data
python -m app.evaluation
```

This will:
- Load the labeled train set
- Calculate Mean Recall@5 and Recall@10
- Save results to `evaluation_results.json`

## 📝 Generate Submission CSV

```bash
# Make sure backend is running first!
cd submission
python genetate_csv.py
```

This creates `submission.csv` with predictions on the test set.

## 🐛 Troubleshooting

### Backend won't start
- Check if port 8000 is available: `lsof -i :8000`
- Verify virtual environment is activated: `which python`
- Check for missing dependencies: `pip list`

### Frontend won't start
- Clear node_modules: `rm -rf node_modules && npm install`
- Check if port 3000 is available: `lsof -i :3000`
- Verify Node version: `node --version` (should be 16+)

### CORS errors
- Ensure backend is running before frontend
- Check API_URL in frontend App.jsx matches backend URL

### No Gemini API key
- System will fall back to heuristic classification
- Still works, but with less accurate query understanding

## 📦 Project Structure

```
.
├── backend/
│   ├── data/
│   │   ├── app/              # Python application
│   │   ├── .env              # Environment variables
│   │   └── shl_catalog.json  # Scraped data
│   ├── requirements.txt
│   └── setup.sh
├── frontend/
│   ├── src/                  # React components
│   ├── package.json
│   └── setup.sh
├── submission/
│   ├── genetate_csv.py       # CSV generator
│   └── submission.csv        # Output file
└── README.md
```

## 📌 Key Files

- **Backend API**: `backend/data/app/main.py`
- **Recommendation Engine**: `backend/data/app/engine.py`
- **Frontend App**: `frontend/src/App.jsx`
- **Design System**: `frontend/src/index.css`

## ✅ Pre-Submission Checklist

- [ ] Backend runs successfully on localhost:8000
- [ ] Frontend displays correctly on localhost:3000
- [ ] Can search and get balanced results
- [ ] Evaluation script runs and generates metrics
- [ ] Submission CSV generated successfully
- [ ] All 377+ assessments scraped
- [ ] Gemini API key configured (or fallback working)

## 🚢 Deployment Instructions

See `README.md` for full deployment guide to Render.com and Vercel.

---

**Need help?** Check the full documentation in README.md and ARCHITECTURE.md
