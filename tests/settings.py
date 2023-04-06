from datetime import datetime

import jwt
from app.settings import Settings
from dotenv import load_dotenv
from pydantic import Field

load_dotenv(dotenv_path="../")

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite://"


class Urls:
    login = "/accounts/login/"
    register = "/accounts/register/"
    logout = "/accounts/logout/"
    user_info = "/accounts/profile/"

    update_email = "/accounts/profile/update/email/"
    update_phone = "/accounts/profile/update/phone/"
    update_name = "/accounts/profile/update/name/"

    forgot_password = "/accounts/forgot-password/"
    reset_password = "/accounts/reset-password/"
    change_password = "/accounts/change-password/"

    delete_profile = "/accounts/profile/delete/"

    create_product = "/products/new/"
    get_products = "/products/get/"


class TestUser:
    email = "test@mail.ru"
    new_email = "new_test@mail.ru"
    wrong_email = "wrong_test@mail.ru"

    new_phone = "89101111111"

    new_name = "UserName"

    password = "TestPassword"
    new_password = "NewTestPassword"
    wrong_password = "WrongTestPassword"


class BaseTestSettings(Settings):
    database_url: str = Field(env="TEST_DATABASE_URL")


urls = Urls()
test_user = TestUser()
settings = BaseTestSettings(_env_file=".env.example")


test_product = {
    "name": "test_product",
    "description": "test_description",
    "producer": "test_producer",
    "price": 10000.0,
}


def create_fake_token(expires_in: datetime = datetime(1999, 1, 1), email: str = test_user.email) -> str:
    to_encode = {"exp": expires_in, "email": email, "is_active": True}
    return jwt.encode(to_encode, settings.secret_key, settings.algorithm)
