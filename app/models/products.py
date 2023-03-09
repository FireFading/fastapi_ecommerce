from sqlalchemy import Column, Float, String
from sqlalchemy_utils import UUIDType

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(UUIDType(binary=False), primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    producer = Column(String, nullable=True)
    price = Column(Float, nullable=False)

    def __repr__(self):
        return f"{self.name}"
