import '../styles/TaskCard.css'
import { capitalizeFirstLetter} from '/utils/stringHelpers';

function TaskCard({ task, onDelete, onEdit, onStatusChange }) {
  const getPriorityClass = (priority) => {
    switch(priority?.toLowerCase()) {
      case 'high':
        return 'priority-high'
      case 'medium':
        return 'priority-medium'
      case 'low':
        return 'priority-low'
      default:
        return 'priority-medium'
    }
  }

  const getStatusClass = (status) => {
    switch(status?.toLowerCase()) {
      case 'completed':
        return 'status-completed'
      case 'wip':
        return 'status-wip'
      case 'pending':
        return 'status-pending'
      default:
        return 'status-pending'
    }
  }

  const formatDate = (dateString) => {
    if (!dateString) return 'No date'
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      year: 'numeric' 
    })
  }

  const nextStatusMap = {
    'pending': 'WIP',
    'WIP': 'completed',
    'completed': 'pending'
  }

  const getNextStatus = () => nextStatusMap[task.status] || 'pending'

  let taskStausButton = ['pending' , 'WIP', 'completed'];
  if (task.status){
    taskStausButton = taskStausButton.filter(status => status !== task.status);
  }
  
  return (
    <div className="task-card">
      <div className="task-header">
        <h3 className="long-title">{task.title}</h3>
        <div className="task-actions">
          <button 
            onClick={() => onEdit(task)}
            className="edit-btn"
            title="Edit task"
          >
            ✎
          </button>
          <button 
            onClick={() => onDelete(task.id)}
            className="delete-btn"
            title="Delete task"
          >
            ✕
          </button>
        </div>
      </div>

      <div className="task-meta">
        <div>
            <span className={`priority-badge ${getPriorityClass(task.priority)}`}>
            {capitalizeFirstLetter(task.priority)}
            </span>
            <span className={`status-badge ${getStatusClass(task.status)}`}>
            {capitalizeFirstLetter(task.status)}
            </span>
        </div>
        <div className="task-status-buttons">
          {taskStausButton.map((status) => (
            <button 
              key={status}
              onClick={() => onStatusChange(task.id, status)} 
              className={`status-toggle ${status.toLowerCase()}`}
              title={`Mark as ${status}`}
            >
              {status.charAt(0).toUpperCase()}
            </button>
          ))}
        </div>
       
      </div>
      <div>
         <span>
            {task.due_date && (
                <div className="task-due-date">
                <span > Due Date: </span>📅 {formatDate(task.due_date)}
                </div>
            )}
        </span>
        </div>
      
      {task.description && (
        <p className="task-description truncate-multi">{task.description}</p>
      )}

     

     
    </div>
  )
}

export default TaskCard
