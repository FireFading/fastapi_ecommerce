import pytest
from fastapi import status

from tests.settings import TestUser, Urls

tokens = {"access_token": "", "refresh_token": ""}
urls = Urls()
test_user = TestUser()


class TestAccountsEndpoints:
    @pytest.mark.asyncio
    async def test_login_unregistered_user(self, client):
        response = client.post(urls.LOGIN_URL, json=test_user.TEST_USER)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "Пользователь с таким Email не существует"}

    @pytest.mark.asyncio
    async def test_register_user(self, client):
        response = client.post(urls.REGISTER_URL, json=test_user.TEST_USER)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {"email": test_user.TEST_USER.get("email")}

    @pytest.mark.asyncio
    async def test_login_user(self, client):
        response = client.post(urls.LOGIN_URL, json=test_user.TEST_USER)
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
        tokens["access_token"] = response.json().get("access_token")
        tokens["refresh_token"] = response.json().get("refresh_token")

    @pytest.mark.asyncio
    async def test_wrong_password_login(self, client):
        response = client.post(urls.LOGIN_URL, json=test_user.TEST_USER_WITH_WRONG_PASSWORD)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"detail": "Неверный пароль"}

    @pytest.mark.asyncio
    async def test_logout_user(self, client):
        response = client.delete(
            urls.LOGOUT_URL, headers={"Authorization": tokens.get("access_token")}
        )
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_user_info_without_phone(self, client):
        response = client.get(
            urls.USER_INFO_URL,
            headers={"Authorization": tokens.get("access_token")},
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == test_user.USER_INFO
