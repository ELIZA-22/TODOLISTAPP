from sqlalchemy import create_engine, Column, String, Boolean, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Todo model
class TodoDB(Base):
    __tablename__ = "todos"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    position = Column(Integer, default=0)
    priority = Column(String, default="medium")  # low, medium, high, urgent
    notes = Column(String, nullable=True)  # Additional notes/scratchpad
    created_at = Column(DateTime, default=datetime.utcnow)

# Note model (standalone notes, not linked to todos)
class NoteDB(Base):
    __tablename__ = "notes"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
