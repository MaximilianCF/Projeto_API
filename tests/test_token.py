import pytest
from httpx import AsyncClient, ASGITransport
from sqlmodel import select

from app.main import app
from app.models.user import User
from app.core.database import get_session
from app.core.security.jwt_auth import pwd_context


@pytest.mark.asyncio
async def test_login_token_flow():
    # Cria o usuário demo se não existir
    async for session in get_session():
        result = await session.execute(select(User).where(User.username == "usuario_demo"))
        user = result.scalar_one_or_none()
        if not user:
            demo_user = User(
                username="usuario_demo",
                email="demo@email.com",
                hashed_password=pwd_context.hash("senha_demo")
            )
            session.add(demo_user)
            await session.commit()
            await session.refresh(demo_user)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/token/",
            data={"username": "usuario_demo", "password": "senha_demo"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
