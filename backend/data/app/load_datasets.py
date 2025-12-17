import pandas as pd
import json
import os
from typing import Dict, List

def load_excel_dataset(file_path: str) -> Dict[str, pd.DataFrame]:
    """
    Load the Gen_AI Dataset.xlsx file containing train and test sets.
    
    Returns:
        Dictionary with 'train' and 'test' DataFrames
    """
    print(f"Loading dataset from {file_path}...")
    
    # Load both sheets
    excel_file = pd.ExcelFile(file_path)
    datasets = {}
    
    # Expected sheet names based on the assignment
    sheet_mapping = {
        'Train-Set': 'train',
        'Test-Set': 'test'
    }
    
    for sheet_name, key in sheet_mapping.items():
        if sheet_name in excel_file.sheet_names:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            # Clean the dataframe
            df = df.dropna(subset=['Query'])  # Remove rows with no query
            datasets[key] = df
            print(f"Loaded {len(df)} queries from {sheet_name}")
        else:
            print(f"Warning: Sheet '{sheet_name}' not found in Excel file")
    
    return datasets

def parse_train_set(train_df: pd.DataFrame) -> List[Dict]:
    """
    Parse the labeled train set into a structured format.
    
    Expected format: Query | Relevant Assessments (URLs or names)
    """
    labeled_data = []
    
    for idx, row in train_df.iterrows():
        query = row['Query']
        
        # Parse relevant assessments (might be comma-separated or in multiple columns)
        relevant_assessments = []
        
        # Try different column patterns
        for col in train_df.columns:
            if 'assessment' in col.lower() or 'url' in col.lower() or 'relevant' in col.lower():
                if pd.notna(row[col]):
                    # Handle comma-separated values
                    if isinstance(row[col], str):
                        assessments = [a.strip() for a in row[col].split(',')]
                        relevant_assessments.extend(assessments)
                    else:
                        relevant_assessments.append(str(row[col]))
        
        labeled_data.append({
            'query': query,
            'relevant_assessments': relevant_assessments
        })
    
    return labeled_data

def get_test_queries(test_df: pd.DataFrame) -> List[str]:
    """
    Extract queries from the test set.
    """
    return test_df['Query'].tolist()

if __name__ == "__main__":
    # Test loading
    dataset_path = "../data/Gen_AI Dataset.xlsx"
    datasets = load_excel_dataset(dataset_path)
    
    if 'train' in datasets:
        labeled = parse_train_set(datasets['train'])
        print(f"\nProcessed {len(labeled)} labeled training examples")
        print(f"Example: {labeled[0]}")
    
    if 'test' in datasets:
        test_queries = get_test_queries(datasets['test'])
        print(f"\nProcessed {len(test_queries)} test queries")
        print(f"Example: {test_queries[0]}")
