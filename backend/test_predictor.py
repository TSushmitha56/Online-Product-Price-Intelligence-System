import os
import sys
import json

# Setup environment to allow using Django and relative imports locally
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from recognition.predictor import predict_product_from_path
from api.models import Image

def test():
    # Find any processed image from DB
    img = Image.objects.exclude(processed_path__isnull=True).exclude(processed_path='').first()
    
    if not img:
        print("No processed images found in the database. Run the upload test first.")
        return
        
    print(f"Testing with image: {img.processed_path}")
    
    # Needs absolute path for PIL
    from django.conf import settings
    
    # Processed path is relative to MEDIA_ROOT ('preprocessed/...')
    # Assuming previously we did: image_instance.processed_path = processed_relative_path
    
    # Let's verify how it's stored
    abs_path = os.path.join(settings.MEDIA_ROOT, img.processed_path)
    print(f"Absolute path to test: {abs_path}")
    
    if not os.path.exists(abs_path):
        print("File does not exist.")
        return
        
    result = predict_product_from_path(abs_path)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test()
