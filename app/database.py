from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

db_url = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(db_url, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
