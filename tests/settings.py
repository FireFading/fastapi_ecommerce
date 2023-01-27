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


urls = Urls()
test_user = TestUser()
