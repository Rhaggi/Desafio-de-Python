from fastapi import APIRouter, HTTPException
from client_service.app.api.models.clients import Cliente, db
from sqlalchemy.orm import sessionmaker

score = APIRouter()

def GetScore( saldo: float):
    saldo = saldo
    score = (saldo * 0.1)
    if score < 0:
        return 0
    if score >= 1000000:
        return 1000
    return score

@score.get("/get-score/{client_id}")
def get_score(client_id: int):
    """
    Essa é a rota para obter o score baseado no saldo fornecido.
    """
    SessionLocal = sessionmaker(bind=db)
    session = SessionLocal()
    try:
        client = session.query(Cliente).filter(Cliente.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Cliente não encontrado.")
        score_value = GetScore(client.saldo)
        return {"client_id": client_id, "score": score_value}
    finally:
        session.close()