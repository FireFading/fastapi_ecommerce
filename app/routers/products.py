import uuid

from app.config import jwt_settings
from app.database import get_session
from app.models.products import Product as m_Product
from app.schemas.products import Product, ProductParams
from app.utils.messages import messages
from fastapi import APIRouter, Depends, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/products", tags=["products"], responses={404: {"description": "Not found"}})
security = HTTPBearer()


@AuthJWT.load_config
def get_jwt_settings():
    return jwt_settings


@router.get(
    "/get/{product_id}",
    status_code=status.HTTP_200_OK,
    summary="Получение продукта по id",
)
async def get_product(product_id: str, session: AsyncSession = Depends(get_session)):
    return await m_Product.get(session=session, product_id=product_id)


@router.get("/get", status_code=status.HTTP_200_OK, summary="Получение всех доступных продуктов")
async def get_products(session: AsyncSession = Depends(get_session), params: ProductParams = Depends()):
    products = await m_Product.filter(
        price__gte=params.from_price,
        price__lte=params.to_price,
        order_by=params.order_by,
        session=session,
    )
    return [Product.from_orm(product).dict() for product in products] if products else None


@router.post("/new", status_code=status.HTTP_201_CREATED, summary="Добавление нового продукта")
async def create_product(
    product: Product,
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    authorize.jwt_required()
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
    await m_Product.delete(session=session, instances=db_product)
    return {"detail": messages.PRODUCT_DELETED}
