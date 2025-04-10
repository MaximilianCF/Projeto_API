import pytest
from httpx import AsyncClient, ASGITransport
from sqlmodel import select

from app.main import app
from app.core.security.jwt_auth import create_access_token, pwd_context
from app.core.database import get_session
from app.models.user import User


@pytest.mark.asyncio
async def test_me_authenticated():
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

    # Gera token manualmente
    token = create_access_token(data={"sub": "usuario_demo"})
    headers = {"Authorization": f"Bearer {token}"}

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/me", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "usuario_demo"
    assert data["email"] == "demo@email.com"

@pytest.mark.asyncio
async def test_me_with_invalid_token():
    # Token inválido (pode ser só um string malformada)
    invalid_token = "invalid.jwt.token"
    headers = {"Authorization": f"Bearer {invalid_token}"}

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/me", headers=headers)

    assert response.status_code == 401
    assert "Token inválido ou expirado" in response.text

from datetime import datetime, timedelta
from jose import jwt

from app.core.security.jwt_auth import SECRET_KEY, ALGORITHM


@pytest.mark.asyncio
async def test_me_with_expired_token():
    # Gera token com expiração no passado
    expired_payload = {
        "sub": "usuario_demo",
        "exp": datetime.utcnow() - timedelta(seconds=5)
    }
    expired_token = jwt.encode(expired_payload, SECRET_KEY, algorithm=ALGORITHM)
    headers = {"Authorization": f"Bearer {expired_token}"}

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/me", headers=headers)

    assert response.status_code == 401
    assert "Token inválido ou expirado" in response.text
