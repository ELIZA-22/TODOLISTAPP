import { useState } from 'react'
import './TodoForm.css'

function TodoForm({ onAdd }) {
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [priority, setPriority] = useState('medium')
  const [notes, setNotes] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    
    if (!title.trim()) {
      alert('Please enter a title')
      return
    }

    onAdd({
      title: title.trim(),
      description: description.trim() || null,
      priority: priority,
      notes: notes.trim() || null
    })

    setTitle('')
    setDescription('')
    setPriority('medium')
    setNotes('')
  }

  return (
    <form onSubmit={handleSubmit} className="todo-form">
      <div className="form-group">
        <input
          type="text"
          placeholder="What needs to be done?"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="form-input"
          autoFocus
        />
      </div>
      
      <div className="form-group">
        <input
          type="text"
          placeholder="Description (optional)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="form-input"
        />
      </div>

      <div className="form-group">
        <select
          value={priority}
          onChange={(e) => setPriority(e.target.value)}
          className="form-select"
        >
          <option value="low">Low Priority</option>
          <option value="medium">Medium Priority</option>
          <option value="high">High Priority</option>
          <option value="urgent">Urgent</option>
        </select>
      </div>

      <div className="form-group">
        <textarea
          placeholder="Additional notes (optional)"
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          className="form-textarea"
          rows="3"
        />
      </div>

      <button type="submit" className="btn-add">
        + Add Todo
      </button>
    </form>
  )
}

export default TodoForm
