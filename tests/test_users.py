import pytest
import httpx
from httpx import AsyncClient
from passlib.context import CryptContext
from sqlmodel import select
from app.main import app
from app.models.user import User
from app.core.database import get_session
from app.routes.v1.registry import include_v1_routes

include_v1_routes(app)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_test_user():
    async for session in get_session():
        statement = select(User).where(User.username == "usuario_demo")
        result = await session.execute(statement)
        user = result.scalar_one_or_none()
        if not user:
            demo = User(
                username="usuario_demo",
                email="demo@email.com",
                hashed_password=pwd_context.hash("senha_demo")
            )
            session.add(demo)
            await session.commit()
            await session.refresh(demo)


@pytest.mark.asyncio
async def test_login_and_me():
    await create_test_user()

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/token/", data={
            "username": "usuario_demo",
            "password": "senha_demo"
        })

        assert response.status_code == 200
        token = response.json()["access_token"]

        headers = {"Authorization": f"Bearer {token}"}
        me_response = await client.get("/api/v1/me", headers=headers)

        assert me_response.status_code == 200
        assert me_response.json()["username"] == "usuario_demo"
