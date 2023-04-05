import uuid

from app.crud import CRUD
from app.database import Base
from sqlalchemy import Column, Float, String
from sqlalchemy_utils import UUIDType


class Product(Base, CRUD):
    __tablename__ = "products"

    product_id = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4())
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    producer = Column(String, nullable=True)
    price = Column(Float, nullable=False)

    def __repr__(self):
        return f"{self.name}"
