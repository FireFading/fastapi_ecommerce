import uuid

from app.crud import CRUD
from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType


class Rating(Base, CRUD):
    __tablename__ = "ratings"

    guid = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4)
    stars = Column(Integer, default=1)

    user_id = Column(UUIDType(binary=False), ForeignKey("users.guid"))
    product_id = Column(UUIDType(binary=False), ForeignKey("products.guid"))

    user = relationship("User", lazy="joined", backref="ratings")

    def __repr__(self):
        return f"{self.user.email} :: {self.starts}"
