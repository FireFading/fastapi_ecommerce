from abc import abstractmethod

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select as f_select

from app.models import User as m_User


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

    async def update_email(self, db: AsyncSession, user: m_User, new_email: str):
        user.email = new_email
        await db.flush()
        await db.commit()

    async def update_phone(self, db: AsyncSession, user: m_User, new_phone: str):
        user.phone = new_phone
        await db.flush()
        await db.commit()

    async def update_password(
        self, db: AsyncSession, user: m_User, new_hashed_password: str
    ):
        user.password = new_hashed_password
        await db.flush()
        await db.commit()

    async def activate_account(self, db: AsyncSession, user: m_User):
        user.is_active = True
        await db.flush()
        await db.commit()

    async def delete(self, db: AsyncSession, user: m_User):
        await db.delete(user)
        await db.commit()

    async def get_user_by_email(self, db: AsyncSession, email: str) -> m_User:
        result = await db.execute(select(m_User).filter(m_User.email == email))
        return result.scalars().first()
