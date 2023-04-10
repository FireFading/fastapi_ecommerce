import uuid

from app.crud import CRUD
from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType


class Rating(Base, CRUD):
    __tablename__ = "ratings"

    rating_id = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4)
    stars = Column(Integer)

    author_id = Column(UUIDType(binary=False), ForeignKey("users.user_id"))
    author = relationship("User", lazy="joined", backref="ratings")

    product_id = Column(UUIDType(binary=False), ForeignKey("products.product_id"))
    product = relationship("Product", lazy="joined", backref="ratings")

    def __repr__(self):
        return f"{self.author.email} :: {self.starts}"
