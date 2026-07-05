from fastapi import APIRouter, Header
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.task_model import Task
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserLogin, UserProfile
from app.utils.jwt_handler import create_access_token, verify_token
from app.utils.security import hash_password, verify_password
router = APIRouter()
from app.core.auth import get_current_user
from fastapi.security import OAuth2PasswordRequestForm

@router.post("/signup")
def signup(user: UserCreate,db: Session = Depends(get_db)):

    

    existing_user = db.query(User).filter(
      User.email == user.email
    ).first()

    if existing_user:
      return {
        "message": "Email already registered"
    }

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()

    return {
        "message": "User created successfully"
    }

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not existing_user:
        return {
            "message": "Invalid email or password"
        }

    if not verify_password(
        form_data.password,
        existing_user.password
    ):
        return {
            "message": "Invalid email or password"
        }

    token = create_access_token(
        {
            "email": existing_user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/profile", response_model=UserProfile)
def profile(token: str = Header(),db: Session = Depends(get_db)):

    payload = verify_token(token)
    
    user = db.query(User).filter(
      User.email == payload["email"]
    ).first()

    return {
    "id": user.id,
    "name": user.name,
    "email": user.email
}


@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }

@router.get("/tasks/count")
def count_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total = db.query(Task).filter(
        Task.owner_id == current_user.id
    ).count()

    return {
        "total_tasks": total
    }