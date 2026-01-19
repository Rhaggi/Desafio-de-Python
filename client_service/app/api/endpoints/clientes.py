from fastapi import APIRouter, HTTPException
from client_service.app.api.models.schemas import ClienteSchema
from ..models.clients import Cliente, db
from sqlalchemy.orm import sessionmaker
from client_service.app.api.endpoints.score import GetScore


clientes = APIRouter(prefix='/client-service', tags=['client-service'])

@clientes.get("/get-client-by-email/{email}")
def get_client_by_email(email: str):
    """
    Essa é a rota para obter um cliente específico pelo email.
    """
    SessionLocal = sessionmaker(bind=db)
    session = SessionLocal()
    try:
        clients = session.query(Cliente).filter(Cliente.email == email).first()
        if not clients:
            raise HTTPException(status_code=404, detail="Nenhum cliente encontrado.")
        score = GetScore(clients.saldo)
        return {"client": {"id": clients.id, "nome": clients.nome, "telefone": clients.telefone, "correntista": clients.correntista, "saldo": clients.saldo, "email": clients.email}, "score": score}
    finally:
        session.close()

@clientes.post("/add-client")
def add_client(cliente_schema: ClienteSchema):
    """
    Essa é a rota para adicionar um novo cliente a lista de clientes cadastrados no banco de dados.
    """
    SessionLocal = sessionmaker(bind=db)
    session = SessionLocal()
    try:
        if cliente_schema.saldo < 0:
            raise HTTPException(status_code=400, detail="Saldo não pode ser negativo.")
        if not cliente_schema.telefone or len(str(cliente_schema.telefone)) < 10 or len(str(cliente_schema.telefone)) > 11:
            raise HTTPException(status_code=400, detail="Telefone inválido.")
        if session.query(Cliente).filter(Cliente.email == cliente_schema.email).first():
            raise HTTPException(status_code=400, detail="Cliente já cadastrado.")
        if cliente_schema.correntista == False:
            raise HTTPException(status_code=400, detail="Cliente deve ser correntista para ser cadastrado.")
        cliente = Cliente(nome=cliente_schema.nome, email=cliente_schema.email, telefone=cliente_schema.telefone, correntista=cliente_schema.correntista, saldo=cliente_schema.saldo)
        session.add(cliente)
        session.commit()
        session.refresh(cliente)
        score = GetScore(cliente.saldo)
        return {"message": "Cliente adicionado com sucesso!", "client": {"id": cliente.id, "nome": cliente.nome, "email": cliente.email, "saldo": cliente.saldo, "score": score}}
    finally:
        session.close()

@clientes.delete("/delete-client/{email}")
def delete_client(email: str):
    """
    Essa é a rota para excluir um cliente da lista de clientes cadastrados no banco de dados.
    """
    SessionLocal = sessionmaker(bind=db)
    session = SessionLocal()
    try:
        client = session.query(Cliente).filter(Cliente.email == email).first()
        if not client:
            raise HTTPException(status_code=404, detail="Cliente não encontrado.")
        if client.saldo > 0:
            raise HTTPException(status_code=400, detail="Não é possível excluir um cliente com saldo positivo.")
        session.delete(client)
        session.commit()
    finally:
        session.close()
    return {"message": f"Cliente de email {email} excluído com sucesso."}

@clientes.put("/saque-saldo/{email}/{valor}")
def delete_saldo(email: str, valor: float):
    SessionLocal = sessionmaker(bind=db)
    session = SessionLocal()
    try:
        client = session.query(Cliente).filter(Cliente.email == email).first()
        if not client:
            raise HTTPException(status_code=404, detail="Cliente não encontrado.")
        if valor > client.saldo:
            raise HTTPException(status_code=400, detail="Saldo insuficiente para saque.")
        client.saldo -= valor
        session.commit()
        session.refresh(client)
        return {"message": f"Saldo do cliente de email {email} sacado com sucesso. Saldo atual: {client.saldo}"}
    finally:
        session.close()

@clientes.put("/deposito-saldo/{email}/{valor}")
def depositar_saldo(email: str, valor: float):
    SessionLocal = sessionmaker(bind=db)
    session = SessionLocal()
    try:
        client = session.query(Cliente).filter(Cliente.email == email).first()
        if not client:
            raise HTTPException(status_code=404, detail="Cliente não encontrado.")
        if valor <= 0:
            raise HTTPException(status_code=400, detail="Valor de depósito deve ser positivo.")
        client.saldo += valor
        session.commit()
        session.refresh(client)
        return {"message": f"Saldo do cliente de email {email} depositado com sucesso. Saldo atual: {client.saldo}"}
    finally:
        session.close()

@clientes.put("/update-client/{email}")
def update_client(nome: str, email:str, telefone: int):
    """
    Essa é a rota para atualizar um cliente da lista de clientes cadastrados no banco de dados.
    """
    SessionLocal = sessionmaker(bind=db)
    session = SessionLocal()
    try:
        client_db = session.query(Cliente).filter(Cliente.email == email).first()
        if not client_db:
            raise HTTPException(status_code=404, detail="Cliente não encontrado.")
        if not telefone or len(str(telefone)) < 10:
            raise HTTPException(status_code=400, detail="Telefone inválido.")

        for key, value in {"nome": nome, "telefone": telefone}.items():
            setattr(client_db, key, value)
        session.commit()
        session.refresh(client_db)
        score = GetScore(client_db.saldo)
        return {"message": f"Cliente de email {email} atualizado com sucesso.", "client": client_db.nome, "score": score}
    finally:
        session.close()

@clientes.get("/get-saldo/{email}")
def get_saldo(email: str):
    """
    Essa é a rota para obter o saldo de um cliente específico pelo email.
    """
    SessionLocal = sessionmaker(bind=db)
    session = SessionLocal()
    try:
        clients = session.query(Cliente).filter(Cliente.email == email).first()
        if not clients:
            raise HTTPException(status_code=404, detail="Nenhum cliente encontrado.")
        return {"saldo": clients.saldo}
    finally:
        session.close()