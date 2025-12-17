# SHL Assessment Recommendation System

![SHL Assessment Intelligence](https://img.shields.io/badge/AI-Powered-purple) ![Status](https://img.shields.io/badge/Status-Production-success) ![License](https://img.shields.io/badge/License-MIT-blue)

An intelligent recommendation system that helps hiring managers and recruiters discover relevant SHL assessments using natural language queries. Built with semantic search, RAG (Retrieval-Augmented Generation), and AI-powered query classification.

## 🌟 Features

- **Semantic Search**: Advanced vector-based search using HuggingFace embeddings
- **Intelligent Balancing**: Automatically balances technical and behavioral assessment recommendations
- **AI-Powered Classification**: Uses Google Gemini API for query understanding (with heuristic fallback)
- **Premium UI**: Modern, responsive frontend with glassmorphism and smooth animations
- **RESTful API**: FastAPI backend with comprehensive endpoints
- **Evaluation Metrics**: Built-in Mean Recall@K calculation for performance tracking

## 🏗️ System Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   Frontend      │  HTTP   │   FastAPI        │  Query  │  Vector DB      │
│   (React +      │────────▶│   Backend        │────────▶│  (ChromaDB)     │
│    Vite)        │         │                  │         │                 │
└─────────────────┘         └──────────────────┘         └─────────────────┘
                                     │                            │
                                     │                            │
                                     ▼                            ▼
                            ┌──────────────────┐       ┌─────────────────┐
                            │  Gemini API      │       │  SHL Catalog    │
                            │  (Classification)│       │  (377+ items)   │
                            └──────────────────┘       └─────────────────┘
```

## 📁 Project Structure

```
SHL Assessment Recommendation System/
├── backend/
│   ├── data/
│   │   ├── app/
│   │   │   ├── main.py              # FastAPI application
│   │   │   ├── engine.py            # RAG & recommendation logic
│   │   │   ├── scraper.py           # SHL catalog scraper
│   │   │   ├── models.py            # Pydantic models
│   │   │   ├── utils.py             # Helper functions
│   │   │   ├── evaluation.py        # Metrics & evaluation
│   │   │   └── load_datasets.py     # Dataset loader
│   │   ├── .env                     # Environment variables
│   │   ├── shl_catalog.json         # Scraped assessment data
│   │   ├── chroma_db/               # Vector database
│   │   └── Gen_AI Dataset.xlsx      # Train/test datasets
│   └── requirements.txt             # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx                  # Main application
│   │   ├── main.jsx                 # Entry point
│   │   ├── index.css                # Design system
│   │   └── components/
│   │       ├── SearchBar.jsx        # Search component
│   │       └── ResultsTable.jsx     # Results display
│   ├── index.html                   # HTML template
│   ├── package.json                 # Node dependencies
│   └── vite.config.js               # Vite configuration
├── submission/
│   ├── approach.pdf                 # 2-page approach document
│   ├── genetate_csv.py              # Test set prediction generator
│   └── submission.csv               # Final predictions
└── README.md                        # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Google Gemini API key (optional, system falls back to heuristics)

### Backend Setup

```bash
cd backend
pip install -r requirements.txt

# Configure environment (add your Gemini API key)
cd data
nano .env  # Add: GEMINI_API_KEY=your_key_here

# Run the backend
python -m app.main
```

Backend will start at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will start at `http://localhost:3000`

## 📊 API Documentation

### Health Check
```bash
GET /health
Response: {"status": "healthy"}
```

### Recommendation Endpoint
```bash
POST /recommend
Content-Type: application/json

{
  "query": "Java developer with collaboration skills"
}

Response: {
  "recommended_assessments": [
    {
      "url": "https://www.shl.com/...",
      "name": "Assessment Name",
      "test_type": ["Knowledge & Skills"],
      "duration": 30,
      "adaptive_support": "Yes",
      "remote_support": "Yes",
      "description": "..."
    }
  ]
}
```

## 📈 Evaluation

Run evaluation on the labeled train set:

```bash
cd backend/data
python -m app.evaluation
```

This calculates Mean Recall@K metrics and saves results to `evaluation_results.json`.

## 📝 Generating Submission CSV

```bash
cd submission
python genetate_csv.py
```

This generates `submission.csv` with predictions on the test set in the required format:
```
Query,Assessment_url
"Query 1","https://www.shl.com/..."
"Query 1","https://www.shl.com/..."
...
```

## 🎯 Key Implementation Details

### Intelligent Balancing Algorithm

The system implements sophisticated query classification to ensure balanced recommendations:

1. **Query Analysis**: Uses Gemini API (or heuristics) to classify queries into technical/behavioral/cognitive needs
2. **Skill Ratio Calculation**: Determines the ratio of technical to behavioral skills required
3. **Balanced Distribution**: Ensures results include appropriate mix of assessment types

Example:
- Query: "Java developer with collaboration skills"
- Classification: `{needs_technical: true, needs_behavioral: true, skill_ratio: 0.6}`
- Result: 60% technical assessments, 40% behavioral assessments

### Semantic Search

- Uses HuggingFace `all-MiniLM-L6-v2` embeddings for semantic understanding
- ChromaDB vector database for efficient similarity search
- Combines assessment name, description, and test types in embeddings

## 🎨 Frontend Design

The frontend features a premium design system with:
- **Glassmorphism effects** for cards and containers
- **Gradient backgrounds** with purple/blue color scheme
- **Micro-animations** on hover and interaction
- **Responsive layout** optimized for all devices
- **Google Fonts** (Outfit for headings, Inter for body)

## 🚢 Deployment

### Backend Deployment (Render.com)

1. Create new Web Service
2. Connect GitHub repository
3. Configure:
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend/data && python -m app.main`
4. Add environment variable: `GEMINI_API_KEY`

### Frontend Deployment (Vercel)

1. Import project from GitHub
2. Configure:
   - Framework: Vite
   - Build Command: `cd frontend && npm run build`
   - Output Directory: `frontend/dist`
3. Add environment variable: `VITE_API_URL` (your backend URL)

## 📄 License

MIT License - see LICENSE file for details

## 👥 Author

Created as part of the SHL GenAI Assessment

---

**Note**: This system requires the SHL catalog data to be scraped first. The scraper will run automatically on backend startup if data is not found.
