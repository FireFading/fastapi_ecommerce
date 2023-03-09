from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUD
from app.models.users import User as m_User


class DBUsers(CRUD):
    async def create(self, db: AsyncSession, user: m_User) -> m_User:
        db.add(user)
        await db.flush()
        await db.commit()

        return user

    async def get(self, db: AsyncSession) -> list[m_User]:
        result = await db.execute(select(m_User))
        return result.scalars().all()

    async def get_user_by_email(self, db: AsyncSession, email: str) -> m_User:
        result = await db.execute(select(m_User).filter(m_User.email == email))
        return result.scalars().first()

    async def update_profile(self, db: AsyncSession, user: m_User, updated_fields: dict):
        for key, value in updated_fields.items():
            setattr(user, key, value)
        await db.flush()
        await db.commit()

    async def activate_account(self, db: AsyncSession, user: m_User):
        user.is_active = True
        await db.flush()
        await db.commit()

    async def delete(self, db: AsyncSession, user: m_User):
        await db.delete(user)
        await db.commit()
