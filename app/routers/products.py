import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.products import DBProducts
from app.database import get_session
from app.models.products import Product as m_Product
from app.schemas.products import Product
from app.settings import JWTSettings
from app.utils.messages import messages

router = APIRouter(prefix="/products", tags=["products"], responses={404: {"description": "Not found"}})

crud_products = DBProducts()


@AuthJWT.load_config
def get_jwt_settings():
    return JWTSettings()


@router.get("/get", status_code=status.HTTP_200_OK, summary="Получение всех доступных продуктов")
async def get_products(db: AsyncSession = Depends(get_session), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return await crud_products.get(db=db)


@router.post("/new", status_code=status.HTTP_201_CREATED, summary="Добавление нового продукта")
async def create_product(
    product: Product,
    db: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
):
    authorize.jwt_required()
    if await crud_products.get_by_params(product=product, db=db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=messages.PRODUCT_ALREADY_EXISTS,
        )
    new_product = m_Product(
        product_id=uuid.uuid4(),
        name=product.name,
        description=product.description,
        producer=product.producer,
        price=product.price,
    )
    await crud_products.create(db=db, product=new_product)
    return {"detail": messages.PRODUCT_CREATED}


@router.delete("/delete/{product_id}", status_code=status.HTTP_200_OK, summary="Удаление продукта")
async def delete_product(
    product_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
):
    authorize.jwt_required()
    db_product = await crud_products.get_by_uuid(product_id=product_id, db=db)
    await crud_products.delete(db=db, product=db_product)
    return {"detail": messages.PRODUCT_DELETED}
