import uuid

from pydantic import BaseModel


class Order(BaseModel):
    guid: uuid.UUID
    user_id: uuid.UUID


class ShowOrderItem(BaseModel):
    quantity: int
    product: uuid.UUID

    class Config:
        orm_mode = True
