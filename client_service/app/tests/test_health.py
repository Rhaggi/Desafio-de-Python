from client_service.app.api.endpoints.health import health

def test_health_status():
    response = health()
    assert response == {"status": "O serviço client-service está funcionando corretamente."}

# def test_health_not_working():
#     response = health()
#     assert response != {"status": "O serviço client-service não está funcionando."}