from api import routes

def test_health():
    response = routes.index()
    response_json = response.json
    assert response.status_code == 200

def test_health_response():
    response = routes.index()
    response_json = response.json
    assert response_json == routes.healthResponse