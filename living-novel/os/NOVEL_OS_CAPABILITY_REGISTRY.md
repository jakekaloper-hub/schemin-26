# NOVEL OS CAPABILITY REGISTRY
**Status:** PHASE-2 RESEARCH BASELINE — 2026-09-27

## Decision standard
ADOPT = use directly where license/fit permit. ADAPT = reproduce a compatible architectural pattern, not copied code. LEARN = design influence only. REJECT = poor fit or unnecessary dependency.

| System | Classification | Capability harvested | Fit / risk |
|---|---|---|---|
| mrigankad/Novel-OS | ADAPT | persistent story state; deterministic continuity; editorial pipeline; pre-check + Guardian; approval blocking | Strong architectural fit. Keep Schemin-specific authority model and existing production chain. |
| sadasdfsaf/canonkit | ADAPT | local-first structured canon; age/timeline/entity/state/relationship checks; scene context packs | Excellent deterministic-validator pattern. Novel OS requires richer provenance and temporal authority. |
| YfengJ/novel-studio-ai | ADAPT | accepted-chapter-only memory mutation; hybrid retrieval; character state; graph facts; context-pack preview | Directly supports zero-canon-authority default and retrieval design. Avoid binding Novel OS to its SQLite/UI implementation. |
| sheengoa/novelforge | ADAPT | auditor categories; human confirmation; false-positive handling; plotline forget-risk | Promise ledger and adversarial QA fit. |
| letuhao/lore-weave | LEARN / selective ADAPT | evidence-linked entities/relationships; knowledge graph; canon-grounded retrieval; model-agnostic/self-hosted approach | AGPL-3.0: architectural study is useful; do not copy code into project without license review. |
| Openapps-free/novel-studio | LEARN | codex, timeline, relationship maps, planning UX | UI inspiration; not required as core dependency. |
| forsonny/book-os | LEARN | layered context and lightweight AI-facing summaries | Useful context-budget pattern; Novel OS authority requirements are stronger. |
| CalWade/novelforge | LEARN | filesystem-as-memory; adversarial review; multi-ledger pattern | Reinforces existing Bullpen pipeline; no dependency required. |
| Fize/novelforge | LEARN | checkpoint/state-machine workflow and incremental fact settlement | Useful operational pattern; no direct adoption required. |

## Adopted architectural patterns
1. Canon writes occur only after acceptance.
2. Deterministic continuity runs before expensive semantic review.
3. Context is assembled per task/scene, not by full-manuscript injection.
4. Narrative promises/plotlines have explicit forget-risk/status.
5. State lives durably outside model chat history.
6. Review is adversarial and can block acceptance.
7. Entity/relationship facts retain evidence links.
8. Workflows are resumable state machines.

## Explicit rejection
- No external novel-writing product becomes Novel OS's source of truth.
- No third-party knowledge graph may auto-promote extracted assertions to canon.
- No SaaS is required for core manuscript/canon survival.
- No repository is blindly cloned into Schemin.
