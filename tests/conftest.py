import pytest
import respx
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import SQLModel

from app.core.database import get_session
from app.core.settings import settings
from app.main import app

# Cria engine de teste com base no ambiente
engine = create_async_engine(settings.DATABASE_URL, echo=False)

from app.models.cdi import Cdi
# Importa todos os modelos necessários
from app.models.challenge import Challenge
from app.models.ibov import Ibov
from app.models.ipca import Ipca
from app.models.leaderboard import Leaderboard
from app.models.selic import Selic
from app.models.source_info import SourceInfo
from app.models.sp500 import SP500
from app.models.submission import Submission
from app.models.treasury import Treasury
from app.models.usd_brl import Usd_brl
from app.models.user import User


@pytest.fixture(scope="session")
async def async_engine():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture(scope="function")
async def async_session(async_engine):
    async with AsyncSession(async_engine) as session:
        yield session

@pytest.fixture(scope="function")
async def override_get_session(async_session):
    async def _override_get_session():
        yield async_session
    app.dependency_overrides[get_session] = _override_get_session
    yield
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
async def client(override_get_session):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
