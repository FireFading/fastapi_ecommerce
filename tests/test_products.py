from app.utils.messages import messages
from fastapi import status
from tests.settings import Product, Urls, create_product_schema


class TestProducts:
    async def test_not_available_without_auth(self, client):
        response = client.post(Urls.CREATE_PRODUCT, json=create_product_schema)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_create_product(self, auth_client):
        response = auth_client.post(Urls.CREATE_PRODUCT, json=create_product_schema)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get("detail") == messages.PRODUCT_CREATED

        response = auth_client.get(Urls.GET_PRODUCTS)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()[0]
        assert result.get("name") == Product.NAME
        assert result.get("description") == Product.DESCRIPTION
        assert result.get("producer") == Product.PRODUCER
        assert result.get("price") == Product.PRICE

    async def test_delete_product(self, create_product, auth_client):
        response = auth_client.get(Urls.GET_PRODUCTS)
        assert response.status_code == status.HTTP_200_OK
        product_id = (response.json()[0]).get("guid")
        response = auth_client.delete(f"{Urls.DELETE_PRODUCT}{product_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("detail") == messages.PRODUCT_DELETED
