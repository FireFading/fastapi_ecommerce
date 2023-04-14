import uuid

from app.crud import CRUD
from app.database import Base
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy_utils import UUIDType


class Product(Base, CRUD):
    __tablename__ = "products"

    guid = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    producer = Column(String, nullable=True)
    price = Column(Float, nullable=False)

    avg_rating = Column(Float, nullable=True)
    reviews_count = Column(Integer, default=0)

    user_id = Column(UUIDType(binary=False), ForeignKey("users.guid"))

    def __repr__(self):
        return f"{self.name}"

    def upgrade_rating(self, rating: float):
        if self.avg_rating is None:
            self.avg_rating = rating
        else:
            self.avg_rating = (self.avg_rating * self.reviews_count + rating) / (self.reviews_count + 1)
        self.reviews_count += 1

    def downgrade_rating(self, rating: float):
        if self.reviews_count > 1:
            self.avg_rating = (self.avg_rating * self.reviews_count - rating) / (self.reviews_count - 1)
        else:
            self.avg_rating = 0
        self.reviews_count -= 1


fields = [column.name for column in Product.__table__.columns]
