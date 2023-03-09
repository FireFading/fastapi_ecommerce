from pydantic import BaseModel
from sqlalchemy_utils import UUIDType


class Product(BaseModel):
    name: str
    description: str
    producer: str
    price: float
