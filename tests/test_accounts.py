import pytest
from fastapi import status

from tests.settings import TEST_USER


class TestAccounts:
    @pytest.mark.asyncio
    async def test_register_user(self, client):
        response = client.post("/accounts/register", json=TEST_USER)
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.asyncio
    async def test_login_user(self, client):
        response = client.post("/accounts/login", json=TEST_USER)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "Пользователь с таким Email не существует"}
