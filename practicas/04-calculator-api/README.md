# Práctica 4: API de calculadora en un contenedor

Backend mínimo construido con Python 3.12 y FastAPI.

## Endpoints

| Método | Ruta | Ejemplo | Resultado |
| --- | --- | --- | --- |
| GET | `/health` | `/health` | Estado del servicio |
| GET | `/suma` | `/suma?a=8&b=2` | `10` |
| GET | `/resta` | `/resta?a=8&b=2` | `6` |
| GET | `/multiplicacion` | `/multiplicacion?a=8&b=2` | `16` |
| GET | `/division` | `/division?a=8&b=2` | `4` |

La división entre cero responde con HTTP `400`. Los parámetros ausentes o
inválidos responden con HTTP `422`.

## Ejecutar localmente

```powershell
python -m pip install -e ".[dev]"
uvicorn calculator_api.app:app --reload
```

Documentación interactiva:

- Swagger UI: <http://localhost:8000/docs>
- OpenAPI: <http://localhost:8000/openapi.json>

## Ejecutar pruebas

```powershell
python -m pytest
python -m ruff check .
```

## Construir y ejecutar el contenedor

Desde esta carpeta:

```powershell
docker build -t iadevops-calculator-api .
docker run --rm -p 8000:8000 iadevops-calculator-api
```

Probar:

```powershell
Invoke-RestMethod "http://localhost:8000/suma?a=8&b=2"
```
