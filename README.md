# 📝 Todo List App

A full-stack todo list application built with **FastAPI** (backend) and **React** (frontend) featuring drag-and-drop reordering and SQLite database persistence.

## ✨ Features

- ✅ Create new todos with title and optional description
- ✏️ Edit existing todos inline
- ✓ Mark todos as complete/incomplete with checkboxes
- 🗑️ Delete todos
- 🎯 **Drag and drop to reorder** todos
- 💾 **SQLite database** - todos persist between sessions
- 📊 View todo statistics (total & completed)
- 🎨 Beautiful gradient UI design with smooth animations
- ⚡ Fast and responsive

## 🎮 How to Use

1. **Add**: Type a title (and optional description), click "Add Todo"
2. **Complete**: Click the checkbox to mark done
3. **Edit**: Click the ✏️ pencil icon
4. **Delete**: Click the 🗑️ trash icon
5. **Reorder**: **Drag and drop** todos to rearrange them!

## 🚀 Quick Start

**📋 See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed beginner-friendly instructions!**

### Prerequisites
- Python 3.8+ 
- Node.js 16+

### Backend Setup
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
python main.py
```
Backend runs at: http://localhost:8000

### Frontend Setup
```powershell
cd frontend
npm install
npm run dev
```
Frontend runs at: http://localhost:5173

## 🏗️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Lightweight database
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI library with Hooks
- **Vite** - Fast build tool and dev server
- **@hello-pangea/dnd** - Drag and drop library
- **Axios** - HTTP client
- **CSS3** - Custom styling with gradients

## 📁 Project Structure

```
TODOLISTAPP/
├── backend/
│   ├── main.py              # FastAPI app with CRUD endpoints
│   ├── database.py          # SQLAlchemy models & DB setup
│   ├── requirements.txt     # Python dependencies
│   ├── todos.db            # SQLite database (auto-created)
│   └── .gitignore
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── TodoForm.jsx      # Add new todos
    │   │   ├── TodoList.jsx      # List with drag-and-drop
    │   │   └── TodoItem.jsx      # Individual todo item
    │   ├── App.jsx               # Main component
    │   └── main.jsx              # Entry point
    ├── index.html
    ├── package.json
    └── vite.config.js
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/todos` | Get all todos (ordered by position) |
| GET | `/api/todos/{id}` | Get a specific todo |
| POST | `/api/todos` | Create a new todo |
| PUT | `/api/todos/{id}` | Update a todo |
| PUT | `/api/todos/reorder` | Reorder todos (drag-and-drop) |
| DELETE | `/api/todos/{id}` | Delete a todo |

API Documentation: http://localhost:8000/docs

## 💾 Database

- Uses **SQLite** database (`backend/todos.db`)
- Todos **persist** between sessions
- Auto-created on first run
- Delete `todos.db` to reset all data

## 🎓 What Makes This Great for Beginners

This project teaches you:
- ✅ Full-stack development (frontend + backend)
- ✅ REST API design and implementation
- ✅ Database operations with ORM
- ✅ React component architecture
- ✅ State management with Hooks
- ✅ Drag-and-drop interactions
- ✅ HTTP requests and error handling

## 🐛 Troubleshooting

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed troubleshooting steps.

**Common Issues:**
- **Python not found**: Install from https://www.python.org/downloads/
- **Port in use**: Backend uses 8000, Frontend uses 5173
- **CORS errors**: Ensure backend is running first

## 🚀 Future Enhancements

Ideas to keep learning:
- [ ] User authentication (login/signup)
- [ ] Due dates and reminders
- [ ] Categories and tags
- [ ] Search and filter
- [ ] Dark mode
- [ ] Cloud deployment
- [ ] Mobile app version

## 📚 Learning Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **React**: https://react.dev/
- **SQLAlchemy**: https://www.sqlalchemy.org/
- **Drag and Drop**: https://github.com/hello-pangea/dnd

## 📄 License

Open source for learning purposes. Feel free to use and modify!

---

**Happy coding! 🎉 You're building real applications!**
