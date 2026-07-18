import TaskCard from './TaskCard'

function TaskList({ tasks, onDelete, onEdit, onStatusChange }) {
  if (!tasks || tasks.length === 0) {
    return (
      <div className="empty-state">
        <p>No tasks yet. Create your first task by clicking the + button above!</p>
      </div>
    )
  }

  return (
    <div className="tasks-grid">
      {tasks.map((task) => (
        <TaskCard 
          key={task.id} 
          task={task} 
          onDelete={onDelete}
          onEdit={onEdit}
          onStatusChange={onStatusChange}
        />
      ))}
    </div>
  )
}

export default TaskList
