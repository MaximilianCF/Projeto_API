import os
from datetime import datetime

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app.core.security.jwt_auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", summary="Upload de dataset CSV")
async def upload_dataset(
    file: UploadFile = File(...),
    nome: str = Form(...),
    descricao: str = Form(...),
    user: User = Depends(get_current_user),
):
    # 🧠 Captura o diretório só no momento do upload (após os.environ já ter sido setado no teste)
    upload_dir = os.getenv("UPLOAD_FOLDER", "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400, detail="Apenas arquivos .csv são permitidos."
        )

    filename = f"{user.username}_{datetime.utcnow().isoformat()}_{file.filename}"
    file_path = os.path.join(upload_dir, filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {
        "message": "Arquivo recebido com sucesso.",
        "nome": nome,
        "descricao": descricao,
        "salvo_como": file_path,
    }
