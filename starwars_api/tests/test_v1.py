from fastapi.testclient import TestClient
from starwars_api.main import app

client = TestClient(app)

def test_get_quote():
    response = client.get("/api/v1/quote")
    assert response.status_code == 200
    assert "quote" in response.json()
