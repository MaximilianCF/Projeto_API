import pytest
from httpx import ASGITransport, AsyncClient

from app.core.security.jwt_auth import create_access_token, get_current_user
from app.main import app
from app.models.user import User
from app.routes.v1.upload import router


# Cria um usuário mockado para autenticação nos testes
def mock_current_user():
    return User(id=1, username="tester", email="tester@example.com")

@pytest.mark.asyncio
async def test_upload_dataset_success(tmp_path):
    app.dependency_overrides[get_current_user] = mock_current_user
    token = create_access_token(data={"sub": "1"})

    test_file = tmp_path / "teste.csv"
    test_file.write_text("coluna1,coluna2\nvalor1,valor2")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        with open(test_file, "rb") as f:
            response = await ac.post(
                "/api/v1/upload/",
                headers={"Authorization": f"Bearer {token}"},
                files={"file": ("teste.csv", f, "text/csv")},
                data={"nome": "Dataset Teste", "descricao": "Descrição genérica"}
            )

    assert response.status_code == 200
    assert response.json()["message"] == "Arquivo recebido com sucesso."

@pytest.mark.asyncio
async def test_upload_sem_token(tmp_path):
    if get_current_user in app.dependency_overrides:
        del app.dependency_overrides[get_current_user]

    test_file = tmp_path / "sem_token.csv"
    test_file.write_text("coluna1,coluna2\nvalor1,valor2")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        with open(test_file, "rb") as f:
            response = await ac.post(
                "/api/v1/upload/",
                files={"file": ("sem_token.csv", f, "text/csv")},
                data={"nome": "Sem Token", "descricao": "Teste sem autenticação"}
            )

    assert response.status_code == 401

    # Restaura para os próximos testes
    app.dependency_overrides[get_current_user] = mock_current_user

@pytest.mark.asyncio
async def test_upload_extensao_invalida(tmp_path):
    app.dependency_overrides[get_current_user] = mock_current_user
    token = create_access_token(data={"sub": "1"})

    test_file = tmp_path / "invalido.txt"
    test_file.write_text("isso não é csv")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        with open(test_file, "rb") as f:
            response = await ac.post(
                "/api/v1/upload/",
                headers={"Authorization": f"Bearer {token}"},
                files={"file": ("invalido.txt", f, "text/plain")},
                data={"nome": "Arquivo inválido", "descricao": "Formato errado"}
            )

    assert response.status_code == 400
    assert response.json()["detail"] == "Formato de arquivo inválido."

@pytest.mark.asyncio
async def test_upload_sem_arquivo():
    app.dependency_overrides[get_current_user] = mock_current_user
    token = create_access_token(data={"sub": "1"})

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/upload/",
            headers={"Authorization": f"Bearer {token}"},
            data={"nome": "Sem Arquivo", "descricao": "Tentativa sem arquivo"}
        )

    assert response.status_code == 422
    assert "detail" in response.json()  # Ensure error details are returned
