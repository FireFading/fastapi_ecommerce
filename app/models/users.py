from fastapi import HTTPException, status
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import validates
from sqlalchemy_utils import UUIDType

from app.database import Base

MAX_NAME_LEN = 100


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUIDType(binary=False), primary_key=True, index=True)
    is_active = Column(Boolean)
    email = Column(String, unique=True)
    phone = Column(String, unique=True, nullable=True)
    password = Column(String)
    name = Column(String, unique=False, nullable=True)

    def __repr__(self):
        return f"Пользователь {self.email}"

    @validates("name")
    def validate_name(self, key, name) -> str:
        if not name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{key} field is empty")
        if len(name) > MAX_NAME_LEN:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{key} max symbol's")
        return name
