from app.utils.messages import messages
from fastapi import status
from tests.settings import rating, urls


class TestRating:
    async def test_create_new_rating(self, create_product, auth_client):
        response = auth_client.get(urls.get_products)
        product_id = response.json()[0].get("guid")
        rating["product_id"] = product_id
        response = auth_client.post(urls.create_rating, json=rating)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get("detail") == messages.RATING_CREATED
