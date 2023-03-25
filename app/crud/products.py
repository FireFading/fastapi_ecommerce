import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUD
from app.models.products import Product


class DBProducts(CRUD):
    async def create(self, db: AsyncSession, product: Product):
        db.add(product)
        await db.flush()
        await db.commit()

        return product

    async def get(self, db: AsyncSession) -> list[Product]:
        result = await db.execute(select(Product))
        return result.scalars().all()

    async def get_by_uuid(self, product_id: uuid.UUID, db: AsyncSession):
        result = await db.execute(select(Product).filter(Product.product_id == product_id))
        return result.scalars().all()

    async def delete(self, db: AsyncSession, product: Product):
        await db.delete(product)
        await db.commit()
