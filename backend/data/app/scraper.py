import requests
from bs4 import BeautifulSoup
import json
import time
import re
import os
from .utils import clean_text, extract_duration, normalize_yes_no, format_test_type

# Configuration
BASE_URL = "https://www.shl.com/solutions/products/product-catalog/"
OUTPUT_FILE = "../data/shl_catalog.json"
MIN_REQUIRED_ITEMS = 377

def get_soup(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return None

def scrape_details(product_url):
    """
    Deep crawl of a specific assessment page to get metadata.
    """
    soup = get_soup(product_url)
    if not soup:
        return {}

    details = {
        "description": "No description available.",
        "duration": 0,
        "test_type": ["General"],
        "adaptive_support": "No",
        "remote_support": "Yes" # Defaulting to Yes as most SHL tests are remote
    }

    # Scrape Description
    # (Selectors based on common SHL page structures - may need adjustment if site updates)
    desc_tag = soup.find('div', class_='product-description') or soup.find('div', class_='content-block')
    if desc_tag:
        details['description'] = desc_tag.get_text(strip=True)

    # Scrape Metadata Table/List
    # SHL often lists these in a sidebar or specific list format
    # We look for keywords since classes change
    text_content = soup.get_text(" ", strip=True)
    
    # Extract Duration
    # Regex for "X mins" or "X minutes"
    dur_match = re.search(r'(\d+)\s*min', text_content, re.IGNORECASE)
    if dur_match:
        details['duration'] = int(dur_match.group(1))

    # Extract Test Type (e.g., "Test Type: K, P")
    # SHL mapping: K=Knowledge, P=Personality, A=Ability
    if "Test Type" in text_content:
        # Heuristic extraction
        type_section = text_content.split("Test Type")[1].split("Remote")[0]
        types = []
        if "K" in type_section: types.append("Knowledge & Skills")
        if "P" in type_section: types.append("Personality & Behavior")
        if "A" in type_section: types.append("Ability & Aptitude")
        if "S" in type_section: types.append("Simulations")
        if types:
            details['test_type'] = types

    # Extract Adaptive
    if "Adaptive" in text_content:
        details['adaptive_support'] = "Yes"

    return details

def run_scraper():
    print("Starting SHL Catalog Scraper...")
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    products = []
    seen_urls = set()
    page = 1
    
    # Pagination loop
    while True:
        print(f"Scraping Page {page}...")
        url = f"{BASE_URL}?page={page}"
        soup = get_soup(url)
        
        if not soup:
            break
            
        # Find product links. 
        # Selector assumes generic anchor tags inside catalog list items.
        # You may need to inspect the live site for exact class, e.g., 'a.product-link'
        links = soup.find_all('a', href=True)
        found_on_page = 0
        
        for link in links:
            href = link['href']
            title = link.get_text(strip=True)
            
            # Filter: Must be a product view url and NOT pre-packaged
            if "/product-catalog/view/" in href and title:
                full_url = href if href.startswith("http") else f"https://www.shl.com{href}"
                
                if full_url in seen_urls:
                    continue
                    
                # Constraint: Ignore "Pre-packaged Job Solutions"
                # This is often filtered by checking the category text or URL patterns
                if "job-solution" in full_url or "packaged" in title.lower():
                    continue

                seen_urls.add(full_url)
                
                # Fetch details
                details = scrape_details(full_url)
                
                product = {
                    "name": title,
                    "url": full_url,
                    "description": details['description'],
                    "duration": details['duration'],
                    "test_type": details['test_type'],
                    "adaptive_support": details['adaptive_support'],
                    "remote_support": details['remote_support']
                }
                
                products.append(product)
                found_on_page += 1
                
                # Politeness delay
                time.sleep(0.2)
        
        if found_on_page == 0:
            print("No more products found. Stopping.")
            break
            
        page += 1
        print(f"Total collected: {len(products)}")
        if len(products) >= MIN_REQUIRED_ITEMS + 50: # Buffer
            break

    # Save to JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2)
    
    print(f"Scraping complete. {len(products)} items saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    run_scraper()