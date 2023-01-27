import pytest
from fastapi import status

from tests.settings import test_user, urls


class TestProfileEndpoints:
    @pytest.mark.asyncio
    async def test_user_info(self, auth_client):
        response = auth_client.get(
            urls.user_info,
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == test_user.USER_INFO

    @pytest.mark.asyncio
    async def test_user_update_email(self, auth_client):
        response = auth_client.post(
            urls.update_email,
            json={"email": test_user.new_email},
        )
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()

    @pytest.mark.asyncio
    async def test_user_update_phone(self, auth_client):
        response = auth_client.post(
            urls.update_phone,
            json={"phone": test_user.new_phone},
        )
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json() == {"detail": "Телефон успешно обновлен"}

    @pytest.mark.asyncio
    async def test_user_delete_profile(self, auth_client):
        response = auth_client.delete(urls.delete_profile)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"detail": "Профиль успешно удален"}
