# app/middleware/rate_limit.py
from slowapi import Limiter
from slowapi.util import get_remote_address

# Configuração do Limiter sem especificar o armazenamento
limiter = Limiter(key_func=get_remote_address)
