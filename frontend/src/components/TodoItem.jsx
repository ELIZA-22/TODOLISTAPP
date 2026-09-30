import { useState } from 'react'
import './TodoItem.css'

function TodoItem({ todo, onToggle, onDelete, onUpdate }) {
  const [isEditing, setIsEditing] = useState(false)
  const [editTitle, setEditTitle] = useState(todo.title)
  const [editDescription, setEditDescription] = useState(todo.description || '')
  const [editPriority, setEditPriority] = useState(todo.priority || 'medium')
  const [editNotes, setEditNotes] = useState(todo.notes || '')

  const handleEdit = () => {
    setIsEditing(true)
  }

  const handleSave = () => {
    if (editTitle.trim()) {
      onUpdate(todo.id, {
        title: editTitle.trim(),
        description: editDescription.trim() || null,
        priority: editPriority,
        notes: editNotes.trim() || null
      })
      setIsEditing(false)
    }
  }

  const handleCancel = () => {
    setEditTitle(todo.title)
    setEditDescription(todo.description || '')
    setEditPriority(todo.priority || 'medium')
    setEditNotes(todo.notes || '')
    setIsEditing(false)
  }

  const getPriorityBadge = (priority) => {
    const badges = {
      urgent: { text: 'Urgent', className: 'priority-urgent' },
      high: { text: 'High', className: 'priority-high' },
      medium: { text: 'Medium', className: 'priority-medium' },
      low: { text: 'Low', className: 'priority-low' }
    }
    return badges[priority] || badges.medium
  }

  if (isEditing) {
    return (
      <div className="todo-item editing">
        <div className="edit-form">
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            className="edit-input"
            placeholder="Title"
            autoFocus
          />
          <input
            type="text"
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            placeholder="Description (optional)"
            className="edit-input"
          />
          <select
            value={editPriority}
            onChange={(e) => setEditPriority(e.target.value)}
            className="edit-select"
          >
            <option value="low">Low Priority</option>
            <option value="medium">Medium Priority</option>
            <option value="high">High Priority</option>
            <option value="urgent">Urgent</option>
          </select>
          <textarea
            value={editNotes}
            onChange={(e) => setEditNotes(e.target.value)}
            placeholder="Notes (optional)"
            className="edit-textarea"
            rows="3"
          />
          <div className="edit-actions">
            <button onClick={handleSave} className="btn-save">Save</button>
            <button onClick={handleCancel} className="btn-cancel">Cancel</button>
          </div>
        </div>
      </div>
    )
  }

  const badge = getPriorityBadge(todo.priority)

  return (
    <div className={`todo-item ${todo.completed ? 'completed' : ''}`}>
      <div className="todo-content">
        <input
          type="checkbox"
          checked={todo.completed}
          onChange={() => onToggle(todo.id, todo.completed)}
          className="todo-checkbox"
        />
        <div className="todo-text">
          <div className="todo-header">
            <h3 className="todo-title">{todo.title}</h3>
            <span className={`priority-badge ${badge.className}`}>
              {badge.text}
            </span>
          </div>
          {todo.description && (
            <p className="todo-description">{todo.description}</p>
          )}
          {todo.notes && (
            <div className="todo-notes">
              <span className="notes-icon">📝</span>
              <span className="notes-text">{todo.notes}</span>
            </div>
          )}
        </div>
      </div>
      <div className="todo-actions">
        <button onClick={handleEdit} className="btn-edit" title="Edit">
          ✏️
        </button>
        <button onClick={() => onDelete(todo.id)} className="btn-delete" title="Delete">
          🗑️
        </button>
      </div>
    </div>
  )
}

export default TodoItem
