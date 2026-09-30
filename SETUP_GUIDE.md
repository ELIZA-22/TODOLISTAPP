# 🚀 Quick Setup Guide for Beginners

## ⚠️ Prerequisites Needed

Before running this app, you need to install:

### 1. Python (for Backend)
**Currently NOT installed on your system.**

**How to Install:**
1. Go to: https://www.python.org/downloads/
2. Download Python 3.11 or newer (recommended)
3. **IMPORTANT**: During installation, check ✅ "Add Python to PATH"
4. Click "Install Now"
5. After installation, restart your terminal/PowerShell

**Verify Installation:**
Open PowerShell and type:
```powershell
python --version
```
You should see: `Python 3.11.x` or similar

### 2. Node.js (for Frontend)
**✅ Already installed! Version: 24.1.0**

---

## 📦 Installation Steps

### Step 1: Install Backend Dependencies

Open PowerShell in the project folder and run:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
```

If you see an error about `pip`, try:
```powershell
python -m pip install -r requirements.txt
```

### Step 2: Install Frontend Dependencies

Open a **NEW** PowerShell window and run:

```powershell
cd frontend
npm install
```

This will install React and the drag-and-drop library.

---

## ▶️ Running the App

You need **TWO terminal windows** open:

### Terminal 1: Start Backend (FastAPI)

```powershell
cd backend
.\venv\Scripts\Activate
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ Backend is ready at: **http://localhost:8000**

### Terminal 2: Start Frontend (React)

```powershell
cd frontend
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

✅ Frontend is ready at: **http://localhost:5173**

---

## 🌐 Open in Browser

Go to: **http://localhost:5173**

You should see your Todo List app! 🎉

---

## 🎮 How to Use the App

1. **Add a Todo**: Type in the title and optional description, click "Add Todo"
2. **Check Off**: Click the checkbox to mark as complete
3. **Edit**: Click the ✏️ icon to edit title/description
4. **Delete**: Click the 🗑️ icon to remove
5. **Reorder**: **Drag and drop** todos to change their order!

---

## 🐛 Troubleshooting

### "Python is not recognized"
- Python is not installed or not in PATH
- Install Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation
- Restart PowerShell after installing

### "pip is not recognized"
- Try using: `python -m pip` instead of just `pip`

### Backend won't start
- Make sure you activated the virtual environment: `.\venv\Scripts\Activate`
- You should see `(venv)` at the start of your PowerShell prompt

### Frontend won't start
- Delete `node_modules` folder and `package-lock.json`
- Run `npm install` again

### Can't connect to backend
- Make sure backend is running (Terminal 1)
- Check that you see "Uvicorn running on http://0.0.0.0:8000"
- Try visiting http://localhost:8000/docs to see API documentation

### Port already in use
- **Backend (8000)**: Another app is using port 8000
  - Stop that app or change port in `backend/main.py` (last line)
- **Frontend (5173)**: Another app is using port 5173
  - Vite will automatically try port 5174

---

## 💾 Database

Your todos are saved in `backend/todos.db` (SQLite database).

- Todos persist even after restarting the servers
- To start fresh, delete `todos.db` file
- The database file is created automatically on first run

---

## 🎓 What You Built

This is a **full-stack application**:

- **Backend (FastAPI + Python)**:
  - REST API with endpoints (GET, POST, PUT, DELETE)
  - SQLite database for data persistence
  - SQLAlchemy ORM for database operations

- **Frontend (React + Vite)**:
  - Modern React with Hooks (useState, useEffect)
  - Component-based architecture
  - Drag-and-drop with @hello-pangea/dnd
  - HTTP requests with Axios

Great job! You're learning real-world development skills! 🎉

---

## 📚 Next Steps to Learn More

1. **Customize the styles** in `.css` files
2. **Add new features** like:
   - Due dates for todos
   - Priority levels (high, medium, low)
   - Categories/tags
   - Search functionality
3. **Deploy online** using:
   - Backend: Railway, Render, or Heroku
   - Frontend: Vercel, Netlify, or GitHub Pages

---

## 📞 Need Help?

If something doesn't work:
1. Check that both servers are running
2. Look for error messages in the terminal
3. Check the browser console (F12 → Console tab)
4. Make sure Python and Node.js are installed correctly
