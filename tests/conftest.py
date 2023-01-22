import pytest_asyncio
from app.database import Base, get_session
from app.main import app as main_app
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=True,
)

Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(autouse=True)
async def app():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield main_app


@pytest_asyncio.fixture
async def db_session(app: FastAPI):
    connection = await engine.connect()
    session = Session(bind=connection)
    yield session
    await session.close()
    await connection.close()


@pytest_asyncio.fixture
async def client(app: FastAPI, db_session: Session):
    async def _get_test_db():
        yield db_session

    app.dependency_overrides[get_session] = _get_test_db
    with TestClient(app) as client:
        yield client
