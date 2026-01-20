from fastapi import APIRouter, HTTPException
from client_service.app.api.models.clients import Cliente, db
from sqlalchemy.orm import sessionmaker

score = APIRouter()

def GetScore( saldo: float):
    saldo = saldo
    score = (saldo * 0.1)
    if saldo < 0:
        return 0
    return score

@score.get("/get-score-by-email/{email}")
def get_score(email: str):
    """
    Essa é a rota para obter o score baseado no email fornecido.
    """
    SessionLocal = sessionmaker(bind=db)
    session = SessionLocal()
    try:
        client = session.query(Cliente).filter(Cliente.email == email).first()
        if not client:
            raise HTTPException(status_code=404, detail="Cliente não encontrado.")
        score_value = GetScore(client.saldo)
        return {"email": email, "score": score_value}
    finally:
        session.close()

