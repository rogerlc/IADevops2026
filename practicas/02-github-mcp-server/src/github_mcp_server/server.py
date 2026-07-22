"""Definición de herramientas y punto de entrada del MCP Server."""

from typing import Any

from mcp.server.fastmcp import FastMCP

from .config import Settings
from .github_client import GitHubClient

mcp = FastMCP(
    "IADevops2026 GitHub MCP",
    instructions=(
        "Servidor educativo de solo lectura. Todas las consultas están limitadas "
        "a rogerlc/IADevops2026. No crea, modifica ni elimina recursos de GitHub."
    ),
)


async def _run(operation: str, **kwargs: Any) -> Any:
    settings = Settings()
    async with GitHubClient(settings) as client:
        method = getattr(client, operation)
        return await method(**kwargs)


@mcp.tool()
async def get_repository() -> dict[str, Any]:
    """Consulta exclusivamente los metadatos de rogerlc/IADevops2026."""
    return await _run("get_repository")


@mcp.tool()
async def list_repository_issues(
    state: str = "open",
    limit: int = 30,
) -> list[dict[str, Any]]:
    """Lista issues de IADevops2026; state acepta open, closed o all."""
    return await _run("list_repository_issues", state=state, limit=limit)


@mcp.tool()
async def list_repository_pull_requests(
    state: str = "open",
    limit: int = 30,
) -> list[dict[str, Any]]:
    """Lista Pull Requests de IADevops2026; state acepta open, closed o all."""
    return await _run("list_repository_pull_requests", state=state, limit=limit)


@mcp.tool()
async def list_repository_branches(limit: int = 30) -> list[dict[str, Any]]:
    """Lista las ramas de IADevops2026, con un máximo de 100 resultados."""
    return await _run("list_repository_branches", limit=limit)


def main() -> None:  # pragma: no cover - integración de proceso stdio
    """Inicia el MCP Server mediante el transporte local stdio."""
    mcp.run(transport="stdio")


if __name__ == "__main__":  # pragma: no cover
    main()
