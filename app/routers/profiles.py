from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import DBUsers
from app.database import get_session
from app.schemas import Email, Phone, User
from app.settings import JWTSettings
from app.utils.exceptions import get_user_or_404

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
    return {"email": user.email, "phone": user.phone}


@router.post("/update-email/", status_code=status.HTTP_202_ACCEPTED, summary="Обновление Email в профиле")
async def update_email(data: Email, db: AsyncSession = Depends(get_session), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    email = authorize.get_jwt_subject()
    user = await get_user_or_404(email=email, db=db)
    await crud_users.update_email(db=db, user=user, new_email=data.email)
    return {
            "access_token": authorize.create_access_token(subject=data.email),
            "refresh_token": authorize.create_access_token(subject=data.email),
        }


@router.post("/update-phone/", status_code=status.HTTP_202_ACCEPTED, summary="Обновление телефона в профиле")
async def update_phone(data: Phone, db: AsyncSession = Depends(get_session), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    email = authorize.get_jwt_subject()
    user = await get_user_or_404(email=email, db=db)
    await crud_users.update_phone(db=db, user=user, new_phone=data.phone)
    return {"detail": "Телефон успешно обновлен"}


@router.delete("/delete/", status_code=status.HTTP_200_OK, summary="Удаление профиля")
async def delete_profile(db: AsyncSession = Depends(get_session), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    email = authorize.get_jwt_subject()
    user = await get_user_or_404(email=email, db=db)
    await crud_users.delete(db=db, user=user)
    return {"detail": "Профиль успешно удален"}
