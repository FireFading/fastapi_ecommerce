from app.utils.messages import messages
from fastapi import status
from tests.settings import Product, Urls, User, rating


class TestRating:
    async def test_create_new_rating(self, create_product, auth_client):
        response = auth_client.get(Urls.GET_PRODUCTS)
        product_id = response.json()[0].get("guid")
        rating["product_id"] = product_id
        response = auth_client.post(Urls.CREATE_RATING, json=rating)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get("detail") == messages.RATING_CREATED

        response = auth_client.get(f"{Urls.GET_RATINGS}{product_id}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()[0]
        assert result.get("stars") == rating.get("stars")
        assert result.get("product_id") == rating.get("product_id")
        assert result.get("user").get("email") == User.EMAIL

    async def test_delete_rating(self, create_rating, auth_client):
        response = auth_client.delete(f"{Urls.DELETE_RATING}{Product.GUID}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("detail") == messages.RATING_DELETED

        response = auth_client.get(f"{Urls.GET_RATINGS}{Product.GUID}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is None

        response = auth_client.get(f"{Urls.GET_AVG_RATING}{Product.GUID}")
        assert response.status_code == status.HTTP_200_OK
        assert float(response.json().get("avg_rating")) == 0
