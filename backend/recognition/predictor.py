import torch
from PIL import Image
from .model_loader import get_model, get_transform
from .label_mapper import map_label_to_keywords
from torchvision.models import EfficientNet_B0_Weights

def predict_product_from_path(processed_path: str) -> dict:
    """
    Given the path to a preprocessed image, returns a structured dictionary
    containing the top product category, keywords, and predictions.
    
    Args:
        processed_path (str): Absolute or relative path to the preprocessed image.
        
    Returns:
        dict: A dictionary containing 'category', 'keywords', 'confidence', 'top_predictions'
    """
    model = get_model()
    transform = get_transform()
    
    # EfficientNet_B0 default ImageNet mapping
    weights = EfficientNet_B0_Weights.IMAGENET1K_V1
    categories = weights.meta["categories"]
    
    # Step 1: Load image from processed path
    image = Image.open(processed_path).convert('RGB')
    
    # Step 2: Apply transform
    tensor = transform(image).unsqueeze(0)  # Add batch dimension
    
    # Step 3 & 4: Inference and Softmax
    with torch.no_grad():
        output = model(tensor)
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        
    # Step 5: Extract Top-5 predictions
    top_prob, top_catid = torch.topk(probabilities, 5)
    
    top_predictions = []
    for i in range(top_prob.size(0)):
        label = categories[top_catid[i].item()]
        score = float(top_prob[i].item())
        top_predictions.append({
            "label": label,
            "score": round(score, 4)
        })
        
    # Step 6: Map to ecommerce keywords
    top_label_raw = top_predictions[0]["label"]
    keywords = map_label_to_keywords(top_label_raw)
    
    # Return structured result
    return {
        "category": top_label_raw,
        "keywords": keywords,
        "confidence": top_predictions[0]["score"],
        "top_predictions": top_predictions
    }
