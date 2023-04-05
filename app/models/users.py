import bcrypt
from app.crud import CRUD
from app.database import Base
from sqlalchemy import Boolean, Column, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_utils import UUIDType


class User(Base, CRUD):
    __tablename__ = "users"

    user_id = Column(UUIDType(binary=False), primary_key=True, index=True)
    is_active = Column(Boolean, default=False)
    email = Column(String, unique=True)
    phone = Column(String, unique=True, nullable=True)
    password = Column(String)
    name = Column(String, unique=False, nullable=True)

    def __repr__(self):
        return f"Пользователь {self.email}"

    def get_hashed_password(self) -> str:
        return bcrypt.hashpw(self.password.encode(), bcrypt.gensalt())

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(self.password.encode(), password)

    async def create(self, session: AsyncSession):
        self.password = self.get_hashed_password()
        return await super().create(session=session)

    async def update(self, session: AsyncSession):
        self.password = self.get_hashed_password()
        return await super().update(session=session)
