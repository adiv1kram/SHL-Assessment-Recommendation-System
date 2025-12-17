import uvicorn
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Import local modules
from .models import QueryRequest, RecommendationResponse
from .engine import get_recommendations, build_index
from .scraper import run_scraper

app = FastAPI(title="SHL Assessment Recommender API")

# Enable CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global DB instance
db_instance = None

@app.on_event("startup")
async def startup_event():
    global db_instance
    print("Initializing RAG Engine...")
    
    # Check if data exists, if not, scrape
    data_path = "../data/shl_catalog.json"
    if not os.path.exists(data_path):
        print("Data not found. Running scraper first...")
        run_scraper()
        
    # Build/Load Vector DB
    # Note: In production, you'd load a persisted DB rather than rebuilding
    db_instance = build_index()
    print("Engine Ready.")

@app.get("/health")
def health_check():
    """
    Health Check Endpoint
    Returns strict 200 OK with {"status": "healthy"}
    """
    return {"status": "healthy"}

@app.post("/recommend", response_model=RecommendationResponse)
def recommend_assessments(request: QueryRequest):
    """
    Assessment Recommendation Endpoint
    Accepts: JSON { "query": "..." }
    Returns: JSON { "recommended_assessments": [ ... ] }
    """
    try:
        # Simple engine doesn't need db_instance, it loads data directly
        results = get_recommendations(request.query, db_instance)
        return {"recommended_assessments": results}
    except Exception as e:
        print(f"Error processing request: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)