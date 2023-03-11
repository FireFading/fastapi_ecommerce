import uvicorn
from fastapi_pagination import add_pagination

from app.routers import products, profiles, users
from app.routers.auth import app

app.include_router(users.router)
app.include_router(profiles.router)
app.include_router(products.router)
add_pagination(app)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
