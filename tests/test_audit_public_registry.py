import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "audit_public_registry.py"
SPEC = importlib.util.spec_from_file_location("audit_public_registry", SCRIPT_PATH)
assert SPEC and SPEC.loader
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


class PublicAccountReposTest(unittest.TestCase):
    def test_fetches_one_partial_page(self):
        page = [{"name": "hapa", "html_url": "https://github.com/calderwong/hapa"}]

        with patch.object(audit, "fetch_json", return_value=page) as fetch_json:
            repos = audit.public_account_repos()

        self.assertEqual(repos, {"hapa": page[0]})
        fetch_json.assert_called_once_with(f"{audit.GITHUB_API}&per_page=100&page=1")

    def test_fetches_repositories_beyond_first_100(self):
        first_page = [
            {"name": f"repo-{index:03d}", "html_url": f"https://github.com/calderwong/repo-{index:03d}"}
            for index in range(100)
        ]
        second_page = [
            {"name": "repo-100", "html_url": "https://github.com/calderwong/repo-100"}
        ]

        with patch.object(audit, "fetch_json", side_effect=[first_page, second_page]) as fetch_json:
            repos = audit.public_account_repos()

        self.assertEqual(len(repos), 101)
        self.assertIn("repo-100", repos)
        self.assertEqual(
            [call.args[0] for call in fetch_json.call_args_list],
            [
                f"{audit.GITHUB_API}&per_page=100&page=1",
                f"{audit.GITHUB_API}&per_page=100&page=2",
            ],
        )


if __name__ == "__main__":
    unittest.main()
