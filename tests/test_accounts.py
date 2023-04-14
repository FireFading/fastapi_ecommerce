from app.utils.messages import messages
from app.utils.tokens import create_token
from fastapi import status
from pytest_mock import MockerFixture
from tests.settings import (
    Urls,
    User,
    change_password_schema,
    create_fake_token,
    login_credentials_schema,
    wrong_change_password_schema,
)


class TestRegister:
    async def test_register_user(self, client, mocker: MockerFixture):
        mocker.patch("app.routers.users.send_mail", return_value=True)
        response = client.post(
            Urls.REGISTER,
            json=login_credentials_schema,
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get("email") == User.EMAIL
        assert response.json().get("detail") == messages.CONFIRM_REGISTRATION_MAIL_SENT

    async def test_failed_repeat_register_user(self, register_user, client):
        response = client.post(
            Urls.REGISTER,
            json=login_credentials_schema,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json().get("detail") == messages.USER_ALREADY_EXISTS

    async def test_login_unregistered_user(self, client):
        response = client.post(Urls.LOGIN, json=login_credentials_schema)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json().get("detail") == messages.USER_NOT_FOUND


class TestLogin:
    async def test_login_user(self, register_user, client):
        response = client.post(Urls.LOGIN, json=login_credentials_schema)
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()

    async def test_wrong_password_login(self, register_user, client):
        response = client.post(
            Urls.LOGIN,
            json={"email": User.EMAIL, "password": User.WRONG_PASSWORD},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json().get("detail") == messages.WRONG_PASSWORD


class TestLogout:
    async def test_logout_user(self, auth_client):
        response = auth_client.delete(Urls.LOGOUT)
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("detail") == messages.USER_LOGOUT


class TestForgotPassword:
    async def test_user_forgot_password(self, register_user, client, mocker: MockerFixture):
        mocker.patch("app.routers.users.send_mail", return_value=True)
        response = client.post(Urls.FORGOT_PASSWORD, json={"email": User.EMAIL})
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json().get("detail") == messages.RESET_PASSWORD_MAIL_SENT

    async def test_unregistered_user_forgot_password(self, client, mocker: MockerFixture):
        mocker.patch("app.routers.users.send_mail", return_value=True)
        response = client.post(Urls.FORGOT_PASSWORD, json={"email": User.EMAIL})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json().get("detail") == messages.USER_NOT_FOUND


class TestResetPassword:
    async def test_user_reset_password(self, register_user, client):
        reset_password_token = create_token(email=User.EMAIL)
        response = client.post(
            f"{Urls.RESET_PASSWORD}{reset_password_token}",
            json=change_password_schema,
        )
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json().get("detail") == messages.PASSWORD_RESET

    async def test_user_reset_password_with_invalid_token(self, register_user, client):
        reset_password_token = create_fake_token()
        response = client.post(
            f"{Urls.RESET_PASSWORD}{reset_password_token}",
            json=change_password_schema,
        )
        assert response.status_code == status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
        assert response.json().get("detail") == messages.INVALID_TOKEN

    async def test_unregistered_user_reset_password(self, client):
        reset_password_token = create_token(email=User.EMAIL)
        response = client.post(
            f"{Urls.RESET_PASSWORD}{reset_password_token}",
            json=change_password_schema,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json().get("detail") == messages.USER_NOT_FOUND

    async def test_user_reset_password_not_match_password(self, register_user, client):
        reset_password_token = create_token(email=User.EMAIL)
        response = client.post(
            f"{Urls.RESET_PASSWORD}{reset_password_token}",
            json=wrong_change_password_schema,
        )
        assert response.status_code == status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
        assert response.json().get("detail") == messages.PASSWORDS_NOT_MATCH


class TestChangePassword:
    async def test_user_change_password(self, auth_client):
        response = auth_client.post(
            Urls.CHANGE_PASSWORD,
            json=change_password_schema,
        )
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json().get("detail") == messages.PASSWORD_UPDATED

    async def test_user_change_password_not_match(self, auth_client):
        response = auth_client.post(
            Urls.CHANGE_PASSWORD,
            json=wrong_change_password_schema,
        )
        assert response.status_code == status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
        assert response.json().get("detail") == messages.PASSWORDS_NOT_MATCH

    async def test_user_change_password_to_old(self, auth_client):
        response = auth_client.post(
            Urls.CHANGE_PASSWORD,
            json={
                "password": User.PASSWORD,
                "confirm_password": User.PASSWORD,
            },
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json().get("detail") == messages.NEW_PASSWORD_SIMILAR_OLD
