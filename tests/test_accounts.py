import jwt
from tests.conftest import client
from tests.settings import TEST_USER

def test_register_user():
    response = client.post("/users/register", json=TEST_USER)
    assert response.status_code == 201

# def test_secret_endpoint():
#     response = client.get("/secret")
#     assert response.status_code == 401

#     jwt = create_jwt()
#     response = client.get("/secret", headers={"Authorization": f"Bearer {jwt}"})
#     assert response.status_code == 200
#     assert response.json() == {"message": "You have access to the secret endpoint"}


# def test_login():
#     response = client.post("/login", json={"username": "test", "password": "wrong"})
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Invalid credentials"}

#     response = client.post("/login", json={"username": "test", "password": "test"})
#     assert response.status_code == 200
#     assert "access_token" in response.json()
#     jwt = response.json()["access_token"]
#     payload = jwt.decode(SECRET_KEY)
#     assert payload["sub"] == "test"


# def create_jwt():
#     # Create a JWT
#     jwt = JWTAuthMiddleware.create_jwt({"sub": "test"})
#     return jwt


# def test_valid_jwt():
#     # Test a valid JWT
#     jwt = create_jwt()
#     payload = jwt.decode(SECRET_KEY)
#     assert payload["sub"] == "test"


# def test_invalid_jwt():
#     jwt = "invalid.jwt.token"
#     with pytest.raises(jwt.exceptions.DecodeError):
#         payload = jwt.decode(SECRET_KEY)
