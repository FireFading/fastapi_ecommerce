from sqlalchemy import Column, String
from sqlalchemy_utils import UUIDType

from app.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUIDType(binary=False), primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
