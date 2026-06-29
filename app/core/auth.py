from fastapi import Header, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.user_model import User
from app.utils.jwt_handler import verify_token

from app.core.oauth2 import oauth2_scheme

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = verify_token(token)

    user = db.query(User).filter(
        User.email == payload["email"]
    ).first()

    return user