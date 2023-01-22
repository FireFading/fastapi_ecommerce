from fastapi import Depends, HTTPException
from fastapi_jwt_auth import JWTAuthMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud import DBUsers
from src.database import get_session
from src.main import app
from src.schemas import User
from src.models import User as m_User

crud_users = DBUsers()

SECRET_KEY = "secret_key"
app.add_middleware(JWTAuthMiddleware, secret_key=SECRET_KEY)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/secret")
def secret_endpoint(jwt: dict):
    return {"message": "You have access to the secret endpoint"}


@app.post(
    "/register",
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
    create_user = m_User(email=user.email, password=user.password)
    new_user = await crud_users.create(db=db, db_user=create_user)
    return new_user


@app.post("/login")
def login(username: str, password: str):
    if username != "test" or password != "test":
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = JWTAuthMiddleware.create_jwt({"sub": username})

    return {"access_token": access_token}
