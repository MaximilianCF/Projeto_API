import os
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.security.jwt_auth import create_access_token


@pytest.fixture
def tmp_upload_folder(tmp_path):
    """Cria uma pasta temporária para uploads durante os testes."""
    os.environ["UPLOAD_FOLDER"] = str(tmp_path)
    return tmp_path


@pytest.fixture
def auth_headers():
    """Gera o token JWT para autenticação nos testes."""
    token = create_access_token(data={"sub": "usuario_demo"})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def csv_file(tmp_upload_folder):
    """Cria um arquivo CSV temporário para upload."""
    csv_content = "coluna1,coluna2\nvalor1,valor2"
    csv_file_path = tmp_upload_folder / "teste.csv"
    csv_file_path.write_text(csv_content)
    return csv_file_path


@pytest.mark.asyncio(loop_scope="session")
async def test_upload_dataset_csv(csv_file, auth_headers):
    """Teste de upload bem-sucedido de arquivo CSV válido."""
    with open(csv_file, "rb") as f:
        files = {
            "file": ("teste.csv", f, "text/csv"),
            "nome": (None, "meu dataset de teste"),
            "descricao": (None, "descrição do dataset"),
        }
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/api/v1/upload/", headers=auth_headers, files=files)

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    json_data = response.json()
    assert json_data["message"] == "Arquivo recebido com sucesso."


@pytest.mark.asyncio(loop_scope="session")
async def test_upload_without_authentication(tmp_upload_folder):
    """Teste de falha ao tentar fazer upload sem autenticação."""
    csv_file_path = tmp_upload_folder / "teste.csv"
    csv_file_path.write_text("coluna1,coluna2\nvalor1,valor2")

    with open(csv_file_path, "rb") as f:
        files = {
            "file": ("teste.csv", f, "text/csv"),
            "nome": (None, "dataset sem auth"),
            "descricao": (None, "deve falhar"),
        }
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/api/v1/upload/", files=files)

    assert response.status_code == 401, f"Unexpected status code: {response.status_code}"
    assert "Not authenticated" in response.text


@pytest.mark.asyncio(loop_scope="session")
async def test_upload_invalid_file_type(tmp_upload_folder, auth_headers):
    """Teste de upload com arquivo de tipo inválido."""
    invalid_file_path = tmp_upload_folder / "teste.txt"
    invalid_file_path.write_text("conteúdo inválido")

    with open(invalid_file_path, "rb") as f:
        files = {
            "file": ("teste.txt", f, "text/plain"),
            "nome": (None, "arquivo inválido"),
            "descricao": (None, "extensão errada"),
        }
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/api/v1/upload/", headers=auth_headers, files=files)

    assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
    assert "Apenas arquivos .csv" in response.text
