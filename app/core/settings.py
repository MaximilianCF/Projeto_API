import os
import logging
from pydantic_settings import BaseSettings
from pydantic import ValidationError

# Configuração básica de logs
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

from pydantic_settings import BaseSettings

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
    settings = Settings()
    logging.info(f"Configurações carregadas com sucesso: {settings.dict()}")
except ValidationError as e:
    # Exibe erros de validação se variáveis obrigatórias estiverem ausentes ou inválidas
    logging.error("Erro na validação das configurações.")
    logging.error(e.json())
