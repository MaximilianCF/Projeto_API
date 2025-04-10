from passlib.context import CryptContext

# 🔐 Cria um contexto de hashing seguro
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔑 Função para gerar hash da senha
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 🔐 Função para verificar senha no login
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
