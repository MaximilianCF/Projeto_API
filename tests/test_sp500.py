import pytest
from httpx import AsyncClient

from app.core.security.jwt_auth import create_access_token
from app.main import app


@pytest.mark.asyncio
async def test_upload_sem_token(tmp_path):
    test_file = tmp_path / "sem_token.csv"
    test_file.write_text("coluna1,coluna2\nvalor1,valor2")

    async with AsyncClient(app=app, base_url="http://test") as ac:
        with open(test_file, "rb") as f:
            response = await ac.post(
                "/api/v1/upload/",
                files={"file": ("sem_token.csv", f, "text/csv")},
                data={"nome": "Sem Token", "descricao": "Teste sem autenticação"}
            )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_upload_extensao_invalida(tmp_path):
    token = create_access_token(subject="1")
    test_file = tmp_path / "invalido.txt"
    test_file.write_text("isso não é um csv")

    async with AsyncClient(app=app, base_url="http://test") as ac:
        with open(test_file, "rb") as f:
            response = await ac.post(
                "/api/v1/upload/",
                headers={"Authorization": f"Bearer {token}"},
                files={"file": ("invalido.txt", f, "text/plain")},
                data={"nome": "Extensão Inválida", "descricao": "Arquivo .txt"}
            )
    assert response.status_code == 400
    assert "Apenas arquivos .csv" in response.text


@pytest.mark.asyncio
async def test_upload_sem_arquivo():
    token = create_access_token(subject="1")

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/upload/",
            headers={"Authorization": f"Bearer {token}"},
            data={"nome": "Sem Arquivo", "descricao": "Teste sem CSV"}
        )
    assert response.status_code == 422  # Falta de campo obrigatório
