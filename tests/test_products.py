import pytest
from fastapi import status

from tests.settings import test_product, urls


class TestProducts:
    @pytest.mark.asyncio
    async def test_not_available_create_without_auth(self, client):
        response = client.post(urls.create_product, json=test_product)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_create_product(self, auth_client):
        response = auth_client.post(urls.create_product, json=test_product)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {"detail": "Товар успешно создан"}

        response = auth_client.get(urls.get_products)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()[0]
        assert result.get("name") == test_product.get("name")
        assert result.get("description") == test_product.get("description")
        assert result.get("producer") == test_product.get("producer")
        assert result.get("price") == test_product.get("price")
