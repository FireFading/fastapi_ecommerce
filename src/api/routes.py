from fastapi import Depends, HTTPException
import uuid
# from fastapi_jwt_auth import JWTAuthMiddleware
from starlette.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud import DBUsers
from src.database import get_session, engine, Base
from src.schemas import User
from src.models import User as m_User


SECRET_KEY = "secret_key"

app = FastAPI()

# app.add_middleware(JWTAuthMiddleware, secret_key=SECRET_KEY)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

crud_users = DBUsers()

@app.on_event("startup")
async def startup():
    # create db tables
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.post(
    "/users/register",
    response_model=User,
    status_code=201,
    summary="Регистрация пользователя",
)
async def register(user: User, db: AsyncSession = Depends(get_session)):
    db_user = await crud_users.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=409, detail="Пользователь с таким Email уже существует"
        )
    user_id = uuid.uuid4()
    create_user = m_User(email=user.email, password=user.password, user_id=user_id)
    new_user = await crud_users.create(db=db, db_user=create_user)
    return new_user
