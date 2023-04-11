from app.utils.messages import messages
from fastapi import status
from tests.settings import test_product, urls


class TestProducts:
    async def test_not_available_without_auth(self, client):
        response = client.post(urls.create_product, json=test_product)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_create_product(self, auth_client):
        response = auth_client.post(urls.create_product, json=test_product)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get("detail") == messages.PRODUCT_CREATED

        response = auth_client.get(urls.get_products)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()[0]
        assert result.get("name") == test_product.get("name")
        assert result.get("description") == test_product.get("description")
        assert result.get("producer") == test_product.get("producer")
        assert result.get("price") == test_product.get("price")

    async def test_delete_product(self, create_product, auth_client):
        response = auth_client.get(urls.get_products)
        assert response.status_code == status.HTTP_200_OK
        product_id = (response.json()[0]).get("guid")
        response = auth_client.delete(f"{urls.delete_product}{product_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("detail") == messages.PRODUCT_DELETED
