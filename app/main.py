from fastapi import FastAPI
from app.schemas.user_schema import UserCreate
from app.database.database import SessionLocal
from app.models.user_model import User
from app.utils.security import hash_password
from app.schemas.user_schema import UserLogin
from app.utils.security import verify_password
from app.utils.jwt_handler import create_access_token
from app.utils.jwt_handler import verify_token
from fastapi import Header
from app.schemas.user_schema import UserProfile
from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from fastapi import APIRouter
from app.routers.auth import router as auth_router
from app.routers.task import router as task_router

router = APIRouter()

app = FastAPI()
app.include_router(auth_router)
app.include_router(task_router)

@app.get("/")
def root():
    return {"message": "DevSync Backend Running"}


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "DevSync Backend"
    }
