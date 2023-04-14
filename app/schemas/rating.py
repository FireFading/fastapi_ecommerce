import uuid

from app.schemas.users import User
from pydantic import BaseModel


class Rating(BaseModel):
    stars: int
    user: User
    product_id: uuid.UUID

    class Config:
        orm_mode = True


class CreateRating(BaseModel):
    stars: int
    product_id: uuid.UUID
