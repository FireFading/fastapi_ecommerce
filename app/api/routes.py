import uuid
from datetime import timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi_pagination import add_pagination
from pydantic import BaseSettings
from sqlalchemy.ext.asyncio import AsyncSession

from starlette.middleware.cors import CORSMiddleware

from app.crud import DBUsers
from app.database import Base, engine, get_session
from app.models import User as m_User
from app.schemas import User
from app.utils import get_hashed_password, verify_password

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class JWTSettings(BaseSettings):
    authjwt_secret_key: str = "secret"
    authjwt_header_type: Optional[str] = None
    authjwt_header_name: str = "Authorization"
    access_token_expires: timedelta = timedelta(minutes=15)
    refresh_token_expires: timedelta = timedelta(days=30)


@AuthJWT.load_config
def get_header_type_none():
    return JWTSettings()


add_pagination(app)

crud_users = DBUsers()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.get("/protected")
def protected(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"hello": "world"})


@app.get("/get_headers_access")
def get_headers_access(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return authorize.get_unverified_jwt_headers()


@app.get("/get_headers_refresh")
def get_headers_refresh(authorize: AuthJWT = Depends()):
    authorize.jwt_refresh_token_required()
    return authorize.get_unverified_jwt_headers()


@app.post(
    "/accounts/register",
    response_model=User,
    status_code=201,
    summary="Регистрация пользователя",
)
async def register(user: User, db: AsyncSession = Depends(get_session)):
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
        status_code=status.HTTP_201_CREATED,
        content={"email": user.email}
    )


@app.post("/accounts/login", status_code=200)
async def login(
    user: User, db: AsyncSession = Depends(get_session), authorize: AuthJWT = Depends()
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


@app.delete("/accounts/logout")
def logout(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"msg": "Successfully logout"}
    )
