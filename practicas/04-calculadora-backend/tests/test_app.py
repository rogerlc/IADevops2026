from app import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_suma() -> None:
    response = client.get("/suma", params={"a": 10, "b": 5})

    assert response.status_code == 200
    assert response.json() == {"resultado": 15.0}


def test_resta() -> None:
    response = client.get("/resta", params={"a": 10, "b": 5})

    assert response.status_code == 200
    assert response.json() == {"resultado": 5.0}


def test_multiplicacion() -> None:
    response = client.get("/multiplicacion", params={"a": 10, "b": 5})

    assert response.status_code == 200
    assert response.json() == {"resultado": 50.0}


def test_division() -> None:
    response = client.get("/division", params={"a": 10, "b": 5})

    assert response.status_code == 200
    assert response.json() == {"resultado": 2.0}


def test_division_entre_cero() -> None:
    response = client.get("/division", params={"a": 10, "b": 0})

    assert response.status_code == 400
    assert response.json() == {"detail": "No se puede dividir entre cero."}


def test_parametro_invalido() -> None:
    response = client.get("/suma", params={"a": "texto", "b": 5})

    assert response.status_code == 422
