from fastapi import APIRouter, HTTPException
from client_service.app.api.models.schemas import ClienteSchema
from ..models.clients import Cliente, db
from sqlalchemy.orm import sessionmaker
from client_service.app.api.endpoints.score import GetScore


clientes = APIRouter(prefix='/client-service', tags=['client-Service'])

@clientes.get("/get-clients")
def get_clients():
    """
    Essa é a rota para obter a lista de clientes cadastrados no banco de dados.
    """
    SessionLocal = sessionmaker(bind=db)
    session = SessionLocal()
    try:
        if not session.query(Cliente).first():
            raise HTTPException(status_code=404, detail="Nenhum cliente encontrado.")
        clients = session.query(Cliente).all()
        return clients
    finally:
        session.close()

@clientes.get("/get-client-by-id/{client_id}")
def get_client_by_id(client_id: int):
    """
    Essa é a rota para obter um cliente específico pelo ID.
    """
    SessionLocal = sessionmaker(bind=db)
    session = SessionLocal()
    try:
        clients = session.query(Cliente).filter(Cliente.id == client_id).first()
        if not clients:
            raise HTTPException(status_code=404, detail="Nenhum cliente encontrado.")
        score = GetScore(clients.saldo)
        return {"client": {"id": clients.id, "nome": clients.nome, "telefone": clients.telefone, "correntista": clients.correntista, "saldo": clients.saldo}, "score": score}
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
        cliente = Cliente(nome=cliente_schema.nome, telefone=cliente_schema.telefone, correntista=cliente_schema.correntista, saldo=cliente_schema.saldo)
        session.add(cliente)
        session.commit()
        session.refresh(cliente)
        score = GetScore(cliente.saldo)
        return {"message": "Cliente adicionado com sucesso!", "client": {"id": cliente.id, "nome": cliente.nome, "saldo": cliente.saldo, "score": score}}
    finally:
        session.close()

@clientes.delete("/delete-client/{client_id}")
def delete_client(client_id: int):
    """
    Essa é a rota para excluir um cliente da lista de clientes cadastrados no banco de dados.
    """
    SessionLocal = sessionmaker(bind=db)
    session = SessionLocal()
    try:
        client = session.query(Cliente).filter(Cliente.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Cliente não encontrado.")
        session.delete(client)
        session.commit()
    finally:
        session.close()
    return {"message": f"Cliente de id {client_id} excluído com sucesso."}

@clientes.patch("/update-client/{client_id}")
def update_client(client_id: int, client: ClienteSchema):
    """
    Essa é a rota para atualizar um cliente da lista de clientes cadastrados no banco de dados.
    """
    SessionLocal = sessionmaker(bind=db)
    session = SessionLocal()
    try:
        client_db = session.query(Cliente).filter(Cliente.id == client_id).first()
        if not client_db:
            raise HTTPException(status_code=404, detail="Cliente não encontrado.")
        if client.saldo < 0:
            raise HTTPException(status_code=400, detail="Saldo não pode ser negativo.")
        if not client.telefone or len(str(client.telefone)) < 10:
            raise HTTPException(status_code=400, detail="Telefone inválido.")
        for key, value in client.model_dump().items():
            setattr(client_db, key, value)
        session.commit()
        session.refresh(client_db)
        score = GetScore(client_db.saldo)
        return {"message": f"Cliente de id {client_id} atualizado com sucesso.", "client": client_db.nome, "score": score}
    finally:
        session.close()