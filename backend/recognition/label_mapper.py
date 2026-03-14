"""
Maps standard ImageNet class labels (IDs) to ecommerce-friendly keywords.
ImageNet has 1000 classes. We map common product categories found in ImageNet.
"""

# A dictionary mapping raw ImageNet class strings to ecommerce keywords.
# Key: A substring or full string of the ImageNet class label.
# Value: List of relevant keywords.
LABEL_MAP = {
    "running shoe": ["running shoe", "sports shoe", "sneaker", "athletic footwear"],
    "shoe": ["shoe", "footwear"],
    "sandal": ["sandal", "summer shoe", "footwear"],
    "handbag": ["bag", "handbag", "purse", "accessory"],
    "backpack": ["backpack", "bag", "school bag", "travel bag"],
    "purse": ["bag", "handbag", "purse", "accessory"],
    "wallet": ["wallet", "leather accessory", "money clip"],
    "water bottle": ["bottle", "water bottle", "flask", "hydration"],
    "nipple": ["baby bottle", "bottle"],  # ImageNet oddity
    "sunglasses": ["sunglasses", "eyewear", "shades", "accessory"],
    "cellular telephone": ["smartphone", "phone", "mobile phone", "electronics"],
    "dial telephone": ["phone", "telephone", "electronics"],
    "laptop": ["laptop", "computer", "notebook", "electronics"],
    "desktop computer": ["computer", "desktop PC", "electronics"],
    "mouse": ["computer mouse", "accessory", "electronics"],
    "monitor": ["computer monitor", "screen", "display"],
    "watch": ["watch", "wristwatch", "timepiece", "accessory"],
    "digital watch": ["watch", "smartwatch", "digital timepiece"],
    "analog clock": ["clock", "wall clock", "timepiece"],
    "wall clock": ["clock", "wall clock"],
    "t-shirt": ["t-shirt", "shirt", "apparel", "clothing"],
    "jersey": ["jersey", "shirt", "sportswear", "clothing"],
    "suit": ["suit", "formal wear", "clothing", "apparel"],
    "cloak": ["cloak", "coat", "outerwear"],
    "cardigan": ["cardigan", "sweater", "outerwear", "clothing"],
    "abaya": ["dress", "clothing", "apparel"],
    "ipod": ["mp3 player", "electronics", "audio player"],
    "perfume": ["perfume", "fragrance", "cologne", "beauty"],
    "lotion": ["lotion", "skincare", "beauty"],
    "lipstick": ["lipstick", "makeup", "cosmetics", "beauty"],
    "hair spray": ["hair spray", "hair care", "beauty"],
    "pill bottle": ["medicine bottle", "bottle", "health"],
    "coffee mug": ["mug", "cup", "drinkware"],
    "cup": ["cup", "drinkware"],
    "plate": ["plate", "dishware"],
    "frying pan": ["pan", "cookware", "kitchen"],
    "sofa": ["sofa", "couch", "furniture"],
    "studio couch": ["sofa", "couch", "furniture"],
    "folding chair": ["chair", "furniture"],
    "table lamp": ["lamp", "lighting", "home decor"],
    "lampshade": ["lamp", "lighting"],
    "television": ["tv", "television", "electronics", "screen"],
    "acoustic guitar": ["guitar", "musical instrument", "acoustic"],
    "electric guitar": ["guitar", "musical instrument", "electric"],
    "microphone": ["microphone", "audio equipment", "electronics"],
    "camera": ["camera", "photography", "digital camera", "electronics"],
    "reflex camera": ["camera", "dslr", "photography", "electronics"],
    "polaroid camera": ["camera", "instant camera", "photography"],
    "bicycle": ["bicycle", "bike", "sports", "transport"],
    "mountain bike": ["mountain bike", "bicycle", "sports"],
    "sports car": ["car", "vehicle"],
    "passenger car": ["car", "vehicle"],
    "minivan": ["car", "van", "vehicle"],
    "toys": ["toy", "children", "game"],
    "teddy": ["teddy bear", "plush toy", "children"],
    "book": ["book", "reading", "literature"],
    "comic book": ["comic", "book", "entertainment"],
}

# ImageNet classes often return multiple comma separated words
# e.g., "running shoe, sneaker" or "cellular telephone, cellular phone, cellphone, cell, mobile phone"

def map_label_to_keywords(label: str) -> list[str]:
    """
    Takes a raw ImageNet class label and tries to match it to our e-commerce mapping.
    
    Args:
        label (str): The raw ImageNet label.
        
    Returns:
        List[str]: A list of relevant e-commerce keywords.
    """
    label_lower = label.lower()
    
    # 1. Split by comma and check individual sub-labels
    sub_labels = [s.strip() for s in label_lower.split(',')]
    
    keywords = []
    
    for sub in sub_labels:
        # Check direct match
        if sub in LABEL_MAP:
            keywords.extend(LABEL_MAP[sub])
            
        # Check partial match as fallback
        else:
            for key, mapped_words in LABEL_MAP.items():
                if key in sub or sub in key:
                    keywords.extend(mapped_words)

    # If no mapping was found, at least return the clean sub-labels
    if not keywords:
        keywords.extend(sub_labels)
        
    # Deduplicate and remove empty strings
    return list(dict.fromkeys(filter(None, keywords)))

