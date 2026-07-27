"""Tests for the calculator API."""

from fastapi.testclient import TestClient

from calculator_api.app import app

client = TestClient(app)


def test_health() -> None:
    assert client.get("/health").json() == {"status": "ok"}


def test_addition() -> None:
    response = client.get("/suma", params={"a": 8, "b": 2})
    assert response.status_code == 200
    assert response.json()["result"] == 10


def test_subtraction() -> None:
    response = client.get("/resta", params={"a": 8, "b": 2})
    assert response.status_code == 200
    assert response.json()["result"] == 6


def test_multiplication() -> None:
    response = client.get("/multiplicacion", params={"a": 8, "b": 2})
    assert response.status_code == 200
    assert response.json()["result"] == 16


def test_division() -> None:
    response = client.get("/division", params={"a": 8, "b": 2})
    assert response.status_code == 200
    assert response.json()["result"] == 4


def test_division_by_zero() -> None:
    response = client.get("/division", params={"a": 8, "b": 0})
    assert response.status_code == 400
    assert response.json() == {"detail": "No se puede dividir entre cero."}


def test_missing_parameter() -> None:
    response = client.get("/suma", params={"a": 8})
    assert response.status_code == 422
