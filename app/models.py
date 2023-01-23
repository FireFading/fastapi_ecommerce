from sqlalchemy import Column, String
from sqlalchemy_utils import UUIDType

from app.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUIDType(binary=False), primary_key=True, index=True)
    email = Column(String, unique=True)
    phone = Column(String, unique=True, nullable=True)
    password = Column(String)

    def __repr__(self):
        return f"Пользователь {self.email}"
