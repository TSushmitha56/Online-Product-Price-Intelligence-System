import requests
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from api.models import Image

def test():
    img = Image.objects.exclude(processed_path__isnull=True).exclude(processed_path='').first()
    if not img:
        print("Upload an image first")
        return
        
    url = "http://127.0.0.1:8000/api/recognize-product/"
    payload = {"image_id": img.image_id}
    
    response = requests.post(url, json=payload)
    print("Status:", response.status_code)
    print("Raw Text:", response.text)
    
    try:
        print("Data:", response.json())
    except:
        pass
    
if __name__ == "__main__":
    test()
