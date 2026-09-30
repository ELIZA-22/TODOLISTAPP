# ⚡ Quick Start - Run Todo App

Your todo app is ready! Just need to install dependencies and run it.

## 📝 Manual Steps (Due to Slow Network)

### Step 1: Install Backend Dependencies

Open PowerShell in this folder and run:

```powershell
cd backend
pip install fastapi uvicorn sqlalchemy
```

Wait for it to finish downloading (may take 5-10 minutes on slow connection).

### Step 2: Install Frontend Dependencies

Open a **NEW** PowerShell window:

```powershell
cd frontend  
npm install
```

This will also take several minutes.

### Step 3: Run Backend

In the first PowerShell (backend folder):

```powershell
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ Backend is running!

### Step 4: Run Frontend

In the second PowerShell (frontend folder):

```powershell
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms
  ➜  Local:   http://localhost:5173/
```

✅ Frontend is running!

### Step 5: Open in Browser

Go to: **http://localhost:5173**

🎉 Your Todo App is live!

---

## 🎮 How to Use

1. **Add Todo**: Type title & description, click "Add Todo"
2. **Check Off**: Click checkbox to mark complete  
3. **Edit**: Click ✏️ pencil icon
4. **Delete**: Click 🗑️ trash icon
5. **Reorder**: **Drag and drop** todos!

---

## ✨ Features

- ✅ SQLite database (todos saved permanently)
- 🎯 Drag & drop to reorder
- ✏️ Edit todos inline
- 📊 Statistics (total & completed)
- 🎨 Beautiful UI with animations

---

## 🛑 To Stop Servers

Press `Ctrl + C` in each PowerShell window

---

## ❓ Troubleshooting

**Backend Error: "ModuleNotFoundError"**
- Run: `pip install fastapi uvicorn sqlalchemy` again

**Frontend Error: "Cannot find module"**
- Delete `node_modules` folder
- Run: `npm install` again

**Can't connect to backend**
- Make sure backend is running (Terminal 1)
- Check you see "Uvicorn running on http://0.0.0.0:8000"

**Port already in use**
- Close other programs using ports 8000 or 5173
- Or restart your computer

---

Good luck! 🚀
