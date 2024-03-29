from datetime import datetime, timedelta

import jwt
from app.config import settings


def create_token(email: str) -> str:
    expires_in = (datetime.now() + timedelta(hours=settings.token_expires_hours)).timestamp()
    payload = {"exp": expires_in, "email": email, "is_active": True}
    return jwt.encode(payload=payload, key=settings.secret_key, algorithm=settings.algorithm).decode("utf-8")


def verify_token(token: str) -> bool:
    try:
        token_data = jwt.decode(jwt=token, key=settings.secret_key, algorithms=[settings.algorithm])
    except Exception:
        return False
    expires_in = token_data.get("exp")
    is_active = token_data.get("is_active")
    return bool(datetime.now().timestamp() < expires_in and is_active)


def get_email_from_token(token: str) -> str:
    token_data = jwt.decode(jwt=token, key=settings.secret_key, algorithms=[settings.algorithm])
    return token_data.get("email")
