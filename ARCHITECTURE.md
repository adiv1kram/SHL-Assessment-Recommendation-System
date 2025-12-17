# SHL Assessment Recommendation System - Architecture

## System Overview

The SHL Assessment Recommendation System is an intelligent platform that uses AI-powered semantic search to match job requirements with relevant SHL assessments. The system combines modern web technologies, vector databases, and LLM-based classification to provide accurate, balanced recommendations.

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **Vector Database**: ChromaDB
- **Embeddings**: HuggingFace `all-MiniLM-L6-v2`
- **LLM**: Google Gemini API (with heuristic fallback)
- **Data Processing**: Pandas, BeautifulSoup4

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite 5
- **HTTP Client**: Axios
- **Styling**: Vanilla CSS (custom design system)

### Data Pipeline
- **Scraper**: Custom web scraper for SHL product catalog
- **Storage**: JSON files + ChromaDB vector store
- **Evaluation**: Custom Mean Recall@K implementation

## Architecture Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                          │
│                     (React + Vite Frontend)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │  SearchBar   │  │ ResultsTable │  │   Premium UI         │ │
│  │  Component   │  │  Component   │  │   (Glassmorphism)    │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘ │
└─────────────────────────────┬──────────────────────────────────┘
                              │ HTTP/JSON
                              ▼
┌────────────────────────────────────────────────────────────────┐
│                       FASTAPI BACKEND                          │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  main.py - API Endpoints                                 │ │
│  │  • POST /recommend - Get recommendations                 │ │
│  │  • GET /health - Health check                           │ │
│  └──────────────────────────────────────────────────────────┘ │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  engine.py - Recommendation Logic                        │ │
│  │                                                           │ │
│  │  1. Query Classification (Gemini API / Heuristic)       │ │
│  │     ├─ Needs technical assessments?                      │ │
│  │     ├─ Needs behavioral assessments?                     │ │
│  │     └─ Calculate skill ratio (0.0-1.0)                  │ │
│  │                                                           │ │
│  │  2. Semantic Search (ChromaDB)                           │ │
│  │     └─ Retrieve top 30 similar assessments              │ │
│  │                                                           │ │
│  │  3. Intelligent Balancing                                │ │
│  │     ├─ Categorize by test type (K/P/A)                  │ │
│  │     ├─ Apply skill ratio distribution                    │ │
│  │     └─ Return balanced top 5-10 results                 │ │
│  └──────────────────────────────────────────────────────────┘ │
│                              │                                  │
└──────────────────────────────┼──────────────────────────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  ChromaDB       │  │  Gemini API     │  │  SHL Catalog    │
│  Vector Store   │  │  Classification │  │  JSON Data      │
│                 │  │                 │  │  (377+ items)   │
│  • Embeddings   │  │  • Query        │  │                 │
│  • Similarity   │  │    Analysis     │  │  • Name         │
│    Search       │  │  • Skill Ratio  │  │  • Description  │
│  • Fast         │  │    Calculation  │  │  • Test Type    │
│    Retrieval    │  │                 │  │  • Duration     │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

## Data Flow

### 1. Data Ingestion (Scraping)

```python
SHL Website
    ↓ scraper.py
    ├─ Parse product catalog pages
    ├─ Extract metadata (name, description, test type, duration)
    ├─ Filter out "Pre-packaged Job Solutions"
    └─ Save to shl_catalog.json (377+ items)
```

### 2. Index Building

```python
shl_catalog.json
    ↓ engine.py:build_index()
    ├─ Create Document objects
    ├─ Combine name + description + test types
    ├─ Generate embeddings (HuggingFace)
    └─ Store in ChromaDB
```

### 3. Query Processing

```python
User Query
    ↓
    ├─ 1. Classification (Gemini API or heuristic)
    │     └─ Output: {needs_technical, needs_behavioral, skill_ratio}
    │
    ├─ 2. Semantic Search
    │     ├─ Embedding generation
    │     ├─ Vector similarity search (k=30)
    │     └─ Retrieve candidate assessments
    │
    ├─ 3. Categorization
    │     ├─ Knowledge & Skills (Type K)
    │     ├─ Personality & Behavior (Type P)
    │     ├─ Ability & Aptitude (Type A)
    │     └─ Cognitive/Other
    │
    └─ 4. Balancing & Selection
          ├─ Apply skill_ratio distribution
          ├─ Ensure diversity
          └─ Return top 5-10 results
```

## Key Design Decisions

### 1. Intelligent Balancing Algorithm

**Problem**: Assignment requires balanced recommendations when a query spans multiple skill domains.

**Solution**: Two-stage classification + distribution
- **Stage 1**: Classify query intent using Gemini API
- **Stage 2**: Distribute results based on skill_ratio
- **Example**: "Java developer with collaboration skills"
  - Classification: `skill_ratio = 0.6` (60% technical, 40% behavioral)
  - Distribution: 6 technical assessments + 4 behavioral assessments

### 2. Gemini API Integration with Fallback

**Why**: Enables accurate understanding of nuanced queries

**Implementation**:
- Primary: Gemini API for sophisticated query analysis
- Fallback: Keyword-based heuristics (no API key required)
- Graceful degradation ensures system works without API

### 3. Semantic Search over Keyword Matching

**Why**: Understands intent beyond exact word matches

**Example**:
- Query: "Team player with coding skills"
- Semantic Search finds:
  - "Collaboration Assessment" (Personality)
  - "Software Engineering Test" (Knowledge)
- Keyword search might miss synonym variations

### 4. Premium Frontend Design

**Design Philosophy**: Create a "WOW" first impression

**Implementation**:
- Glassmorphism for modern aesthetic
- Rich gradients (purple/blue scheme)
- Micro-animations for engagement
- Card-based layout for scannability
- Color-coded badges for quick identification

## Scalability Considerations

### Current Implementation
- In-memory vector database
- Single-server deployment
- Synchronous request processing

### Production Improvements
1. **Database**: Migrate ChromaDB to persistent Pinecone/Weaviate
2. **Caching**: Add Redis for frequent queries
3. **Async**: Convert to async/await for concurrent requests
4. **Load Balancing**: Deploy multiple backend instances
5. **CDN**: Serve frontend via CloudFlare/AWS CloudFront

## Evaluation Strategy

### Metric: Mean Recall@K

```python
Recall@K = (Relevant items in top K) / (Total relevant items)

Mean Recall@K = Average across all queries
```

### Process
1. Load labeled train set (10 queries)
2. Generate predictions for each query
3. Calculate Recall@5 and Recall@10
4. Compare against ground truth labels
5. Iterate on balancing algorithm to optimize

### Target Performance
- **Recall@5**: >0.6
- **Recall@10**: >0.8

## Security Considerations

1. **API Keys**: Stored in `.env` file (not committed to Git)
2. **CORS**: Configured for specific origins in production
3. **Input Validation**: Pydantic models ensure type safety
4. **Rate Limiting**: Should be added for production deployment
5. **HTTPS**: Required for production (handled by Render/Vercel)

## Deployment Architecture

### Development
```
localhost:3000 (Frontend) ──→ localhost:8000 (Backend)
```

### Production
```
vercel.app (Frontend) ──→ render.com (Backend)
        │                         │
        ├─ Static CDN             ├─ Auto-scaling
        └─ Global edge            └─ HTTPS
```

## Future Enhancements

1. **Query Suggestions**: Auto-complete based on common patterns
2. **Assessment Comparison**: Side-by-side comparison feature
3. **Saved Searches**: User accounts with search history
4. **Analytics Dashboard**: Track popular queries and assessments
5. **Multi-language Support**: Internationalization
6. **Advanced Filters**: Duration, adaptive support, remote capability

---

**Document Version**: 1.0  
**Last Updated**: December 2025  
**Maintainer**: SHL GenAI Assessment Team
