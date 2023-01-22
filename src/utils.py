from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"
JWT_SECRET_KEY = "secret"
JWT_REFRESH_SECRET_KEY = "secret2"


def get_hashed_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password, hashed_password)


def create_access_token(user: str, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_in = datetime.now(timezone.utc) + expires_delta
    else:
        expires_in = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"expires_in": expires_in, "sub": user}
    return jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)


def create_refresh_token(user: str, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_in = datetime.now(timezone.utc) + expires_delta
    else:
        expires_in = datetime.now(timezone.utc) + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"expires_in": expires_in, "user": user}
    return jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
