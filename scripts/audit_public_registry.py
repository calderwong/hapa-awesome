#!/usr/bin/env python3
"""Verify that Hapa's public registry is complete, reachable, and discoverable."""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "nodes.json"
CATALOG_PATH = ROOT / "docs" / "NODES.md"
README_PATH = ROOT / "README.md"
GITHUB_API = "https://api.github.com/users/calderwong/repos?per_page=100&sort=full_name&type=public"
EXTRA_PUBLIC_REPOS = {"CardAppPrototype", "mtplx", "overwatch"}


def fetch_json(url: str):
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "hapa-awesome-registry-audit"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def public_hapa_repos() -> set[str]:
    repos = fetch_json(GITHUB_API)
    return {
        repo["name"]
        for repo in repos
        if "hapa" in repo["name"].lower() or repo["name"] in EXTRA_PUBLIC_REPOS
    }


def url_status(url: str) -> int:
    request = urllib.request.Request(url, headers={"User-Agent": "hapa-awesome-registry-audit"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.status
    except urllib.error.HTTPError as error:
        return error.code


def main() -> int:
    registry = json.loads(REGISTRY_PATH.read_text())
    entries = registry["nodes"]
    registered_names = {entry["repo"].split("/", 1)[1] for entry in entries}
    github_names = public_hapa_repos()
    catalog = CATALOG_PATH.read_text()
    readme = README_PATH.read_text()

    errors: list[str] = []
    if len(entries) != len(registered_names):
        errors.append("registry contains duplicate repositories")
    if registered_names != github_names:
        errors.append(f"registry/API mismatch: missing={sorted(github_names - registered_names)} extra={sorted(registered_names - github_names)}")
    if "data/nodes.json" not in readme or "docs/NODES.md" not in readme:
        errors.append("README does not link both public registries")

    for entry in entries:
        url = entry["url"]
        if url not in catalog:
            errors.append(f"human catalog does not link {url}")
        status = url_status(url)
        if status != 200:
            errors.append(f"repository link returned HTTP {status}: {url}")

    result = {
        "ok": not errors,
        "schema": registry.get("schemaVersion"),
        "audited_at": registry.get("auditedAt"),
        "registered_repositories": len(entries),
        "github_public_hapa_repositories": len(github_names),
        "errors": errors,
    }
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
