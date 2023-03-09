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

    async def get_by_id(self, product: Product, db: AsyncSession):
        result = await db.execute(select(Product).filter(Product.name == product.name, Product.producer == product.producer))
        return result.scalars().all()

    async def delete(self, db: AsyncSession, product: Product):
        await db.delete(product)
        await db.commit()
