from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.settings import JWTSettings

router = APIRouter(prefix="/products", tags=["products"], responses={404: {"description": "Not found"}})


@AuthJWT.load_config
def get_jwt_settings():
    return JWTSettings()


@router.get("/get")
async def get_products(db: AsyncSession = Depends(get_session), authorize: AuthJWT = Depends()):
    pass
