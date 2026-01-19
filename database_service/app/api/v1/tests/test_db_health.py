from database_service.app.api.v1.endpoints.db_health import health

def test_health_status():
    response = health()
    assert response == {"status": "O serviço database-service está funcionando corretamente."}