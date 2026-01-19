from fastapi import APIRouter

router_db = APIRouter()

@router_db.get("/health")
def health():
    return {"status": "O serviço database-service está funcionando corretamente."}