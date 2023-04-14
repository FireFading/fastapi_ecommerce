from app.utils.messages import messages
from fastapi import status
from tests.settings import Urls, User


class TestProfileEndpoints:
    async def test_not_available_without_auth(self, client):
        response = client.get(Urls.USER_INFO)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = client.post(Urls.UPDATE_EMAIL)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = client.post(Urls.UPDATE_PHONE)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = client.post(Urls.UPDATE_NAME)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = client.delete(Urls.DELETE_PROFILE)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_user_info(self, auth_client):
        response = auth_client.get(Urls.USER_INFO)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result.get("email") == User.EMAIL
        assert result.get("phone") == User.PHONE
        assert result.get("name") == User.NAME
        assert result.get("guid") is not None

    async def test_user_update_email(self, auth_client):
        response = auth_client.post(Urls.UPDATE_EMAIL, json={"email": User.NEW_EMAIL})
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()

    async def test_user_update_phone(self, auth_client):
        response = auth_client.post(Urls.UPDATE_PHONE, json={"phone": User.NEW_PHONE})
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json().get("detail") == messages.PHONE_UPDATED

    async def test_user_update_name(self, auth_client):
        response = auth_client.post(Urls.UPDATE_NAME, json={"name": User.NEW_PHONE})
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json().get("detail") == messages.NAME_UPDATED

    async def test_user_delete_profile(self, auth_client):
        response = auth_client.delete(Urls.DELETE_PROFILE)
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("detail") == messages.PROFILE_DELETED
