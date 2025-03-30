from fastapi.testclient import TestClient
from app.main import app
from app.models.user import User
from app.core.database import get_session
from sqlmodel import select
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

def test_protected_endpoint():
    seed_user()
    with TestClient(app) as client:
        # 1. Login
        response = client.post("/api/token", json={
            "username": "usuario_demo",
            "password": "senha_demo"
        })
        assert response.status_code == 200
        token = response.json()["access_token"]

        # 2. Acessar rota protegida
        headers = {"Authorization": f"Bearer {token}"}
        protected = client.get("/api/protected", headers=headers)

        assert protected.status_code == 200
        assert "Bem-vindo" in protected.json()["message"]
