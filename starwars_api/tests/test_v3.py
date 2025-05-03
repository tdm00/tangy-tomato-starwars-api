from fastapi.testclient import TestClient
from starwars_api.main import app

client = TestClient(app)


def test_get_all_quotes_json_format():
    response = client.get("/api/v3/quote")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert "quotes" in response.json()


def test_get_quote_text_format():
    response = client.get("/api/v3/quote?format=text")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert "–" in response.text


def test_get_quote_xml_format():
    response = client.get("/api/v3/quote?format=xml")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/xml")
    assert b"<quote>" in response.content


def test_filter_by_character():
    response = client.get("/api/v3/quote?character=Yoda")
    assert response.status_code == 200
    quotes = response.json()["quotes"]
    assert all("Yoda" in q["character"] for q in quotes)


def test_filter_by_category_json():
    response = client.get("/api/v3/quote?category=wisdom")
    assert response.status_code == 200
    quotes = response.json()["quotes"]
    assert all("wisdom" == q["category"] for q in quotes)


def test_filter_by_category_xml():
    response = client.get("/api/v3/quote?category=wisdom&format=xml")
    assert response.status_code == 200
    assert b"<category>wisdom</category>" in response.content


def test_get_quote_by_id_json_format():
    response = client.get("/api/v3/quote/1?format=json")
    assert response.status_code == 200
    data = response.json()
    assert data["quote"]["id"] == 1
    assert "version" in data
    assert "timestamp" in data


def test_get_quote_by_id_text_format():
    response = client.get("/api/v3/quote/3?format=text")
    assert response.status_code == 200
    assert "–" in response.text


def test_get_quote_by_id_xml_format():
    response = client.get("/api/v3/quote/2?format=xml")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/xml")
    assert b"<quote>" in response.content


def test_invalid_format():
    response = client.get("/api/v3/quote?format=unsupported")
    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported format"


def test_quote_not_found():
    response = client.get("/api/v3/quote/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Quote not found"