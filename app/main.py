from fastapi import FastAPI
from app.schemas.user_schema import UserCreate

app = FastAPI()


@app.get("/")
def root():
    return {"message": "DevSync Backend Running"}


@app.post("/signup")
def signup(user: UserCreate):
    return {
        "message": "User created successfully",
        "user": user
    }