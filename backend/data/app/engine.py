"""
Simple recommendation engine without ML dependencies
Uses TF-IDF for semantic matching - lightweight and fast!
"""
import json
import os
import re
from typing import List, Dict
from collections import Counter
import math


def build_simple_index():
    """Load catalog data - no vector DB needed"""
    # Working directory is backend/data/, catalog is in the same directory
    catalog_path = "./shl_catalog.json"
    
    print(f"DEBUG: CWD: {os.getcwd()}")
    print(f"DEBUG: Looking for catalog at: {os.path.abspath(catalog_path)}")
    
    if not os.path.exists(catalog_path):
        print(f"DEBUG: File not found at {catalog_path}!")
        return []
    
    with open(catalog_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"DEBUG: Loaded {len(data)} items from catalog")
    return data


def tokenize(text: str) -> List[str]:
    """Simple tokenizer"""
    text = text.lower()
    tokens = re.findall(r'\b\w+\b', text)
    return tokens


def compute_tfidf(documents: List[str]) -> tuple:
    """Compute TF-IDF for all documents"""
    # Build vocabulary and document frequency
    vocab = set()
    doc_tokens = []
    
    for doc in documents:
        tokens = tokenize(doc)
        doc_tokens.append(tokens)
        vocab.update(tokens)
    
    vocab = sorted(vocab)
    word_to_idx = {word: idx for idx, word in enumerate(vocab)}
    
    # Compute IDF
    N = len(documents)
    idf = {}
    for word in vocab:
        df = sum(1 for tokens in doc_tokens if word in tokens)
        idf[word] = math.log(N / (1 + df))
    
    # Compute TF-IDF vectors
    vectors = []
    for tokens in doc_tokens:
        tf = Counter(tokens)
        vector = [0.0] * len(vocab)
        for word, count in tf.items():
            if word in word_to_idx:
                idx = word_to_idx[word]
                vector[idx] = count * idf[word]
        # Normalize
        norm = math.sqrt(sum(x*x for x in vector))
        if norm > 0:
            vector = [x / norm for x in vector]
        vectors.append(vector)
    
    return vectors, word_to_idx, idf


def cosine_similarity(vec1, vec2):
    """Compute cosine similarity"""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    return dot_product


def get_recommendations(query: str, db_instance=None, k: int = 10) -> List[Dict]:
    """Get recommendations using TF-IDF similarity"""
    # Load catalog
    catalog = build_simple_index()
    
    if not catalog:
        return []
    
    # Create document corpus
    # Use name and test_type since descriptions are often empty from scraping
    documents = []
    for item in catalog:
        # Combine name and test types for matching
        name = item.get('name', '')
        test_types = ' '.join(item.get('test_type', []))
        doc_text = f"{name} {test_types}"
        documents.append(doc_text)
    
    # Add query as last document
    documents.append(query)
    
    # Compute TF-IDF
    vectors, word_to_idx, idf = compute_tfidf(documents)
    
    # Query vector is the last one
    query_vector = vectors[-1]
    doc_vectors = vectors[:-1]
    
    # Compute similarities
    similarities = []
    for idx, doc_vector in enumerate(doc_vectors):
        sim = cosine_similarity(query_vector, doc_vector)
        similarities.append((idx, sim))
    
    # Sort by similarity
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # Get top k results
    results = []
    for idx, score in similarities[:k]:
        item = catalog[idx]
        
        # Convert duration safely (might be int or string)
        duration_val = item.get("duration", 0)
        if isinstance(duration_val, int):
            duration = duration_val
        elif isinstance(duration_val, str) and duration_val.isdigit():
            duration = int(duration_val)
        else:
            duration = 0
        
        # Convert to match AssessmentItem model exactly
        results.append({
            "url": item.get("url", ""),
            "name": item.get("name", ""),
            "adaptive_support": item.get("adaptive_support", "No"),
            "description": item.get("description", ""),
            "duration": duration,
            "remote_support": item.get("remote_support", "No"),
            "test_type": item.get("test_type", [])
        })
    
    return results


# For compatibility with main.py
def build_index():
    """Dummy function for compatibility"""
    return None
