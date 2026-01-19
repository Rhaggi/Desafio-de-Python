from fastapi import APIRouter, Depends, Form, HTTPException, Query
from database_service.app.api.v1.models.client_model import Cliente, get_db
from sqlalchemy.orm import Session
import httpx

db_clients = APIRouter(prefix='/database-service', tags=['database-service'])

BASE_URL = "http://127.0.0.1:8000/client-service"

@db_clients.get("/clientes")
def listar_clientes(db: Session = Depends(get_db)):
    clientes = db.query(Cliente).all()
    if not clientes:
        raise HTTPException(status_code=404, detail="Nenhum cliente encontrado.")
    return [{
        "id": cliente.id,
        "nome": cliente.nome,
        "email": cliente.email,
        "telefone": cliente.telefone,
        "saldo": cliente.saldo,

    }
    for cliente in clientes
    ]

@db_clients.post('/adicionar')
async def adicionar(nome: str = Form(...), email: str = Form(...), telefone: int = Form(...), correntista: bool = Form(...), saldo: float = Form(...)):
    if saldo < 0:
        raise HTTPException(status_code=400, detail="O saldo não pode ser negativo.")
    if correntista != True:
        raise HTTPException(status_code=400, detail="Deve ser correntista para se cadastrar no banco.")
    if len(str(telefone)) < 10 or len(str(telefone)) > 11:
        raise HTTPException(status_code=400, detail="Telefone inválido.")
    dados = {
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "correntista": correntista,
        "saldo": saldo
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/add-client", json=dados)
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail= response.json().get("detail", "Erro no serviço de clientes"))
    
@db_clients.get('/buscar')
async def buscar(email: str):
    if not email:
        raise HTTPException(status_code=404, detail="Nenhum cliente encontrado.")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/get-client-by-email/{email}")
        if response.status_code == 200:
            return response.json()
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Nenhum cliente encontrado.")
    
@db_clients.put('/atualizar')
async def atualizar(email: str = Query(...), nome: str = Query(...),  telefone: int = Query(...)):
    if len(str(telefone)) < 10 or len(str(telefone)) > 11:
        raise HTTPException(status_code=400, detail="Telefone inválido.")
    async with httpx.AsyncClient() as client:
        response = await client.put(f'{BASE_URL}/update-client/{email}', params = {"nome": nome, "telefone": telefone})
        if response.status_code == 200:
            return "message: Cliente atualizado com sucesso.", response.json() 
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Nenhum cliente encontrado.")
    
@db_clients.delete('/excluir')
async def excluir(email: str):
    if not email:
        raise HTTPException(status_code=404, detail="Nenhum cliente encontrado.")
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{BASE_URL}/delete-client/{email}")
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail= response.json().get("detail", "Erro no serviço de clientes"))