from collections.abc import AsyncGenerator

import pytest_asyncio
from app.database import Base, get_session
from app.main import app as main_app
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from tests.settings import Urls, create_product_schema, login_credentials_schema, rating, settings

engine = create_async_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture()
async def app() -> AsyncGenerator:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield main_app
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session(app: FastAPI) -> AsyncGenerator:
    connection = await engine.connect()
    transaction = await connection.begin()
    session = async_session(bind=connection)
    yield session
    await session.close()
    await transaction.rollback()
    await connection.close()


@pytest_asyncio.fixture
async def client(app: FastAPI, db_session: async_session) -> AsyncGenerator | TestClient:
    async def _get_test_db():
        yield db_session

    app.dependency_overrides[get_session] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest_asyncio.fixture
async def register_user(client: AsyncGenerator | TestClient, mocker: MockerFixture) -> AsyncGenerator:
    mocker.patch("app.routers.users.send_mail", return_value=True)
    response = client.post(Urls.REGISTER, json=login_credentials_schema)
    assert response.status_code == status.HTTP_201_CREATED


@pytest_asyncio.fixture
async def auth_client(register_user, client: AsyncGenerator | TestClient) -> AsyncGenerator | TestClient:
    response = client.post(Urls.LOGIN, json=login_credentials_schema)
    assert response.status_code == status.HTTP_200_OK
    access_token = response.json().get("access_token")
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    yield client


@pytest_asyncio.fixture
async def create_product(
    auth_client: AsyncGenerator | TestClient,
) -> AsyncGenerator | TestClient:
    response = auth_client.post(Urls.CREATE_PRODUCT, json=create_product_schema)
    assert response.status_code == status.HTTP_201_CREATED


@pytest_asyncio.fixture
async def create_rating(auth_client: AsyncGenerator | TestClient, create_product) -> AsyncGenerator | TestClient:
    response = auth_client.post(Urls.CREATE_RATING, json=rating)
    assert response.status_code == status.HTTP_201_CREATED


# @pytest_asyncio.fixture
# async def get_product(auth_client: AsyncGenerator | TestClient, create_product) -> AsyncGenerator | TestClient:
#     response = auth_client.get(Urls.GET_PRODUCTS)
#     assert response.status_code == status.HTTP_200_OK
#     result = response.json()[0]
