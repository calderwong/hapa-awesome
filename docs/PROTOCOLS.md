# Hapa Protocols

Hapa protocols are practical operating rules for keeping many local nodes coherent.

## 1. Node ownership protocol

Every durable artifact should have an owning node.

Ask:

- Which repo owns this behavior?
- Which README explains it?
- Which board or Overwatch record tracks it?
- Which source/vault path owns any heavy or private payload?
- Which other nodes consume the output?

Rule: edit the owning node first. Update the entry-point docs only after the owning node's README or behavior changes.

## 2. README contract protocol

Each node README should answer:

- What is this node for?
- What does it consume?
- What does it emit?
- What interfaces exist: API, CLI, UI, event log, database, files, or service?
- What related Hapa nodes does it connect to, with explanations?
- What is verified versus partial, scaffold, blocked, deprecated, or speculative?
- What must stay out of Git?
- What cheap checks prove the README is still true?

GitHub READMEs should use working GitHub links for published repos. Local-only and vault-only material should be described as a boundary, not linked as broken GitHub paths.

## 3. Source and custody protocol

Source material can be local, private, large, licensed, generated, or sensitive. Preserve it without accidentally publishing it.

Use GitHub for:

- Small source files.
- Docs and README contracts.
- Schemas and manifests.
- Sanitized examples.
- Pointer files and vault manifests.

Use vault/local storage for:

- Raw exports.
- Live databases.
- Large generated corpora.
- Model weights.
- Media payloads.
- Secrets and tokens.
- Licensed asset packs.

When moving or referencing private material, record a hash, size, source path token, and custody note where possible.

## 4. Board evidence protocol

Operational work should leave an evidence trail.

Minimum evidence:

- Task or project ID.
- Actor or agent name.
- Files or repos touched.
- Commands run.
- Test/smoke result.
- Git commit or artifact hash.
- Remaining risks.

Use:

- [Overwatch](https://github.com/calderwong/overwatch) for broad operations.
- [Hapa Quest Keeper](https://github.com/calderwong/hapa-quest-keeper) for consolidated board state.
- [Hapa Overwatch Kanban](https://github.com/calderwong/hapa-overwatch-kanban) for per-project append-only event logs.
- [Hapa Open Tasks Node](https://github.com/calderwong/hapa-open-tasks-node) for operational task-node flows.

## 5. Canon promotion protocol

Generated content is not canon by default.

Use these lanes:

- Raw source: observed input with provenance.
- Draft: useful but not reviewed.
- Proposal: generated or inferred artifact awaiting review.
- Verified: behavior or fact checked against source or runtime.
- Canon: deliberately promoted into the canon/wiki layer.

Prefer draft/proposal lanes until the operator explicitly promotes material.

## 6. Local-first runtime protocol

Default stance:

- Use loopback services first.
- Treat ports as local runtime details.
- Use bearer tokens or `.node_token` locally, but never commit token values.
- Check `/health`, `/capabilities`, CLI `health`, or the node smoke test before claiming a service is live.
- Do not expose network services without explicit operator intent.

## 7. Agent operating protocol

For AI agents:

1. Orient: read this repo, the target node README, and `AGENTS.md` if present.
2. Inspect: check git status, existing tests, and current docs.
3. Plan: choose the smallest owning-node change.
4. Act: edit only what the task requires.
5. Verify: run cheap checks first, then broader checks if risk demands.
6. Record: note what changed, what passed, commits, links, and what remains.

Do not revert unrelated user changes. Do not sweep generated/runtime files into commits unless they are explicitly part of the task and boundary-approved.

## 8. Publication protocol

Before pushing:

1. Confirm the intended private GitHub target.
2. Check `git status`.
3. Stage only intended files.
4. Run `git diff --cached --check`.
5. Run a staged secret scan when available.
6. Check large-file boundaries.
7. Commit with a clear message.
8. Push to the intended private publication remote.
9. Verify local and remote SHAs match.
10. Re-run README/link checks if docs changed.

## 9. Link hygiene protocol

README links are part of the Hapa interface.

Rules:

- Related node sections should use GitHub repo links and explain the relationship.
- Do not use `hapa://`, `file://`, raw absolute local paths, or env-var paths in GitHub-rendered README links.
- If the target is local/vault-only, explain the boundary in prose.
- For images, track small README assets or remove the image reference.
- Recheck links after changing README content.

## 10. Handoff protocol

A good Hapa handoff says:

- Objective.
- Repos/files touched.
- Important commits or artifact hashes.
- Verification performed.
- Remaining local dirt or unrelated changes.
- Next logical action.

The handoff should let a new human or agent resume without reconstructing the whole thread.
