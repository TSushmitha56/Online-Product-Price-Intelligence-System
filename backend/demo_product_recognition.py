"""
Demo script for product recognition module.

This demo uses the existing preprocessing pipeline in `image_preprocessing.py` and
runs a lightweight model for demonstration. For a full pretrained run, set
`weights='imagenet'` in `load_model` (requires TensorFlow and download of weights).
"""

from product_recognition_model import load_model, predict_product
from image_preprocessing import preprocess_image
import numpy as np
import argparse
import json


def run_demo(image_path: str, weights: str = None, num_classes: int = 5):
    # Preprocess
    img = preprocess_image(image_path, target_size=(224, 224))

    # Load model (weights=None to avoid large downloads in demo)
    model = load_model(num_classes=num_classes, model_name='MobileNetV2', weights=weights)

    # Predict
    result = predict_product(model, img, model_name='MobileNetV2')

    # Pretty print JSON result
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, required=False, default=None, help='Path to an image file to demo')
    parser.add_argument('--weights', type=str, default=None, help='Model weights (imagenet or None)')
    args = parser.parse_args()

    if args.image is None:
        # Create a random demo image using the preprocessing demo helper if available
        from PIL import Image
        demo_path = 'demo_product.jpg'
        img = Image.new('RGB', (800, 600), color=(150, 100, 200))
        img.save(demo_path)
        image_path = demo_path
    else:
        image_path = args.image

    run_demo(image_path, weights=args.weights)
