import stackprinter
import uvicorn
from app.config import settings
from app.routers import products, profiles, rating, users
from app.routers.auth import app
from fastapi_pagination import add_pagination

stackprinter.set_excepthook()

app.include_router(users.router)
app.include_router(profiles.router)
app.include_router(products.router)
app.include_router(rating.router)
add_pagination(app)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        workers=settings.workers_count,
        log_level=settings.log_level.value.lower(),
    )
