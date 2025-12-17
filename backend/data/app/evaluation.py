import json
import numpy as np
from typing import List, Dict
from .load_datasets import load_excel_dataset, parse_train_set
from .engine import get_recommendations, build_index

def calculate_recall_at_k(predicted_urls: List[str], relevant_urls: List[str], k: int = 10) -> float:
    """
    Calculate Recall@K metric.
    
    Recall@K = (Number of relevant items in top K) / (Total relevant items)
    
    Args:
        predicted_urls: List of predicted assessment URLs (top K)
        relevant_urls: List of ground truth relevant assessment URLs
        k: Number of top predictions to consider
        
    Returns:
        Recall@K score (0.0 to 1.0)
    """
    if not relevant_urls:
        return 0.0
    
    # Take top K predictions
    top_k_predictions = predicted_urls[:k]
    
    # Count how many relevant items are in top K
    relevant_in_top_k = sum(1 for url in top_k_predictions if url in relevant_urls)
    
    # Calculate recall
    recall = relevant_in_top_k / len(relevant_urls)
    
    return recall

def mean_recall_at_k(predictions: List[Dict], labeled_data: List[Dict], k: int = 10) -> float:
    """
    Calculate Mean Recall@K across all queries.
    
    Args:
        predictions: List of {query, predicted_urls} dicts
        labeled_data: List of {query, relevant_assessments} dicts from training data
        k: Number of top predictions to consider
        
    Returns:
        Mean Recall@K score
    """
    recall_scores = []
    
    for pred in predictions:
        query = pred['query']
        predicted_urls = pred['predicted_urls']
        
        # Find corresponding labeled data
        relevant_urls = None
        for labeled in labeled_data:
            if labeled['query'].strip() == query.strip():
                relevant_urls = labeled['relevant_assessments']
                break
        
        if relevant_urls:
            recall = calculate_recall_at_k(predicted_urls, relevant_urls, k)
            recall_scores.append(recall)
            print(f"Query: {query[:50]}... | Recall@{k}: {recall:.3f}")
    
    if not recall_scores:
        return 0.0
    
    mean_recall = np.mean(recall_scores)
    return mean_recall

def evaluate_on_train_set(db_instance, dataset_path: str = "../data/Gen_AI Dataset.xlsx"):
    """
    Evaluate the recommendation system on the labeled train set.
    
    Returns evaluation metrics for the approach document.
    """
    print("="*60)
    print("EVALUATION ON LABELED TRAIN SET")
    print("="*60)
    
    # Load datasets
    datasets = load_excel_dataset(dataset_path)
    
    if 'train' not in datasets:
        print("Error: Train set not found in dataset")
        return None
    
    # Parse labeled data
    labeled_data = parse_train_set(datasets['train'])
    print(f"\nEvaluating on {len(labeled_data)} labeled queries...\n")
    
    # Generate predictions
    predictions = []
    for item in labeled_data:
        query = item['query']
        results = get_recommendations(query, db_instance)
        predicted_urls = [r['url'] for r in results]
        
        predictions.append({
            'query': query,
            'predicted_urls': predicted_urls
        })
    
    # Calculate metrics
    recall_5 = mean_recall_at_k(predictions, labeled_data, k=5)
    recall_10 = mean_recall_at_k(predictions, labeled_data, k=10)
    
    print("\n" + "="*60)
    print("EVALUATION RESULTS")
    print("="*60)
    print(f"Mean Recall@5:  {recall_5:.4f}")
    print(f"Mean Recall@10: {recall_10:.4f}")
    print("="*60)
    
    # Save results
    results = {
        'mean_recall_at_5': float(recall_5),
        'mean_recall_at_10': float(recall_10),
        'num_queries': len(labeled_data),
        'predictions': predictions
    }
    
    output_file = "../data/evaluation_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to {output_file}")
    
    return results

if __name__ == "__main__":
    # Build index and evaluate
    print("Building search index...")
    db = build_index()
    
    print("\nStarting evaluation...")
    results = evaluate_on_train_set(db)
