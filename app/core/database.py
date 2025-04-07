from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core import settings

# Engine assíncrono (PostgreSQL com asyncpg)
engine = create_async_engine("postgresql+asyncpg://pulso:pulso123@localhost:5432/pulsodb", echo=False, future=True)

# Fábrica de sessões assíncronas
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependência para FastAPI
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
