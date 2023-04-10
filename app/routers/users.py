from app.config import jwt_settings
from app.database import get_session
from app.models.users import User as m_User
from app.schemas.users import CreateUser, Email, LoginCredentials, UpdatePassword
from app.templates.activate_account import html_activate_account_mail
from app.templates.reset_password import html_reset_password_mail
from app.utils.exceptions import get_user_or_404
from app.utils.mail import send_mail
from app.utils.messages import messages
from app.utils.tokens import create_token, get_email_from_token, verify_token
from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/accounts", tags=["accounts"], responses={404: {"description": "Not found"}})
security = HTTPBearer()


@AuthJWT.load_config
def get_jwt_settings():
    print(jwt_settings)
    return jwt_settings


@router.post(
    "/register/",
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация пользователя",
)
async def register(user: CreateUser, session: AsyncSession = Depends(get_session)):
    email = user.email
    if await m_User.get(session=session, email=email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.USER_ALREADY_EXISTS)
    await m_User(**user.dict()).create(session=session)
    token = create_token(email=email)
    html_activate_account_mail(token=token)
    # await send_mail(subject=subject, recipients=[email], body=body)
    return {"email": email, "detail": messages.CONFIRM_REGISTRATION_MAIL_SENT}


@router.post(
    "/activate-account/{token}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Активация аккаунта",
)
async def activate_account(token: str, session: AsyncSession = Depends(get_session)):
    if not verify_token(token=token):
        raise HTTPException(
            status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
            detail=messages.INVALID_TOKEN,
        )
    email = get_email_from_token(token=token)
    user = await get_user_or_404(email=email, session=session)
    user.is_active = True
    await user.update(session=session)
    return {"detail": messages.PROFILE_ACTIVATED}


@router.post("/login/", status_code=status.HTTP_200_OK, summary="Авторизация, получение токенов")
async def login(
    user: LoginCredentials,
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
):
    db_user = await get_user_or_404(email=user.email, session=session)
    print(db_user)
    if not db_user.verify_password(password=user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.WRONG_PASSWORD)
    return {
        "access_token": authorize.create_access_token(subject=user.email),
        "refresh_token": authorize.create_refresh_token(subject=user.email),
    }


@router.delete("/logout/", status_code=status.HTTP_200_OK, summary="Выход из аккаунта")
async def logout(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return {"detail": messages.USER_LOGOUT}


@router.post(
    "/forgot-password/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Запрос на получение письма с токеном для сброса пароля",
)
async def forgot_password(data: Email, session: AsyncSession = Depends(get_session)):
    user = await get_user_or_404(email=data.email, session=session)
    reset_password_token = create_token(email=user.email)

    subject = "Reset password"
    recipients = [user.email]
    body = html_reset_password_mail(reset_password_token=reset_password_token)
    await send_mail(subject=subject, recipients=recipients, body=body)
    return {"detail": messages.RESET_PASSWORD_MAIL_SENT}


@router.post(
    "/reset-password/{token}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Сброс пароля",
)
async def reset_password(token: str, data: UpdatePassword, session: AsyncSession = Depends(get_session)):
    if not verify_token(token=token):
        raise HTTPException(
            status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
            detail=messages.INVALID_TOKEN,
        )
    email = get_email_from_token(token=token)
    user = await get_user_or_404(email=email, session=session)
    print(data)
    if data.password != data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
            detail=messages.PASSWORDS_NOT_MATCH,
        )
    await user.update(session=session)
    return {"detail": messages.PASSWORD_RESET}


@router.post(
    "/change-password/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Изменение пароля",
)
async def change_password(
    data: UpdatePassword,
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    authorize.jwt_required()
    if data.password != data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
            detail=messages.PASSWORDS_NOT_MATCH,
        )
    email = authorize.get_jwt_subject()
    user = await get_user_or_404(email=email, session=session)
    if user.verify_password(password=data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=messages.NEW_PASSWORD_SIMILAR_OLD,
        )
    await user.update(session=session)
    return {"detail": messages.PASSWORD_UPDATED}
