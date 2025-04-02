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
	docker-compose build

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
openapi:
	yq eval-all 'reduce . as $$item ({}; .openapi = $$item.openapi // .openapi | .info = $$item.info // .info | .paths += $$item.paths // {} | .components.schemas += $$item.components.schemas // {} )' docs/openapi/*.yaml > docs/openapi/openapi.yaml
