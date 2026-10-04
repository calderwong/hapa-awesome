import contextlib
import importlib.util
import io
import http.client
import json
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "audit_public_registry.py"
SPEC = importlib.util.spec_from_file_location("audit_public_registry", SCRIPT_PATH)
assert SPEC and SPEC.loader
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


def repository(index):
    name = f"repo-{index:04d}"
    return {"id": index + 1, "name": name, "full_name": f"calderwong/{name}",
            "private": False, "html_url": f"https://github.com/calderwong/{name}"}


def count(number):
    return {"public_repos": number}


class PublicAccountReposTest(unittest.TestCase):
    def test_empty_partial_exact_and_multiple_pages(self):
        for total in (0, 1, 99, 100, 101, 200, 251, 1001):
            with self.subTest(total=total):
                items = [repository(i) for i in range(total)]
                pages = [items[i:i + 100] for i in range(0, total, 100)]
                responses = [count(total), *pages, [], count(total)]
                with patch.object(audit, "fetch_json", side_effect=responses) as fetch:
                    repos = audit.public_account_repos()
                self.assertEqual(repos, {repo["name"]: repo for repo in items})
                self.assertEqual([call.args[0] for call in fetch.call_args_list], [
                    audit.GITHUB_ACCOUNT_API,
                    *[f"{audit.GITHUB_API}&per_page=100&page={p}"
                      for p in range(1, len(pages) + 2)],
                    audit.GITHUB_ACCOUNT_API,
                ])

    def test_short_page_does_not_silently_end_enumeration(self):
        with patch.object(audit, "fetch_json", side_effect=[
            count(2), [repository(0)], [repository(1)], [], count(2)
        ]):
            self.assertEqual(len(audit.public_account_repos()), 2)

    def test_truncation_or_concurrent_count_change_is_incomplete(self):
        for before, after in ((2, 2), (1, 2), (2, 1), (0, 0)):
            with self.subTest(before=before, after=after):
                with patch.object(audit, "fetch_json", side_effect=[
                    count(before), [repository(0)], [], count(after)
                ]):
                    with self.assertRaisesRegex(audit.IncompleteInventoryError, "count mismatch") as error:
                        audit.public_account_repos()
                self.assertEqual(error.exception.observed, 1)

    def test_duplicate_names_ids_and_repeated_page_are_incomplete(self):
        same_name = dict(repository(0), id=3)
        same_id = dict(repository(1), id=1)
        for duplicate in (repository(0), same_name, same_id):
            with self.subTest(duplicate=duplicate):
                with patch.object(audit, "fetch_json", side_effect=[
                    count(2), [repository(0)], [duplicate]
                ]):
                    with self.assertRaisesRegex(audit.IncompleteInventoryError, "duplicate") as error:
                        audit.public_account_repos()
                self.assertEqual(error.exception.page, 2)
                self.assertEqual(error.exception.observed, 1)

    def test_malformed_pages_and_entries_are_incomplete(self):
        invalid = [None, {"message": "API error"}, "text", [None], [{}],
                   [dict(repository(0), private=True)],
                   [dict(repository(0), id=True)], [dict(repository(0), name="")],
                   [dict(repository(0), full_name="other/repo")],
                   [dict(repository(0), html_url="https://example.org")],
                   [repository(i) for i in range(101)]]
        for page in invalid:
            with self.subTest(page=page):
                with patch.object(audit, "fetch_json", side_effect=[count(1), page]):
                    with self.assertRaises(audit.IncompleteInventoryError):
                        audit.public_account_repos()

    def test_invalid_account_count_is_incomplete(self):
        for account in (None, [], {}, count(-1), count(True), count("1")):
            with self.subTest(account=account):
                with patch.object(audit, "fetch_json", return_value=account):
                    with self.assertRaisesRegex(audit.IncompleteInventoryError, "invalid account"):
                        audit.public_account_repos()

    def test_transport_rate_limit_timeout_and_invalid_json_never_return_partial(self):
        failures = [http.client.IncompleteRead(b"partial", 100),
                    urllib.error.HTTPError("url", 403, "rate limited", {}, None),
                    urllib.error.HTTPError("url", 429, "rate limited", {}, None),
                    urllib.error.HTTPError("url", 500, "server error", {}, None),
                    urllib.error.URLError("offline"), TimeoutError("timed out"),
                    json.JSONDecodeError("invalid", "x", 0)]
        for failure in failures:
            for stage in ("before", "page", "after"):
                with self.subTest(failure=failure, stage=stage):
                    responses = {"before": [failure],
                                 "page": [count(1), [repository(0)], failure],
                                 "after": [count(1), [repository(0)], [], failure]}[stage]
                    with patch.object(audit, "fetch_json", side_effect=responses):
                        with self.assertRaises(audit.IncompleteInventoryError):
                            audit.public_account_repos()

    def test_main_reports_incomplete_json_and_skips_downstream_checks(self):
        error = audit.IncompleteInventoryError("page 2 unavailable", 100, 2)
        with patch.object(audit, "public_account_repos", side_effect=error), \
                patch.object(audit, "url_status") as status, \
                contextlib.redirect_stdout(io.StringIO()) as output:
            result = audit.main()
        self.assertEqual(result, 1)
        report = json.loads(output.getvalue())
        self.assertFalse(report["ok"])
        self.assertFalse(report["inventory_complete"])
        self.assertIsNone(report["public_account_repositories"])
        self.assertEqual(report["observed_public_account_repositories"], 100)
        self.assertEqual(report["failed_page"], 2)
        self.assertEqual(report["errors"], ["page 2 unavailable"])
        status.assert_not_called()

    def test_complete_inventory_is_distinct_from_passing_audit(self):
        registry = json.loads(audit.REGISTRY_PATH.read_text())
        scope = json.loads(audit.SCOPE_PATH.read_text())
        entries = registry["nodes"] + scope["publicSupportingRepositories"] + scope["otherPublicAccountRepositories"]
        repos = {entry["repo"].split("/", 1)[1]: {"html_url": entry["url"]} for entry in entries}
        for reachability, expected_ok in ((200, True), (503, False)):
            with self.subTest(reachability=reachability):
                with patch.object(audit, "public_account_repos", return_value=repos), \
                        patch.object(audit, "url_status", return_value=reachability), \
                        contextlib.redirect_stdout(io.StringIO()) as output:
                    result = audit.main()
                report = json.loads(output.getvalue())
                self.assertEqual(result, 0 if expected_ok else 1)
                self.assertEqual(report["ok"], expected_ok)
                self.assertTrue(report["inventory_complete"])
                self.assertEqual(report["public_account_repositories"], len(repos))


if __name__ == "__main__":
    unittest.main()
