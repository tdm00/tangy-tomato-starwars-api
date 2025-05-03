from fastapi.testclient import TestClient
from starwars_api.main import app

client = TestClient(app)


def test_v3_json_format():
    response = client.get("/api/v3/quote")
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "v3"
    assert "timestamp" in data
    assert isinstance(data["quotes"], list)
    assert len(data["quotes"]) > 0


def test_v3_text_format():
    response = client.get("/api/v3/quote?format=text")
    assert response.status_code == 200
    assert "API Version: v3" in response.text
    assert "Timestamp:" in response.text


def test_v3_search_by_character():
    response = client.get("/api/v3/quote?character=Yoda")
    assert response.status_code == 200
    data = response.json()
    for quote in data["quotes"]:
        assert quote["character"].lower() == "yoda"


def test_v3_search_by_category():
    response = client.get("/api/v3/quote?category=wisdom")
    assert response.status_code == 200
    data = response.json()
    for quote in data["quotes"]:
        assert quote["category"].lower() == "wisdom"