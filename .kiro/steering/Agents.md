---
inclusion: auto
name: API Testing Guidelines
description: Guidelines for testing API endpoints and validating functionality
---

# API Testing Guidelines for Todo App

## Test Requirements

When working with this todo application, you MUST:

1. **Write tests for ALL endpoints** you create or modify
2. **Validate that endpoints are working** before marking tasks as complete
3. **Run tests after changes** to ensure nothing breaks

---

## Backend API Endpoints to Test

### 1. GET /api/todos
- **Purpose**: Retrieve all todos
- **Expected**: Returns array of todos ordered by position
- **Test**: Verify empty array when no todos exist, populated array with todos

### 2. GET /api/todos/{todo_id}
- **Purpose**: Get a specific todo by ID
- **Expected**: Returns single todo object
- **Test**: Verify 404 when ID doesn't exist, correct data when ID exists

### 3. POST /api/todos
- **Purpose**: Create a new todo
- **Expected**: Returns created todo with ID, status 201
- **Test**: Verify title is required, description is optional, position auto-assigned

### 4. PUT /api/todos/{todo_id}
- **Purpose**: Update an existing todo
- **Expected**: Returns updated todo, status 200
- **Test**: Verify partial updates work, 404 for non-existent ID

### 5. PUT /api/todos/reorder
- **Purpose**: Reorder todos via drag-and-drop
- **Expected**: Returns all todos in new order
- **Test**: Verify positions update correctly, order is maintained

### 6. DELETE /api/todos/{todo_id}
- **Purpose**: Delete a todo
- **Expected**: Status 204, todo removed from database
- **Test**: Verify 404 for non-existent ID, todo is actually deleted

---

## Test Framework Setup

### Backend Testing (Python/FastAPI)

**Install test dependencies:**
```bash
pip install pytest pytest-asyncio httpx
```

**Test file location:** `backend/test_main.py`

**Run tests:**
```bash
pytest backend/test_main.py -v
```

---

## Validation Checklist

Before completing any backend work, verify:

- [ ] All endpoints return correct HTTP status codes
- [ ] Data validation works (required fields, data types)
- [ ] Error handling works (404, 400, 500)
- [ ] CORS is configured correctly
- [ ] Database operations persist correctly
- [ ] Endpoints documented in OpenAPI/Swagger docs

---

## Frontend Testing

### Component Testing
- Test that todos render correctly
- Test add/edit/delete operations
- Test drag-and-drop functionality
- Test error messages display properly
- Test loading states work

### Integration Testing
- Test API calls succeed
- Test error handling when backend is down
- Test data persistence (refresh page)

---

## Manual Testing Steps

After any changes, perform these manual tests:

1. **Create Todo**: Add a new todo with title and description
2. **Read Todos**: Refresh page, verify todos load
3. **Update Todo**: Edit title, mark as complete, verify changes save
4. **Delete Todo**: Remove a todo, verify it's gone
5. **Reorder Todos**: Drag and drop, refresh page, verify order persists
6. **Error Handling**: Stop backend, verify frontend shows error message

---

## Testing Best Practices

1. **Test edge cases**: Empty strings, very long text, special characters
2. **Test error scenarios**: Invalid IDs, missing required fields
3. **Test database state**: Verify data persists after server restart
4. **Test CORS**: Verify frontend can connect from different ports
5. **Test concurrent operations**: Multiple users modifying same data

---

## Automated Testing Goals

- **Coverage target**: 80%+ of backend code
- **Run tests**: Before every commit
- **CI/CD**: Automate test runs on push (future enhancement)

---

## Example Test Structure

```python
# backend/test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_todo():
    response = client.post("/api/todos", json={
        "title": "Test Todo",
        "description": "Test Description"
    })
    assert response.status_code == 201
    assert response.json()["title"] == "Test Todo"

def test_get_todos():
    response = client.get("/api/todos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_todo():
    # Create a todo first
    create_response = client.post("/api/todos", json={
        "title": "Original"
    })
    todo_id = create_response.json()["id"]
    
    # Update it
    update_response = client.put(f"/api/todos/{todo_id}", json={
        "completed": True
    })
    assert update_response.status_code == 200
    assert update_response.json()["completed"] == True

def test_delete_todo():
    # Create a todo first
    create_response = client.post("/api/todos", json={
        "title": "To Delete"
    })
    todo_id = create_response.json()["id"]
    
    # Delete it
    delete_response = client.delete(f"/api/todos/{todo_id}")
    assert delete_response.status_code == 204
    
    # Verify it's gone
    get_response = client.get(f"/api/todos/{todo_id}")
    assert get_response.status_code == 404
```

---

## When Adding New Features

When adding notes, priorities, or any new features:

1. **Update this document** with new endpoints to test
2. **Write tests FIRST** (TDD approach) or immediately after
3. **Run full test suite** to ensure no regressions
4. **Update API documentation** in README.md
5. **Test manually** in browser before considering done

---

## Continuous Validation

- **Daily**: Run test suite
- **Before commits**: Verify all tests pass
- **After changes**: Validate affected endpoints manually
- **Weekly**: Review test coverage, add missing tests

---

## Code Quality Standards

### Backend (Python/FastAPI)

**Required practices:**
- Use type hints for all function parameters and return values
- Follow PEP 8 style guide (use `black` formatter)
- Add docstrings to all functions and classes
- Handle all exceptions gracefully
- Use Pydantic models for all request/response data
- Keep database sessions properly managed (use dependencies)
- Use meaningful variable names

**Example:**
```python
@app.get("/api/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: str, db: Session = Depends(get_db)) -> Todo:
    """
    Get a specific todo by ID.
    
    Args:
        todo_id: Unique identifier of the todo
        db: Database session dependency
        
    Returns:
        Todo: The requested todo object
        
    Raises:
        HTTPException: 404 if todo not found
    """
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo
```

### Frontend (React/JavaScript)

**Required practices:**
- Use functional components with hooks (no class components)
- Keep components small and focused (single responsibility)
- Use meaningful component and variable names
- Add PropTypes or TypeScript for type safety
- Handle loading and error states
- Clean up effects and event listeners
- Use CSS modules or styled components (avoid inline styles)
- Keep API calls in centralized functions or hooks

**Component structure:**
```jsx
function TodoItem({ todo, onToggle, onDelete, onUpdate }) {
  const [isEditing, setIsEditing] = useState(false)
  
  // Event handlers
  const handleSave = () => { /* ... */ }
  
  // Early returns for different states
  if (isEditing) return <EditMode />
  
  // Main render
  return <DisplayMode />
}
```

---

## Database Best Practices

### Schema Changes
- **NEVER** delete the database file in production
- **ALWAYS** create migration scripts for schema changes
- Test migrations on a copy of the database first
- Document all schema changes in README

### Data Integrity
- Use foreign keys where appropriate
- Add indexes for frequently queried fields
- Set appropriate default values
- Use NOT NULL constraints where data is required
- Consider adding created_at and updated_at timestamps

### Example migration workflow:
```python
# When adding a new field:
# 1. Update database.py model
# 2. Create migration script
# 3. Test on dev database
# 4. Document changes
# 5. Apply to production
```

---

## Security Considerations

### Backend Security
- **Input Validation**: Validate all user input (length, format, type)
- **SQL Injection**: Use ORM (SQLAlchemy) parameterized queries only
- **CORS**: Only allow trusted origins
- **Rate Limiting**: Consider adding rate limits to prevent abuse
- **Authentication**: Add JWT or session-based auth (future feature)
- **Environment Variables**: Store secrets in .env files (never commit)

### Frontend Security
- **XSS Prevention**: React auto-escapes by default, don't use dangerouslySetInnerHTML
- **API Keys**: Never expose API keys in frontend code
- **Sensitive Data**: Don't log sensitive information to console

---

## Error Handling Guidelines

### Backend Error Responses
Always return consistent error format:
```python
{
    "detail": "Clear error message for client",
    "error_code": "TODO_NOT_FOUND",  # Optional
    "field": "todo_id"  # Optional, for validation errors
}
```

**HTTP Status Codes:**
- 200: Success (GET, PUT)
- 201: Created (POST)
- 204: No Content (DELETE)
- 400: Bad Request (validation error)
- 404: Not Found
- 500: Internal Server Error

### Frontend Error Handling
```jsx
try {
  const response = await axios.post('/api/todos', todoData)
  setTodos([...todos, response.data])
} catch (err) {
  if (err.response?.status === 404) {
    setError('Todo not found')
  } else if (err.response?.status === 400) {
    setError('Invalid todo data')
  } else {
    setError('Failed to create todo. Please try again.')
  }
  console.error('Error creating todo:', err)
}
```

---

## Performance Optimization

### Backend
- Use database indexes for frequently queried fields
- Implement pagination for large lists (future)
- Use connection pooling for database
- Cache frequently accessed data (future)
- Optimize queries (avoid N+1 queries)

### Frontend
- Lazy load components when appropriate
- Debounce search and filter inputs
- Memoize expensive computations (useMemo, useCallback)
- Optimize re-renders (React.memo for components)
- Use virtual scrolling for very long lists (future)

---

## Git Workflow

### Commit Messages
Follow conventional commit format:
```
feat: add priority levels to todos
fix: resolve drag-and-drop reorder bug
docs: update README with new features
test: add tests for reorder endpoint
refactor: simplify TodoItem component
style: format code with black
```

### Branch Strategy (for team projects)
- `main`: Production-ready code
- `develop`: Development branch
- `feature/feature-name`: New features
- `fix/bug-description`: Bug fixes

### Before Every Commit
- [ ] Run tests: `pytest backend/test_main.py`
- [ ] Format code: `black backend/`
- [ ] Check for console.logs in production code
- [ ] Update documentation if needed
- [ ] Test manually in browser

---

## Documentation Requirements

### When Adding Features
1. **Update README.md** with:
   - Feature description
   - How to use it
   - Screenshots if UI changed

2. **Update API docs** in code:
   - Add docstrings to new endpoints
   - Update Pydantic models
   - FastAPI will auto-generate Swagger docs

3. **Update this Agents.md**:
   - Add new endpoints to test
   - Update validation checklist
   - Add new best practices if applicable

4. **Update SETUP_GUIDE.md**:
   - New dependencies
   - Setup steps
   - Troubleshooting for new features

---

## Accessibility (a11y) Requirements

### Frontend Accessibility
- Use semantic HTML (`<button>`, `<input>`, not `<div onclick>`)
- Add `aria-label` to icon buttons
- Ensure keyboard navigation works (Tab, Enter, Escape)
- Use sufficient color contrast (WCAG AA minimum)
- Add loading states for screen readers
- Test with keyboard only (no mouse)

**Example:**
```jsx
<button 
  onClick={handleDelete} 
  className="btn-delete" 
  aria-label="Delete todo"
  title="Delete"
>
  🗑️
</button>
```

---

## Debugging Guidelines

### Backend Debugging
- Use print statements or logging module
- Check database state: `sqlite3 todos.db "SELECT * FROM todos;"`
- Use FastAPI's /docs endpoint to test APIs manually
- Check server logs for error messages
- Use `pdb` debugger for complex issues

### Frontend Debugging
- Use React DevTools browser extension
- Check Network tab for API calls
- Use console.log strategically (remove after debugging)
- Check browser console for errors
- Use React strict mode to catch issues

---

## When Things Break

### Systematic Debugging Process
1. **Identify**: What's the exact error message?
2. **Isolate**: Can you reproduce it consistently?
3. **Locate**: Which component/function is failing?
4. **Fix**: Make the minimal change to fix it
5. **Test**: Verify fix works and doesn't break other things
6. **Document**: Add test case to prevent regression

### Common Issues & Solutions

**Backend won't start:**
- Check if port 8000 is already in use
- Verify all dependencies installed: `pip list`
- Check for syntax errors in main.py
- Delete todos.db and restart (dev only)

**Frontend won't start:**
- Delete `node_modules` and `package-lock.json`, run `npm install`
- Check if port 5173 is already in use
- Clear browser cache
- Check for syntax errors in JSX files

**API returns 404:**
- Check endpoint order in main.py (specific routes before parameterized ones)
- Verify CORS is configured
- Check API URL in frontend (should be http://localhost:8000)
- Test endpoint directly in /docs

**Drag-and-drop not working:**
- Check reorder endpoint is defined before /{todo_id} endpoint
- Verify @hello-pangea/dnd is installed
- Check browser console for errors
- Ensure todoIds array is being sent correctly

---

## Project Structure Standards

```
TODOLISTAPP/
├── backend/
│   ├── main.py              # FastAPI app & endpoints
│   ├── database.py          # Database models & config
│   ├── test_main.py         # API tests
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # Environment variables (gitignored)
│   └── todos.db            # SQLite database (gitignored)
│
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── hooks/          # Custom hooks (future)
│   │   ├── utils/          # Helper functions (future)
│   │   ├── App.jsx         # Main app component
│   │   ├── App.css         # Main app styles
│   │   └── main.jsx        # Entry point
│   ├── public/             # Static assets
│   └── package.json        # Node dependencies
│
├── .kiro/
│   └── steering/
│       └── Agents.md       # This file!
│
├── README.md               # Project overview
├── SETUP_GUIDE.md         # Installation guide
├── QUICK_START.md         # Quick start guide
└── .gitignore             # Git ignore rules
```

---

## Feature Development Workflow

### Step-by-Step Process

1. **Planning**
   - [ ] Define feature requirements clearly
   - [ ] Sketch UI mockup (if frontend change)
   - [ ] Design database schema changes (if needed)
   - [ ] List affected endpoints
   - [ ] Estimate complexity

2. **Backend Development**
   - [ ] Update database.py models
   - [ ] Add/modify endpoints in main.py
   - [ ] Write tests in test_main.py
   - [ ] Run tests: `pytest -v`
   - [ ] Test manually in /docs

3. **Frontend Development**
   - [ ] Create/modify components
   - [ ] Update API calls in App.jsx
   - [ ] Add styling
   - [ ] Test in browser manually
   - [ ] Test on different screen sizes

4. **Integration Testing**
   - [ ] Test full user flow
   - [ ] Check error handling
   - [ ] Verify data persists (restart servers)
   - [ ] Test edge cases

5. **Documentation**
   - [ ] Update README.md
   - [ ] Update SETUP_GUIDE.md if needed
   - [ ] Add comments to complex code
   - [ ] Update Agents.md if needed

6. **Deployment Preparation**
   - [ ] All tests passing
   - [ ] No console errors
   - [ ] Code formatted and clean
   - [ ] Database migrations documented
   - [ ] Ready to commit

---

## Maintenance Checklist

### Weekly
- [ ] Run full test suite
- [ ] Check for dependency updates (security)
- [ ] Review and remove TODO comments
- [ ] Check for deprecated dependencies

### Monthly
- [ ] Update dependencies to latest stable
- [ ] Review and optimize database queries
- [ ] Check application performance
- [ ] Review error logs

### Before Production Release
- [ ] All tests passing (100% of test suite)
- [ ] Manual testing completed
- [ ] Documentation up to date
- [ ] Security review completed
- [ ] Performance testing done
- [ ] Backup database
- [ ] Deployment plan ready

---

Remember: **A feature without tests is a feature that will break!** ✅

**Good code is:**
- Tested thoroughly
- Documented clearly  
- Validated constantly
- Secure by default
- Accessible to all
- Maintainable long-term
