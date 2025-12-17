import pandas as pd
import requests
import csv
import sys
import os

# Configuration
DATASET_PATH = "../backend/data/Gen_AI Dataset.xlsx"
API_URL = "http://localhost:8000/recommend"
OUTPUT_FILE = "submission.csv"

def generate_submission_csv():
    """
    Generate submission CSV from test set predictions.
    Format: Query | Assessment_url
    """
    print("="*60)
    print("GENERATING SUBMISSION CSV")
    print("="*60)
    
    # Load Test Set
    try:
        df = pd.read_excel(DATASET_PATH, sheet_name='Test-Set')
        print(f"\nLoaded {len(df)} test queries from dataset")
    except FileNotFoundError:
        print(f"Error: Dataset file not found at {DATASET_PATH}")
        print("Please ensure Gen_AI Dataset.xlsx exists in backend/data/")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        sys.exit(1)
    
    # Create CSV with proper format
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Query", "Assessment_url"])
        
        for index, row in df.iterrows():
            query_text = row['Query']
            
            print(f"\nProcessing query {index + 1}/{len(df)}:")
            print(f"  {query_text[:80]}...")
            
            try:
                response = requests.post(API_URL, json={"query": query_text}, timeout=30)
                
                if response.status_code == 200:
                    recs = response.json()['recommended_assessments']
                    
                    # Write one row per recommendation (as per submission format)
                    for rec in recs:
                        writer.writerow([query_text, rec['url']])
                    
                    print(f"  ✓ Generated {len(recs)} recommendations")
                else:
                    print(f"  ✗ API error: HTTP {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                print(f"  ✗ Connection error: Is the backend running at {API_URL}?")
                sys.exit(1)
            except Exception as e:
                print(f"  ✗ Failed: {e}")
    
    print("\n" + "="*60)
    print(f"✓ Submission CSV generated: {OUTPUT_FILE}")
    print("="*60)

if __name__ == "__main__":
    generate_submission_csv()