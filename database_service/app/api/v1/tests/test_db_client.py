
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import httpx
from database_service.app.api.v1.core.config_db import app_db
from database_service.app.api.v1.models.client_model import Cliente, get_db

client = TestClient(app_db)

BASE_URL = "http://127.0.0.1:8000/client-service"

def _get_db_session() -> Session:
    gen = get_db()
    db = next(gen)
    return db, gen

def _close(gen):
    try:
        next(gen)
    except StopIteration:
        pass

def _clear():
    db, gen = _get_db_session()
    try:
        db.query(Cliente).delete()
        db.commit()
    finally:
        _close(gen)


class FakeResponse:
    def __init__(self, code, payload):
        self.status_code = code
        self._payload = payload

    def json(self):
        return self._payload

class MockAsyncClient:
    def __init__(self, responses):
        self.responses = responses

    async def __aenter__(self): return self
    async def __aexit__(self, *args): return False

    def _r(self, m, url):
        return FakeResponse(*self.responses.get((m,url), (404,{"detail":"Mocked"})))

    async def post(self, url, json=None): return self._r("POST",url)
    async def get(self, url): return self._r("GET",url)
    async def put(self, url, params=None): return self._r("PUT",url)
    async def delete(self, url): return self._r("DELETE",url)


@pytest.fixture
def mock_http(monkeypatch):
    def apply(responses: dict):
        monkeypatch.setattr(httpx, "AsyncClient", lambda: MockAsyncClient(responses))
    return apply


def test_listar_clientes_vazio():
    _clear()
    r = client.get("/database-service/clientes")
    assert r.status_code == 404

def test_listar_clientes():
    _clear()
    db, gen = _get_db_session()
    try:
        db.add(Cliente(nome="Alice",email="alice@gmail.com",telefone=1111111111,correntista=True,saldo=10))
        db.commit()
    finally:
        _close(gen)

    r = client.get("/database-service/clientes")
    assert r.status_code == 200
    assert len(r.json()) == 1

def test_adicionar_saldo_negativo():
    data = {"nome":"A","email":"a@a.com","telefone":"1111111111","correntista":"true","saldo":"-1"}
    r = client.post("/database-service/adicionar", data=data)
    assert r.status_code == 400

def test_adicionar_correntista_false():
    data = {"nome":"A","email":"a@a.com","telefone":"1111111111","correntista":"false","saldo":"10"}
    r = client.post("/database-service/adicionar", data=data)
    assert r.status_code == 400

def test_adicionar_telefone_invalido():
    data = {"nome":"A","email":"a@a.com","telefone":"123","correntista":"true","saldo":"10"}
    r = client.post("/database-service/adicionar", data=data)
    assert r.status_code == 400

def test_adicionar(mock_http):
    mock_http({
        ("POST", f"{BASE_URL}/add-client"): (200, {"ok":True})
    })
    data = {"nome":"A","email":"a@a.com","telefone":"1111111111","correntista":"true","saldo":"10"}
    r = client.post("/database-service/adicionar", data=data)
    assert r.status_code == 200
    assert r.json() == {"ok":True}

def test_adicionar_erro_generico(mock_http):
    mock_http({
        ("POST", f"{BASE_URL}/add-client"): (500, {})
    })
    data = {"nome":"A","email":"a@a.com","telefone":"1111111111","correntista":"true","saldo":"10"}
    r = client.post("/database-service/adicionar", data=data)
    assert r.status_code == 500
    assert r.json()["detail"] == "Erro no serviço de clientes"

def test_buscar_email_vazio():
    resp = client.get("/database-service/buscar", params={"email": ""})
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Nenhum cliente encontrado."

def test_buscar_email_nao_cadastrado():
    resp = client.get("/database-service/buscar", params={"email": "naoexiste@gmail.com"})
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Nenhum cliente encontrado."

def test_buscar(mock_http):
    mock_http({
        ("GET", f"{BASE_URL}/get-client-by-email/x"): (200, {"x":1})
    })
    r = client.get("/database-service/buscar", params={"email":"x"})
    assert r.status_code == 200
    assert r.json() == {"x":1}

def test_atualizar_email_vazio():
    resp = client.put(
        "/database-service/atualizar",
        params={"email": "", "nome": "A", "telefone": "1111111111"}
    )
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Nenhum cliente encontrado."


def test_atualizar_tel_invalido():
    r = client.put("/database-service/atualizar",
                   params={"email":"a","nome":"b","telefone":"123"})
    assert r.status_code == 400

def test_atualizar(mock_http):
    mock_http({
        ("PUT", f"{BASE_URL}/update-client/a"): (200, {"ok":1})
    })
    r = client.put("/database-service/atualizar",
                   params={"email":"a","nome":"b","telefone":"1111111111"})
    assert r.status_code == 200
    assert r.json()[1] == {"ok":1}

def test_excluir_email_vazio():
    resp = client.delete("/database-service/excluir", params={"email": ""})
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Nenhum cliente encontrado."


def test_excluir(mock_http):
    mock_http({
        ("DELETE", f"{BASE_URL}/delete-client/a"): (200, {"ok":True})
    })
    r = client.delete("/database-service/excluir", params={"email":"a"})
    assert r.status_code == 200

def test_excluir_erro_generico(mock_http):
    mock_http({
        ("DELETE", f"{BASE_URL}/delete-client/a"): (500, {})
    })
    r = client.delete("/database-service/excluir", params={"email":"a"})
    assert r.status_code == 500