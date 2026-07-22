"""Valida mensajes de commit y títulos de Pull Request convencionales."""

from __future__ import annotations

import argparse
import re
import subprocess
from collections.abc import Sequence

ALLOWED_TYPES = (
    "feat",
    "fix",
    "docs",
    "style",
    "refactor",
    "test",
    "build",
    "ci",
    "chore",
    "perf",
    "revert",
)

CONVENTIONAL_COMMIT_PATTERN = re.compile(
    rf"^(?:{'|'.join(ALLOWED_TYPES)})"
    r"(?:\([a-z0-9][a-z0-9._/-]*\))?"
    r"!?: "
    r"\S.*$"
)


def is_conventional_commit(message: str) -> bool:
    """Indica si el asunto cumple el formato y usa un tipo permitido."""
    return CONVENTIONAL_COMMIT_PATTERN.fullmatch(message) is not None


def invalid_messages(messages: Sequence[str]) -> list[str]:
    """Devuelve los asuntos que incumplen la convención."""
    return [message for message in messages if not is_conventional_commit(message)]


def commit_subjects(base: str, head: str) -> list[str]:
    """Obtiene los asuntos de los commits exclusivos del Pull Request."""
    result = subprocess.run(
        ["git", "log", "--format=%s", f"{base}..{head}"],
        check=True,
        capture_output=True,
        encoding="utf-8",
    )
    return [line for line in result.stdout.splitlines() if line]


def build_parser() -> argparse.ArgumentParser:
    """Construye la interfaz de línea de comandos."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="SHA base del Pull Request")
    parser.add_argument("--head", required=True, help="SHA final del Pull Request")
    parser.add_argument("--title", required=True, help="Título del Pull Request")
    return parser


def main() -> int:
    """Valida el título del PR y todos sus asuntos de commit."""
    arguments = build_parser().parse_args()
    messages = [arguments.title, *commit_subjects(arguments.base, arguments.head)]
    failures = invalid_messages(messages)

    if not failures:
        print("El título y todos los commits cumplen Conventional Commits.")
        return 0

    allowed = ", ".join(ALLOWED_TYPES)
    print("Se encontraron mensajes que no cumplen Conventional Commits:")
    for message in failures:
        print(f"- {message}")
    print(f"Tipos permitidos: {allowed}")
    print("Formato esperado: tipo(alcance opcional): descripción")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
