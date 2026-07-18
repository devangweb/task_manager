import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import TaskForm from '../components/TaskForm'
import TaskList from '../components/TaskList'
import Header from '../components/Header'
import '../styles/TaskManager.css'
import { API_BASE_URL } from '../config'

function TaskManager() {
  const [user, setUser] = useState(null)
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [showEditForm, setShowEditForm] = useState(false)
  const [editingTask, setEditingTask] = useState(null)
  const [statusFilter, setStatusFilter] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    fetchUserInfo()
    fetchTasks()
  }, [statusFilter])

  const fetchUserInfo = async () => {
    try {
      const token = localStorage.getItem('token')
      // You can add an endpoint to get current user info here
      fetch(`${API_BASE_URL}/auth/me`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      .then(response => response.json())
      .then(data => setUser(data))
    } catch (err) {
        
      console.error('Error fetching user:', err)
    }
  }

  const fetchTasks = async () => {
    try {
      const token = localStorage.getItem('token')
      let url = `${API_BASE_URL}/tasks`
      if (statusFilter) {
        url += `?status_filter=${statusFilter}`
      }
      
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        const data = await response.json()
        setTasks(data || [])
      }
    } catch (err) {
      console.error('Error fetching tasks:', err)
      setTasks([])
    } finally {
      setLoading(false)
    }
  }

  const handleCreateTask = async (taskData) => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch(`${API_BASE_URL}/tasks`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
      })

      if (response.ok) {
        const newTask = await response.json()
        setTasks([...tasks, newTask])
        setShowForm(false)
      } else {
        throw new Error('Failed to create task')
      }
    } catch (err) {
      console.error('Error creating task:', err)
      alert('Failed to create task')
    }
  }

  const handleEditTask = async (taskId, taskData) => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
      })

      if (response.ok) {
        const updatedTask = await response.json()
        setTasks(tasks.map(task => task.id === taskId ? updatedTask : task))
        setShowEditForm(false)
        setEditingTask(null)
      } else {
        throw new Error('Failed to update task')
      }
    } catch (err) {
      console.error('Error updating task:', err)
      alert('Failed to update task')
    }
  }

  const handleDeleteTask = async (taskId) => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return
    }

    try {
      const token = localStorage.getItem('token')
      const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        setTasks(tasks.filter(task => task.id !== taskId))
      }
    } catch (err) {
      console.error('Error deleting task:', err)
    }
  }

  const handleUpdateStatus = async (taskId, newStatus) => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch(`${API_BASE_URL}/tasks/${taskId}/status`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus }),
      })

      if (response.ok) {
        const updatedTask = await response.json()
        setTasks(tasks.map(task => task.id === taskId ? updatedTask : task))
      }
    } catch (err) {
      console.error('Error updating task status:', err)
    }
  }

  const handleLogout = async () => {
    try {
      const token = localStorage.getItem('token')
      await fetch(`${API_BASE_URL}/auth/logout`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      })
    } catch (err) {
      console.error('Error during logout:', err)
    } finally {
      localStorage.removeItem('token')
      localStorage.removeItem('token_type')
      navigate('/login')
    }
  }

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  return (
    
    <div className="task-manager-container">
        {  <Header userdata={user} handleLogout={handleLogout} />}
  
      <main className="main-content">
        <div className="tasks-section">
          <div className="section-header">
            <h2>Your Tasks</h2>
            <button 
              onClick={() => setShowForm(!showForm)} 
              className="create-btn"
              title="Create new task"
            >
              <span className="plus-icon">+</span>
            </button>
          </div>

          <div className="filter-bar">
            <label>Filter by Status:</label>
            <button 
              className={`filter-btn ${!statusFilter ? 'active' : ''}`}
              onClick={() => setStatusFilter(null)}
            >
              All
            </button>
            <button 
              className={`filter-btn ${statusFilter === 'pending' ? 'active' : ''}`}
              onClick={() => setStatusFilter('pending')}
            >
              Pending
            </button>
            <button 
              className={`filter-btn ${statusFilter === 'WIP' ? 'active' : ''}`}
              onClick={() => setStatusFilter('WIP')}
            >
              WIP
            </button>
            <button 
              className={`filter-btn ${statusFilter === 'completed' ? 'active' : ''}`}
              onClick={() => setStatusFilter('completed')}
            >
              Completed
            </button>
          </div>

          {showForm && (
            <TaskForm 
              onSubmit={handleCreateTask}
              onCancel={() => setShowForm(false)}
            />
          )}

          {showEditForm && editingTask && (
            <TaskForm 
              task={editingTask}
              onSubmit={(data) => handleEditTask(editingTask.id, data)}
              onCancel={() => {
                setShowEditForm(false)
                setEditingTask(null)
              }}
              isEditing={true}
            />
          )}

          <TaskList 
            tasks={tasks}
            onDelete={handleDeleteTask}
            onEdit={(task) => {
              setEditingTask(task)
              setShowEditForm(true)
            }}
            onStatusChange={handleUpdateStatus}
          />
        </div>
      </main>
    </div>
  )
}

export default TaskManager
