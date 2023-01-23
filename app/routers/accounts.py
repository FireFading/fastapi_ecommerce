import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import DBUsers
from app.database import get_session
from app.models import User as m_User
from app.schemas import LoginCredentials, User
from app.utils import get_hashed_password, verify_password


crud_users = DBUsers()

router = APIRouter(
    prefix="/accounts", tags=["accounts"], responses={404: {"description": "Not found"}}
)


@router.post(
    "/register/",
    response_model=User,
    status_code=201,
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


@router.post("/login/", status_code=200)
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


@router.delete("/logout/")
async def logout(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"msg": "Successfully logout"}
    )


@router.get(
    "/me",
    response_model=User,
    status_code=200,
    summary="Получение информации о пользователе",
)
async def user_info(
    db: AsyncSession = Depends(get_session), authorize: AuthJWT = Depends()
):
    authorize.jwt_required()
    email = authorize.get_jwt_subject()
    user = await crud_users.get_user_by_email(db=db, email=email)
    user_info = {"email": user.email, "phone": user.phone}
    return JSONResponse(status_code=status.HTTP_200_OK, content=user_info)
