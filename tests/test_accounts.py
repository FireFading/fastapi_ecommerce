import pytest
from app.utils.messages import messages
from app.utils.tokens import create_token
from fastapi import status
from pytest_mock import MockerFixture
from tests.settings import create_fake_token, test_user, urls


class TestRegister:
    async def test_register_user(self, client, mocker: MockerFixture):
        mocker.patch("app.routers.users.send_mail", return_value=True)
        response = client.post(
            urls.register,
            json={"email": test_user.email, "password": test_user.password},
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get("email") == test_user.email
        assert response.json().get("detail") == messages.CONFIRM_REGISTRATION_MAIL_SENT

    async def test_failed_repeat_register_user(self, register_user, client):
        response = client.post(
            urls.register,
            json={"email": test_user.email, "password": test_user.password},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json().get("detail") == messages.USER_ALREADY_EXISTS

    async def test_login_unregistered_user(self, client):
        response = client.post(urls.login, json={"email": test_user.email, "password": test_user.password})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json().get("detail") == messages.USER_NOT_FOUND


class TestLogin:
    async def test_login_user(self, register_user, client):
        response = client.post(urls.login, json={"email": test_user.email, "password": test_user.password})
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()

    async def test_wrong_password_login(self, register_user, client):
        response = client.post(
            urls.login,
            json={"email": test_user.email, "password": test_user.wrong_password},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json().get("detail") == messages.WRONG_PASSWORD


class TestLogout:
    async def test_logout_user(self, auth_client):
        response = auth_client.delete(urls.logout)
        # assert response.status_code == status.HTTP_200_OK
        assert response.json().get("detail") == messages.USER_LOGOUT


class TestForgotPassword:
    async def test_user_forgot_password(self, register_user, client, mocker: MockerFixture):
        mocker.patch("app.routers.users.send_mail", return_value=True)
        response = client.post(urls.forgot_password, json={"email": test_user.email})
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json().get("detail") == messages.RESET_PASSWORD_MAIL_SENT

    async def test_unregistered_user_forgot_password(self, client, mocker: MockerFixture):
        mocker.patch("app.routers.users.send_mail", return_value=True)
        response = client.post(urls.forgot_password, json={"email": test_user.email})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json().get("detail") == messages.USER_NOT_FOUND


class TestResetPassword:
    async def test_user_reset_password(self, register_user, client):
        reset_password_token = create_token(email=test_user.email)
        response = client.post(
            f"{urls.reset_password}{reset_password_token}",
            json={
                "password": test_user.new_password,
                "confirm_password": test_user.new_password,
            },
        )
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json().get("detail") == messages.PASSWORD_RESET

    async def test_user_reset_password_with_invalid_token(self, register_user, client):
        reset_password_token = create_fake_token()
        response = client.post(
            f"{urls.reset_password}{reset_password_token}",
            json={
                "password": test_user.new_password,
                "confirm_password": test_user.new_password,
            },
        )
        assert response.status_code == status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
        assert response.json().get("detail") == messages.INVALID_TOKEN

    async def test_unregistered_user_reset_password(self, client):
        reset_password_token = create_token(email=test_user.email)
        response = client.post(
            f"{urls.reset_password}{reset_password_token}",
            json={
                "password": test_user.new_password,
                "confirm_password": test_user.new_password,
            },
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json().get("detail") == messages.USER_NOT_FOUND

    async def test_user_reset_password_not_match_password(self, register_user, client):
        reset_password_token = create_token(email=test_user.email)
        response = client.post(
            f"{urls.reset_password}{reset_password_token}",
            json={
                "password": test_user.new_password,
                "confirm_password": test_user.wrong_password,
            },
        )
        assert response.status_code == status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
        assert response.json().get("detail") == messages.PASSWORDS_NOT_MATCH


class TestChangePassword:
    async def test_user_change_password(self, auth_client):
        response = auth_client.post(
            urls.change_password,
            json={
                "password": test_user.new_password,
                "confirm_password": test_user.new_password,
            },
        )
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json().get("detail") == messages.PASSWORD_UPDATED

    async def test_user_change_password_not_match(self, auth_client):
        response = auth_client.post(
            urls.change_password,
            json={
                "password": test_user.new_password,
                "confirm_password": test_user.wrong_password,
            },
        )
        assert response.status_code == status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
        assert response.json().get("detail") == messages.PASSWORDS_NOT_MATCH

    async def test_user_change_password_to_old(self, auth_client):
        response = auth_client.post(
            urls.change_password,
            json={
                "password": test_user.password,
                "confirm_password": test_user.password,
            },
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json().get("detail") == messages.NEW_PASSWORD_SIMILAR_OLD
