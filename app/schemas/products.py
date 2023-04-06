from app.models.products import fields
from pydantic import BaseModel, validator


class Product(BaseModel):
    name: str
    description: str
    producer: str
    price: float

    class Config:
        orm_mode = True


class ProductParams(BaseModel):
    from_price: float | None = None
    to_price: float | None = None
    order_by: str = "price"

    @validator("from_price", "to_price")
    def validate_price(cls, value: float | None = None) -> float | None:
        if not value:
            return None
        if value <= 0:
            raise ValueError("price can't be negative")
        return value

    @validator("order_by")
    def validate_order_by(cls, value: str | None) -> str | None:
        if value is not None:
            if value[1:] not in fields and value not in fields:
                raise ValueError("product model didn't have this field")
        return value
