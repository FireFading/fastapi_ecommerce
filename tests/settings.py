from datetime import datetime

import jwt

from app.settings import settings


class Urls:
    login = "/accounts/login/"
    register = "/accounts/register/"
    logout = "/accounts/logout/"
    user_info = "/accounts/profile/"
    update_email = "/accounts/profile/update-email/"
    update_phone = "/accounts/profile/update-phone/"
    forgot_password = "/accounts/forgot-password/"
    reset_password = "/accounts/reset-password/"
    change_password = "/accounts/change-password/"
    delete_profile = "/accounts/profile/delete/"


class TestUser:
    email = "test@mail.ru"
    new_email = "new_test@mail.ru"
    wrong_email = "wrong_test@mail.ru"
    new_phone = "89101111111"
    password = "TestPassword"
    new_password = "NewTestPassword"
    wrong_password = "WrongTestPassword"


urls = Urls()
test_user = TestUser()


def create_fake_token(expires_in: datetime = datetime(1999, 1, 1), email: str = test_user.email) -> str:
    to_encode = {"exp": expires_in, "email": email, "is_active": True}
    return jwt.encode(to_encode, settings.secret_key, settings.algorithm)
