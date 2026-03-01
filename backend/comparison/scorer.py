def calculate_score(
    price: float,
    min_price_in_group: float,
    max_price_in_group: float,
    shipping_cost: float,
    seller_rating: float = None,
    price_weight: float = 0.6,
    shipping_weight: float = 0.2,
    rating_weight: float = 0.2
) -> float:
    """
    Computes a normalized score (0 to 100) for a product offer.
    A higher score indicates a better overall configuration (lower cost, higher rating).
    """
    if price is None or price <= 0:
        return 0.0
        
    # 1. Normalize Price (Lower is better, so we invert)
    # Avoid division by zero
    price_range = max_price_in_group - min_price_in_group
    if price_range == 0:
        # All items cost exactly the same
        norm_price_score = 1.0
    else:
        # scale from 0 to 1 where min_price gets 1.0 and max_price gets 0.0
        norm_price_score = 1.0 - ((price - min_price_in_group) / price_range)

    # 2. Normalize Shipping (Lower is better, e.g., 0 shipping = 1.0 score, >$20 = 0.0)
    # We'll treat $20+ as the maximum penalty out of simplicity
    max_shipping_cap = 20.0
    if shipping_cost <= 0:
        norm_shipping_score = 1.0
    elif shipping_cost >= max_shipping_cap:
        norm_shipping_score = 0.0
    else:
        norm_shipping_score = 1.0 - (shipping_cost / max_shipping_cap)

    # 3. Normalize Rating (0 to 5 scale -> 0.0 to 1.0)
    # If absent, we penalize slightly by assuming an average 3.0 (0.6 score)
    if seller_rating is None:
        norm_rating_score = 0.6
    else:
        norm_rating_score = min(max(seller_rating / 5.0, 0.0), 1.0)

    # Calculate final weighted score
    raw_score = (
        (price_weight * norm_price_score) +
        (shipping_weight * norm_shipping_score) +
        (rating_weight * norm_rating_score)
    )
    
    # Scale to 100
    return round(raw_score * 100, 2)

def extract_shipping_cost(shipping_str: str) -> float:
    """
    Attempts to extract a float shipping cost from a string like "Free shipping", "+$5.99 shipping"
    """
    if not shipping_str:
        return 0.0
        
    lower_str = shipping_str.lower()
    if "free" in lower_str:
        return 0.0
        
    import re
    # Look for dollar amounts
    matches = re.findall(r'\$?(\d+\.\d{2})', shipping_str)
    if matches:
        try:
            return float(matches[0])
        except ValueError:
            return 0.0
            
    return 0.0
