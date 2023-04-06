import uuid

from app.crud import CRUD
from app.database import Base
from sqlalchemy import Column, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType


class Product(Base, CRUD):
    __tablename__ = "products"

    product_id = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4())
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    producer = Column(String, nullable=True)
    price = Column(Float, nullable=False)

    author_id = Column(UUIDType(binary=False), ForeignKey("users.user_id"))
    author = relationship("User", lazy="joined", backref="products")

    def __repr__(self):
        return f"{self.name}"


fields = [column.name for column in Product.__table__.columns]
