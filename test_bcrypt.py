from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

hashed = pwd_context.hash("senha_demo")
print("Hash:", hashed)

print("Verificação:", pwd_context.verify("senha_demo", hashed))
