# AGENTS.md

## Repository role

`hapa-awesome` is the canonical public discovery registry for Hapa. It orients humans and agents; it does not own the runtime, records, permissions, license, or maturity claim of any listed capability.

## Truth and stage rules

- Treat the ecosystem as **First Pass / Prototype Stage** unless the owning repository declares a narrower, evidence-backed state.
- A public URL proves discovery only. It does not prove runtime health, compatibility, partnership, endorsement, decentralization, commerce, or a license grant.
- Preserve bounded claims. In particular, Subscriber App is static UI only; Roomlet lacks distinct-network and signed-release proof; Trellis stub parity is not model-quality proof; Wisdom Studio's Overwind adapter is planned; and the Second Brain Node public package excludes private corpus data.
- Distinguish similarly named repositories. `hapa-second-brain-node` is the focused capability package published in this pass; `hapa-second-brain` is an existing public knowledge-database/UI repository.
- Preserve Hapa Language's bounded status: Prototype 0.1 is verified locally across UI/API/CLI, but its ten bundled Cards remain candidate/inference and are not accepted for teaching.
- Use apps and nodes as prepared paint/work surfaces, Cards and Decks as swatches/recipes, agents as paintbrushes, and protocols as custody/attribution discipline. Jump-off points must still be inspected and verified.
- The open invite to organizations is permission to suggest a bounded exploration, not an agreement or announcement.

## Source-of-truth files

- `data/nodes.json` — canonical machine-readable public registry.
- `data/repository-scope.json` — account-wide classification ledger for public Hapa repos, supporting inputs, and public account repos not asserted as Hapa.
- `docs/NODES.md` — human-readable public catalog.
- `docs/REPOSITORY_SCOPE.md` — human-readable inclusion and exclusion boundary.
- `README.md` — ecosystem orientation and family-level routes.
- `scripts/audit_public_registry.py` — deterministic public-API, reachability, and catalog-coverage audit.

## Editing and verification

- Add or remove public Hapa repositories in `data/nodes.json`, `docs/NODES.md`, and `README.md` where family orientation changes. Classify every other public account repository in `data/repository-scope.json` and explain the boundary in `docs/REPOSITORY_SCOPE.md`.
- Keep repository names, URLs, roles, statuses, upstream attribution, and ownership boundaries aligned with the owning README.
- Do not list private/local-only locations as public GitHub destinations.
- Validate JSON, inspect the diff, and run:

```bash
jq empty data/nodes.json
jq empty data/repository-scope.json
python3 scripts/audit_public_registry.py
```
