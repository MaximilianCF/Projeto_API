# Caminho para o diretório da aplicação
APP_DIR=app

# Porta do servidor FastAPI/Uvicorn no container
PORT=8000

# 🔥 Inicia a API localmente no container com reload
run:
	docker-compose exec api uvicorn $(APP_DIR).main:app --host 0.0.0.0 --port $(PORT) --reload

# 🧪 Roda os testes com cobertura
test:
	docker-compose exec api pytest --cov=$(APP_DIR) tests/

# 🧪 Roda os testes sem cobertura (mais leve)
test-simple:
	docker-compose exec api pytest tests/

# 🧼 Linter com Ruff
lint:
	docker-compose exec api ruff check $(APP_DIR) tests

# 🛠️ Rebuild da imagem
build:
	docker-compose up --build -d

# 🚀 Sobe os containers
up:
	docker-compose up -d

# 🛑 Para os containers
down:
	docker-compose down

# 💣 Remove o banco de dados e recria (se SQLite for usado localmente)
reset-db:
	rm -f db.sqlite3 && touch db.sqlite3

# 📄 Junta YAMLs da OpenAPI
OPENAPI_PORT := $(shell python3 -c 'import socket; s=socket.socket(); s.bind(("",0)); print(s.getsockname()[1]); s.close()')

openapi:
	@echo "🔄 Gerando documentação OpenAPI na porta dinâmica $(OPENAPI_PORT)..."

	@uvicorn app.main:app --port $(OPENAPI_PORT) & echo $$! > uvicorn.pid; \
	sleep 3; \
	until curl -s http://localhost:$(OPENAPI_PORT)/openapi.json > /dev/null; do \
		echo "⏳ Esperando o Uvicorn responder em :$(OPENAPI_PORT)..."; \
		sleep 1; \
	done; \
	curl -s http://localhost:$(OPENAPI_PORT)/openapi.json > docs/openapi/openapi.json; \
	if command -v yq >/dev/null 2>&1; then \
		yq -P docs/openapi/openapi.json > docs/openapi/openapi.yaml; \
	else \
		echo "⚠️  yq não instalado. Apenas JSON gerado."; \
	fi; \
	kill `cat uvicorn.pid`; \
	rm uvicorn.pid; \
	echo "✅ Documentação OpenAPI gerada com sucesso!"; \
	echo "📁 Arquivos gerados: docs/openapi/openapi.json e docs/openapi/openapi.yaml"

# 🧪 Teste da rota de upload isolada
test-upload:
	docker-compose exec api pytest tests/test_upload.py

test-desafios:
	docker-compose exec api pytest tests/test_desafios.py

test-submissoes:
	docker-compose exec api pytest tests/test_submissoes.py

test-leaderboard:
	docker-compose exec api pytest tests/test_leaderboard.py

