import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello, World!" in response.data


def test_health(client):
    assert client.get("/health").get_json() == {"status": "ok"}


def test_execute_accepts_literals(client):
    response = client.get("/execute?code=123")
    assert b"Result of execution: 123" in response.data


def test_execute_rejects_code(client):
    response = client.get("/execute?code=__import__('os').system('id')")
    assert b"Only literal values allowed" in response.data


def test_execute_escapes_html(client):
    response = client.get("/execute?code='<script>alert(1)</script>'")
    assert b"<script>" not in response.data
    assert b"&lt;script&gt;" in response.data
