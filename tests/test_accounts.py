import pytest

from app.utils import create_reset_password_token
from fastapi import status
from pytest_mock import MockerFixture

from tests.settings import TestUser, Urls

tokens = {"access_token": "", "refresh_token": ""}
urls = Urls()
test_user = TestUser()


class TestAccountsEndpoints:
    @pytest.mark.asyncio
    async def test_login_unregistered_user(self, client):
        response = client.post(urls.login, json=test_user.TEST_USER)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "Пользователь с таким Email не существует"}

    @pytest.mark.asyncio
    async def test_register_user(self, client):
        response = client.post(urls.register, json=test_user.TEST_USER)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {"email": test_user.TEST_USER.get("email")}

    @pytest.mark.asyncio
    async def test_login_user(self, client):
        response = client.post(urls.login, json=test_user.TEST_USER)
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
        tokens["access_token"] = response.json().get("access_token")
        tokens["refresh_token"] = response.json().get("refresh_token")

    @pytest.mark.asyncio
    async def test_wrong_password_login(self, client):
        response = client.post(urls.login, json=test_user.TEST_USER_WITH_WRONG_PASSWORD)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"detail": "Неверный пароль"}

    @pytest.mark.asyncio
    async def test_logout_user(self, client):
        response = client.delete(
            urls.logout, headers={"Authorization": tokens.get("access_token")}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"detail": "Вы вышли из аккаунта"}

    @pytest.mark.asyncio
    async def test_user_forgot_password(self, client, mocker: MockerFixture):
        mocker.patch("app.routers.accounts.send_mail", return_value=True)
        response = client.post(urls.forgot_password, json={"email": test_user.email})
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json() == {
            "detail": "Письмо с токеном для сброса пароля отправлено"
        }

    @pytest.mark.asyncio
    async def test_user_reset_password(self, client):
        reset_password_token = create_reset_password_token(email=test_user.email)
        response = client.post(
            f"{urls.reset_password}{reset_password_token}",
            json={
                "password": test_user.new_password,
                "confirm_password": test_user.new_password,
            },
        )
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json() == {"detail": "Пароль успешно сброшен"}

    @pytest.mark.asyncio
    async def test_user_change_password(self, client):
        response = client.post(
            urls.change_password,
            json={
                "password": test_user.new_password,
                "confirm_password": test_user.new_password,
            },
            headers={"Authorization": tokens.get("access_token")},
        )
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json() == {"detail": "Пароль успешно обновлен"}


class TestProfileEndpoints:
    @pytest.mark.asyncio
    async def test_user_info(self, client):
        response = client.get(
            urls.user_info,
            headers={"Authorization": tokens.get("access_token")},
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == test_user.USER_INFO

    @pytest.mark.asyncio
    async def test_user_update_email(self, client):
        response = client.post(
            urls.update_email,
            headers={"Authorization": tokens.get("access_token")},
            json={"email": test_user.new_email},
        )
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
        tokens["access_token"] = response.json().get("access_token")
        tokens["refresh_token"] = response.json().get("refresh_token")

    @pytest.mark.asyncio
    async def test_user_update_phone(self, client):
        response = client.post(
            urls.update_phone,
            headers={"Authorization": tokens.get("access_token")},
            json={"phone": test_user.new_phone},
        )
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json() == {"detail": "Телефон успешно обновлен"}
