from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import uuid
import os

from database import get_db, init_db, TodoDB, NoteDB

# Initialize database on startup using lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown (cleanup if needed)

# Create FastAPI app - compatible with Vercel
app = FastAPI(title="Todo List API", lifespan=lifespan)

# Configure CORS - allow all origins for Vercel deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Vercel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"  # low, medium, high, urgent
    notes: Optional[str] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    notes: Optional[str] = None

class TodoReorder(BaseModel):
    todoIds: List[str]

class NoteCreate(BaseModel):
    title: str
    content: Optional[str] = None

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class Note(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    title: str
    content: Optional[str] = None
    created_at: str
    updated_at: str

class Todo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    position: int = 0
    priority: str = "medium"
    notes: Optional[str] = None
    created_at: str

@app.get("/")
def read_root():
    return {"message": "Todo List API with SQLite", "version": "2.0.0"}

@app.get("/api/todos", response_model=List[Todo])
def get_todos(db: Session = Depends(get_db)):
    """Get all todos ordered by position"""
    todos = db.query(TodoDB).order_by(TodoDB.position).all()
    return [Todo(
        id=todo.id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        position=todo.position,
        priority=todo.priority,
        notes=todo.notes,
        created_at=todo.created_at.isoformat()
    ) for todo in todos]

@app.put("/api/todos/reorder", response_model=List[Todo])
def reorder_todos(reorder: TodoReorder, db: Session = Depends(get_db)):
    """Reorder todos based on drag and drop"""
    for index, todo_id in enumerate(reorder.todoIds):
        todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
        if todo:
            todo.position = index
    
    db.commit()
    
    # Return all todos in new order
    todos = db.query(TodoDB).order_by(TodoDB.position).all()
    return [Todo(
        id=todo.id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        position=todo.position,
        priority=todo.priority,
        notes=todo.notes,
        created_at=todo.created_at.isoformat()
    ) for todo in todos]

@app.get("/api/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: str, db: Session = Depends(get_db)):
    """Get a specific todo by ID"""
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return Todo(
        id=todo.id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        position=todo.position,
        priority=todo.priority,
        notes=todo.notes,
        created_at=todo.created_at.isoformat()
    )

@app.post("/api/todos", response_model=Todo, status_code=201)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """Create a new todo"""
    # Get the highest position
    max_position = db.query(TodoDB).count()
    
    todo_id = str(uuid.uuid4())
    db_todo = TodoDB(
        id=todo_id,
        title=todo.title,
        description=todo.description,
        completed=False,
        position=max_position,
        priority=todo.priority or "medium",
        notes=todo.notes,
        created_at=datetime.utcnow()
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    
    return Todo(
        id=db_todo.id,
        title=db_todo.title,
        description=db_todo.description,
        completed=db_todo.completed,
        position=db_todo.position,
        priority=db_todo.priority,
        notes=db_todo.notes,
        created_at=db_todo.created_at.isoformat()
    )

@app.put("/api/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: str, todo_update: TodoUpdate, db: Session = Depends(get_db)):
    """Update an existing todo"""
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    update_data = todo_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo, key, value)
    
    db.commit()
    db.refresh(todo)
    
    return Todo(
        id=todo.id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        position=todo.position,
        priority=todo.priority,
        notes=todo.notes,
        created_at=todo.created_at.isoformat()
    )

@app.delete("/api/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: str, db: Session = Depends(get_db)):
    """Delete a todo"""
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo)
    db.commit()
    return None

# ============== NOTES ENDPOINTS ==============

@app.get("/api/notes", response_model=List[Note])
def get_notes(db: Session = Depends(get_db)):
    """Get all notes ordered by updated date"""
    notes = db.query(NoteDB).order_by(NoteDB.updated_at.desc()).all()
    return [Note(
        id=note.id,
        title=note.title,
        content=note.content,
        created_at=note.created_at.isoformat(),
        updated_at=note.updated_at.isoformat()
    ) for note in notes]

@app.get("/api/notes/{note_id}", response_model=Note)
def get_note(note_id: str, db: Session = Depends(get_db)):
    """Get a specific note by ID"""
    note = db.query(NoteDB).filter(NoteDB.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return Note(
        id=note.id,
        title=note.title,
        content=note.content,
        created_at=note.created_at.isoformat(),
        updated_at=note.updated_at.isoformat()
    )

@app.post("/api/notes", response_model=Note, status_code=201)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    """Create a new note"""
    note_id = str(uuid.uuid4())
    db_note = NoteDB(
        id=note_id,
        title=note.title,
        content=note.content,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    
    return Note(
        id=db_note.id,
        title=db_note.title,
        content=db_note.content,
        created_at=db_note.created_at.isoformat(),
        updated_at=db_note.updated_at.isoformat()
    )

@app.put("/api/notes/{note_id}", response_model=Note)
def update_note(note_id: str, note_update: NoteUpdate, db: Session = Depends(get_db)):
    """Update an existing note"""
    note = db.query(NoteDB).filter(NoteDB.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    update_data = note_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(note, key, value)
    
    note.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(note)
    
    return Note(
        id=note.id,
        title=note.title,
        content=note.content,
        created_at=note.created_at.isoformat(),
        updated_at=note.updated_at.isoformat()
    )

@app.delete("/api/notes/{note_id}", status_code=204)
def delete_note(note_id: str, db: Session = Depends(get_db)):
    """Delete a note"""
    note = db.query(NoteDB).filter(NoteDB.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(note)
    db.commit()
    return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Vercel handler
handler = app