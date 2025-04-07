import pytest
from fastapi.testclient import TestClient
from passlib.context import CryptContext
from sqlmodel import select

from app.core.database import get_session
from app.main import app
from app.models.user import User

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

    response = client.post("/api/v1/token", data={
        "username": "usuario_demo",
        "password": "senha_demo"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    me_response = client.get("/api/v1/me", headers=headers)
    assert me_response.status_code == 200
    assert me_response.json()["username"] == "usuario_demo"
