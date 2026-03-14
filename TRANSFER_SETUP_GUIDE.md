# 🚀 PriceIntel – Project Transfer & Setup Guide

This guide explains how to set up and run the **Online Product Price Intelligence System (PriceIntel)** on a new laptop from scratch.

---

## 📦 Tech Stack

| Layer    | Technology                          |
|----------|-------------------------------------|
| Backend  | Python 3.11+, Django 4.2, DRF, SQLite |
| Frontend | Node.js 18+, React 19, Vite 7, Tailwind CSS |
| Scrapers | BeautifulSoup / Requests / Selenium |

---

## 🖥️ Prerequisites (Install These First on the New Laptop)

### 1. Python 3.11 or higher
- Download from: https://www.python.org/downloads/
- ✅ During install, check **"Add Python to PATH"**
- Verify: `python --version`

### 2. Node.js 18 or higher (includes npm)
- Download from: https://nodejs.org/en/download/
- Choose **LTS version**
- Verify: `node --version` and `npm --version`

### 3. Git (to clone or receive the project)
- Download from: https://git-scm.com/downloads
- Verify: `git --version`

---

## 📁 Step 1: Get the Project Files

**Option A – Copy from USB/Drive:**
Copy the entire `internship/` project folder to the new laptop (e.g., `C:\Users\YourName\internship`).

> ⚠️ Do NOT copy the `.venv`, `venv`, `dt_venv`, or `node_modules` folders — they are machine-specific and will be recreated below.

**Option B – From GitHub (if pushed):**
```bash
git clone https://github.com/TSushmitha56/Online-Product-Price-Intelligence-System.git
cd Online-Product-Price-Intelligence-System
```

---

## ⚙️ Step 2: Set Up the Backend (Django / Python)

Open a terminal (PowerShell or Command Prompt) and navigate to the project root.

```powershell
# Go to the backend folder
cd path\to\internship\backend

# Create a fresh virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Install all Python dependencies
pip install -r requirements.txt
```

### Configure Environment Variables

```powershell
# Still inside backend/
copy .env.example .env
```

Now open `backend\.env` in Notepad and set at minimum:

```env
DEBUG=True
SECRET_KEY=any-random-string-you-make-up-keep-it-secret
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=          # Leave empty to use SQLite (recommended for dev)
REDIS_URL=             # Leave empty if you don't have Redis installed
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:5174
```

### Run Database Migrations

```powershell
python manage.py migrate
```

### (Optional) Create an Admin User

```powershell
python manage.py createsuperuser
```

### Start the Backend Server

```powershell
python manage.py runserver
```

✅ Backend is now running at: **http://localhost:8000**

---

## 🎨 Step 3: Set Up the Frontend (React / Vite)

Open a **new terminal window** and navigate to the frontend folder.

```powershell
cd path\to\internship\frontend

# Install all Node.js dependencies
npm install

# Configure environment variables
copy .env.example .env
```

Open `frontend\.env` and confirm it contains:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=PriceIntel
```

### Start the Frontend Dev Server

```powershell
npm run dev
```

✅ Frontend is now running at: **http://localhost:5173**

---

## 🌐 Step 4: Open the Application

1. Make sure **both** the backend and frontend servers are running simultaneously.
2. Open your browser and go to: **http://localhost:5173**
3. Register a new account or log in.

---

## 🔑 Admin Panel

Visit **http://localhost:8000/admin/** and log in with the superuser credentials you created.

---

## 📋 Quick Reference – All Commands

```powershell
# ── BACKEND ──────────────────────────────────────────
cd path\to\internship\backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env         # then edit .env
python manage.py migrate
python manage.py runserver     # runs on port 8000

# ── FRONTEND (new terminal) ───────────────────────────
cd path\to\internship\frontend
npm install
copy .env.example .env         # confirm VITE_API_BASE_URL
npm run dev                    # runs on port 5173
```

---

## ❓ Troubleshooting

| Problem | Solution |
|---|---|
| `python` not found | Re-install Python and ensure "Add to PATH" was checked |
| `pip install` fails on `psycopg2-binary` | Install Visual C++ Build Tools from Microsoft, or use `pip install psycopg2-binary --no-binary psycopg2-binary` |
| `python-magic-bin` install fails | Run `pip install python-magic-bin==0.4.14` separately after other packages |
| CORS errors in browser | Confirm `CORS_ALLOWED_ORIGINS` in `backend/.env` includes your frontend URL |
| `migrate` fails | Make sure you are inside the `backend/` folder with the venv activated |
| `npm install` takes too long | Normal on first run – it downloads all packages |
| Port already in use | Backend: add `python manage.py runserver 8001`. Frontend: Vite will auto-pick next available port |
| No module named `cv2` | Run: `pip install opencv-python` |
| No module named `PIL` | Run: `pip install Pillow` |

---

## 🗂️ Folders to EXCLUDE When Transferring

When copying the project to a USB drive or zip, **exclude** these large/machine-specific folders:

```
.venv/
venv/
dt_venv/
backend/.venv/
backend/venv/
backend/dt_venv/
frontend/node_modules/
```

All of these will be recreated by running `pip install -r requirements.txt` and `npm install`.

---

## ✅ Checklist for the New Laptop

- [ ] Python 3.11+ installed and on PATH
- [ ] Node.js 18+ (LTS) installed
- [ ] Project folder copied (excluding venv/node_modules)
- [ ] `backend/venv` created and dependencies installed
- [ ] `backend/.env` file created from `.env.example`
- [ ] `python manage.py migrate` run successfully
- [ ] `frontend/.env` file created from `.env.example`
- [ ] `npm install` completed in `frontend/`
- [ ] Backend server running on port 8000
- [ ] Frontend server running on port 5173
- [ ] App accessible at http://localhost:5173 ✅
