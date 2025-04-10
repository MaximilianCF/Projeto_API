import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import SQLModel
from app.core.database import get_session
from app.main import app
from app.core.settings import settings

# Cria engine para testes
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# Importa modelos para criação das tabelas
from app.models.challenge import Challenge
from app.models.user import User
from app.models.submission import Submission
from app.models.leaderboard import Leaderboard
from app.models.source_info import SourceInfo
from app.models.sp500 import SP500
from app.models.treasury import Treasury
from app.models.selic import Selic
from app.models.ipca import Ipca
from app.models.ibov import Ibov
from app.models.usd_brl import Usd_brl
from app.models.cdi import Cdi


@pytest.fixture(scope="session")
async def async_engine():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def async_session(async_engine):
    async with AsyncSession(async_engine, expire_on_commit=False) as session:
        yield session


@pytest.fixture(scope="function")
async def client(async_session):
    # Override da sessão
    async def override_get_session():
        yield async_session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
