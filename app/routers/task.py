from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.task_model import Task
from app.schemas.task_schema import TaskCreate, TaskResponse

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