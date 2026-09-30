# Schemin '26 — Bullpen Command Adapter V2

## Authority

Canonical Bullpen organization, Director identities, universal command semantics, intent compilation, and lifecycle semantics live in `jakekaloper-hub/bullpen`.

Schemin '26 owns league-specific context, evidence, canon, domain aliases, workflows, stricter production gates, and durable Schemin state.

FLA is legacy/upstream creative-platform heritage and may be researched for reusable patterns, but it is not the canonical Bullpen organization and does not own Schemin state.

## Primary UX

Jake is not required to remember Bullpen commands.

Any broad invocation such as:
- "Bullpen, handle this."
- "Bullpen, figure this out."
- "Bullpen, fix this."
- "Bullpen, what's next?"
- "Bullpen, make this better."
- "Bullpen, finish this."
- "Bullpen, investigate this."
- "Bullpen, audit this."

MUST be compiled through the canonical Bullpen command layer first, then enriched by this Schemin adapter.

The adapter must not ask Jake to select a command when intent can be inferred with reasonable confidence. Ambiguity that changes irreversible behavior or major canon still escalates.

## Schemin domain mappings

| Natural language / domain command | Core command | Schemin workflow |
|---|---|---|
| continue the Prologue | resume | Novel OS current production chain |
| ingest Week N | run | Data Gateway ingest -> freshness -> validation -> evidence freeze |
| audit Chapter N | audit | continuity + Guardians + evidence audit |
| resolve this character | research | owner -> inhabitant -> alias -> state -> renderer-addressable references |
| produce next composition | run | beat -> visual value -> reference packet -> art brief -> composition -> visual/continuity QA |
| check canon | reconcile | authority-ranked canon assertions/conflicts/unknowns/provenance |
| prepare next chapter | plan | context pack -> promises -> causal consequences -> production readiness |
| weekly memo / build memo | mission | Memo OS production lifecycle through final release gate |
| character drift / wrong character | incident | stop unsafe retries -> reference-path diagnosis -> repair -> regression/visual QA |
| Flaim / ESPN truth | research | Scout-led League Truth/Data Quality workflow |
| what's next? | next | inspect repo/runtime state and advance next legitimate gate |

## Routing doctrine

Core command answers WHEN/HOW. Core Director router answers WHO. Schemin project assignments and domain evidence then refine the route.

Permanent project roles do not create a 19th Director. Preserve the canonical 18-Director constitution.

For substantial execution, `skills/schemin-bullpen-execution/SKILL.md` remains binding: evidence before completion claims; smallest competent team; creator and final gatekeeper differ; proceed through reversible work without founder interruption.

## Cross-repo propagation

Reusable organizational improvements:
Schemin discovery -> document requirement -> implement in canonical `/bullpen` -> verify there -> consume through Schemin adapter.

League-specific improvements:
implement and retain in `/schemin-26`; do not push league state/canon into Bullpen Core.

FLA-derived reusable patterns may be researched and ported only after compatibility/provenance review.

## Safe fallback

When Jake says only "Bullpen" plus a broad objective and no specific command is recognized, use core `run` with the smallest competent team. Do not default to a full 18-Director board.

When the objective is an outcome spanning multiple unknown phases, prefer `mission`.

When repeated production failure, data corruption, canon drift, or unsafe retry language is present, prefer `incident`.

Explicit constraints such as "planning only", "don't execute", "audit only", or "do not generate" override generic execution defaults.
