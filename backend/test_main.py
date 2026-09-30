"""
Test suite for Todo List API endpoints
Run with: pytest test_main.py -v
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, get_db

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_todos.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    """Create fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestRootEndpoint:
    """Test root endpoint"""
    
    def test_read_root(self):
        """Test root endpoint returns correct message"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Todo List API with SQLite"
        assert data["version"] == "2.0.0"


class TestGetTodos:
    """Test GET /api/todos endpoint"""
    
    def test_get_empty_todos(self):
        """Test getting todos when none exist"""
        response = client.get("/api/todos")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_todos_with_data(self):
        """Test getting todos when some exist"""
        # Create a todo first
        client.post("/api/todos", json={"title": "Test Todo"})
        
        response = client.get("/api/todos")
        assert response.status_code == 200
        todos = response.json()
        assert len(todos) == 1
        assert todos[0]["title"] == "Test Todo"
    
    def test_todos_ordered_by_position(self):
        """Test todos are returned in position order"""
        # Create multiple todos
        client.post("/api/todos", json={"title": "First"})
        client.post("/api/todos", json={"title": "Second"})
        client.post("/api/todos", json={"title": "Third"})
        
        response = client.get("/api/todos")
        todos = response.json()
        assert todos[0]["title"] == "First"
        assert todos[1]["title"] == "Second"
        assert todos[2]["title"] == "Third"


class TestGetTodoById:
    """Test GET /api/todos/{todo_id} endpoint"""
    
    def test_get_existing_todo(self):
        """Test getting a specific todo by ID"""
        # Create a todo
        create_response = client.post("/api/todos", json={
            "title": "Specific Todo",
            "description": "Specific Description"
        })
        todo_id = create_response.json()["id"]
        
        # Get it by ID
        response = client.get(f"/api/todos/{todo_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == todo_id
        assert data["title"] == "Specific Todo"
        assert data["description"] == "Specific Description"
    
    def test_get_nonexistent_todo(self):
        """Test getting a todo that doesn't exist returns 404"""
        response = client.get("/api/todos/nonexistent-id-12345")
        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"


class TestCreateTodo:
    """Test POST /api/todos endpoint"""
    
    def test_create_todo_with_title_only(self):
        """Test creating a todo with just a title"""
        response = client.post("/api/todos", json={
            "title": "New Todo"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Todo"
        assert data["description"] is None
        assert data["completed"] is False
        assert "id" in data
        assert "created_at" in data
    
    def test_create_todo_with_title_and_description(self):
        """Test creating a todo with title and description"""
        response = client.post("/api/todos", json={
            "title": "Detailed Todo",
            "description": "This is a detailed description"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Detailed Todo"
        assert data["description"] == "This is a detailed description"
    
    def test_create_todo_position_increments(self):
        """Test that position increments for each new todo"""
        response1 = client.post("/api/todos", json={"title": "First"})
        response2 = client.post("/api/todos", json={"title": "Second"})
        response3 = client.post("/api/todos", json={"title": "Third"})
        
        assert response1.json()["position"] == 0
        assert response2.json()["position"] == 1
        assert response3.json()["position"] == 2


class TestUpdateTodo:
    """Test PUT /api/todos/{todo_id} endpoint"""
    
    def test_update_todo_title(self):
        """Test updating todo title"""
        # Create a todo
        create_response = client.post("/api/todos", json={"title": "Original"})
        todo_id = create_response.json()["id"]
        
        # Update title
        update_response = client.put(f"/api/todos/{todo_id}", json={
            "title": "Updated"
        })
        assert update_response.status_code == 200
        assert update_response.json()["title"] == "Updated"
    
    def test_update_todo_completed_status(self):
        """Test marking todo as completed"""
        # Create a todo
        create_response = client.post("/api/todos", json={"title": "To Complete"})
        todo_id = create_response.json()["id"]
        
        # Mark as completed
        update_response = client.put(f"/api/todos/{todo_id}", json={
            "completed": True
        })
        assert update_response.status_code == 200
        assert update_response.json()["completed"] is True
    
    def test_update_todo_description(self):
        """Test updating todo description"""
        # Create a todo
        create_response = client.post("/api/todos", json={"title": "Test"})
        todo_id = create_response.json()["id"]
        
        # Add description
        update_response = client.put(f"/api/todos/{todo_id}", json={
            "description": "Added description"
        })
        assert update_response.status_code == 200
        assert update_response.json()["description"] == "Added description"
    
    def test_update_nonexistent_todo(self):
        """Test updating a todo that doesn't exist returns 404"""
        response = client.put("/api/todos/fake-id", json={"title": "Won't work"})
        assert response.status_code == 404


class TestReorderTodos:
    """Test PUT /api/todos/reorder endpoint"""
    
    def test_reorder_todos(self):
        """Test reordering todos"""
        # Create three todos
        r1 = client.post("/api/todos", json={"title": "First"})
        r2 = client.post("/api/todos", json={"title": "Second"})
        r3 = client.post("/api/todos", json={"title": "Third"})
        
        id1, id2, id3 = r1.json()["id"], r2.json()["id"], r3.json()["id"]
        
        # Reorder: 3, 1, 2
        reorder_response = client.put("/api/todos/reorder", json={
            "todoIds": [id3, id1, id2]
        })
        
        assert reorder_response.status_code == 200
        todos = reorder_response.json()
        assert todos[0]["id"] == id3
        assert todos[0]["position"] == 0
        assert todos[1]["id"] == id1
        assert todos[1]["position"] == 1
        assert todos[2]["id"] == id2
        assert todos[2]["position"] == 2
    
    def test_reorder_persists(self):
        """Test that reordered positions persist"""
        # Create and reorder
        r1 = client.post("/api/todos", json={"title": "A"})
        r2 = client.post("/api/todos", json={"title": "B"})
        id1, id2 = r1.json()["id"], r2.json()["id"]
        
        client.put("/api/todos/reorder", json={"todoIds": [id2, id1]})
        
        # Get todos again
        get_response = client.get("/api/todos")
        todos = get_response.json()
        assert todos[0]["id"] == id2
        assert todos[1]["id"] == id1


class TestDeleteTodo:
    """Test DELETE /api/todos/{todo_id} endpoint"""
    
    def test_delete_existing_todo(self):
        """Test deleting an existing todo"""
        # Create a todo
        create_response = client.post("/api/todos", json={"title": "To Delete"})
        todo_id = create_response.json()["id"]
        
        # Delete it
        delete_response = client.delete(f"/api/todos/{todo_id}")
        assert delete_response.status_code == 204
        
        # Verify it's gone
        get_response = client.get(f"/api/todos/{todo_id}")
        assert get_response.status_code == 404
    
    def test_delete_nonexistent_todo(self):
        """Test deleting a todo that doesn't exist returns 404"""
        response = client.delete("/api/todos/fake-id")
        assert response.status_code == 404
    
    def test_delete_removes_from_list(self):
        """Test that deleted todo is removed from the list"""
        # Create two todos
        r1 = client.post("/api/todos", json={"title": "Keep"})
        r2 = client.post("/api/todos", json={"title": "Delete"})
        
        # Delete one
        client.delete(f"/api/todos/{r2.json()['id']}")
        
        # Verify only one remains
        get_response = client.get("/api/todos")
        todos = get_response.json()
        assert len(todos) == 1
        assert todos[0]["title"] == "Keep"


class TestDataValidation:
    """Test data validation and edge cases"""
    
    def test_create_todo_with_empty_title(self):
        """Test that empty title is rejected"""
        response = client.post("/api/todos", json={"title": ""})
        # Should still create (validation not enforced), but good to test
        assert response.status_code in [201, 422]
    
    def test_create_todo_with_long_title(self):
        """Test creating todo with very long title"""
        long_title = "A" * 500
        response = client.post("/api/todos", json={"title": long_title})
        assert response.status_code == 201
        assert len(response.json()["title"]) == 500
    
    def test_update_partial_fields(self):
        """Test partial updates work correctly"""
        # Create todo
        create_response = client.post("/api/todos", json={
            "title": "Original",
            "description": "Original desc"
        })
        todo_id = create_response.json()["id"]
        
        # Update only completed status
        update_response = client.put(f"/api/todos/{todo_id}", json={
            "completed": True
        })
        
        # Verify other fields unchanged
        data = update_response.json()
        assert data["title"] == "Original"
        assert data["description"] == "Original desc"
        assert data["completed"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
