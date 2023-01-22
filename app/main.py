import uvicorn
from fastapi_pagination import add_pagination

from app.api import accounts
from app.api.auth import app


app.include_router(accounts.router)
add_pagination(app)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
