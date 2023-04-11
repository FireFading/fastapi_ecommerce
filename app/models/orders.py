import uuid

from app.crud import CRUD
from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy_utils import UUIDType


class Order(Base, CRUD):
    __tablename__ = "orders"

    guid = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4)

    user_id = Column(UUIDType(binary=False), ForeignKey("users.guid"))


class OrderItem(Base, CRUD):
    __tablename__ = "order_items"

    guid = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4)
    quantity = Column(Integer, default=1)

    order_id = Column(UUIDType(binary=False), ForeignKey("orders.guid"))
    product_id = Column(UUIDType(binary=False), ForeignKey("products.guid"))
