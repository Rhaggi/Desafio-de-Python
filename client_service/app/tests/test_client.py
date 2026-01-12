from fastapi.testclient import TestClient
from client_service.app.api.core.config import app
from client_service.app.api.models.clients import Cliente

client = TestClient(app)

def test_get_clients_empty_returns_404():
    from client_service.app.api.models.clients import Cliente, db
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(bind=db)
    session = SessionLocal()
    try:
        session.query(Cliente).delete()
        session.commit()
    finally:
        session.close()

def test_get_client_not_found():
    response = client.get("/client-service/get-clients")
    assert response.status_code == 404
    assert response.json()["detail"] == "Nenhum cliente encontrado."

def test_get_clients():
    create_client = client.post("/client-service/add-client", json={"nome": "Joana", "telefone": 1234567890, "correntista": True, "saldo": 100})
    response = client.get("/client-service/get-clients")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_client_by_id():
    create_client = client.post("/client-service/add-client", json={"nome": "Joao", "telefone": 1234567890, "correntista": True, "saldo": 100})
    client_id = create_client.json()["client"]["id"]
    response = client.get(f"/client-service/get-client-by-id/{client_id}")
    assert response.status_code == 200
    assert response.json() == {"client": {"id": client_id, "nome": "Joao", "telefone": 1234567890, "correntista": True, "saldo": 100}, "score": 10.0}

def test_add_client():
    new_client = {
        "nome": "Teste Cliente",
        "telefone": "1234567890",
        "correntista": True,
        "saldo": 1500
    }
    response = client.post("/client-service/add-client", json=new_client)
    assert response.status_code == 200
    assert response.json() == {"message": "Cliente adicionado com sucesso!", "client": {"id": response.json()["client"]["id"], "nome": "Teste Cliente", "saldo": 1500, "score": 150}}

def test_delete_client():

    create_response = client.post("/client-service/add-client", json={"nome": "Ana", "telefone": "1234567890", "correntista": False, "saldo": 1000})
    client_id = create_response.json()["client"]["id"]

    delete_resp = client.delete(f"/client-service/delete-client/{client_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json() == {"message": f"Cliente de id {client_id} excluído com sucesso."}

def test_delete_user_not_found():
    response = client.delete("/client-service/delete-client/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente não encontrado."

def test_atualizar_cliente():
    create_response = client.post("/client-service/add-client", json={"nome": "Analu", "telefone": "1234567890", "correntista": False, "saldo": 1000})
    client_id = create_response.json()["client"]["id"]

    updated_data = {
        "nome": "Carlos Silva",
        "telefone": "1122334455",
        "correntista": False,
        "saldo": 2500
    }

    update_response = client.patch(f"/client-service/update-client/{client_id}", json=updated_data)
    assert update_response.status_code == 200
    assert update_response.json() == {'message': f'Cliente de id {client_id} atualizado com sucesso.', "client": "Carlos Silva", "score": 250}

def test_atualizar_cliente_not_found():
    updated_data = {
        "nome": "Carlos Silva",
        "telefone": "1122334455",
        "correntista": False,
        "saldo": 2500
    }
    response = client.patch("/client-service/update-client/999", json=updated_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente não encontrado."

def test_add_client_invalid_phone():
    new_client = {
        "nome": "Teste Cliente",
        "telefone": "12345",
        "correntista": True,
        "saldo": 1500
    }
    response = client.post("/client-service/add-client", json=new_client)
    assert response.status_code == 400
    assert response.json()["detail"] == "Telefone inválido."

def test_add_client_negative_saldo():
    new_client = {
        "nome": "Teste Cliente",
        "telefone": "1234567890",
        "correntista": True,
        "saldo": -500
    }
    response = client.post("/client-service/add-client", json=new_client)
    assert response.status_code == 400
    assert response.json()["detail"] == "Saldo não pode ser negativo."

def test_get_client_by_id_not_found():
    response = client.get("/client-service/get-client-by-id/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Nenhum cliente encontrado."

def test_update_client_negative_saldo():
    create = client.post("/client-service/add-client", json={"nome": "Joao", "telefone": "1234567890", "correntista": True, "saldo": 100})
    id = create.json()["client"]["id"]
    resp = client.patch(f"/client-service/update-client/{id}", json={"saldo": -1, "nome": "Joao", "telefone": "1234567890", "correntista": True})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Saldo não pode ser negativo."

def test_update_client_invalid_phone():
    create = client.post("/client-service/add-client", json={"nome": "Joao", "telefone": "1234567890", "correntista": True, "saldo": 100})
    id = create.json()["client"]["id"]
    resp = client.patch(f"/client-service/update-client/{id}", json={"saldo": 100, "nome": "Joao", "telefone": "123", "correntista": True})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Telefone inválido."