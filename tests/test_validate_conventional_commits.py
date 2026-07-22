"""Pruebas del validador de Conventional Commits."""

import unittest

from scripts.validate_conventional_commits import invalid_messages, is_conventional_commit


class ConventionalCommitTests(unittest.TestCase):
    def test_accepts_every_allowed_type(self) -> None:
        allowed_types = (
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

        for commit_type in allowed_types:
            with self.subTest(commit_type=commit_type):
                self.assertTrue(is_conventional_commit(f"{commit_type}: valid description"))

    def test_accepts_scope_and_breaking_change_marker(self) -> None:
        self.assertTrue(is_conventional_commit("feat(mcp): add repository tool"))
        self.assertTrue(is_conventional_commit("refactor(api)!: change response schema"))

    def test_rejects_unknown_type(self) -> None:
        self.assertFalse(is_conventional_commit("feature: add repository tool"))

    def test_rejects_missing_description(self) -> None:
        self.assertFalse(is_conventional_commit("fix:"))
        self.assertFalse(is_conventional_commit("fix: "))

    def test_rejects_invalid_spacing_or_capitalization(self) -> None:
        self.assertFalse(is_conventional_commit("Fix: correct error"))
        self.assertFalse(is_conventional_commit("fix:correct error"))

    def test_rejects_invalid_scope(self) -> None:
        self.assertFalse(is_conventional_commit("feat(MCP): add tool"))
        self.assertFalse(is_conventional_commit("feat(): add tool"))

    def test_returns_all_invalid_messages(self) -> None:
        messages = ["feat: valid", "invalid message", "update: invalid"]

        self.assertEqual(invalid_messages(messages), ["invalid message", "update: invalid"])


if __name__ == "__main__":
    unittest.main()
