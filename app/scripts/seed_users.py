# app/scripts/seed_users.py

from sqlmodel import Session, select

from app.core.database import engine
from app.core.security.jwt_auth import pwd_context
from app.models.user import User


def seed_demo_user():
    with Session(engine) as session:
        user = session.exec(
            select(User).where(
                User.username == "usuario_demo")).first()
        if not user:
            demo_user = User(
                username="usuario_demo",
                email="demo@pulso.io",
                hashed_password=pwd_context.hash("123456"),
                score=100,
                level="pro"
            )
            session.add(demo_user)
            session.commit()
            print("✅ Usuário demo criado.")
        else:
            print("ℹ️ Usuário demo já existe.")
