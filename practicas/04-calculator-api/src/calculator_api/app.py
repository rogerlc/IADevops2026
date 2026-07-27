"""Minimal HTTP API for calculator operations."""

from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Calculator API",
    description="API educativa con operaciones aritméticas básicas.",
    version="1.0.0",
)


def response(operation: str, a: float, b: float, result: float) -> dict[str, float | str]:
    """Build a consistent operation response."""
    return {"operation": operation, "a": a, "b": b, "result": result}


@app.get("/health")
def health() -> dict[str, str]:
    """Report whether the service is ready."""
    return {"status": "ok"}


@app.get("/suma")
def add(a: float, b: float) -> dict[str, float | str]:
    """Add two numbers."""
    return response("suma", a, b, a + b)


@app.get("/resta")
def subtract(a: float, b: float) -> dict[str, float | str]:
    """Subtract the second number from the first."""
    return response("resta", a, b, a - b)


@app.get("/multiplicacion")
def multiply(a: float, b: float) -> dict[str, float | str]:
    """Multiply two numbers."""
    return response("multiplicacion", a, b, a * b)


@app.get("/division")
def divide(a: float, b: float) -> dict[str, float | str]:
    """Divide the first number by the second."""
    if b == 0:
        raise HTTPException(status_code=400, detail="No se puede dividir entre cero.")
    return response("division", a, b, a / b)
