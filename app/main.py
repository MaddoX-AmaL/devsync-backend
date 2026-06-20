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

app = FastAPI()


@app.get("/")
def root():
    return {"message": "DevSync Backend Running"}


@app.post("/signup")
def signup(user: UserCreate):

    db = SessionLocal()

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

@app.post("/login")
def login(user: UserLogin):

    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:
        return {
            "message": "Invalid email or password"
        }

    if not verify_password(
        user.password,
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
    "access_token": token
    }

@app.get("/profile", response_model=UserProfile)
def profile(token: str = Header()):

    payload = verify_token(token)

    db = SessionLocal()

    user = db.query(User).filter(
      User.email == payload["email"]
    ).first()

    return {
    "id": user.id,
    "name": user.name,
    "email": user.email
}
