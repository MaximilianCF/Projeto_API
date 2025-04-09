FROM python:3.11-slim

# Instalar o cliente PostgreSQL para utilizar pg_isready
RUN apt-get update && apt-get install -y postgresql-client

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia e instala as dependências primeiro para otimizar cache
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta usada pela aplicação FastAPI/Uvicorn
EXPOSE 8000

# Ensure the module path matches your application structure
CMD ["sh", "-c", "./wait-for-db.sh && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
