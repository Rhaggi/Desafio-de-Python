from client_service.app.api.endpoints.score import GetScore
from fastapi.testclient import TestClient
from client_service.app.api.core.config import app

client = TestClient(app)

def test_score_client_not_found():
    response = client.get("/get-score/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente não encontrado."

def test_score_with_valid_client():
    response = client.get("/get-score/1")
    client_id = response.json()["client_id"]
    score_value = response.json()["score"]
    assert response.status_code == 200
    assert response.json() == {"client_id": client_id, "score": score_value}

def test_score_return_type():
    value_score = GetScore(500)
    assert isinstance(value_score, float)

def test_score_with_zero_saldo():
    value_score = GetScore(0)
    assert value_score == 0

def test_score_cannot_be_negative():
    value_score = GetScore(-200)
    assert value_score == 00

def test_score_with_large_saldo():
    value_score = GetScore(10000000)
    assert value_score == 1000