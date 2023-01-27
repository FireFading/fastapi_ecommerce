import pytest

from app.utils import create_reset_password_token
from fastapi import status
from pytest_mock import MockerFixture

from tests.settings import test_user, urls


class TestAccountsEndpoints:
    @pytest.mark.asyncio
    async def test_register_user(self, client):
        response = client.post(urls.register, json=test_user.TEST_USER)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {"email": test_user.TEST_USER.get("email")}

    @pytest.mark.asyncio
    async def test_login_unregistered_user(self, client):
        response = client.post(urls.login, json=test_user.TEST_USER)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "Пользователь с таким Email не существует"}

    @pytest.mark.asyncio
    async def test_login_user(self, user):
        response = user.post(urls.login, json=test_user.TEST_USER)
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()

    @pytest.mark.asyncio
    async def test_wrong_password_login(self, user):
        response = user.post(urls.login, json=test_user.TEST_USER_WITH_WRONG_PASSWORD)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"detail": "Неверный пароль"}

    @pytest.mark.asyncio
    async def test_logout_user(self, auth_client):
        response = auth_client.delete(urls.logout)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"detail": "Вы вышли из аккаунта"}

    @pytest.mark.asyncio
    async def test_user_forgot_password(self, user, mocker: MockerFixture):
        mocker.patch("app.routers.accounts.send_mail", return_value=True)
        response = user.post(urls.forgot_password, json={"email": test_user.email})
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json() == {
            "detail": "Письмо с токеном для сброса пароля отправлено"
        }

    @pytest.mark.asyncio
    async def test_user_reset_password(self, user):
        reset_password_token = create_reset_password_token(email=test_user.email)
        response = user.post(
            f"{urls.reset_password}{reset_password_token}",
            json={
                "password": test_user.new_password,
                "confirm_password": test_user.new_password,
            },
        )
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json() == {"detail": "Пароль успешно сброшен"}

    @pytest.mark.asyncio
    async def test_user_change_password(self, auth_client):
        response = auth_client.post(
            urls.change_password,
            json={
                "password": test_user.new_password,
                "confirm_password": test_user.new_password,
            },
        )
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json() == {"detail": "Пароль успешно обновлен"}
