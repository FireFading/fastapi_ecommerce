from app.models.users import User as m_User
from app.utils.messages import messages
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_or_404(email: str, session: AsyncSession) -> m_User | Exception:
    if not (user := await m_User.get(session=session, email=email)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.USER_NOT_FOUND)
    return user
