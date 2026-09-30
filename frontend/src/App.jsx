import { useState, useEffect } from 'react'
import axios from 'axios'
import TodoForm from './components/TodoForm'
import TodoList from './components/TodoList'
import NotesView from './components/NotesView'
import './App.css'

const API_URL = '/api/todos'  // Same domain, relative path

// Mock data for demo purposes when backend is not available
const MOCK_TODOS = [
  {
    id: '1',
    title: 'Welcome to your Todo App! 🎉',
    description: 'This is a demo todo. Try creating your own!',
    completed: false,
    position: 0,
    priority: 'high',
    notes: 'This app features drag & drop, priorities, and notes!',
    created_at: new Date().toISOString()
  },
  {
    id: '2', 
    title: 'Features you can try:',
    description: 'Drag todos around, set priorities, add notes',
    completed: false,
    position: 1,
    priority: 'medium',
    notes: '• Drag & drop reordering\n• Priority levels\n• Notes on each todo\n• Separate Notes tab',
    created_at: new Date().toISOString()
  }
]

function App() {
  const [todos, setTodos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [activeTab, setActiveTab] = useState('tasks') // 'tasks' or 'notes'

  // Fetch todos on component mount
  useEffect(() => {
    fetchTodos()
  }, [])

  const fetchTodos = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await axios.get(API_URL)
      setTodos(response.data)
    } catch (err) {
      setError('Failed to fetch todos. Make sure the backend is running.')
      console.error('Error fetching todos:', err)
    } finally {
      setLoading(false)
    }
  }

  const addTodo = async (todoData) => {
    try {
      const response = await axios.post(API_URL, todoData)
      setTodos([...todos, response.data])
    } catch (err) {
      setError('Failed to add todo')
      console.error('Error adding todo:', err)
    }
  }

  const updateTodo = async (id, updates) => {
    try {
      const response = await axios.put(`${API_URL}/${id}`, updates)
      setTodos(todos.map(todo => todo.id === id ? response.data : todo))
    } catch (err) {
      setError('Failed to update todo')
      console.error('Error updating todo:', err)
    }
  }

  const deleteTodo = async (id) => {
    try {
      await axios.delete(`${API_URL}/${id}`)
      setTodos(todos.filter(todo => todo.id !== id))
    } catch (err) {
      setError('Failed to delete todo')
      console.error('Error deleting todo:', err)
    }
  }

  const toggleComplete = async (id, completed) => {
    await updateTodo(id, { completed: !completed })
  }

  const reorderTodos = async (todoIds) => {
    try {
      const response = await axios.put(`${API_URL}/reorder`, { todoIds })
      setTodos(response.data)
    } catch (err) {
      setError('Failed to reorder todos')
      console.error('Error reordering todos:', err)
    }
  }

  // Calculate momentum stats
  const completedCount = todos.filter(t => t.completed).length
  const totalCount = todos.length
  const completionPercentage = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0

  // Get current date
  const currentDate = new Date().toLocaleDateString('en-US', { 
    weekday: 'long', 
    month: 'long', 
    day: 'numeric' 
  }).toUpperCase()

  return (
    <div className="app">
      <div className="container">
        <div className="header">
          <div className="date-context">{currentDate}</div>
          <h1 className="app-title">Todo App</h1>
        </div>

        {totalCount > 0 && (
          <div className="momentum-card">
            <div className="momentum-header">
              <span className="momentum-label">Momentum</span>
              <span className="momentum-stats">
                <span className="momentum-count">{completedCount} of {totalCount}</span> completed {completionPercentage}%
              </span>
            </div>
            <div className="progress-bar-container">
              <div 
                className="progress-bar-fill" 
                style={{ width: `${completionPercentage}%` }}
              />
            </div>
          </div>
        )}

        {/* Tab Switcher */}
        <div className="tab-switcher">
          <button 
            className={`tab-button ${activeTab === 'tasks' ? 'active' : ''}`}
            onClick={() => setActiveTab('tasks')}
          >
            <span className="tab-icon">✓</span>
            Tasks
          </button>
          <button 
            className={`tab-button ${activeTab === 'notes' ? 'active' : ''}`}
            onClick={() => setActiveTab('notes')}
          >
            <span className="tab-icon">📝</span>
            Notes
          </button>
        </div>
        
        {error && (
          <div className="error-message">
            {error}
            <button onClick={() => setError(null)} className="close-btn">×</button>
          </div>
        )}

        {loading ? (
          <div className="loading">Loading...</div>
        ) : (
          <>
            {activeTab === 'tasks' ? (
              <>
                <TodoForm onAdd={addTodo} />
                {todos.length > 0 && (
                  <div className="drag-hint">
                    💡 Drag and drop to reorder todos
                  </div>
                )}
                <TodoList
                  todos={todos}
                  onToggle={toggleComplete}
                  onDelete={deleteTodo}
                  onUpdate={updateTodo}
                  onReorder={reorderTodos}
                />
                {todos.length > 0 && (
                  <div className="stats">
                    <p>Total: <span className="stats-count">{totalCount}</span> | Completed: <span className="stats-count">{completedCount}</span></p>
                  </div>
                )}
              </>
            ) : (
              <NotesView />
            )}
          </>
        )}
      </div>
    </div>
  )
}

export default App
