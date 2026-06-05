# Start Here

This page gives role-based routes into Hapa. Use it when the full system feels too wide.

## If you are brand new

Read:

1. [Hapa Awesome](../README.md)
2. [hapa](https://github.com/calderwong/hapa)
3. [Hapa Worldbuilding Wiki](https://github.com/calderwong/hapa-worldbuilding-wiki)
4. [Overwatch](https://github.com/calderwong/overwatch)
5. [docs/NODES.md](NODES.md)

Goal: understand that Hapa is a local-first node ecosystem, not one monolithic app.

## If you want to run something

Start with:

1. [Hapa Dev Proto](https://github.com/calderwong/hapa-dev-proto-private) for the main local app lineage.
2. [Hapa Space](https://github.com/calderwong/hapa-space) for the Unity Black Horizon fleet.
3. [Hapa Character Sheet](https://github.com/calderwong/hapa-character-sheet) for the private resume, skill codex, lineage dossier, and portfolio surface.
4. [Hapa Chat App](https://github.com/calderwong/hapa-chat-app) for chat/workroom flows.
5. [Hapa Wiki Viewer](https://github.com/calderwong/hapa-wiki-viewer) for browsing the wiki.
6. [Hapa Quest Keeper](https://github.com/calderwong/hapa-quest-keeper) for board coverage and work overview.

Protocol:

1. Read the target node README.
2. Check requirements, ports, tokens, and smoke tests.
3. Run local-only first.
4. Do not commit runtime state or secrets.
5. Record what you verified.

## If you want to understand the canon

Start with:

1. [Hapa Worldbuilding Wiki](https://github.com/calderwong/hapa-worldbuilding-wiki)
2. [Hapa Lore Node](https://github.com/calderwong/hapa-lore-node)
3. [Hapa Second Brain](https://github.com/calderwong/hapa-second-brain)
4. [MassiveHistory Chunks](https://github.com/calderwong/massivehistory-chunks)
5. [Open Notebook](https://github.com/calderwong/open-notebook)

Protocol:

1. Treat raw sources as provenance, not instant canon.
2. Use wiki pages and node manifests to preserve context.
3. Promote only reviewed material into canon-facing areas.
4. Keep heavy/private source payloads in the vault.

## If you want to build a new feature

Start with:

1. [Overwatch](https://github.com/calderwong/overwatch) for current operational state.
2. [Hapa Overwatch Kanban](https://github.com/calderwong/hapa-overwatch-kanban) for per-project boards.
3. [Hapa Spec Scaffold](https://github.com/calderwong/hapa-spec-scaffold) for compact contracts.
4. [Consul Node Proto](https://github.com/calderwong/consul-node-proto) for proof/evidence harness patterns.
5. The owning node README.

Protocol:

1. Identify the owning node.
2. Open or reuse a board task.
3. Keep the implementation in that node.
4. Add/adjust tests proportional to risk.
5. Update README and related-node links when contracts change.

## If you want to do media or model work

Start with:

1. [Hapa MLX Station](https://github.com/calderwong/hapa-mlx-station)
2. [Hapa LLaDA Node](https://github.com/calderwong/hapa-llada-node)
3. [MTPLX](https://github.com/calderwong/mtplx)
4. [Hapa Drama](https://github.com/calderwong/hapa-drama)
5. [Hapa LiTo](https://github.com/calderwong/hapa-lito)
6. [Hapa Avatar Node](https://github.com/calderwong/hapa-avatar-node)
7. [Hapa Song Registry](https://github.com/calderwong/hapa-song-registry)
8. [Cymatica](https://github.com/calderwong/cymatica)

Protocol:

1. Keep generated media out of Git unless it is small and intentionally published.
2. Preserve prompt, source, model, runtime, and command provenance.
3. Register reusable outputs as cards, manifests, wiki pages, or board evidence.
4. Review license and model constraints before promoting outputs.

## If you are an AI agent

Start with:

1. [docs/PROTOCOLS.md](PROTOCOLS.md)
2. The target node README.
3. The target node `AGENTS.md`, if present.
4. Overwatch or the relevant Kanban board.

Protocol:

1. Inspect before acting.
2. Do not assume local paths, secrets, ports, or running services.
3. Keep edits narrow and reversible.
4. Use the node's own checks.
5. Write a concise handoff with paths, commits, tests, and unresolved risks.
