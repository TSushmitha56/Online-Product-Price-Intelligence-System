from typing import List, Dict, Any

def apply_filters(
    products: List[Dict[str, Any]], 
    min_rating: float = 0.0,
    must_be_in_stock: bool = False,
    max_shipping: float = None,
    min_price: float = 0.0,
    max_price: float = None
) -> List[Dict[str, Any]]:
    """
    Filters a list of products based on given criteria.
    Missing rating defaults to neutral evaluation (so we don't drop items with no rating).
    Missing shipping defaults to 0 treated as a flag in the algorithm later.
    """
    filtered = []
    
    for p in products:
        # Price: only drop items with an explicitly invalid price (zero or negative)
        # Allow None prices — means "See options" or price unavailable, still worth showing
        price = p.get('price')
        if price is not None:
            if price <= 0:
                continue
            if price < min_price:
                continue
            if max_price is not None and price > max_price:
                continue
            
        # Rating
        rating = p.get('rating')
        if rating is not None and rating < min_rating:
            continue
            
        # In stock
        if must_be_in_stock:
            avail = str(p.get('availability', '')).lower()
            if "out of stock" in avail or avail == "":
                 continue
                 
        # Shipping 
        shipping_cost = p.get('shipping_cost', 0.0)
        if max_shipping is not None and shipping_cost > max_shipping:
            continue
            
        filtered.append(p)
        
    return filtered
