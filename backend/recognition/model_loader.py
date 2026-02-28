import torch
from torchvision import models, transforms
import logging

logger = logging.getLogger(__name__)

# Singleton pattern variable
_MODEL = None
_TRANSFORM = None


def get_model():
    """
    Returns the EfficientNet-B0 model loaded in eval mode.
    Only loads the model once (singleton).
    """
    global _MODEL
    
    if _MODEL is None:
        logger.info("Loading EfficientNet-B0 model...")
        warnings_filter = True # Ignore warnings 
        try:
            # Load pretrained EfficientNet-B0
            _MODEL = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1)
            # EfficientNet-B0 is lightweight and suitable for CPU
            _MODEL.eval()  # Set model to evaluation mode
            logger.info("Successfully loaded EfficientNet-B0")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise e
            
    return _MODEL


def get_transform():
    """
    Returns the standard ImageNet transformations required for EfficientNet-B0.
    """
    global _TRANSFORM
    
    if _TRANSFORM is None:
        # Standard PyTorch ImageNet transforms
        _TRANSFORM = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        
    return _TRANSFORM
