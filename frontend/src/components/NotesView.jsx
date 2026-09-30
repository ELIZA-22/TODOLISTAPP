import { useState, useEffect } from 'react'
import axios from 'axios'
import './NotesView.css'

const NOTES_API_URL = import.meta.env.VITE_API_URL ? `${import.meta.env.VITE_API_URL.replace('/todos', '')}/notes` : 'http://localhost:8000/api/notes'

function NotesView() {
  const [notes, setNotes] = useState([])
  const [selectedNote, setSelectedNote] = useState(null)
  const [editingTitle, setEditingTitle] = useState('')
  const [editingContent, setEditingContent] = useState('')
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchNotes()
  }, [])

  const fetchNotes = async () => {
    try {
      const response = await axios.get(NOTES_API_URL)
      setNotes(response.data)
    } catch (err) {
      setError('Failed to fetch notes')
      console.error('Error fetching notes:', err)
    }
  }

  const handleSelectNote = (note) => {
    setSelectedNote(note)
    setEditingTitle(note.title)
    setEditingContent(note.content || '')
  }

  const handleNewNote = () => {
    setSelectedNote({ isNew: true }) // Use a flag instead of null
    setEditingTitle('')
    setEditingContent('')
  }

  const handleSaveNote = async () => {
    if (!editingTitle.trim()) {
      alert('Please enter a title')
      return
    }

    try {
      if (selectedNote && !selectedNote.isNew) {
        // Update existing note
        const response = await axios.put(`${NOTES_API_URL}/${selectedNote.id}`, {
          title: editingTitle.trim(),
          content: editingContent.trim() || null
        })
        setNotes(notes.map(n => n.id === selectedNote.id ? response.data : n))
        setSelectedNote(response.data)
      } else {
        // Create new note
        const response = await axios.post(NOTES_API_URL, {
          title: editingTitle.trim(),
          content: editingContent.trim() || null
        })
        setNotes([response.data, ...notes])
        setSelectedNote(response.data)
      }
    } catch (err) {
      setError('Failed to save note')
      console.error('Error saving note:', err)
    }
  }

  const handleDeleteNote = async (noteId) => {
    if (!confirm('Delete this note?')) return

    try {
      await axios.delete(`${NOTES_API_URL}/${noteId}`)
      setNotes(notes.filter(n => n.id !== noteId))
      if (selectedNote?.id === noteId) {
        handleNewNote()
      }
    } catch (err) {
      setError('Failed to delete note')
      console.error('Error deleting note:', err)
    }
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
  }

  return (
    <div className="notes-view">
      {error && (
        <div className="notes-error">
          {error}
          <button onClick={() => setError(null)}>×</button>
        </div>
      )}

      <div className="notes-layout">
        {/* Notes Sidebar */}
        <div className="notes-sidebar">
          <div className="sidebar-header">
            <h3>All Notes</h3>
            <button className="btn-new-note" onClick={handleNewNote}>
              + New
            </button>
          </div>

          {notes.length === 0 ? (
            <div className="notes-empty">
              <p>📝</p>
              <p>No notes yet</p>
              <button className="btn-create-first" onClick={handleNewNote}>
                Create your first note
              </button>
            </div>
          ) : (
            <div className="notes-list">
              {notes.map(note => (
                <div
                  key={note.id}
                  className={`note-card ${selectedNote?.id === note.id ? 'selected' : ''}`}
                  onClick={() => handleSelectNote(note)}
                >
                  <div className="note-card-header">
                    <h4 className="note-card-title">{note.title}</h4>
                    <button
                      className="btn-delete-note"
                      onClick={(e) => {
                        e.stopPropagation()
                        handleDeleteNote(note.id)
                      }}
                    >
                      🗑️
                    </button>
                  </div>
                  {note.content && (
                    <p className="note-card-preview">
                      {note.content.substring(0, 80)}
                      {note.content.length > 80 && '...'}
                    </p>
                  )}
                  <div className="note-card-date">
                    {formatDate(note.updated_at)}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Notes Editor */}
        <div className="notes-editor">
          {!selectedNote ? (
            <div className="editor-placeholder">
              <div className="placeholder-icon">📝</div>
              <h3>Create a new note</h3>
              <p>Click "New" to start writing</p>
            </div>
          ) : (
            <>
              <input
                type="text"
                className="editor-title-input"
                placeholder="Note title..."
                value={editingTitle}
                onChange={(e) => setEditingTitle(e.target.value)}
              />
              <textarea
                className="editor-textarea"
                placeholder="Start writing your note...&#10;&#10;• Ideas and thoughts&#10;• Meeting notes&#10;• Quick reminders&#10;• Anything you want to remember"
                value={editingContent}
                onChange={(e) => setEditingContent(e.target.value)}
              />
              <div className="editor-actions">
                <button onClick={handleSaveNote} className="btn-save-note">
                  💾 {selectedNote.isNew ? 'Save' : 'Update'} Note
                </button>
                <div className="editor-info">
                  {editingContent.length} characters
                  {selectedNote && !selectedNote.isNew && (
                    <span> • Last updated: {formatDate(selectedNote.updated_at)}</span>
                  )}
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default NotesView
