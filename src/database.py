import config
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

DATABASE_URL = f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"


engine = create_async_engine(DATABASE_URL, echo=True)


async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()

async def get_session():
    async with async_session() as session:
        yield session