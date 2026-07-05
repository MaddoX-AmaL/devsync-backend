from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from pydantic import BaseModel
from sqlalchemy.orm import Session


from app.dependencies import get_db
from app.models.task_model import Task
from app.schemas.task_schema import TaskCreate, TaskResponse, TaskUpdate

from app.core.auth import get_current_user
from app.models.user_model import User

router = APIRouter()

@router.post("/tasks", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_task = Task(
        title=task.title,
        description=task.description,
        completed=False,
        owner_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@router.get("/tasks", response_model=list[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tasks = db.query(Task).filter(Task.owner_id == current_user.id).all()

    return tasks

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task: TaskUpdate,
    token: str = Header(),   # ADD THIS
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not existing_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if existing_task.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    existing_task.title = task.title
    existing_task.description = task.description
    existing_task.completed = task.completed

    db.commit()
    db.refresh(existing_task)

    return existing_task


@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not existing_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if existing_task.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    db.delete(existing_task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }

@router.get("/tasks/completed")
def get_completed_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    tasks = db.query(Task).filter(
        Task.owner_id == current_user.id,
        Task.completed == True
    ).all()

    return tasks

@router.get("/tasks/pending")
def get_pending_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    tasks = db.query(Task).filter(
        Task.owner_id == current_user.id,
        Task.completed == False
    ).all()

    return tasks

@router.get("/tasks/stats")
def get_task_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    total = db.query(Task).filter(
        Task.owner_id == current_user.id
    ).count()

    completed = db.query(Task).filter(
        Task.owner_id == current_user.id,
        Task.completed == True
    ).count()

    pending = db.query(Task).filter(
        Task.owner_id == current_user.id,
        Task.completed == False
    ).count()

    return {
        "total": total,
        "completed": completed,
        "pending": pending
    }