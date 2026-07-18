from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime
from core.database import get_db
from models.task import Task
from schemas.task import TaskCreate, TaskUpdate, TaskStatusUpdate, TaskResponse
from api.dependencies import get_current_user
from models.user import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("", response_model=list[TaskResponse])
def get_tasks(
    status_filter: str = Query(None, description="Filter by status: pending, WIP, completed"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all non-deleted tasks for the current user, optionally filtered by status"""
    query = db.query(Task).filter(
        Task.user_id == current_user.id,
        Task.deleted_at.is_(None)
    )
    
    if status_filter:
        query = query.filter(Task.status == status_filter)
    
    tasks = query.all()
    return tasks

@router.get("/deleted", response_model=list[TaskResponse])
def get_deleted_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all deleted (soft deleted) tasks for the current user"""
    tasks = db.query(Task).filter(
        Task.user_id == current_user.id,
        Task.deleted_at.isnot(None)
    ).all()
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific task by ID"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id,
        Task.deleted_at.is_(None)
    ).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new task"""
    due_date = None
    if task.due_date:
        try:
            due_date = datetime.fromisoformat(task.due_date.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            due_date = None

    new_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        status=task.status,
        due_date=due_date,
        user_id=current_user.id
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an existing task"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id,
        Task.deleted_at.is_(None)
    ).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.priority is not None:
        task.priority = task_data.priority
    if task_data.status is not None:
        task.status = task_data.status
    if task_data.due_date is not None:
        try:
            task.due_date = datetime.fromisoformat(task_data.due_date.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            task.due_date = None
    
    db.commit()
    db.refresh(task)
    return task

@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_task_status(
    task_id: int,
    status_data: TaskStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Quick update of task status"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id,
        Task.deleted_at.is_(None)
    ).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    task.status = status_data.status
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Soft delete a task"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id,
        Task.deleted_at.is_(None)
    ).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    task.deleted_at = datetime.utcnow()
    db.commit()
    return None

@router.post("/{task_id}/restore", response_model=TaskResponse)
def restore_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Restore a soft deleted task"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id,
        Task.deleted_at.isnot(None)
    ).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deleted task not found"
        )
    
    task.deleted_at = None
    db.commit()
    db.refresh(task)
    return task
