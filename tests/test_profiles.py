from app.utils.messages import messages
from fastapi import status
from tests.settings import test_user, urls


class TestProfileEndpoints:
    async def test_not_available_without_auth(self, client):
        response = client.get(urls.user_info)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = client.post(urls.update_email)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = client.post(urls.update_phone)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = client.post(urls.update_name)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = client.delete(urls.delete_profile)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_user_info(self, auth_client):
        response = auth_client.get(urls.user_info)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result.get("email") == test_user.email
        assert result.get("phone") == test_user.phone
        assert result.get("name") == test_user.name
        assert result.get("user_id") is not None

    async def test_user_update_email(self, auth_client):
        response = auth_client.post(urls.update_email, json={"email": test_user.new_email})
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()

    async def test_user_update_phone(self, auth_client):
        response = auth_client.post(urls.update_phone, json={"phone": test_user.new_phone})
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json().get("detail") == messages.PHONE_UPDATED

    async def test_user_update_name(self, auth_client):
        response = auth_client.post(urls.update_name, json={"name": test_user.new_phone})
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json().get("detail") == messages.NAME_UPDATED

    async def test_user_delete_profile(self, auth_client):
        response = auth_client.delete(urls.delete_profile)
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("detail") == messages.PROFILE_DELETED
