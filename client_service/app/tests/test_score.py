from client_service.app.api.endpoints.score import GetScore
from fastapi.testclient import TestClient
from client_service.app.api.core.config import app

client = TestClient(app)

def test_score_client_not_found():
    response = client.get("/get-score-by-email/teste@test.com")
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente não encontrado."

def test_score_with_valid_client():
    client.post("/client-service/add-client", json={"nome": "Lucio", "email": "lucio@teste.com", "telefone": "1234567890", "correntista": True, "saldo": 2000})
    response = client.get("/get-score-by-email/lucio@teste.com")
    score_value = response.json()["score"]
    assert response.status_code == 200
    assert response.json() == {"email": "lucio@teste.com", "score": score_value}

def test_score_with_zero_saldo():
    value_score = GetScore(0)
    assert value_score == 0

def test_score_cannot_be_negative():
    value_score = GetScore(-200)
    assert value_score == 00