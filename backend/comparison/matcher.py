import re
from rapidfuzz import fuzz
from typing import List, Dict, Any

STOPWORDS = {"for", "with", "new", "the", "a", "an", "and", "or", "in", "on", "of", "at", "to", "by"}

def normalize_name(name: str) -> str:
    """
    Normalizes a product name by:
    - Lowercasing
    - Stripping punctuation
    - Removing common stopwords
    - Normalizing standard units (TB, GB, MB)
    """
    if not name:
        return ""
    
    # Lowercase
    name = name.lower()
    
    # Remove punctuation, but keep alphanumeric and spaces
    name = re.sub(r'[^\w\s]', ' ', name)
    
    # Normalize units
    name = re.sub(r'\b(\d+)\s*(tb|gb|mb)\b', r'\1\2', name)
    
    # Tokenize and remove stopwords
    tokens = name.split()
    filtered_tokens = [t for t in tokens if t not in STOPWORDS]
    
    # Rejoin
    return " ".join(filtered_tokens).strip()

def is_match(name1: str, name2: str, threshold: float = 85.0) -> bool:
    """
    Checks if two normalized names match using RapidFuzz.
    """
    if not name1 or not name2:
        return False
        
    score = fuzz.token_set_ratio(name1, name2)
    return score >= threshold

def group_products(products: List[Dict[str, Any]], query: str, threshold: float = 80.0) -> List[List[Dict[str, Any]]]:
    """
    Groups products that appear to be the same based on fuzzy string matching
    of their normalized titles against the query.
    
    For a single recognized product query, our primary grouping strategy is 
    comparing each product title directly to the intent query to determine
    if it's the requested product or an unrelated accessory.
    """
    normalized_query = normalize_name(query)
    
    matched_group = []
    
    for product in products:
        title = product.get("title", "")
        norm_title = normalize_name(title)
        
        # We group items if they match the query well enough
        if is_match(normalized_query, norm_title, threshold=threshold):
            product["normalized_name"] = norm_title
            matched_group.append(product)
            
    # For a robust engine, we essentially return chunks of matched clusters
    # Since we are typically querying 1 product at a time from recognition,
    # we return one big cluster for the valid matches.
    if matched_group:
         # List of clusters.
         # For more complex pipelines, you might do pairwise clustering.
         # We just cluster everything that aligns with the root query.
        return [matched_group]
    return []
