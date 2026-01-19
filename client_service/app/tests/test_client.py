from fastapi.testclient import TestClient
from client_service.app.api.core.config import app

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

def test_get_cliente_pelo_email():
    create_client = client.post("/client-service/add-client", json={"nome": "Jon", "email": "jon@teste.com", "telefone": 1234567890, "correntista": True, "saldo": 100})
    client_id = create_client.json()["client"]["id"]
    response = client.get(f"/client-service/get-client-by-email/jon@teste.com")
    assert response.status_code == 200
    assert response.json() == {"client": {"id": client_id, "nome": "Jon", "email": "jon@teste.com", "telefone": 1234567890, "correntista": True, "saldo": 100}, "score": 10.0}

def test_adicionar_cliente():
    new_client = {
        "nome": "Teste Cliente",
        "email": "teste@teste.com",
        "telefone": "1234567890",
        "correntista": True,
        "saldo": 1500,
        
    }
    response = client.post("/client-service/add-client", json=new_client)
    assert response.status_code == 200
    assert response.json() == {"message": "Cliente adicionado com sucesso!", "client": {"id": response.json()["client"]["id"], "nome": "Teste Cliente", "email": "teste@teste.com", "saldo": 1500, "score": 150}}

def test_excluir_cliente():

    client.post("/client-service/add-client", json={"nome": "Ana", "email": "ana@teste.com", "telefone": "1234567890", "correntista": True, "saldo": 0})
    delete_resp = client.delete(f"/client-service/delete-client/ana@teste.com")
    assert delete_resp.status_code == 200
    assert delete_resp.json() == {"message": f"Cliente de email ana@teste.com excluído com sucesso."}

def test_excluir_cliente_nao_encontrado():
    response = client.delete("/client-service/delete-client/emailinvalido@teste.com")
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente não encontrado."

def test_atualizar_cliente():
    client.post("/client-service/add-client", json={"nome": "aline", "email": "aline@teste.com", "telefone": "1234567890", "correntista": True, "saldo": 1000})

    update_response = client.put(f"/client-service/update-client/aline@teste.com?nome=aline Silva&telefone=11999990012")
    assert update_response.status_code == 200
    assert update_response.json() == {'message': f'Cliente de email aline@teste.com atualizado com sucesso.', "client": "aline Silva", "score": 100.0}

def test_adicionar_correntista_como_false():
    new_client = {
        "nome": "alicio",
        "email": "alicio@teste.com",
        "telefone": "1234567890",
        "correntista": False,
        "saldo": 1500
    }

    response = client.post("/client-service/add-client", json=new_client)
    assert response.status_code == 400 
    assert response.json()["detail"] == "Cliente deve ser correntista para ser cadastrado."

def test_atualizar_cliente_nao_encontrado():
    response = client.put("/client-service/update-client/emailinexistente@teste.com?nome=email inexistente&telefone=11999990012")
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente não encontrado."

def test_adicionar_cliente_telefone_invalido():
    new_client = {
        "nome": "Paula",
        "email": "paula@teste.com",
        "telefone": "12345",
        "correntista": True,
        "saldo": 1500
    }
    response = client.post("/client-service/add-client", json=new_client)
    assert response.status_code == 400
    assert response.json()["detail"] == "Telefone inválido."

def test_adicionar_cliente_com_saldo_negativo():
    new_client = {
        "nome": "Laura",
        "email": "laura@teste.com",
        "telefone": "12345678900",
        "correntista": True,
        "saldo": -500
    }
    response = client.post("/client-service/add-client", json=new_client)
    assert response.status_code == 400
    assert response.json()["detail"] == "Saldo não pode ser negativo."

def test_get_cliente_nao_encontrado():
    response = client.get("/client-service/get-client-by-email/emailinvalido@teste.com")
    assert response.status_code == 404
    assert response.json()["detail"] == "Nenhum cliente encontrado."

def test_atualizar_cliente_telefone_invalido():
    client.post("/client-service/add-client", json={"nome": "Joao", "email": "joao@teste.com", "telefone": "1234567890", "correntista": True, "saldo": 100})
    resp = client.put(f"/client-service/update-client/joao@teste.com?nome=joao&telefone=11999")
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Telefone inválido."

def test_sacar_saldo_client():
    client.post("/client-service/add-client", json={"nome": "Mariana", "email": "mariana@teste.com", "telefone": "1234567890", "correntista": True, "saldo": 1000.0})
    sacar_response = client.put(f"/client-service/saque-saldo/mariana@teste.com/200.0")
    assert sacar_response.status_code == 200
    assert sacar_response.json() == {"message": f"Saldo do cliente de email mariana@teste.com sacado com sucesso. Saldo atual: 800.0"}

def test_sacar_saldo_cliente_nao_encontrado():
    response = client.put("/client-service/saque-saldo/emailinvalido@teste.com/100")
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente não encontrado."

def test_depositar_saldo_cliente():
    client.post("/client-service/add-client", json={"nome": "Pedro", "email": "pedro@teste.com", "telefone": "1234567890", "correntista": True, "saldo": 500.0})
    depositar_response = client.put(f"/client-service/deposito-saldo/pedro@teste.com/300")
    assert depositar_response.status_code == 200
    assert depositar_response.json() == {"message": f"Saldo do cliente de email pedro@teste.com depositado com sucesso. Saldo atual: 800.0"}

def test_depositar_saldo_sem_cliente():
    response = client.put("/client-service/deposito-saldo/emailinvalido@teste.com/200")
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente não encontrado."

def test_sacar_saldo_client_insuficiente():
    client.post("/client-service/add-client", json={"nome": "Mariana", "email": "mariana@teste.com", "telefone": "1234567890", "correntista": True, "saldo": 1000.0})
    sacar_response = client.put(f"/client-service/saque-saldo/mariana@teste.com/1200.0")
    assert sacar_response.status_code == 400
    assert sacar_response.json()["detail"] == "Saldo insuficiente para saque."

def test_excluir_cliente_com_saldo():
    client.post("/client-service/add-client", json={"nome": "livia", "email": "livia@teste.com", "telefone": "1234567890", "correntista": True, "saldo": 100})
    response = client.delete("/client-service/delete-client/livia@teste.com")
    assert response.status_code == 400
    assert response.json()["detail"] == "Não é possível excluir um cliente com saldo positivo."

def test_depositar_saldo_negativo():
    client.post("/client-service/add-client", json={"nome": "clara", "email": "clara@teste.com", "telefone": "1234567890", "correntista": True, "saldo": 100})
    response = client.put("/client-service/deposito-saldo/clara@teste.com/-200")
    assert response.status_code == 400
    assert response.json()["detail"] == "Valor de depósito deve ser positivo."

def test_get_saldo_cliente():
    client.post("/client-service/add-client", json={"nome": "Rafael", "email": "rafael@teste.com", "telefone": "1234567890", "correntista": True, "saldo": 100})
    response = client.get("/client-service/get-saldo/rafael@teste.com")
    assert response.status_code == 200
    assert response.json() == {"saldo": 100}

def test_get_saldo_cliente_nao_encontrado():
    response = client.get("/client-service/get-saldo/emailinvalido@teste.com")
    assert response.status_code == 404
    assert response.json()["detail"] == "Nenhum cliente encontrado."
