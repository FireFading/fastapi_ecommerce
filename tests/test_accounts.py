import pytest
from fastapi import status

from tests.settings import TEST_USER, TEST_USER_WITH_WRONG_PASSWORD, LOGIN_URL, REGISTER_URL


class TestAccounts:
    @pytest.mark.asyncio
    async def test_login_unregistered_user(self, client):
        response = client.post(LOGIN_URL, json=TEST_USER)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "Пользователь с таким Email не существует"}

    @pytest.mark.asyncio
    async def test_register_user(self, client):
        response = client.post(REGISTER_URL, json=TEST_USER)
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.asyncio
    async def test_login_user(self, client):
        response = client.post(LOGIN_URL, json=TEST_USER)
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("access_token") is not None

    @pytest.mark.asyncio
    async def test_wrong_password_login(self, client):
        response = client.post(LOGIN_URL, json=TEST_USER_WITH_WRONG_PASSWORD)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"detail": "Неверный пароль"}
