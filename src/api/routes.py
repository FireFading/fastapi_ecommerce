import uuid

from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi_pagination import add_pagination
from sqlalchemy.ext.asyncio import AsyncSession

from starlette.middleware.cors import CORSMiddleware

from src.crud import DBUsers
from src.database import Base, engine, get_session
from src.models import User as m_User
from src.schemas import User
from src.utils import (
    create_access_token,
    create_refresh_token,
    get_hashed_password,
    verify_password,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_pagination(app)

crud_users = DBUsers()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


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
    return Response(
        status_code=status.HTTP_201_CREATED,
    )


@app.post("/accounts/login", status_code=200)
async def login(user: User, db: AsyncSession = Depends(get_session)):
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
    access_token = create_access_token(user=user.email)
    refresh_token = create_refresh_token(user=user.email)
    return {"access_token": access_token, "refresh_token": refresh_token}
