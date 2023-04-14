from dataclasses import dataclass
from datetime import datetime

import jwt
from app.settings import Settings
from dotenv import load_dotenv
from pydantic import Field

load_dotenv(dotenv_path="../")

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite://"


@dataclass
class Urls:
    LOGIN = "/accounts/login/"
    REGISTER = "/accounts/register/"
    LOGOUT = "/accounts/logout/"
    USER_INFO = "/accounts/profile/"

    UPDATE_EMAIL = "/accounts/profile/update/email/"
    UPDATE_PHONE = "/accounts/profile/update/phone/"
    UPDATE_NAME = "/accounts/profile/update/name/"

    FORGOT_PASSWORD = "/accounts/forgot-password/"
    RESET_PASSWORD = "/accounts/reset-password/"
    CHANGE_PASSWORD = "/accounts/change-password/"

    DELETE_PROFILE = "/accounts/profile/delete/"

    CREATE_PRODUCT = "/products/new/"
    GET_PRODUCTS = "/products/get/"
    DELETE_PRODUCT = "/products/delete/"

    CREATE_RATING = "/products/ratings/new/"
    GET_RATINGS = "/products/ratings/get/"


@dataclass
class User:
    EMAIL = "test@mail.ru"
    NEW_EMAIL = "new_test@mail.ru"
    WRONG_EMAIL = "wrong_test@mail.ru"

    PHONE = None
    NEW_PHONE = "89101111111"

    NAME = None
    NEW_NAME = "UserName"

    PASSWORD = "Abc123!@#def456$%^"
    NEW_PASSWORD = "NewAbc123!@#def456$%^"
    WRONG_PASSWORD = "WrongAbc123!@#def456$%^"


class BaseTestSettings(Settings):
    database_url: str = Field(env="TEST_DATABASE_URL")


def create_fake_token(expires_in: datetime = datetime(1999, 1, 1), email: str = User.EMAIL) -> str:
    to_encode = {"exp": expires_in, "email": email, "is_active": True}
    return jwt.encode(to_encode, settings.secret_key, settings.algorithm)


settings = BaseTestSettings(_env_file=".env.example")


test_product = {
    "name": "test_product",
    "description": "test_description",
    "producer": "test_producer",
    "price": 10000.0,
}

rating = {"stars": 2, "product_id": "00000000-0000-0000-0000-000000000000"}
