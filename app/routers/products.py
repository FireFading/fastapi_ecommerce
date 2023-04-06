import uuid

from app.config import jwt_settings
from app.database import get_session
from app.models.products import Product as m_Product
from app.schemas.products import Product
from app.utils.messages import messages
from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/products", tags=["products"], responses={404: {"description": "Not found"}})
security = HTTPBearer()


@AuthJWT.load_config
def get_jwt_settings():
    return jwt_settings


@router.get("/get", status_code=status.HTTP_200_OK, summary="Получение всех доступных продуктов")
async def get_products(session: AsyncSession = Depends(get_session)):
    return await m_Product.get(session=session)


@router.post("/new", status_code=status.HTTP_201_CREATED, summary="Добавление нового продукта")
async def create_product(
    product: Product,
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    authorize.jwt_required()
    if await m_Product.all(session=session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=messages.PRODUCT_ALREADY_EXISTS,
        )
    await m_Product(**product.dict()).create(session=session)
    return {"detail": messages.PRODUCT_CREATED}


@router.delete("/delete/{product_id}", status_code=status.HTTP_200_OK, summary="Удаление продукта")
async def delete_product(
    product_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    authorize.jwt_required()
    db_product = await m_Product.get(product_id=product_id, session=session)
    await db_product.delete(session=session)
    return {"detail": messages.PRODUCT_DELETED}
