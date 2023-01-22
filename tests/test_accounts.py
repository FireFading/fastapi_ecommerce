import jwt
import pytest
from app.utils import ALGORITHM, JWT_REFRESH_SECRET_KEY, JWT_SECRET_KEY
from fastapi import status

from tests.settings import (
    LOGIN_URL,
    REGISTER_URL,
    TEST_USER,
    TEST_USER_WITH_WRONG_PASSWORD,
)


class TestAccounts:
    test_user = TEST_USER
    test_user_with_wrong_password = TEST_USER_WITH_WRONG_PASSWORD

    @pytest.mark.asyncio
    async def test_login_unregistered_user(self, client):
        response = client.post(LOGIN_URL, json=self.test_user)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "Пользователь с таким Email не существует"}

    @pytest.mark.asyncio
    async def test_register_user(self, client):
        response = client.post(REGISTER_URL, json=self.test_user)
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.asyncio
    async def test_login_user(self, client):
        response = client.post(LOGIN_URL, json=self.test_user)
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
        access_token = response.json().get("access_token")
        payload = jwt.decode(
            jwt=access_token, key=JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        assert payload.get("user") == self.test_user.get("email")
        refresh_token = response.json().get("refresh_token")
        payload = jwt.decode(
            jwt=refresh_token, key=JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM]
        )
        assert payload.get("user") == self.test_user.get("email")

    @pytest.mark.asyncio
    async def test_wrong_password_login(self, client):
        response = client.post(LOGIN_URL, json=self.test_user_with_wrong_password)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"detail": "Неверный пароль"}
