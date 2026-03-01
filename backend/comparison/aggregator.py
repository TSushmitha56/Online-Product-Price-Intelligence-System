from typing import List, Dict, Any
from scrapers.base_scraper import Product
from .matcher import normalize_name, is_match
from .filters import apply_filters
from .scorer import calculate_score, extract_shipping_cost

def aggregate_prices(
    product_query: str, 
    sources: List[List[Product]],
    min_rating: float = 0.0,
    max_price: float = None
) -> Dict[str, Any]:
    """
    Aggregates scraped products, normalizes, scores, and outputs the structured comparison JSON.
    """
    
    # 1. Flatten all sources into one big list
    all_products = []
    for source_list in sources:
        all_products.extend(source_list)
        
    # 2. Add raw 'shipping_cost' floats for the scoring algorithm
    for p in all_products:
        p['shipping_cost'] = extract_shipping_cost(p.get('shipping', ''))
        
    # 3. Apply general filters (e.g. drop bad ratings, drop negative prices)
    filtered_products = apply_filters(
        all_products, 
        min_rating=min_rating, 
        max_price=max_price
    )
    
    if not filtered_products:
        return {
            "query": product_query,
            "matched_products": []
        }

    # 4. Group matches by normalized query
    normalized_query = normalize_name(product_query)
    
    matched_group = []
    for p in filtered_products:
        title = p.get('title', '')
        # Only accept if the title fuzzy matches the original intended product query
        if is_match(normalized_query, normalize_name(title), threshold=70.0):
            matched_group.append(p)
            
    if not matched_group:
         return {
            "query": product_query,
            "matched_products": []
        }

    # 5. Calculate statistics for the matched group
    prices = [p['price'] for p in matched_group if p.get('price') is not None]
    
    if not prices:
        return {"query": product_query, "matched_products": []}
        
    lowest_price = min(prices)
    highest_price = max(prices)
    average_price = round(sum(prices) / len(prices), 2)
    
    # 6. Score all listings in the group
    scored_offers = []
    for p in matched_group:
        score = calculate_score(
            price=p['price'],
            min_price_in_group=lowest_price,
            max_price_in_group=highest_price,
            shipping_cost=p.get('shipping_cost', 0.0),
            seller_rating=p.get('rating')
        )
        p['comparison_score'] = score
        scored_offers.append(p)
        
    # 7. Sort by score descending
    scored_offers.sort(key=lambda x: x['comparison_score'], reverse=True)
    
    # Identify the best individual offers
    best_overall = scored_offers[0]
    
    # lowest price (guaranteed to be min(prices))
    lowest_offer = next((o for o in scored_offers if o['price'] == lowest_price), None)
    
    # Generate Output JSON Structure
    output = {
        "query": product_query,
        "matched_products": [
            {
                "normalized_name": normalized_query,
                "price_stats": {
                    "lowest": lowest_price,
                    "highest": highest_price,
                    "average": average_price,
                    "count": len(prices)
                },
                "best_overall_offer": {
                    "store": best_overall.get('platform'),
                    "price": best_overall.get('price'),
                    "shipping": best_overall.get('shipping_cost'),
                    "seller_rating": best_overall.get('rating'),
                    "product_url": best_overall.get('product_url'),
                    "score": best_overall.get('comparison_score')
                },
                "lowest_price_offer": {
                     "store": lowest_offer.get('platform'),
                     "price": lowest_offer.get('price'),
                     "product_url": lowest_offer.get('product_url')
                } if lowest_offer else None,
                "offers": scored_offers
            }
        ]
    }
    
    return output
