"""Backend de la calculadora."""

from fastapi import FastAPI, HTTPException

app = FastAPI(title="Calculadora API")


@app.get("/suma")
def sumar(a: float, b: float) -> dict[str, float]:
    """Suma dos números recibidos como parámetros."""
    return {"resultado": a + b}


@app.get("/resta")
def restar(a: float, b: float) -> dict[str, float]:
    """Resta el segundo número al primero."""
    return {"resultado": a - b}


@app.get("/multiplicacion")
def multiplicar(a: float, b: float) -> dict[str, float]:
    """Multiplica dos números."""
    return {"resultado": a * b}


@app.get("/division")
def dividir(a: float, b: float) -> dict[str, float]:
    """Divide el primer número entre el segundo."""
    if b == 0:
        raise HTTPException(
            status_code=400,
            detail="No se puede dividir entre cero.",
        )

    return {"resultado": a / b}
