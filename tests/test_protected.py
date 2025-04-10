import pytest
from httpx import AsyncClient, ASGITransport
from sqlmodel import select

from app.main import app
from app.core.database import get_session
from app.core.security.jwt_auth import create_access_token, pwd_context
from app.models.user import User


@pytest.mark.asyncio
async def test_protected_route_authenticated():
    # Garantir usuário de teste
    async for session in get_session():
        result = await session.execute(select(User).where(User.username == "usuario_demo"))
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

    token = create_access_token(data={"sub": "usuario_demo"})
    headers = {"Authorization": f"Bearer {token}"}

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/protected", headers=headers)

    assert response.status_code == 200
    assert "Bem-vindo" in response.json()["message"]

@pytest.mark.asyncio
async def test_protected_route_without_token():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/protected")

    assert response.status_code == 401
    assert "Not authenticated" in response.text

