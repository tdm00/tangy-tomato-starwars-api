from fastapi.testclient import TestClient
from starwars_api.main import app

client = TestClient(app)

def test_get_quote_json_format():
    response = client.get("/api/v3/quote?format=json")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert data["version"] == "v3"
    assert "timestamp" in data
    assert "quotes" in data
    assert isinstance(data["quotes"], list)

def test_get_quote_text_format():
    response = client.get("/api/v3/quote?format=text")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert isinstance(response.text, str)
    assert len(response.text) > 0

def test_get_quote_xml_format():
    response = client.get("/api/v3/quote?format=xml")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/xml")
    assert b"<response>" in response.content
    assert b"<quotes>" in response.content

def test_filter_by_category_json():
    response = client.get("/api/v3/quote?category=wisdom&format=json")
    assert response.status_code == 200
    data = response.json()
    assert all(q["category"].lower() == "wisdom" for q in data["quotes"])

def test_filter_by_category_xml():
    response = client.get("/api/v3/quote?category=wisdom&format=xml")
    assert response.status_code == 200
    assert b"<category>wisdom</category>" in response.content