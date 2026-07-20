#!/usr/bin/env python3
"""Verify that Hapa's public registry is complete, reachable, and discoverable."""

from __future__ import annotations

import json
import socket
import sys
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "nodes.json"
SCOPE_PATH = ROOT / "data" / "repository-scope.json"
CATALOG_PATH = ROOT / "docs" / "NODES.md"
SCOPE_DOC_PATH = ROOT / "docs" / "REPOSITORY_SCOPE.md"
README_PATH = ROOT / "README.md"
GITHUB_API = "https://api.github.com/users/calderwong/repos?sort=full_name&type=public"
GITHUB_PAGE_SIZE = 100
LIVE_DEMOS = {
    "hapa-node-atlas": "https://calderwong.github.io/hapa-node-atlas/",
    "hapa-scroll-site": "https://calderwong.github.io/hapa-scroll-site/",
}


def fetch_json(url: str):
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "hapa-awesome-registry-audit"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def public_account_repos() -> dict[str, dict]:
    repos: list[dict] = []
    page = 1
    while True:
        page_repos = fetch_json(f"{GITHUB_API}&per_page={GITHUB_PAGE_SIZE}&page={page}")
        repos.extend(page_repos)
        if len(page_repos) < GITHUB_PAGE_SIZE:
            break
        page += 1
    return {repo["name"]: repo for repo in repos}


def url_status(url: str) -> int:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "hapa-awesome-registry-audit"},
        method="HEAD",
    )
    for attempt in range(2):
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                return response.status
        except urllib.error.HTTPError as error:
            return error.code
        except (urllib.error.URLError, TimeoutError, socket.timeout):
            if attempt == 1:
                return 0
    return 0


def main() -> int:
    registry = json.loads(REGISTRY_PATH.read_text())
    scope = json.loads(SCOPE_PATH.read_text())
    entries = registry["nodes"]
    registered_names = {entry["repo"].split("/", 1)[1] for entry in entries}
    supporting_entries = scope["publicSupportingRepositories"]
    other_entries = scope["otherPublicAccountRepositories"]
    supporting_names = {entry["repo"].split("/", 1)[1] for entry in supporting_entries}
    other_names = {entry["repo"].split("/", 1)[1] for entry in other_entries}
    github_repos = public_account_repos()
    github_names = set(github_repos)
    classified_names = registered_names | supporting_names | other_names
    catalog = CATALOG_PATH.read_text()
    scope_doc = SCOPE_DOC_PATH.read_text()
    readme = README_PATH.read_text()

    errors: list[str] = []
    if len(entries) != len(registered_names):
        errors.append("registry contains duplicate repositories")
    if len(supporting_entries) != len(supporting_names):
        errors.append("supporting-repository scope contains duplicates")
    if len(other_entries) != len(other_names):
        errors.append("other-repository scope contains duplicates")
    if registered_names & supporting_names or registered_names & other_names or supporting_names & other_names:
        errors.append("repository scope classifications overlap")
    if classified_names != github_names:
        errors.append(
            "account scope/API mismatch: "
            f"unclassified={sorted(github_names - classified_names)} "
            f"not_public={sorted(classified_names - github_names)}"
        )
    expected_counts = {
        "publicAccountRepositories": len(github_names),
        "publicHapaRepositories": len(registered_names),
        "publicSupportingRepositories": len(supporting_names),
        "otherPublicAccountRepositories": len(other_names),
    }
    if scope.get("counts") != expected_counts:
        errors.append(f"scope count mismatch: expected={expected_counts} actual={scope.get('counts')}")
    required_readme_links = {
        "data/nodes.json",
        "docs/NODES.md",
        "data/repository-scope.json",
        "docs/REPOSITORY_SCOPE.md",
        "https://calderwong.github.io/hapa-scroll-site/",
    }
    missing_readme_links = sorted(link for link in required_readme_links if link not in readme)
    if missing_readme_links:
        errors.append(f"README is missing discovery links: {missing_readme_links}")

    for entry in entries:
        url = entry["url"]
        if url not in catalog:
            errors.append(f"human catalog does not link {url}")
        status = url_status(url)
        if status != 200:
            errors.append(f"repository link returned HTTP {status}: {url}")

    entries_by_name = {entry["name"]: entry for entry in entries}
    for name, demo_url in LIVE_DEMOS.items():
        actual_demo_url = entries_by_name.get(name, {}).get("demoUrl")
        if actual_demo_url != demo_url:
            errors.append(f"demo URL mismatch for {name}: {actual_demo_url} != {demo_url}")
            continue
        if demo_url not in catalog or demo_url not in readme:
            errors.append(f"live demo is not linked from both discovery documents: {demo_url}")
        status = url_status(demo_url)
        if status != 200:
            errors.append(f"live demo returned HTTP {status}: {demo_url}")

    for entry in supporting_entries + other_entries:
        name = entry["repo"].split("/", 1)[1]
        expected_url = github_repos.get(name, {}).get("html_url")
        if expected_url and entry["url"] != expected_url:
            errors.append(f"scope URL mismatch for {name}: {entry['url']} != {expected_url}")
    for entry in supporting_entries:
        if entry["url"] not in scope_doc:
            errors.append(f"scope document does not link supporting repository {entry['url']}")

    result = {
        "ok": not errors,
        "schema": registry.get("schemaVersion"),
        "scope_schema": scope.get("schemaVersion"),
        "audited_at": registry.get("auditedAt"),
        "public_account_repositories": len(github_names),
        "registered_hapa_repositories": len(entries),
        "supporting_repositories": len(supporting_names),
        "other_public_account_repositories": len(other_names),
        "errors": errors,
    }
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
