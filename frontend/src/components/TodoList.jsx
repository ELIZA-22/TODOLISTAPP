import { DragDropContext, Droppable, Draggable } from '@hello-pangea/dnd'
import TodoItem from './TodoItem'
import './TodoList.css'

function TodoList({ todos, onToggle, onDelete, onUpdate, onReorder }) {
  if (todos.length === 0) {
    return (
      <div className="empty-state">
        <p>🎉 No todos yet! Add one to get started.</p>
      </div>
    )
  }

  const handleDragEnd = (result) => {
    if (!result.destination) return

    const items = Array.from(todos)
    const [reorderedItem] = items.splice(result.source.index, 1)
    items.splice(result.destination.index, 0, reorderedItem)

    // Call the reorder function with new order
    onReorder(items.map(item => item.id))
  }

  return (
    <DragDropContext onDragEnd={handleDragEnd}>
      <Droppable droppableId="todos">
        {(provided, snapshot) => (
          <div
            className={`todo-list ${snapshot.isDraggingOver ? 'dragging-over' : ''}`}
            {...provided.droppableProps}
            ref={provided.innerRef}
          >
            {todos.map((todo, index) => (
              <Draggable key={todo.id} draggableId={todo.id} index={index}>
                {(provided, snapshot) => (
                  <div
                    ref={provided.innerRef}
                    {...provided.draggableProps}
                    {...provided.dragHandleProps}
                    className={snapshot.isDragging ? 'dragging' : ''}
                  >
                    <TodoItem
                      todo={todo}
                      onToggle={onToggle}
                      onDelete={onDelete}
                      onUpdate={onUpdate}
                    />
                  </div>
                )}
              </Draggable>
            ))}
            {provided.placeholder}
          </div>
        )}
      </Droppable>
    </DragDropContext>
  )
}

export default TodoList
