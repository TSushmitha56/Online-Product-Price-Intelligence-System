# Backend API Documentation

## Overview
This is a Django REST Framework backend API for the ImageHub application, providing image upload functionality with validation and storage.

## Setup Instructions

### Prerequisites
- Python 3.8+
- Virtual environment (already created)
- Django and Django REST Framework (already installed)

### Installation

1. **Navigate to the backend directory:**
```bash
cd backend
```

2. **Activate the virtual environment:**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install required packages (if not already installed):**
```bash
pip install django djangorestframework django-cors-headers Pillow
```

4. **Run migrations to create the database:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create a superuser (optional for Admin panel):**
```bash
python manage.py createsuperuser
```

6. **Start the development server:**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

---

## API Endpoints

### 1. Health Check
**Endpoint:** `GET /api/health/`

**Description:** Verify the backend service is running.

**Example Request:**
```bash
curl http://localhost:8000/api/health/
```

**Response:**
```json
{
  "status": "healthy",
  "service": "backend-api"
}
```

---

### 2. Hello World
**Endpoint:** `GET /api/hello/`

**Description:** Test endpoint to verify basic connectivity.

**Example Request:**
```bash
curl http://localhost:8000/api/hello/
```

**Response:**
```json
{
  "message": "Hello World from Django!",
  "status": "success"
}
```

---

### 3. Image Upload ⭐
**Endpoint:** `POST /api/upload-image/`

**Description:** Upload an image file with validation and storage.

**Request Method:** POST

**Request Headers:**
- `Content-Type`: multipart/form-data (automatic in most clients)

**Request Body:**
- `file` (required): Image file (JPEG, PNG, or WebP)

**File Requirements:**
- **Supported Formats:** 
  - `image/jpeg` (.jpg, .jpeg)
  - `image/png` (.png)
  - `image/webp` (.webp)
- **Maximum Size:** 10MB
- **Device:** You cannot upload files larger than 10MB

**Success Response (HTTP 201):**
```json
{
  "status": "success",
  "message": "Image uploaded successfully",
  "image_id": "20260217_550e8400e29b41d4a716446655440000",
  "filename": "20260217_550e8400e29b41d4a716446655440000.jpg",
  "original_filename": "my-photo.jpg",
  "file_size": 2048576,
  "file_size_mb": 1.95,
  "mime_type": "image/jpeg",
  "timestamp": "2026-02-17T15:30:45.123456Z"
}
```

**Error Response Examples:**

#### Missing File (HTTP 400):
```json
{
  "status": "error",
  "message": "No file provided. Please upload an image file."
}
```

#### Invalid File Type (HTTP 400):
```json
{
  "status": "error",
  "message": "Invalid file type: application/pdf. Allowed types: image/jpeg, image/png, image/webp"
}
```

#### File Too Large (HTTP 400):
```json
{
  "status": "error",
  "message": "File size (15.50MB) exceeds maximum limit (10MB)"
}
```

#### Server Error (HTTP 500):
```json
{
  "status": "error",
  "message": "An unexpected error occurred during upload. Please try again."
}
```

---

## Testing the API

### Using cURL

**1. Upload an image:**
```bash
curl -X POST http://localhost:8000/api/upload-image/ \
  -F "file=@/path/to/image.jpg"
```

**2. Upload with verbose output:**
```bash
curl -v -X POST http://localhost:8000/api/upload-image/ \
  -F "file=@/path/to/image.jpg"
```

### Using Python Requests

```python
import requests

# Upload image
with open('image.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:8000/api/upload-image/',
        files=files
    )
    print(response.json())
```

### Using Postman

1. **Create a new POST request**
2. **URL:** `http://localhost:8000/api/upload-image/`
3. **Body:**
   - Select "form-data"
   - Key: `file`
   - Type: Select "File"
   - Value: Choose your image file
4. **Click Send**

### Using the Frontend

The React frontend automatically integrates with this endpoint. Simply:
1. Open `http://localhost:5173/`
2. Go to the "Upload Your Image" section
3. Drag and drop an image or click "Browse Files"
4. Click the "Upload" button

---

## File Storage

### Storage Location
Uploaded images are stored in:
```
backend/media/images/YYYY/MM/DD/
```

Example:
```
backend/media/images/2026/02/17/20260217_550e8400e29b41d4a716446655440000.jpg
```

### Accessing Uploaded Images
During development, images are served at:
```
http://localhost:8000/media/images/2026/02/17/20260217_550e8400e29b41d4a716446655440000.jpg
```

---

## Project Structure

```
backend/
├── config/                    # Django project configuration
│   ├── settings.py           # Project settings (MEDIA_ROOT, etc.)
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI application
│   └── asgi.py              # ASGI application
│
├── api/                       # Main API app
│   ├── migrations/           # Database migrations
│   │   ├── 0001_initial.py  # Image model migration
│   │   └── __init__.py
│   ├── models.py             # Image model definition
│   ├── views.py              # API endpoint views
│   ├── urls.py               # API URL routing
│   ├── utils.py              # Utility functions (validation, storage)
│   ├── admin.py              # Django admin configuration
│   ├── apps.py               # App configuration
│   └── tests.py              # Unit tests
│
├── media/                     # User uploaded files (created after first upload)
│   └── images/
│       └── YYYY/MM/DD/      # Organized by date
│
├── venv/                      # Virtual environment
├── manage.py                  # Django management script
└── db.sqlite3                 # SQLite database
```

---

## Image Model

### Fields
- **id**: UUID primary key
- **image_id**: Unique string identifier (e.g., "20260217_550e8400e29b41d4a716446655440000")
- **original_filename**: Original filename from upload
- **stored_filename**: Filename as stored on disk
- **file**: ImageField - the actual image file
- **file_size**: Size in bytes
- **mime_type**: MIME type (e.g., "image/jpeg")
- **uploaded_at**: Timestamp of upload

### Access via Django Admin
1. Create a superuser: `python manage.py createsuperuser`
2. Visit: `http://localhost:8000/admin/`
3. Login with superuser credentials
4. View all uploaded images in the "Images" section

---

## Configuration

### Settings in `config/settings.py`

```python
# Maximum file size (10MB)
MAX_UPLOAD_SIZE = 10 * 1024 * 1024

# Allowed image extensions
ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'webp']

# Allowed MIME types
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp']

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# CORS configuration (allows requests from frontend)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

### Modifying Settings
To change upload limits or allowed formats, edit `backend/config/settings.py`:

```python
# Increase max size to 50MB
MAX_UPLOAD_SIZE = 50 * 1024 * 1024

# Add more allowed formats
ALLOWED_IMAGE_TYPES = [
    'image/jpeg',
    'image/png',
    'image/webp',
    'image/gif',  # Add GIF support
]
```

---

## Error Handling

The API returns appropriate HTTP status codes:

| Status Code | Meaning | Example |
|------------|---------|---------|
| 200 | Success | Health check passed |
| 201 | Created | Image uploaded successfully |
| 400 | Bad Request | Missing file, invalid format, file too large |
| 500 | Server Error | Unexpected error during processing |

---

## Security Considerations

1. **File Validation**: All uploads are validated for file type and size
2. **MIME Type Checking**: Uses file's content-type, not just extension
3. **CORS Configuration**: Only allows requests from approved origins
4. **Unique Naming**: Files are renamed with UUIDs to prevent overwrites
5. **Date-based Organization**: Files organized by upload date for manageability

---

## Integration with Frontend

The frontend React component automatically:
1. Accepts drag-and-drop files
2. Validates file types locally
3. Shows preview before upload
4. Sends to `/api/upload-image/` endpoint
5. Displays upload status and image metadata
6. Handles errors gracefully

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'PIL'"
**Solution:** Install Pillow
```bash
pip install Pillow
```

### Issue: CORS errors from frontend
**Solution:** Ensure frontend URL is in `CORS_ALLOWED_ORIGINS` in settings.py

### Issue: "No such table" error
**Solution:** Run migrations
```bash
python manage.py migrate
```

### Issue: Media files not serving
**Solution:** Ensure `DEBUG = True` in settings.py (for development only)

---

## Production Deployment

For production:
1. Set `DEBUG = False` in settings.py
2. Configure static file serving (nginx, CloudFront, etc.)
3. Use cloud storage (AWS S3, Google Cloud Storage) for media files
4. Set proper ALLOWED_HOSTS
5. Use environment variables for sensitive data
6. Implement proper logging and monitoring

---

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review API response error messages
3. Check Django logs: `python manage.py runserver` output
4. Verify backend is running: `curl http://localhost:8000/api/health/`
