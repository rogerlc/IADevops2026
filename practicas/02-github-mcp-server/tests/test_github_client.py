"""Pruebas del cliente GitHub sin solicitudes de red reales."""

import json

import httpx
import pytest

from github_mcp_server.config import Settings
from github_mcp_server.github_client import GitHubAPIError, GitHubClient


def json_response(data: object, status_code: int = 200) -> httpx.Response:
    return httpx.Response(
        status_code,
        content=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def settings() -> Settings:
    return Settings()


@pytest.mark.asyncio
async def test_get_repository_uses_expected_public_headers(settings: Settings) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/repos/rogerlc/IADevops2026"
        assert "Authorization" not in request.headers
        assert request.headers["X-GitHub-Api-Version"] == "2026-03-10"
        return json_response(
            {
                "full_name": "rogerlc/IADevops2026",
                "description": None,
                "visibility": "public",
                "default_branch": "main",
                "html_url": "https://github.com/rogerlc/IADevops2026",
            }
        )

    async with GitHubClient(settings, transport=httpx.MockTransport(handler)) as client:
        result = await client.get_repository()

    assert result["full_name"] == "rogerlc/IADevops2026"


@pytest.mark.asyncio
async def test_get_repository_is_restricted_to_iadevops2026(settings: Settings) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/repos/rogerlc/IADevops2026"
        return json_response(
            {
                "full_name": "rogerlc/IADevops2026",
                "description": None,
                "visibility": "public",
                "default_branch": "main",
                "html_url": "https://github.com/rogerlc/IADevops2026",
            }
        )

    async with GitHubClient(settings, transport=httpx.MockTransport(handler)) as client:
        result = await client.get_repository()

    assert result["full_name"] == "rogerlc/IADevops2026"
    assert result["visibility"] == "public"


@pytest.mark.asyncio
async def test_list_issues_excludes_pull_requests(settings: Settings) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["state"] == "all"
        assert request.url.params["per_page"] == "10"
        return json_response(
            [
                {"number": 1, "title": "Issue", "state": "open", "html_url": "issue-url"},
                {
                    "number": 2,
                    "title": "PR",
                    "state": "open",
                    "html_url": "pr-url",
                    "pull_request": {},
                },
            ]
        )

    async with GitHubClient(settings, transport=httpx.MockTransport(handler)) as client:
        result = await client.list_repository_issues(state="all", limit=10)

    assert result == [{"number": 1, "title": "Issue", "state": "open", "html_url": "issue-url"}]


@pytest.mark.asyncio
async def test_list_pull_requests_returns_read_only_projection(settings: Settings) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/repos/rogerlc/IADevops2026/pulls"
        return json_response(
            [
                {
                    "number": 3,
                    "title": "Documentation",
                    "state": "open",
                    "draft": True,
                    "html_url": "pr-url",
                }
            ]
        )

    async with GitHubClient(settings, transport=httpx.MockTransport(handler)) as client:
        result = await client.list_repository_pull_requests()

    assert result[0]["draft"] is True


@pytest.mark.asyncio
async def test_list_branches_returns_read_only_projection(settings: Settings) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/repos/rogerlc/IADevops2026/branches"
        assert request.url.params["per_page"] == "5"
        return json_response(
            [{"name": "main", "protected": False, "commit": {"sha": "abc123"}}]
        )

    async with GitHubClient(settings, transport=httpx.MockTransport(handler)) as client:
        result = await client.list_repository_branches(limit=5)

    assert result == [{"name": "main", "protected": False, "commit_sha": "abc123"}]


@pytest.mark.parametrize("state", ["invalid", "OPEN", ""])
@pytest.mark.asyncio
async def test_list_rejects_invalid_state(settings: Settings, state: str) -> None:
    transport = httpx.MockTransport(lambda _: json_response([]))
    async with GitHubClient(settings, transport=transport) as client:
        with pytest.raises(ValueError, match="state"):
            await client.list_repository_issues(state=state)


@pytest.mark.parametrize("limit", [0, 101])
@pytest.mark.asyncio
async def test_list_rejects_invalid_limit(settings: Settings, limit: int) -> None:
    transport = httpx.MockTransport(lambda _: json_response([]))
    async with GitHubClient(settings, transport=transport) as client:
        with pytest.raises(ValueError, match="limit"):
            await client.list_repository_pull_requests(limit=limit)


@pytest.mark.asyncio
async def test_api_error_does_not_expose_token(settings: Settings) -> None:
    async def handler(_: httpx.Request) -> httpx.Response:
        return json_response({"message": "Not Found"}, status_code=404)

    async with GitHubClient(settings, transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(GitHubAPIError, match="404: Not Found") as error:
            await client.get_repository()

    assert "Authorization" not in str(error.value)


@pytest.mark.asyncio
async def test_network_error_is_translated(settings: Settings) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection failed", request=request)

    async with GitHubClient(settings, transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(GitHubAPIError, match="No fue posible consultar GitHub"):
            await client.get_repository()
