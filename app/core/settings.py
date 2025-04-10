import os
import logging
import sys # <--- Adicionar import
from pydantic_settings import BaseSettings
from pydantic import ValidationError

DATABASE_URL="postgresql+asyncpg://pulso:pulso123@db:5432/pulsodb"

# Configuração básica de logs
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Removido 'from pydantic_settings import BaseSettings' duplicado

class Settings(BaseSettings):
    TESTING: bool = False
    DATABASE_URL: str
    SECRET_KEY: str
    OPENAI_API_KEY: str
    FRED_API_KEY: str
    SENTRY_DSN: str
    ENV: str = "development"
    SEED_DEMO_USER: bool = False

    class Config:
        env_file = ".env"

try:
    settings = Settings() # <--- Instanciar PRIMEIRO
except ValidationError as e:
    # Logar o erro detalhado é crucial para debug
    logging.error("❌ ERRO FATAL: Erro na validação das configurações. Verifique .env ou variáveis de ambiente.")
    logging.error(e.json())
    sys.exit(1) # <--- Sair imediatamente se a validação falhar

# Logar SÓ DEPOIS de garantir que 'settings' foi criado com sucesso
logging.info("Configurações carregadas com sucesso.")
# (Opcional, mais seguro para produção: evite logar segredos)
# logging.info(f"Loaded settings (excluding sensitive): {settings.dict(exclude={'SECRET_KEY', 'OPENAI_API_KEY', 'DATABASE_URL'})}")
