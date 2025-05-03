from fastapi.testclient import TestClient
from starwars_api.main import app

client = TestClient(app)

def test_get_quote_v2():
    response = client.get("/api/v2/quote")
    assert response.status_code == 200
    json_data = response.json()
    assert "quote" in json_data
    assert "version" in json_data
    assert json_data["version"] == "v2"
    assert "timestamp" in json_data