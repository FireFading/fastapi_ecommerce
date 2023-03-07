from app.crud import DBUsers
from app.models import User
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

crud_users = DBUsers()


async def get_user_or_404(email: str, db: AsyncSession) -> User | Exception:
    user = await crud_users.get_user_by_email(db=db, email=email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь с таким Email не существует")
    return user
