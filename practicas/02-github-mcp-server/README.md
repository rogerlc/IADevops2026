# Práctica 2: MCP Server para GitHub

## Objetivo

Construir un servidor MCP local y de solo lectura que permita a Codex consultar
exclusivamente el repositorio público `rogerlc/IADevops2026` mediante la API REST
de GitHub.

## Alcance

El servidor expone cuatro herramientas:

- `get_repository`: consulta los datos principales de `rogerlc/IADevops2026`.
- `list_repository_issues`: lista los issues del repositorio.
- `list_repository_pull_requests`: lista los Pull Requests del repositorio.
- `list_repository_branches`: lista las ramas del repositorio.

No contiene herramientas de escritura y no acepta otro propietario o repositorio
como entrada. Como el repositorio es público, no utiliza tokens ni otras
credenciales.

## Requisitos

- Python 3.12.

## Instalación local

Desde la raíz del repositorio, en PowerShell:

```powershell
& 'C:\Users\rogei\AppData\Local\Programs\Python\Python312\python.exe' -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".\practicas\02-github-mcp-server[dev]"
```

## Ejecución

```powershell
.\.venv\Scripts\iadevops-github-mcp.exe
```

El proceso usa `stdio`; por ello no muestra una interfaz web y normalmente será
iniciado por un cliente MCP como Codex.

## Validación

```powershell
.\.venv\Scripts\python.exe -m pytest .\practicas\02-github-mcp-server
.\.venv\Scripts\python.exe -m ruff check .\practicas\02-github-mcp-server
```

Las pruebas usan un transporte HTTP simulado y no necesitan credenciales ni
realizan solicitudes a GitHub.

## Limitaciones

- Solo funciona con `rogerlc/IADevops2026`.
- Requiere conectividad con `api.github.com` durante el uso real.
- Está sujeto al límite de 60 solicitudes públicas por hora asociado a la IP.
- La primera versión no crea ni modifica recursos.

## Referencias oficiales

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [GitHub REST API](https://docs.github.com/rest)
- [Autenticación de GitHub REST API](https://docs.github.com/rest/authentication)
