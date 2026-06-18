from jose import jwt

SECRET_KEY = "devsync-secret-key"
ALGORITHM = "HS256"


def create_access_token(data: dict):
    return jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )