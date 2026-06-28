from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.task_model import Task
from app.models.user_model import User
from app.routers import task

router = APIRouter()

@router.get("/test")
def test(
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == 5
    ).first()

    return {
        "task": task.title,
        "owner": task.owner.name
    }