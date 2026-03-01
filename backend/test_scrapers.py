import json
import logging
from scrapers import search_all_platforms

logging.basicConfig(level=logging.INFO)

def test_scrapers():
    query = "Sony Headphones WH-1000XM5"
    print(f"Executing cross-platform scraping for: {query}")
    
    results = search_all_platforms(query)
    
    print("\n" + "="*50)
    print(f"Results Found: {len(results)}")
    print("="*50)
    
    # Dump for validation check
    for r in results:
        print(json.dumps(r, indent=2))

if __name__ == "__main__":
    test_scrapers()
