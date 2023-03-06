from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import DBUsers
from app.database import get_session
from app.models import User as m_User
from app.schemas import Email, Phone, User
from app.settings import JWTSettings, settings

crud_users = DBUsers()


router = APIRouter(prefix="/accounts/profile", tags=["accounts"], responses={404: {"description": "Not found"}})


@AuthJWT.load_config
def get_jwt_settings():
    return JWTSettings()


@router.get("/", response_model=User, status_code=status.HTTP_200_OK, summary="Получение информации о пользователе")
async def user_info(db: AsyncSession = Depends(get_session), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    email = authorize.get_jwt_subject()
    user = await crud_users.get_user_by_email(db=db, email=email)
    user_info = {"email": user.email, "phone": user.phone}
    return JSONResponse(status_code=status.HTTP_200_OK, content=user_info)


@router.post("/update-email/", status_code=status.HTTP_202_ACCEPTED, summary="Обновление Email в профиле")
async def update_email(data: Email, db: AsyncSession = Depends(get_session), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    email = authorize.get_jwt_subject()
    user = await crud_users.get_user_by_email(db=db, email=email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    await crud_users.update_email(db=db, user=user, new_email=data.email)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={
            "access_token": authorize.create_access_token(subject=data.email),
            "refresh_token": authorize.create_access_token(subject=data.email),
        },
    )


@router.post("/update-phone/", status_code=status.HTTP_202_ACCEPTED, summary="Обновление телефона в профиле")
async def update_phone(data: Phone, db: AsyncSession = Depends(get_session), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    email = authorize.get_jwt_subject()
    user = await crud_users.get_user_by_email(db=db, email=email)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь не найден")
    await crud_users.update_phone(db=db, user=user, new_phone=data.phone)
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"detail": "Телефон успешно обновлен"})


@router.delete("/delete/", status_code=status.HTTP_200_OK, summary="Удаление профиля")
async def delete_profile(db: AsyncSession = Depends(get_session), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    email = authorize.get_jwt_subject()
    user = await crud_users.get_user_by_email(db=db, email=email)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь не найден")
    await crud_users.delete(db=db, user=user)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Профиль успешно удален"})
