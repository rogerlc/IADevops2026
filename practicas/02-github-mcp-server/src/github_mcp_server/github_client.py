"""Cliente HTTP mínimo para las consultas de solo lectura a GitHub."""

from collections.abc import Mapping
from typing import Any

import httpx

from .config import Settings


class GitHubAPIError(RuntimeError):
    """Representa una respuesta no exitosa o inválida de GitHub."""


class GitHubClient:
    """Cliente asíncrono limitado al repositorio configurado."""

    def __init__(
        self,
        settings: Settings,
        *,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._settings = settings
        self._client = httpx.AsyncClient(
            base_url=settings.api_url,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "IADevops2026-GitHub-MCP-Server/0.1.0",
                "X-GitHub-Api-Version": settings.api_version,
            },
            timeout=httpx.Timeout(10.0),
            transport=transport,
        )

    async def __aenter__(self) -> "GitHubClient":
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        """Libera las conexiones HTTP."""
        await self._client.aclose()

    async def _get(
        self,
        path: str,
        *,
        params: Mapping[str, str | int] | None = None,
    ) -> Any:
        try:
            response = await self._client.get(path, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as error:
            message = "GitHub rechazó la solicitud."
            try:
                detail = error.response.json().get("message")
                if detail:
                    message = str(detail)
            except (ValueError, AttributeError):
                pass
            raise GitHubAPIError(
                f"GitHub API respondió {error.response.status_code}: {message}"
            ) from error
        except (httpx.RequestError, ValueError) as error:
            raise GitHubAPIError(f"No fue posible consultar GitHub: {error}") from error

    @property
    def _repository_path(self) -> str:
        return f"/repos/{self._settings.owner}/{self._settings.repository}"

    async def get_repository(self) -> dict[str, Any]:
        """Devuelve los metadatos principales del único repositorio permitido."""
        data = await self._get(self._repository_path)
        return {
            "full_name": data["full_name"],
            "description": data.get("description"),
            "visibility": data["visibility"],
            "default_branch": data["default_branch"],
            "html_url": data["html_url"],
        }

    async def list_repository_issues(
        self,
        *,
        state: str = "open",
        limit: int = 30,
    ) -> list[dict[str, Any]]:
        """Lista issues reales, excluyendo Pull Requests devueltos por este endpoint."""
        self._validate_list_parameters(state, limit)
        data = await self._get(
            f"{self._repository_path}/issues",
            params={"state": state, "per_page": limit},
        )
        return [
            {
                "number": issue["number"],
                "title": issue["title"],
                "state": issue["state"],
                "html_url": issue["html_url"],
            }
            for issue in data
            if "pull_request" not in issue
        ]

    async def list_repository_pull_requests(
        self,
        *,
        state: str = "open",
        limit: int = 30,
    ) -> list[dict[str, Any]]:
        """Lista Pull Requests del único repositorio permitido."""
        self._validate_list_parameters(state, limit)
        data = await self._get(
            f"{self._repository_path}/pulls",
            params={"state": state, "per_page": limit},
        )
        return [
            {
                "number": pull_request["number"],
                "title": pull_request["title"],
                "state": pull_request["state"],
                "draft": pull_request.get("draft", False),
                "html_url": pull_request["html_url"],
            }
            for pull_request in data
        ]

    async def list_repository_branches(self, *, limit: int = 30) -> list[dict[str, Any]]:
        """Lista ramas del único repositorio permitido."""
        self._validate_limit(limit)
        data = await self._get(
            f"{self._repository_path}/branches",
            params={"per_page": limit},
        )
        return [
            {
                "name": branch["name"],
                "protected": branch["protected"],
                "commit_sha": branch["commit"]["sha"],
            }
            for branch in data
        ]

    @staticmethod
    def _validate_list_parameters(state: str, limit: int) -> None:
        if state not in {"open", "closed", "all"}:
            raise ValueError("state debe ser open, closed o all.")
        GitHubClient._validate_limit(limit)

    @staticmethod
    def _validate_limit(limit: int) -> None:
        if not 1 <= limit <= 100:
            raise ValueError("limit debe estar entre 1 y 100.")
