FROM python:3.11-slim

WORKDIR /app

# Copia e instala dependências primeiro para melhor cache
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia restante da aplicação
COPY . .

# Expõe a porta do FastAPI
EXPOSE 8000

# Executa FastAPI via Uvicorn em modo produção
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]

