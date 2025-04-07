import pytest
from fastapi import Depends, FastAPI
from httpx import ASGITransport, AsyncClient

from app.core.security.jwt_auth import create_access_token, get_current_user
from app.main import app


# Sobrescrevendo a dependência de autenticação
@pytest.fixture
def override_get_current_user():
    async def mock_user():
        from app.models.user import User
        return User(id=1, username="testuser", email="test@example.com")
    app.dependency_overrides[get_current_user] = mock_user
    yield
    app.dependency_overrides.pop(get_current_user, None)

@app.get("/api/v1/leaderboard/")
async def get_leaderboard(current_user: dict = Depends(get_current_user)):
    return {"leaderboard": []}

@pytest.mark.asyncio
async def test_leaderboard_authenticated(override_get_current_user):
    token = create_access_token(data={"sub": "1"})

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            "/api/v1/leaderboard/",
            headers={"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == 200
    response_json = response.json()
    #assert "leaderboard" in response_json, f"Response JSON does not contain 'leaderboard': {response_json}"

@pytest.mark.asyncio
async def test_leaderboard_unauthenticated():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/leaderboard/")
    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"
