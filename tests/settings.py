import uuid
from dataclasses import dataclass
from datetime import datetime

import jwt
from app.settings import Settings
from dotenv import load_dotenv
from pydantic import Field

load_dotenv(dotenv_path="../")


@dataclass
class Urls:
    LOGIN: str = "/accounts/login/"
    REGISTER: str = "/accounts/register/"
    LOGOUT: str = "/accounts/logout/"
    USER_INFO: str = "/accounts/profile/"

    UPDATE_EMAIL: str = "/accounts/profile/update/email/"
    UPDATE_PHONE: str = "/accounts/profile/update/phone/"
    UPDATE_NAME: str = "/accounts/profile/update/name/"

    FORGOT_PASSWORD: str = "/accounts/forgot-password/"
    RESET_PASSWORD: str = "/accounts/reset-password/"
    CHANGE_PASSWORD: str = "/accounts/change-password/"

    DELETE_PROFILE: str = "/accounts/profile/delete/"

    CREATE_PRODUCT: str = "/products/new/"
    GET_PRODUCTS: str = "/products/get/"
    DELETE_PRODUCT: str = "/products/delete/"

    CREATE_RATING: str = "/products/ratings/new/"
    GET_RATINGS: str = "/products/ratings/get/"
    GET_AVG_RATING: str = "/products/ratings/avg/"
    DELETE_RATING: str = "/products/ratings/delete/"


@dataclass
class User:
    EMAIL: str = "test@mail.ru"
    NEW_EMAIL: str = "new_test@mail.ru"
    WRONG_EMAIL: str = "wrong_test@mail.ru"

    PHONE: str | None = None
    NEW_PHONE: str = "89101111111"

    NAME: str | None = None
    NEW_NAME: str = "UserName"

    PASSWORD: str = "Abc123!@#def456$%^"
    NEW_PASSWORD: str = "NewAbc123!@#def456$%^"
    WRONG_PASSWORD: str = "WrongAbc123!@#def456$%^"


@dataclass
class Product:
    GUID: uuid.UUID = uuid.UUID("00000000-0000-0000-0000-000000000000")
    NAME: str = "test_product"
    DESCRIPTION: str = "test_description"
    PRODUCER: str = "test_producer"
    PRICE: float = 10000.0


class BaseTestSettings(Settings):
    database_url: str = Field(env="TEST_DATABASE_URL")


def create_fake_token(expires_in: datetime = datetime(1999, 1, 1), email: str = User.EMAIL) -> str:
    to_encode = {"exp": expires_in, "email": email, "is_active": True}
    return jwt.encode(to_encode, settings.secret_key, settings.algorithm)


settings = BaseTestSettings(_env_file=".env.example")
zero_uuid = "00000000-0000-0000-0000-000000000000"

login_credentials_schema = {"email": User.EMAIL, "password": User.PASSWORD}

change_password_schema = {
    "password": User.NEW_PASSWORD,
    "confirm_password": User.NEW_PASSWORD,
}

wrong_change_password_schema = {
    "password": User.NEW_PASSWORD,
    "confirm_password": User.WRONG_PASSWORD,
}

create_product_schema = {
    "guid": Product.GUID,
    "name": Product.NAME,
    "description": Product.DESCRIPTION,
    "producer": Product.PRODUCER,
    "price": Product.PRICE,
}

rating = {"stars": 2, "product_id": Product.GUID}
