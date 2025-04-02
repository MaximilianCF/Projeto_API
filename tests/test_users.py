import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.user import User
from app.core.database import get_session
from sqlmodel import select
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
client = TestClient(app)

def seed_user():
    session = next(get_session())
    user = session.exec(select(User).where(User.username == "usuario_demo")).first()
    if not user:
        demo = User(
            username="usuario_demo",
            email="demo@email.com",
            hashed_password=pwd_context.hash("senha_demo")
        )
        session.add(demo)
        session.commit()

def test_login_and_me():
    seed_user()

    # login via /token
    response = client.post("/api/token", data={
        "username": "usuario_demo",
        "password": "senha_demo"
    })

    assert response.status_code == 200, f"Erro no login: {response.text}"
    token = response.json()["access_token"]

    # acesso à rota autenticada /me
    headers = {"Authorization": f"Bearer {token}"}
    me_response = client.get("/api/me", headers=headers)

    assert me_response.status_code == 200
    data = me_response.json()
    assert data["username"] == "usuario_demo"
