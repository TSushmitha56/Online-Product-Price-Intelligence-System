# ImageHub - Backend API Quick Start Guide

## 🚀 Quick Setup

### 1. Start Backend Server
```bash
cd backend
# Activate virtual environment (Windows)
venv\Scripts\activate

# Start Django server
python manage.py runserver
```
✅ Backend runs at: `http://localhost:8000`

### 2. Start Frontend Server
```bash
cd frontend
npm run dev
```
✅ Frontend runs at: `http://localhost:5173`

---

## 📤 API Endpoint Summary

### Image Upload
**POST** `/api/upload-image/`

**Quick Test with cURL:**
```bash
curl -X POST http://localhost:8000/api/upload-image/ \
  -F "file=@image.jpg"
```

**Expected Success Response (201):**
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

---

## ✅ File Requirements

| Requirement | Value |
|---|---|
| Allowed Formats | JPEG, PNG, WebP |
| Maximum Size | 10 MB |
| Min Size | No minimum |

---

## 🗂️ Uploaded Files Storage

Files are stored at:
```
backend/media/images/YYYY/MM/DD/
```

Example path:
```
backend/media/images/2026/02/17/20260217_550e8400e29b41d4a716446655440000.jpg
```

Access uploaded files at:
```
http://localhost:8000/media/images/2026/02/17/20260217_550e8400e29b41d4a716446655440000.jpg
```

---

## 🧪 Testing the API

### Using Python
```python
import requests

# Upload file
with open('image.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/upload-image/',
        files={'file': f}
    )
    print(response.json())
```

### Using Postman
1. Create POST request to: `http://localhost:8000/api/upload-image/`
2. Go to **Body** → **form-data**
3. Key: `file`, Type: `File`, Value: Select your image
4. Click **Send**

### Using Frontend
1. Open `http://localhost:5173/`
2. Drag and drop an image or click "Browse Files"
3. Click "Upload" button
4. See upload status and image metadata

---

## 📊 Admin Panel

View all uploaded images:

1. Create superuser:
```bash
python manage.py createsuperuser
```

2. Visit: `http://localhost:8000/admin/`

3. Login and navigate to **Images** section

---

## 🔧 Troubleshooting

| Issue | Solution |
|---|---|
| Pillow not installed | Run: `pip install Pillow` |
| CORS errors | Check `CORS_ALLOWED_ORIGINS` in `settings.py` |
| No database tables | Run: `python manage.py migrate` |
| Files not serving | Enable: `DEBUG = True` in `settings.py` |

---

## 📁 Project Structure

```
backend/
├── media/              # Uploaded images
│   └── images/
├── api/                # API app
│   ├── models.py       # Image model
│   ├── views.py        # Upload endpoint
│   ├── utils.py        # Validation & storage
│   └── urls.py         # Routes
├── config/             # Django config
│   └── settings.py     # Upload limits
└── manage.py

frontend/
├── src/
│   ├── components/
│   │   ├── ImageUpload.jsx  # Upload UI
│   │   ├── Header.jsx
│   │   └── Footer.jsx
│   ├── App.jsx
│   └── main.jsx
└── package.json
```

---

## ⚙️ Configuration

Edit `backend/config/settings.py` to customize:

```python
# Max file size (currently 10MB)
MAX_UPLOAD_SIZE = 10 * 1024 * 1024

# Allowed formats (currently JPEG, PNG, WebP)
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp']

# Add more if needed
ALLOWED_IMAGE_TYPES = [
    'image/jpeg',
    'image/png',
    'image/webp',
    'image/gif',  # Add GIF
]
```

---

## 📝 API Response Codes

| Code | Meaning | Example |
|---|---|---|
| 200 | OK | Health check passed |
| 201 | Created | Image uploaded ✅ |
| 400 | Bad Request | Invalid file, too large |
| 500 | Server Error | Unexpected error |

---

## 🛡️ Features

✅ File type validation (MIME type checking)
✅ File size validation (10MB max)
✅ Unique image identifiers (UUID-based)
✅ Date-based file organization
✅ CORS enabled for frontend
✅ Comprehensive error messages
✅ Admin panel for image management
✅ RESTful API design
✅ Responsive frontend with preview
✅ Drag-and-drop support

---

## 📚 Full Documentation

See [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) for complete API reference.

---

## 🚦 Status Indicators

### Backend Health
```bash
curl http://localhost:8000/api/health/
```

### Frontend Running
Visit `http://localhost:5173/` in browser

---

## 💡 Quick Test

1. **Start both servers** (backend and frontend)
2. **Open browser** to `http://localhost:5173/`
3. **Upload an image**:
   - Drag image into upload area OR
   - Click "Browse Files"
   - See preview
   - Click "Upload"
4. **Check response** with image ID and details
5. **Verify file stored** at `backend/media/images/YYYY/MM/DD/`

---

**Need help?** Check the troubleshooting section or see API_DOCUMENTATION.md for detailed information.
