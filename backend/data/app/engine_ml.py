import json
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API (optional - fallback to heuristics if not available)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY and GEMINI_API_KEY != 'your_gemini_api_key_here':
    genai.configure(api_key=GEMINI_API_KEY)
    USE_GEMINI = True
else:
    USE_GEMINI = False
    print("Warning: Gemini API key not configured. Using heuristic balancing.")

# 1. Initialize Vector DB
def build_index():
    """Build or load the vector database from scraped SHL catalog."""
    with open('../data/shl_catalog.json', 'r') as f:
        data = json.load(f)
    
    documents = []
    for item in data:
        # Embed the description and name for semantic search
        # Include test_type for better matching
        content = f"{item['name']} {item['description']} Test Types: {', '.join(item['test_type'])}"
        documents.append(Document(page_content=content, metadata=item))
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Persist DB
    db = Chroma.from_documents(documents, embeddings, persist_directory="../data/chroma_db")
    return db

def classify_query_with_gemini(query: str) -> dict:
    """
    Use Gemini API to intelligently classify the query needs.
    
    Returns:
        {
            'needs_technical': bool,
            'needs_behavioral': bool,
            'needs_cognitive': bool,
            'skill_ratio': float (0.0-1.0, higher means more technical)
        }
    """
    if not USE_GEMINI:
        # Fallback to heuristic classification
        return classify_query_heuristic(query)
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""Analyze this job requirement query and classify what types of assessments are needed:

Query: "{query}"

Respond ONLY with a JSON object in this exact format:
{{
    "needs_technical": true/false,
    "needs_behavioral": true/false,
    "needs_cognitive": true/false,
    "skill_ratio": 0.0-1.0
}}

Where skill_ratio is 0.0-1.0 (0.0 = purely behavioral/soft skills, 1.0 = purely technical/hard skills, 0.5 = balanced)

Examples:
- "Java developer" → {{"needs_technical": true, "needs_behavioral": false, "needs_cognitive": true, "skill_ratio": 0.8}}
- "Team leader with communication skills" → {{"needs_technical": false, "needs_behavioral": true, "needs_cognitive": false, "skill_ratio": 0.2}}
- "Python developer who collaborates well" → {{"needs_technical": true, "needs_behavioral": true, "needs_cognitive": true, "skill_ratio": 0.6}}

Only return the JSON, nothing else."""

        response = model.generate_content(prompt)
        result = json.loads(response.text.strip())
        return result
        
    except Exception as e:
        print(f"Gemini API error: {e}. Falling back to heuristics.")
        return classify_query_heuristic(query)

def classify_query_heuristic(query: str) -> dict:
    """
    Heuristic-based query classification as fallback.
    """
    query_lower = query.lower()
    
    # Technical indicators
    technical_keywords = ['java', 'python', 'sql', 'javascript', 'developer', 'programmer', 
                         'coding', 'technical', 'engineering', 'data', 'analyst', 'software']
    
    # Behavioral indicators
    behavioral_keywords = ['collaborate', 'leadership', 'communication', 'team', 'personality',
                          'behavioral', 'soft skill', 'interpersonal', 'stakeholder', 'management']
    
    # Cognitive indicators
    cognitive_keywords = ['problem-solving', 'analytical', 'cognitive', 'reasoning', 'aptitude',
                         'critical thinking', 'logical']
    
    needs_technical = any(kw in query_lower for kw in technical_keywords)
    needs_behavioral = any(kw in query_lower for kw in behavioral_keywords)
    needs_cognitive = any(kw in query_lower for kw in cognitive_keywords) or needs_technical
    
    # Calculate ratio
    if needs_technical and needs_behavioral:
        skill_ratio = 0.5  # Balanced
    elif needs_technical:
        skill_ratio = 0.8  # Mostly technical
    elif needs_behavioral:
        skill_ratio = 0.2  # Mostly behavioral
    else:
        skill_ratio = 0.5  # Default balanced
    
    return {
        'needs_technical': needs_technical,
        'needs_behavioral': needs_behavioral,
        'needs_cognitive': needs_cognitive,
        'skill_ratio': skill_ratio
    }

# 2. Retrieval Logic with Intelligent Balancing
def get_recommendations(query, db, max_results=10):
    """
    Get balanced recommendations based on query analysis.
    
    CRITICAL: This implements the "Recommendation Balance" requirement from the assignment.
    If a query mentions both technical and behavioral skills, results MUST include both types.
    """
    # Step 1: Classify the query
    classification = classify_query_with_gemini(query)
    
    # Step 2: Perform Similarity Search (get more than needed for filtering)
    results = db.similarity_search(query, k=30)
    
    # Step 3: Categorize results by test type
    categorized = {
        'knowledge_skills': [],  # Test Type K
        'personality_behavior': [],  # Test Type P
        'ability_aptitude': [],  # Test Type A
        'cognitive': [],  # Any cognitive/reasoning test
        'other': []
    }
    
    for doc in results:
        test_types = doc.metadata.get('test_type', [])
        test_types_str = ' '.join(test_types).lower()
        
        categorized_flag = False
        
        if 'knowledge' in test_types_str or 'skills' in test_types_str:
            categorized['knowledge_skills'].append(doc)
            categorized_flag = True
        
        if 'personality' in test_types_str or 'behavior' in test_types_str:
            categorized['personality_behavior'].append(doc)
            categorized_flag = True
        
        if 'ability' in test_types_str or 'aptitude' in test_types_str:
            categorized['ability_aptitude'].append(doc)
            categorized_flag = True
        
        if 'cognitive' in test_types_str or 'reasoning' in test_types_str:
            categorized['cognitive'].append(doc)
            categorized_flag = True
        
        if not categorized_flag:
            categorized['other'].append(doc)
    
    # Step 4: Balance the recommendations based on classification
    final_recs = []
    seen_urls = set()
    
    # Calculate target counts based on skill_ratio
    skill_ratio = classification['skill_ratio']
    
    if classification['needs_technical'] and classification['needs_behavioral']:
        # BALANCED MODE: Ensure mix of both (Critical for evaluation!)
        target_technical = int(max_results * skill_ratio)
        target_behavioral = max_results - target_technical
        
        # Add technical assessments
        for doc in categorized['knowledge_skills'][:target_technical]:
            if doc.metadata['url'] not in seen_urls:
                final_recs.append(doc)
                seen_urls.add(doc.metadata['url'])
        
        # Add behavioral assessments
        for doc in categorized['personality_behavior'][:target_behavioral]:
            if doc.metadata['url'] not in seen_urls:
                final_recs.append(doc)
                seen_urls.add(doc.metadata['url'])
        
        # Fill remaining with cognitive/ability if needed
        if len(final_recs) < max_results:
            for doc in categorized['cognitive'] + categorized['ability_aptitude']:
                if doc.metadata['url'] not in seen_urls and len(final_recs) < max_results:
                    final_recs.append(doc)
                    seen_urls.add(doc.metadata['url'])
    
    elif classification['needs_technical']:
        # Mostly technical
        for doc in categorized['knowledge_skills'] + categorized['cognitive'] + categorized['ability_aptitude']:
            if doc.metadata['url'] not in seen_urls and len(final_recs) < max_results:
                final_recs.append(doc)
                seen_urls.add(doc.metadata['url'])
    
    elif classification['needs_behavioral']:
        # Mostly behavioral
        for doc in categorized['personality_behavior']:
            if doc.metadata['url'] not in seen_urls and len(final_recs) < max_results:
                final_recs.append(doc)
                seen_urls.add(doc.metadata['url'])
    
    else:
        # General - use top semantic matches
        for doc in results:
            if doc.metadata['url'] not in seen_urls and len(final_recs) < max_results:
                final_recs.append(doc)
                seen_urls.add(doc.metadata['url'])
    
    # Ensure we always return at least 5 results (requirement: minimum 5, maximum 10)
    if len(final_recs) < 5:
        for doc in results:
            if doc.metadata['url'] not in seen_urls and len(final_recs) < 10:
                final_recs.append(doc)
                seen_urls.add(doc.metadata['url'])
    
    # Format for API (trim to max 10)
    response_data = []
    for doc in final_recs[:max_results]:
        meta = doc.metadata
        response_data.append({
            "url": meta['url'],
            "name": meta['name'],
            "adaptive_support": meta['adaptive_support'],
            "description": meta['description'],
            "duration": meta['duration'],
            "remote_support": meta['remote_support'],
            "test_type": meta['test_type']
        })
    
    return response_data