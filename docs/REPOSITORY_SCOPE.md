# Public Repository Scope

This ledger explains what “complete” means for Hapa's public GitHub directory as of 2026-10-04. It prevents two opposite errors: silently missing a public Hapa repository, and claiming that every repository on Calder Wong's public account is a Hapa node.

## Account-wide audit

| Classification | Count | Meaning |
| --- | ---: | --- |
| Public Hapa repositories | 51 | Directly reachable Hapa apps, nodes, protocols, operations surfaces, and labeled experiments in [`data/nodes.json`](../data/nodes.json). |
| Public supporting repositories | 2 | Source inputs used by Hapa, but not owned or described as Hapa nodes. |
| Other public account repositories | 10 | Public account projects or forks without current evidence that they belong in the Hapa node registry. |
| Total public account repositories | 63 | Every public repository returned by GitHub for `calderwong` is classified exactly once. |

The machine-readable boundary is [`data/repository-scope.json`](../data/repository-scope.json). `scripts/audit_public_registry.py` compares its union with GitHub's public-repository API, so a new public repository cannot remain silently unclassified.

## Supporting sources, not Hapa nodes

| Repository | Current relationship | Boundary |
| --- | --- | --- |
| [calderwong/wikidict-it](https://github.com/calderwong/wikidict-it) | Pinned declared fork used by Hapa Language as an immutable historical WikiDict seed. | Interwiki-title data is not a sense, translation-equivalence, currency, community-acceptance, or teaching-quality claim. |
| [calderwong/wikidict-zh](https://github.com/calderwong/wikidict-zh) | Pinned declared fork used by Hapa Language as an immutable historical WikiDict seed. | Same source and pedagogy limits; upstream ownership and CC0 data lineage remain distinct from Hapa documentation. |

## Public account repositories not asserted as Hapa

The following repositories are deliberately outside the Hapa node registry until an owning document establishes a real capability relationship, custody boundary, attribution, and truthful current state:

- `FramePackherHimthorMethu`
- `OpenManus`
- `cake`
- `databy-ai-backend`
- `echomimic_v3`
- `ideology-visualizer`
- `shard`
- `try_git`
- `wikidict-eo` — not one of the Calder forks pinned by the current Hapa Language source review.
- [wutw-public-hapa-proto](https://github.com/calderwong/wutw-public-hapa-proto) — fork of [max99x/wutw-public](https://github.com/max99x/wutw-public); the reviewed owning README describes the upstream game without establishing a Hapa capability relationship.

Exclusion is not a quality judgment and does not prevent a future integration. It means only that public account ownership, a fork, or thematic similarity is insufficient evidence to call something a Hapa node.

## Classification refresh: 2026-10-04

The complete live inventory found two repositories added after the July ledger:

- **Hapa Living Resume** is included in the Hapa registry as a public prototype discovery surface. Its [owning README at `fabf8463`](https://github.com/calderwong/hapa-living-resume/blob/fabf84631f4461a931df94e5837f80fda6b45030/README.md) describes a living résumé, portfolio, Hapa ecosystem timeline, evidence boundaries, and agent-readable discovery. Its public-safe projection does not establish production usage or automatic inference of a person's experience.
- **wutw-public-hapa-proto** remains outside the Hapa registry as `not-asserted-as-hapa`. GitHub identifies it as a fork of [max99x/wutw-public](https://github.com/max99x/wutw-public), and its [owning README at `97f9d5ec`](https://github.com/calderwong/wutw-public-hapa-proto/blob/97f9d5ec2a5b984ff1705d8bbb164566918edeaf/README.md) describes the upstream Worlds Upon The Wind game. The reviewed README does not establish a Hapa capability relationship; the repository name alone is insufficient. This classification leaves future Hapa integration unresolved and does not transfer upstream release, runtime, or license claims to a Hapa implementation. Revisit it when an owning document establishes that relationship and its boundaries.

This refresh changes the historical 61-repository ledger (50 Hapa, 2 supporting, 9 other) to 63 repositories (51 Hapa, 2 supporting, 10 other). Public visibility and HTTP reachability establish discovery only.

## Stage and participation boundary

Every registry entry defaults to **First Pass / Prototype Stage** unless its owning repository declares a narrower, evidence-backed status. Public discovery does not promise runtime health, stability, compatibility, partnership, endorsement, decentralization, commerce, or a license grant.

For-profit and nonprofit organizations may propose a bounded, attributable integration or presence through the [Hapa participation guidance](https://github.com/calderwong/hapa/blob/main/docs/ECOSYSTEM_STAGE_AND_PARTICIPATION.md). An invitation or proposed directory entry is not itself an accepted integration or commercial relationship.

## Audit completeness contract

Run `python3 scripts/audit_public_registry.py` to obtain one JSON report and a
zero (all checks pass) or nonzero (failed/incomplete) exit status.

The unauthenticated GitHub user-repositories endpoint returns public repositories
owned by `calderwong`, including forks. The audit requests `type=owner`, an explicit
ascending full-name sort, and batches of 100. **100 is GitHub's maximum page size,
not a maximum inventory size.** The audit continues through every nonempty page,
including short pages, until an empty page proves traversal has ended. It checks
unique repository IDs/names and valid public ownership/URLs, and reconciles the
observed total against the account's `public_repos` count both before and after
traversal. There is no hard-coded repository or page-count cap.

- `inventory_complete: true` means traversal and count validation succeeded for
  the public-account scope. `ok` separately reports whether classification,
  catalog, discovery, and link checks passed.
- `inventory_complete: false` means enumeration failed, was malformed, repeated
  an identity, or disagreed with the account count. The report includes the observed
  count, failure page, and reason; `public_account_repositories` is `null` rather
  than a misleading partial total. Downstream completeness checks are skipped.
- `checked_at` is the current run's UTC start time. The legacy `audited_at` field
  remains the registry document's recorded audit date, not evidence of a new run.
- HTTP failures (including rate limits), invalid JSON, and timeouts fail closed.
  Correct the source or wait for access/rate-limit recovery and rerun; never work
  around an incomplete result by inserting an arbitrary limit or ignoring errors.

GitHub pagination is not an atomic snapshot. Count changes and duplicates detect
some concurrent mutations, but equal-count replacements can evade these checks.
For strong point-in-time claims, rerun against a stable account and retain the
report/commit evidence. This audit makes no claim about private or local-only
repositories, inaccessible sources, runtime health, or the completeness of other
nodes' internal data. The dated ledger above is an observation, not a permanent
account total; a new run may correctly flag added or removed repositories for classification.

The `Registry regression tests` GitHub Actions workflow runs offline regression
tests, JSON validation, and compilation for every pull request and push to `main`.
The live network audit remains a separate operator check so API rate limits and
external site availability cannot masquerade as a code regression test.

### Why the 100-repository bug existed

Commit [`0db18669`](https://github.com/calderwong/hapa-awesome/commit/0db18669c6ab74aaab12ec03491968c488916456)
introduced the audit on 2026-07-17 with a single `fetch_json` request using
`per_page=100`. It then treated that one page as the full public inventory. The
account-wide scope expansion in
[`458022d6`](https://github.com/calderwong/hapa-awesome/commit/458022d6303f3e3bbe7a479f21b7d9dab384fef9)
retained that request on 2026-07-18; the recorded 61-repository inventory did not
exercise the boundary. This was a missing-pagination defect, not an API-wide
100-repository limit. History establishes the mechanism, not the author's motive.
[PR #2](https://github.com/calderwong/hapa-awesome/pull/2) first added pagination;
its follow-up adds fail-closed reporting, independent count reconciliation,
boundary/error regression tests, and the shared
[complete enumeration protocol](PROTOCOLS.md#11-complete-enumeration-and-audit-visibility-protocol).

References: [GitHub repository listing](https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user),
[account public counts](https://docs.github.com/en/rest/users/users#get-a-user),
and [pagination](https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api).
