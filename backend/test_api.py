"""
ImageHub - API Test Script
Tests the backend API endpoints and image upload functionality.

Usage:
    python test_api.py

Requirements:
    - Backend running at http://localhost:8000
    - Requests library: pip install requests
"""

import requests
import os
import json
from pathlib import Path

# Configuration
BACKEND_URL = "http://localhost:8000"
API_BASE = f"{BACKEND_URL}/api"

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def test_backend_connection():
    """Test if backend is running"""
    print("\n" + "="*60)
    print("TEST 1: Backend Connection")
    print("="*60)
    
    try:
        response = requests.get(f"{API_BASE}/health/", timeout=5)
        if response.status_code == 200:
            print_success("Backend is running")
            print(f"Response: {response.json()}")
            return True
        else:
            print_error(f"Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to backend at http://localhost:8000")
        print_warning("Make sure backend is running: python manage.py runserver")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_hello_endpoint():
    """Test the hello world endpoint"""
    print("\n" + "="*60)
    print("TEST 2: Hello World Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{API_BASE}/hello/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success("Hello endpoint works")
            print(f"Message: {data.get('message')}")
            print(f"Status: {data.get('status')}")
            return True
        else:
            print_error(f"Hello endpoint returned status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_upload_no_file():
    """Test upload endpoint with no file"""
    print("\n" + "="*60)
    print("TEST 3: Upload Without File (Should Fail)")
    print("="*60)
    
    try:
        response = requests.post(f"{API_BASE}/upload-image/", timeout=5)
        if response.status_code == 400:
            data = response.json()
            print_success("Correctly rejected request without file")
            print(f"Error message: {data.get('message')}")
            return True
        else:
            print_warning(f"Expected 400, got {response.status_code}")
            print(f"Response: {response.json()}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def create_test_image():
    """Create a small test image for upload testing"""
    print("\n" + "="*60)
    print("SETUP: Creating Test Image")
    print("="*60)
    
    try:
        from PIL import Image
        
        # Create a simple 100x100 test image
        img = Image.new('RGB', (100, 100), color='red')
        img_path = Path('test_image.jpg')
        img.save(img_path, 'JPEG')
        
        file_size = img_path.stat().st_size
        print_success(f"Test image created: test_image.jpg ({file_size} bytes)")
        return str(img_path)
    except ImportError:
        print_warning("PIL/Pillow not available, using pre-existing image")
        return None
    except Exception as e:
        print_error(f"Could not create test image: {str(e)}")
        return None

def test_upload_with_file(image_path):
    """Test image upload with a real file"""
    print("\n" + "="*60)
    print("TEST 4: Image Upload with File")
    print("="*60)
    
    if not os.path.exists(image_path):
        print_error(f"Test image not found: {image_path}")
        print_warning("Skipping upload test")
        return False
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f"{API_BASE}/upload-image/",
                files=files,
                timeout=10
            )
        
        if response.status_code == 201:
            data = response.json()
            print_success("Image uploaded successfully!")
            print("\nUpload Details:")
            print(f"  Status: {data.get('status')}")
            print(f"  Image ID: {data.get('image_id')}")
            print(f"  Filename: {data.get('filename')}")
            print(f"  Original: {data.get('original_filename')}")
            print(f"  Size: {data.get('file_size_mb')} MB")
            print(f"  Type: {data.get('mime_type')}")
            print(f"  Timestamp: {data.get('timestamp')}")
            
            # Check if file exists locally
            stored_filename = data.get('filename')
            print(f"\n✓ File should be stored at:")
            print(f"  backend/media/images/YYYY/MM/DD/{stored_filename}")
            
            return True
        else:
            print_error(f"Upload failed with status {response.status_code}")
            print(f"Response: {response.json()}")
            return False
    except Exception as e:
        print_error(f"Error during upload: {str(e)}")
        return False

def test_upload_large_file():
    """Test upload with file exceeding size limit"""
    print("\n" + "="*60)
    print("TEST 5: Upload File Too Large (Should Fail)")
    print("="*60)
    
    try:
        # Create a file larger than 10MB (using PIL if available)
        try:
            from PIL import Image
            img = Image.new('RGB', (5000, 5000), color='blue')
            img_path = Path('large_test_image.jpg')
            img.save(img_path, 'JPEG', quality=95)
        except:
            print_warning("Could not create large test image, creating with binary data")
            img_path = Path('large_test_image.jpg')
            with open(img_path, 'wb') as f:
                f.write(b'JPEG_HEADER' * (12 * 1024 * 1024))  # ~120MB of data
        
        file_size = img_path.stat().st_size / (1024 * 1024)
        print_info(f"Test file size: {file_size:.2f} MB")
        
        with open(img_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f"{API_BASE}/upload-image/",
                files=files,
                timeout=10
            )
        
        # Clean up
        img_path.unlink()
        
        if response.status_code == 400:
            data = response.json()
            print_success("Correctly rejected oversized file")
            print(f"Error message: {data.get('message')}")
            return True
        else:
            print_warning(f"Expected 400, got {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("ImageHub - API Test Suite")
    print("="*60)
    
    results = {}
    
    # Test 1: Backend connection
    results['Backend Connection'] = test_backend_connection()
    
    if not results['Backend Connection']:
        print_error("Cannot continue - backend is not running")
        return results
    
    # Test 2: Hello endpoint
    results['Hello Endpoint'] = test_hello_endpoint()
    
    # Test 3: Upload without file
    results['Upload No File'] = test_upload_no_file()
    
    # Test 4: Upload with file
    image_path = create_test_image()
    if image_path:
        results['Upload with File'] = test_upload_with_file(image_path)
    
    # Test 5: Upload large file
    results['Large File Rejection'] = test_upload_large_file()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_status in results.items():
        status = "✅ PASS" if passed_status else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print_success("All tests passed! 🎉")
    else:
        print_warning(f"{total - passed} test(s) failed")
    
    return results

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
