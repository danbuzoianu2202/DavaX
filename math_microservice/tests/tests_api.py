import pytest

from app import create_app
from app.extensions import db


@pytest.fixture
def client():
    """
    Create a test client for the Flask application.
    This client can be used to make requests to the application
    and test the API endpoints."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield app.test_client()


def test_pow(client):
    """
    Test the power operation endpoint.
    It sends a POST request with base and exponent,
    and checks if the response contains the correct result.
    """
    response = client.post("/api/v1/pow", json={"base": 2, "exponent": 5})
    assert response.status_code == 200
    assert response.json["result"] == 32


def test_fibonacci(client):
    """Test the Fibonacci operation endpoint.
    It sends a POST request with n and checks if the response
    contains the correct Fibonacci number."""
    response = client.post("/api/v1/fibonacci", json={"n": 7})
    assert response.status_code == 200
    assert response.json["result"] == 13


def test_factorial(client):
    """
    Test the Factorial operation endpoint.
    It sends a POST request with n and checks if the response
    contains the correct factorial result.
    """
    response = client.post("/api/v1/factorial", json={"n": 4})
    assert response.status_code == 200
    assert response.json["result"] == 24


def test_invalid_input(client):
    """
    Test the API with invalid input.
    It sends a POST request with negative n for factorial
    and checks if the response returns a 400 status code.
    """
    response = client.post("/api/v1/factorial", json={"n": -1})
    assert response.status_code == 400
