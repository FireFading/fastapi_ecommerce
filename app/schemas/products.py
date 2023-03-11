from pydantic import BaseModel


class Product(BaseModel):
    name: str
    description: str
    producer: str
    price: float
