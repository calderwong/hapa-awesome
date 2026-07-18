# Public Repository Scope

This ledger explains what “complete” means for Hapa's public GitHub directory as of 2026-07-18. It prevents two opposite errors: silently missing a public Hapa repository, and claiming that every repository on Calder Wong's public account is a Hapa node.

## Account-wide audit

| Classification | Count | Meaning |
| --- | ---: | --- |
| Public Hapa repositories | 50 | Directly reachable Hapa apps, nodes, protocols, operations surfaces, and labeled experiments in [`data/nodes.json`](../data/nodes.json). |
| Public supporting repositories | 2 | Source inputs used by Hapa, but not owned or described as Hapa nodes. |
| Other public account repositories | 9 | Public account projects or forks without current evidence that they belong in the Hapa node registry. |
| Total public account repositories | 61 | Every public repository returned by GitHub for `calderwong` is classified exactly once. |

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

Exclusion is not a quality judgment and does not prevent a future integration. It means only that public account ownership, a fork, or thematic similarity is insufficient evidence to call something a Hapa node.

## Stage and participation boundary

Every registry entry defaults to **First Pass / Prototype Stage** unless its owning repository declares a narrower, evidence-backed status. Public discovery does not promise runtime health, stability, compatibility, partnership, endorsement, decentralization, commerce, or a license grant.

For-profit and nonprofit organizations may propose a bounded, attributable integration or presence through the [Hapa participation guidance](https://github.com/calderwong/hapa/blob/main/docs/ECOSYSTEM_STAGE_AND_PARTICIPATION.md). An invitation or proposed directory entry is not itself an accepted integration or commercial relationship.
