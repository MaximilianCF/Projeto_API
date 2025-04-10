import asyncio
import logging
from sqlmodel import SQLModel, select
# Importar o engine e a fábrica de sessão de database.py
from app.core.database import engine, AsyncSessionLocal
from app.models.user import User
from app.core.security import get_password_hash
import os

# Configuração do logger
logger = logging.getLogger("init_db")
logging.basicConfig(level=logging.INFO)

# Carregar de variáveis de ambiente ou settings (melhor ainda buscar de app.core.settings se aplicável)
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "pulso")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@admin.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "pulso123")

# Importando os modelos
from app.models import (
    cdi, challenge, ibov, indicator_metadata, ipca, leaderboard,
    selic, sp500, submission, treasury, usd_brl, User
)

async def init_db():
    try:
        logger.info("🔌 Iniciando conexão com o banco de dados (usando engine de database.py)...")

        # Cria as tabelas diretamente usando o engine
        logger.info("⏳ Criando tabelas (se não existirem)...")
        async with engine.begin() as conn: # Usa o engine importado para obter uma conexão
            # Executa create_all de forma síncrona dentro do contexto da conexão async
            await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("🗂️ Tabelas verificadas/criadas com sucesso.")

        # Verificando e criando o usuário admin usando AsyncSessionLocal importado
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(User).where(User.username == ADMIN_USERNAME))
            admin_user = result.scalars().first()

            if not admin_user:
                logger.info(f"👤 Usuário admin '{ADMIN_USERNAME}' não encontrado. Criando...")
                admin = User(
                    username=ADMIN_USERNAME,
                    email=ADMIN_EMAIL,
                    hashed_password=get_password_hash(ADMIN_PASSWORD),
                    score=0,
                    level="iniciante",
                )
                session.add(admin)
                await session.commit()
                logger.info(f"✅ Usuário admin '{ADMIN_USERNAME}' criado.")
            else:
                logger.info(f"ℹ️ Usuário admin '{ADMIN_USERNAME}' já existe.")

        logger.info("🎉 Banco de dados pronto para uso.")

    except Exception as e:
        logger.exception(f"❌ Erro ao inicializar o banco de dados: {e}")
        raise

if __name__ == "__main__":
    logger.info("🚀 Executando script de inicialização do banco de dados...")
    # Não precisa mais criar o engine aqui, ele é importado
    asyncio.run(init_db())
    logger.info("🏁 Script de inicialização concluído.")