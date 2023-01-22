from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    email: str
    exp: datetime
