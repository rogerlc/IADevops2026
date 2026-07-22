"""Configuración segura y alcance fijo del servidor."""

from dataclasses import dataclass

GITHUB_OWNER = "rogerlc"
GITHUB_REPOSITORY = "IADevops2026"
GITHUB_API_URL = "https://api.github.com"
GITHUB_API_VERSION = "2026-03-10"


@dataclass(frozen=True, slots=True)
class Settings:
    """Valores necesarios para acceder a GitHub sin ampliar el alcance."""

    owner: str = GITHUB_OWNER
    repository: str = GITHUB_REPOSITORY
    api_url: str = GITHUB_API_URL
    api_version: str = GITHUB_API_VERSION
