from abc import abstractmethod

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select as f_select

from src.models import User as m_User


class CRUD:
    @abstractmethod
    async def get(self, *args):
        pass

    @abstractmethod
    async def create(self, *args):
        pass

    @abstractmethod
    async def update(self, *args):
        pass

    @abstractmethod
    async def delete(self, *args):
        pass


class DBUsers(CRUD):
    async def get(self, db: AsyncSession) -> list[m_User]:
        result = await db.execute(select(m_User))
        return result.scalars().all()

    async def create(self, db: AsyncSession, db_user: m_User) -> m_User:
        db.add(db_user)
        await db.flush()
        await db.commit()

        return db_user

    async def update(self, db: AsyncSession, user: m_User, updated_fields: dict):
        for field, new_value in updated_fields.items():
            user[field] = new_value
        await db.flush()
        await db.commit()

    async def delete(self, db: AsyncSession, user: m_User):
        await db.delete(user)
        await db.commit()

    async def get_user_by_email(self, db: AsyncSession, email: str) -> m_User:
        result = await db.execute(select(m_User).filter(m_User.email == email))
        return result.scalars().first()
