from app.config import jwt_settings
from app.database import get_session
from app.models.users import User as m_User
from app.schemas.users import Email, Name, Phone, User
from app.utils.exceptions import get_user_or_404
from app.utils.messages import messages
from fastapi import APIRouter, Depends, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/accounts/profile",
    tags=["accounts"],
    responses={404: {"description": "Not found"}},
)
security = HTTPBearer()


@AuthJWT.load_config
def get_jwt_settings():
    return jwt_settings


@router.get(
    "/",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Получение информации о пользователе",
)
async def user_info(
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    authorize.jwt_required()
    email = authorize.get_jwt_subject()
    user = await m_User.get(session=session, email=email)
    return {"email": user.email, "phone": user.phone, "name": user.name}


@router.post(
    "/update/email/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Обновление Email в профиле",
)
async def update_email(
    data: Email,
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    authorize.jwt_required()
    email = authorize.get_jwt_subject()
    user = await get_user_or_404(email=email, session=session)
    user.email = data.email
    await user.update(session=session)
    return {
        "access_token": authorize.create_access_token(subject=data.email),
        "refresh_token": authorize.create_access_token(subject=data.email),
    }


@router.post(
    "/update/phone/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Обновление телефона в профиле",
)
async def update_phone(
    data: Phone,
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    authorize.jwt_required()
    email = authorize.get_jwt_subject()
    user = await get_user_or_404(email=email, session=session)
    user.phone = data.phone
    await user.update_profile(session=session)
    return {"detail": messages.PHONE_UPDATED}


@router.post(
    "/update/name/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Обновление имени в профиле",
)
async def update_name(
    data: Name,
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    authorize.jwt_required()
    email = authorize.get_jwt_subject()
    user = await get_user_or_404(email=email, session=session)
    user.name = data.name
    await user.update(session=session)
    return {"detail": messages.NAME_UPDATED}


@router.delete("/delete/", status_code=status.HTTP_200_OK, summary="Удаление профиля")
async def delete_profile(
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    authorize.jwt_required()
    email = authorize.get_jwt_subject()
    user = await get_user_or_404(email=email, session=session)
    await user.delete(session=session)
    return {"detail": messages.PROFILE_DELETED}
