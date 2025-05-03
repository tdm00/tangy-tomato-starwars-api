from fastapi.testclient import TestClient
from starwars_api.main import app

client = TestClient(app)

def test_get_all_quotes_json():
    response = client.get("/api/v3/quote")
    assert response.status_code == 200
    assert response.json()["version"] == "v3"

def test_filter_by_character():
    response = client.get("/api/v3/quote?character=Yoda")
    assert response.status_code == 200
    quotes = response.json()["quotes"]
    assert all(q["character"] == "Yoda" for q in quotes)

def test_filter_by_category():
    response = client.get("/api/v3/quote?category=wisdom")
    assert response.status_code == 200
    quotes = response.json()["quotes"]
    assert all(q["category"] == "wisdom" for q in quotes)

def test_filter_by_category_xml():
    response = client.get("/api/v3/quote?category=wisdom&format=xml")
    assert response.status_code == 200
    assert b"<category>wisdom</category>" in response.content

def test_get_quote_by_id_json_format():
    response = client.get("/api/v3/quote?id=1")
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "v3"
    assert data["quote"]["id"] == 1

def test_get_quote_by_id_text_format():
    response = client.get("/api/v3/quote?id=1&format=text")
    assert response.status_code == 200
    assert b"Do. Or do not." in response.content

def test_get_quote_by_id_xml_format():
    response = client.get("/api/v3/quote?id=1&format=xml")
    assert response.status_code == 200
    assert b"<quote>" in response.content
    assert b"<character>Yoda</character>" in response.content

def test_get_quote_xml_format():
    response = client.get("/api/v3/quote?format=xml")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/xml")

# 🚫 Failure scenarios
def test_get_invalid_id():
    response = client.get("/api/v3/quote?id=9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Quote not found"

def test_invalid_format():
    response = client.get("/api/v3/quote?format=unsupported")
    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported format"

def test_empty_result_filters():
    response = client.get("/api/v3/quote?character=NotACharacter")
    assert response.status_code == 200
    assert response.json()["quotes"] == []


    