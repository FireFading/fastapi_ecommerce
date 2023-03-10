import pytest

from app.utils.tokens import create_token
from fastapi import status
from pytest_mock import MockerFixture

from tests.settings import create_fake_token, test_user, urls


class TestRegister:
    @pytest.mark.asyncio
    async def test_register_user(self, client):
        response = client.post(urls.register, json={"email": test_user.email, "password": test_user.password})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get("email") == test_user.email
        assert response.json().get("detail") == "На почту отправлено письмо для подтверждения регистрации"

    @pytest.mark.asyncio
    async def test_failed_repeat_register_user(self, register_user, client):
        response = client.post(urls.register, json={"email": test_user.email, "password": test_user.password})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "Пользователь с таким Email уже существует"}

    @pytest.mark.asyncio
    async def test_login_unregistered_user(self, client):
        response = client.post(urls.login, json={"email": test_user.email, "password": test_user.password})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Пользователь с таким Email не существует"}


class TestLogin:
    @pytest.mark.asyncio
    async def test_login_user(self, register_user, client):
        response = client.post(urls.login, json={"email": test_user.email, "password": test_user.password})
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()

    @pytest.mark.asyncio
    async def test_wrong_password_login(self, register_user, client):
        response = client.post(urls.login, json={"email": test_user.email, "password": test_user.wrong_password})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"detail": "Неверный пароль"}


class TestLogout:
    @pytest.mark.asyncio
    async def test_logout_user(self, auth_client):
        response = auth_client.delete(urls.logout)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"detail": "Вы вышли из аккаунта"}


class TestForgotPassword:
    @pytest.mark.asyncio
    async def test_user_forgot_password(self, register_user, client, mocker: MockerFixture):
        mocker.patch("app.routers.users.send_mail", return_value=True)
        response = client.post(urls.forgot_password, json={"email": test_user.email})
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json() == {"detail": "Письмо с токеном для сброса пароля отправлено"}

    @pytest.mark.asyncio
    async def test_unregistered_user_forgot_password(self, client, mocker: MockerFixture):
        mocker.patch("app.routers.users.send_mail", return_value=True)
        response = client.post(urls.forgot_password, json={"email": test_user.email})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Пользователь с таким Email не существует"}


class TestResetPassword:
    @pytest.mark.asyncio
    async def test_user_reset_password(self, register_user, client):
        reset_password_token = create_token(email=test_user.email)
        response = client.post(
            f"{urls.reset_password}{reset_password_token}",
            json={"password": test_user.new_password, "confirm_password": test_user.new_password},
        )
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json() == {"detail": "Пароль успешно сброшен"}

    @pytest.mark.asyncio
    async def test_user_reset_password_with_invalid_token(self, register_user, client):
        reset_password_token = create_fake_token()
        response = client.post(
            f"{urls.reset_password}{reset_password_token}",
            json={"password": test_user.new_password, "confirm_password": test_user.new_password},
        )
        assert response.status_code == status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
        assert response.json() == {"detail": "Токен недействителен"}

    @pytest.mark.asyncio
    async def test_unregistered_user_reset_password(self, client):
        reset_password_token = create_token(email=test_user.email)
        response = client.post(
            f"{urls.reset_password}{reset_password_token}",
            json={"password": test_user.new_password, "confirm_password": test_user.new_password},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Пользователь с таким Email не существует"}

    @pytest.mark.asyncio
    async def test_user_reset_password_not_match_password(self, register_user, client):
        reset_password_token = create_token(email=test_user.email)
        response = client.post(
            f"{urls.reset_password}{reset_password_token}",
            json={"password": test_user.new_password, "confirm_password": test_user.wrong_password},
        )
        assert response.status_code == status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
        assert response.json() == {"detail": "Пароли не совпадают"}


class TestChangePassword:
    @pytest.mark.asyncio
    async def test_user_change_password(self, auth_client):
        response = auth_client.post(
            urls.change_password, json={"password": test_user.new_password, "confirm_password": test_user.new_password}
        )
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json() == {"detail": "Пароль успешно обновлен"}

    @pytest.mark.asyncio
    async def test_user_change_password_not_match(self, auth_client):
        response = auth_client.post(
            urls.change_password,
            json={"password": test_user.new_password, "confirm_password": test_user.wrong_password},
        )
        assert response.status_code == status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
        assert response.json() == {"detail": "Пароли не совпадают"}

    @pytest.mark.asyncio
    async def test_user_change_password_to_old(self, auth_client):
        response = auth_client.post(
            urls.change_password, json={"password": test_user.password, "confirm_password": test_user.password}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "Новый пароль похож на старый"}
