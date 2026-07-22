"""Pruebas de configuración y registro de herramientas MCP."""

import pytest

from github_mcp_server import server
from github_mcp_server.config import (
    GITHUB_OWNER,
    GITHUB_REPOSITORY,
    Settings,
)
from github_mcp_server.server import mcp


def test_settings_are_restricted_to_expected_repository() -> None:
    settings = Settings()

    assert settings.owner == GITHUB_OWNER == "rogerlc"
    assert settings.repository == GITHUB_REPOSITORY == "IADevops2026"
@pytest.mark.asyncio
async def test_server_registers_only_four_read_tools() -> None:
    tools = await mcp.list_tools()

    assert {tool.name for tool in tools} == {
        "get_repository",
        "list_repository_issues",
        "list_repository_pull_requests",
        "list_repository_branches",
    }


@pytest.mark.asyncio
async def test_tool_handlers_delegate_to_read_only_client(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[str, dict[str, object]]] = []

    class FakeClient:
        def __init__(self, settings: Settings) -> None:
            assert settings.owner == "rogerlc"

        async def __aenter__(self) -> "FakeClient":
            return self

        async def __aexit__(self, *_: object) -> None:
            return None

        def __getattr__(self, operation: str):  # type: ignore[no-untyped-def]
            async def execute(**kwargs: object) -> dict[str, str]:
                calls.append((operation, kwargs))
                return {"operation": operation}

            return execute

    monkeypatch.setattr(server, "GitHubClient", FakeClient)

    assert await server.get_repository() == {"operation": "get_repository"}
    assert await server.list_repository_issues(state="all", limit=5) == {
        "operation": "list_repository_issues"
    }
    assert await server.list_repository_pull_requests(state="closed", limit=6) == {
        "operation": "list_repository_pull_requests"
    }
    assert await server.list_repository_branches(limit=7) == {
        "operation": "list_repository_branches"
    }
    assert calls == [
        ("get_repository", {}),
        ("list_repository_issues", {"state": "all", "limit": 5}),
        ("list_repository_pull_requests", {"state": "closed", "limit": 6}),
        ("list_repository_branches", {"limit": 7}),
    ]
