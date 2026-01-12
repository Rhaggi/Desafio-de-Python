from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "O serviço client-service está funcionando corretamente."}