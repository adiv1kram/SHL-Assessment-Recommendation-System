import re
from typing import List, Union

def clean_text(text: str) -> str:
    """
    Normalizes text for embedding generation.
    Removes special characters and extra whitespace to improve vector quality.
    """
    if not text:
        return ""
    # Remove HTML tags if any leaked through
    text = re.sub(r'<[^>]+>', '', text)
    # Remove non-alphanumeric characters (preserving spaces)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()

def extract_duration(duration_str: Union[str, int]) -> int:
    """
    Parses duration string to integer minutes.
    Example: "Approx 30 mins" -> 30
    """
    if isinstance(duration_str, int):
        return duration_str
        
    if not duration_str:
        return 0
        
    # Extract first sequence of digits
    match = re.search(r'(\d+)', str(duration_str))
    if match:
        return int(match.group(1))
    return 0

def normalize_yes_no(value: str) -> str:
    """
    Standardizes boolean-like strings to strict 'Yes'/'No' format[cite: 183].
    """
    if not value:
        return "No"
    
    val_lower = value.lower().strip()
    if val_lower in ['yes', 'true', 'y', 'adaptive', 'remote']:
        return "Yes"
    return "No"

def format_test_type(test_types: Union[str, List[str]]) -> List[str]:
    """
    Ensures test_type is always a list of strings.
    """
    if isinstance(test_types, list):
        return [t.strip() for t in test_types if t]
    
    if isinstance(test_types, str):
        # Handle comma-separated strings
        return [t.strip() for t in test_types.split(',') if t.strip()]
        
    return ["General"]