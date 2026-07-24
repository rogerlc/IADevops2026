import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SecurityConfigurationTests(unittest.TestCase):
    def test_workflow_contains_secret_scan(self) -> None:
        workflow = (ROOT / ".github/workflows/quality.yml").read_text(
            encoding="utf-8"
        )

        self.assertIn("name: Secret Scan", workflow)
        self.assertIn("gitleaks/gitleaks-action@", workflow)
        self.assertIn("fetch-depth: 0", workflow)

    def test_local_secret_files_are_ignored(self) -> None:
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")

        for pattern in (".env", ".env.*", "*.key", "*.pem", "id_ed25519"):
            with self.subTest(pattern=pattern):
                self.assertIn(pattern, gitignore)

    def test_environment_example_contains_only_placeholders(self) -> None:
        example = (ROOT / ".env.example").read_text(encoding="utf-8")
        placeholder = "DB_" + "PASSWORD=CHANGE_ME"

        self.assertIn(placeholder, example)
        self.assertNotIn("secret-test-key", example)

    def test_gitleaks_extends_default_rules(self) -> None:
        config = (ROOT / ".gitleaks.toml").read_text(encoding="utf-8")

        self.assertIn("useDefault = true", config)
        self.assertIn('id = "database-password-assignment"', config)


if __name__ == "__main__":
    unittest.main()
