import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import DBUsers
from app.database import get_session
from app.models import User as m_User
from app.schemas import Email, LoginCredentials, UpdatePassword, User
from app.settings import JWTSettings, settings
from app.utils import (
    create_reset_password_token,
    get_email_from_reset_password_token,
    get_hashed_password,
    html_reset_password_mail,
    send_mail,
    verify_password,
    verify_reset_password_token,
)


crud_users = DBUsers()

router = APIRouter(
    prefix="/accounts", tags=["accounts"], responses={404: {"description": "Not found"}}
)


@AuthJWT.load_config
def get_jwt_settings():
    return JWTSettings()


@router.post(
    "/register/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация пользователя",
)
async def register(user: LoginCredentials, db: AsyncSession = Depends(get_session)):
    db_user = await crud_users.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким Email уже существует",
        )
    user_id = uuid.uuid4()
    hashed_password = get_hashed_password(password=user.password)
    create_user = m_User(email=user.email, password=hashed_password, user_id=user_id)
    await crud_users.create(db=db, db_user=create_user)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content={"email": user.email}
    )


@router.post(
    "/login/", status_code=status.HTTP_200_OK, summary="Авторизация, получение токенов"
)
async def login(
    user: LoginCredentials,
    db: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
):
    db_user = await crud_users.get_user_by_email(db=db, email=user.email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким Email не существует",
        )
    if not verify_password(password=user.password, hashed_password=db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный пароль"
        )
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={
            "access_token": authorize.create_access_token(subject=user.email),
            "refresh_token": authorize.create_refresh_token(subject=user.email),
        },
    )


@router.delete("/logout/", status_code=status.HTTP_200_OK, summary="Выход из аккаунта")
async def logout(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"detail": "Вы вышли из аккаунта"}
    )


@router.post(
    "/forgot-password/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Запрос на получение письма с токеном для сброса пароля",
)
async def forgot_password(data: Email, db: AsyncSession = Depends(get_session)):
    user = await crud_users.get_user_by_email(db=db, email=data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    reset_password_token = create_reset_password_token(email=user.email)

    subject = "Reset password"
    recipients = [user.email]
    body = html_reset_password_mail(reset_password_token=reset_password_token)
    await send_mail(subject=subject, recipients=recipients, body=body)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={"detail": "Письмо с токеном для сброса пароля отправлено"},
    )


@router.post(
    "/reset-password/{token}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Сброс пароля",
)
async def reset_password(
    token: str, data: UpdatePassword, db: AsyncSession = Depends(get_session)
):
    if not verify_reset_password_token(token=token):
        raise HTTPException(
            status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
            detail="Токен недействителен",
        )
    email = get_email_from_reset_password_token(token=token)
    user = await crud_users.get_user_by_email(db=db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    if data.password != data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
            detail="Пароли не совпадают",
        )
    new_hashed_password = get_hashed_password(password=data.password)
    await crud_users.update_password(
        db=db, user=user, new_hashed_password=new_hashed_password
    )
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={"detail": "Пароль успешно сброшен"},
    )


@router.post(
    "/change-password/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Изменение пароля",
)
async def reset_password(
    data: UpdatePassword,
    db: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
):
    authorize.jwt_required()
    if data.password != data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
            detail="Пароли не совпадают",
        )
    email = authorize.get_jwt_subject()
    user = await crud_users.get_user_by_email(db=db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    if user.password == data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Новый пароль похож на старый",
        )
    new_hashed_password = get_hashed_password(password=data.password)
    await crud_users.update_password(
        db=db, user=user, new_hashed_password=new_hashed_password
    )
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={"detail": "Пароль успешно обновлен"},
    )
