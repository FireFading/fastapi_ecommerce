from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUD
from app.models.products import Product as m_Product
from app.schemas.products import Product


class DBProducts(CRUD):
    async def create(self, db: AsyncSession, product: m_Product):
        db.add(product)
        await db.flush()
        await db.commit()

        return product

    async def get(self, db: AsyncSession) -> list[m_Product]:
        result = await db.execute(select(m_Product))
        return result.scalars().all()

    async def get_by_params(self, product: Product, db: AsyncSession):
        result = await db.execute(
            select(m_Product).filter(
                m_Product.name == product.name
                and m_Product.producer == product.producer
                and m_Product.price == product.price
            )
        )
        return result.scalars().all()

    async def delete(self, db: AsyncSession, product: m_Product):
        await db.delete(product)
        await db.commit()
