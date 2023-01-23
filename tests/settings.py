class Urls:
    LOGIN_URL = "/accounts/login/"
    REGISTER_URL = "/accounts/register/"
    LOGOUT_URL = "/accounts/logout/"
    USER_INFO_URL = "/accounts/me"


class TestUser:
    email = "test@mail.ru"
    TEST_USER = {"email": email, "password": "TestPassword"}
    TEST_USER_WITH_WRONG_PASSWORD = {
        "email": email,
        "password": "WrongTestPassword",
    }
    USER_INFO = {"email": email, "phone": None }
