import uvicorn
from fastapi_pagination import add_pagination

from app.routers import accounts, profiles
from app.routers.auth import app


app.include_router(accounts.router)
app.include_router(profiles.router)
add_pagination(app)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
