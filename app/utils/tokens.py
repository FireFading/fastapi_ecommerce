from datetime import datetime, timedelta, timezone

import jwt

from app.settings import settings


def create_token(email: str) -> str:
    expires_in = (datetime.now(timezone.utc) + timedelta(hours=settings.token_expire_hours)).timestamp()
    to_encode = {"exp": expires_in, "email": email, "is_active": True}
    return jwt.encode(to_encode, settings.secret_key, settings.algorithm).decode("utf-8")


def verify_token(token: str) -> bool:
    try:
        token_data = jwt.decode(jwt=token, key=settings.secret_key, algorithms=[settings.algorithm])
    except jwt.exceptions.ExpiredSignatureError:
        return False
    expires_in = token_data.get("exp")
    is_active = token_data.get("is_active")
    return bool(datetime.now(timezone.utc).timestamp() < expires_in and is_active)


def get_email_from_token(token: str) -> str:
    token_data = jwt.decode(jwt=token, key=settings.secret_key, algorithms=[settings.algorithm])
    return token_data.get("email")
