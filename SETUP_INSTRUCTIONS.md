# 🚀 Project Setup Instructions

Complete development environment for Django Backend + React Frontend with Hello World examples.

## Prerequisites
- **Python 3.9+** (installed and in PATH)
- **Node.js 16+** (installed and in PATH)
- **Git** (optional, for version control)

---

## ✅ Backend Setup (Django)

### Step 1: Install Dependencies
```powershell
cd backend
pip install -r ../requirements.txt
```

### Step 2: Run Migrations
```powershell
python manage.py migrate
```

### Step 3: Start Django Server
```powershell
python manage.py runserver
```

✅ **Backend runs at:** `http://localhost:8000`
- Hello World API: `http://localhost:8000/api/hello/`
- Health Check: `http://localhost:8000/api/health/`

---

## ✅ Frontend Setup (React)

### Step 1: Install Dependencies
```powershell
cd frontend
npm install
```

### Step 2: Start React Development Server
```powershell
npm start
```

✅ **Frontend runs at:** `http://localhost:3000`
- Opens automatically in your browser
- Shows backend status directly on the page

---

## ✅ Version Control (Optional)

### Initialize Git Repository
```powershell
cd .. (go back to project root)
git init
git add .
git commit -m "Initial commit: Project setup"
```

---

## 📁 Project Structure

```
internship/
├── backend/
│   ├── config/
│   │   ├── settings.py       (Django settings with CORS)
│   │   ├── urls.py           (Main URL routing)
│   │   ├── asgi.py
│   │   └── wsgi.py
│   ├── api/
│   │   ├── views.py          (Hello World + Health Check endpoints)
│   │   ├── urls.py           (API endpoints routing)
│   │   ├── models.py
│   │   ├── admin.py
│   │   └── apps.py
│   ├── manage.py
│   ├── db.sqlite3            (Auto-created after migrations)
│   └── venv/                 (Virtual environment)
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.jsx           (Main React component)
│   │   ├── App.css           (Styling)
│   │   ├── index.js          (Entry point)
│   │   └── index.css
│   ├── package.json
│   └── node_modules/         (Auto-created after npm install)
│
├── requirements.txt          (Python dependencies)
└── .gitignore               (Git exclusions)
```

---

## 🔍 API Endpoints

### Hello World Endpoint
```
GET http://localhost:8000/api/hello/
Response:
{
  "message": "Hello World from Django!",
  "status": "success"
}
```

### Health Check Endpoint
```
GET http://localhost:8000/api/health/
Response:
{
  "status": "healthy",
  "service": "backend-api"
}
```

---

## 🛠️ Common Commands

### Backend
```powershell
# Run development server
python manage.py runserver

# Create superuser for admin panel
python manage.py createsuperuser

# Apply migrations
python manage.py migrate

# Make migrations
python manage.py makemigrations

# Access admin panel
# http://localhost:8000/admin/
```

### Frontend
```powershell
# Start dev server
npm start

# Build for production
npm build

# Run tests
npm test
```

---

## 🚨 Troubleshooting

### Python not found
- Ensure Python is installed: `python --version`
- Reinstall with "Add Python to PATH" checked

### npm not found
- Ensure Node.js is installed: `node --version`
- Restart terminal after installing

### Port already in use
- Backend (8000): `python manage.py runserver 8001`
- Frontend (3000): `PORT=3001 npm start`

### CORS errors
- Backend CORS is configured for `http://localhost:3000`
- If using different port, update `CORS_ALLOWED_ORIGINS` in `backend/config/settings.py`

---

## 📦 Dependencies

### Backend (Python)
- Django 4.2.7 - Web framework
- djangorestframework 3.14.0 - REST API
- django-cors-headers 4.3.1 - CORS support
- python-dotenv 1.0.0 - Environment variables

### Frontend (Node.js)
- React 18.2.0 - UI library
- react-dom 18.2.0 - React DOM rendering
- axios 1.6.0 - HTTP client
- react-scripts 5.0.1 - Build tools

---

## 🎯 Next Steps

1. ✅ Backend: Test `/api/hello/` and `/api/health/` endpoints in browser
2. ✅ Frontend: Verify React app loads and displays backend data
3. ✅ Git: Make your first commit
4. 📚 Add: Models, views, and components as needed
5. 🔐 Security: Change `SECRET_KEY` and `DEBUG=False` before production

---

## 💡 Tips

- Backend and frontend run independently; both must be running for full functionality
- Django debug toolbar helps with development (optional dependency)
- Use `Ctrl+C` to stop servers
- Check console for errors and logs

Happy coding! 🎉
