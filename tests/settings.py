class Urls:
    LOGIN_URL = "/accounts/login/"
    REGISTER_URL = "/accounts/register/"
    LOGOUT_URL = "/accounts/logout/"
    USER_INFO_URL = "/accounts/profile/"
    UPDATE_EMAIL_URL = "/accounts/profile/update-email/"
    UPDATE_PHONE_URL = "/accounts/profile/update-phone/"
    FORGOT_PASSWORD_URL = "/accounts/forgot-password/"
    RESET_PASSWORD_URL = "/accounts/reset-password/"


class TestUser:
    email = "test@mail.ru"
    new_email = "new_test@mail.ru"
    wrong_email = "wrong_test@mail.ru"
    new_phone = "89101111111"
    password = "TestPassword"
    new_password = "NewTestPassword"
    wrong_password = "WrongTestPassword"

    TEST_USER = {"email": email, "password": password}
    TEST_USER_WITH_WRONG_PASSWORD = {
        "email": email,
        "password": wrong_password,
    }

    USER_INFO = {"email": email, "phone": None}

    UPDATE_EMAIL_TEST_USER = {"email": new_email, "password": password}
    UPDATE_PHONE_TEST_USER = {
        "phone": new_phone,
        "email": new_email,
        "password": password,
    }
