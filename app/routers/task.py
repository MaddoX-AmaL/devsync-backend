from fastapi import APIRouter, Depends
from pydantic import BaseModel
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.task_model import Task
from app.schemas.task_schema import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter()

@router.post("/tasks", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    new_task = Task(
        title=task.title,
        description=task.description,
        completed=False,
        owner_id=1
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@router.get("/tasks", response_model=list[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db)
):
    tasks = db.query(Task).all()

    return tasks

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db)
):
    existing_task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    existing_task.title = task.title
    existing_task.description = task.description
    existing_task.completed = task.completed

    db.commit()
    db.refresh(existing_task)

    return existing_task

@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)

):
    existing_task = db.query(Task).filter(
    Task.id == task_id
).first()
    db.delete(existing_task)
    db.commit()
    return {
    "message": "Task deleted successfully"
}