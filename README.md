# Schemin '26

Canonical operating repository for the 2026 Pro Schemin' Football League project.

Schemin ’26 is a persistent fantasy-sports storytelling and publication universe. Real fantasy-football events enter as verified league evidence, become character and world consequences, and then propagate through the Weekly Memo, Living Novel, Universe Atlas, visual production, and future world state.

> **Real fantasy-football event → verified league evidence → character consequence → world translation → story architecture → publication → governed world-state evolution → future continuity**

The governing rule is simple: these are not separate creative projects. They are different publication surfaces over **one persistent fictional reality**.

## Start here

For substantial project work, read in this order:

1. `SCHEMIN_26_PROJECT_MISSION.md` — Commissioner-approved north star
2. `PROJECT_CONTROL_REGISTRY.md` — current controlling systems, releases, and read order
3. `docs/governance/SOURCE_OF_TRUTH.md` — evidence and authority precedence
4. `governance/release-evidence/_INDEX.md` — current-vs-historical release evidence
5. the controlling document for the subsystem being changed

Known migrations and recovery items remain in `MIGRATION_LEDGER.md`.

## Canonical league

- ESPN league ID: `1417621`
- Season: `2026`
- Teams: `12`
- Scoring: PPR, H2H Points
- Regular season: 14 weeks
- Playoff teams: 7

Verified league truth outranks remembered state, screenshots, narrative convenience, or stale cached data.

## Project architecture

```text
JAKE / COMMISSIONER INTENT
          ↓
CONTROL — Schemin Collaboration Kernel / governed Bullpen routing
          ↓
TRUTH — League Data Platform / Data Gateway / freshness evidence
          ↓
PRODUCTION — Memo OS / Novel OS / Mercer / World & Visual systems
          ↓
GOVERNANCE — independent QA / release control / evidence registry
          ↓
LEARNING — regression / research / versioned memory
```

The architecture is intentionally fail-closed at authority boundaries. A file existing in the repository does not make it active, released, current, or safe to publish.

## Current control state

As of the 2026-09-30 Bullpen README audit:

| Domain | Current authority |
|---|---|
| Project mission | `SCHEMIN_26_PROJECT_MISSION.md` — canonical |
| Weekly Memo | **Memo OS V5.5** — ACTIVE; Week 3 closed/immutable, Week 4 next production cycle |
| Memo V5.6 | RELEASE CANDIDATE / NOT ACTIVE; current release evidence retains a real Week 4 acceptance blocker |
| Living Novel | **Novel OS v1.0** — production baseline PASS; league facts remain externally verified and canon mutation remains gated |
| World | **Schemin World Engine V1.1** — RELEASED / ACTIVE |
| Universe | **Universe OS V1.2** — RELEASED / ACTIVE |
| Spatial control | **Atlas Control Plane V2** — RELEASED / ACTIVE over the existing World Engine / Atlas layers |
| Character control | Master Canon/current registry remain authoritative; Character Control Plane v2 is RELEASE_CANDIDATE / NOT ACTIVE |
| Character generation safety | Fail-closed enforcement runtime is ACTIVE; production rendering remains BLOCKED without durable current references, proven provider subject-binding, and final-raster QA |
| League truth | Schemin Data Gateway + freshness metadata |
| GM analysis | Jack Mercer Front Office V2 for ObiWan Jacoby |

Always defer to `PROJECT_CONTROL_REGISTRY.md` and `governance/release-evidence/registry.json` when a later release changes this snapshot.

## One world, one spatial control plane

World and publication systems obey the project architectural lock:

> **One World Model. One Spatial Control Plane. Many Views. No Forked Geography.**

- World Engine owns persistent physical geography, encounter venue policy, routes, travel topology, recurring locations, inhabitant ontology, and environmental state.
- Universe OS layers governed ontology, civilization, institutions, memory, state, and query contracts over that world.
- Atlas Control Plane provides spatial representation and QA over the same canonical IDs.
- Memo OS, Novel OS, Interactive Atlas, and visual production consume that truth; they may not create competing active geography.
- Renderers consume world truth. They do not silently mutate it.

See `world/`, `governance/SCHEMIN_OS_CONTRACT_MAP_V1.md`, and `PROJECT_CONTROL_REGISTRY.md`.

## Character canon and rendering

Character identity follows:

> **OWNER → CANONICAL CHARACTER → CURRENT TEAM NAME**

Current Commissioner-approved corrections outrank historical art, older team names, and stale reference plates.

Character-bearing generation is fail-closed. A production request requires current character authority, renderer-addressable reference evidence, subject binding, governed invocation, output-instance receipts, and independent Character QA. Missing evidence must return a blocked state rather than inventing or semantically reconstructing a character.

The world may define what kind of being a character is; it may not redesign that principal character.

Primary entry point: `canon/_INDEX.md`.

## Bullpen operating model

Canonical Bullpen organization, Director identities, command semantics, lifecycle semantics, and Director counterweights live in the separate canonical repository:

`jakekaloper-hub/bullpen`

Schemin consumes Bullpen through project adapters and adds league-specific context, evidence, canon, stricter production gates, and project-local roles. It does **not** recreate a 19th Director or fork Bullpen Core.

Jake is not required to memorize commands. Broad requests such as “Bullpen, audit this,” “fix this,” “strengthen this,” or “what’s next?” are compiled through the canonical command layer before Schemin-specific routing.

Key local contracts:

- `docs/architecture/BULLPEN_COMMAND_ADAPTER_V2.md`
- `skills/schemin-bullpen-execution/SKILL.md`
- `bullpen-runtime/`
- `bullpen/`

Evidence is required before completion claims. The creator and final gatekeeper must be different roles.

## Fantasy League Artworks relationship

`schemin-26` is the league-specific operating repository.

Fantasy League Artworks (FLA) remains legacy/upstream creative-platform heritage and a source of reusable patterns. It is **not** the canonical Bullpen organization, does not own current Schemin league state, and may not override Schemin canon, Data Gateway truth, or release control.

Reusable ideas may flow from FLA into Schemin only after compatibility and provenance review. League-specific state remains here.

See `docs/architecture/FLA_INTEGRATION.md`.

## Repository map

- `memo-os/` — Weekly Memo production system, issue gates, acceptance suites, Week 4 control
- `living-novel/` — Novel OS, manuscript lineage, literary governance, POV/continuity systems
- `world/` — World Engine, Universe OS, Atlas, locations, routes, environments, world evolution
- `canon/` — team/owner/character authority and character-generation safety controls
- `data-gateway/` — ESPN acquisition, validation, fallback, snapshots, freshness policy
- `data/` — repository-managed league/project data artifacts
- `mercer/` — Jack Mercer AI GM / Front Office contracts
- `bullpen/` — Schemin-specific Bullpen reviews, decisions, remediation, and governance evidence
- `bullpen-runtime/` — executable Schemin adapters for canonical Bullpen routing
- `governance/` — cross-OS contracts, release evidence, mutation and authority controls
- `governance/publication-manifest/` — derived publication identity/relationship index; never a release authority
- `docs/` — architecture, governance, integration, and operating documentation
- `schemas/` — machine-readable contracts
- `skills/` — Schemin execution skills and operator contracts
- `chronicles/` — released/history-aware narrative and visual production material
- `productions/` — production outputs and project-specific deliverables
- `planning/` — bounded planning, archaeology, and recovery work
- `tests/` plus subsystem QA directories — regression, acceptance, and anti-drift evidence

## Release and publication law

- Evidence before inference.
- Stale data never masquerades as live.
- A red current check outranks an old PASS receipt.
- Historical release evidence remains historical when controlled bytes change.
- Canon blocks visual publication when unresolved.
- Generated output has zero canon authority by default.
- Production agents may not self-certify release.
- File existence is not release readiness.
- Late corrections reopen only dependent artifacts when possible.
- Material operating changes belong in Git history.

The canonical Week 2 publication is the league-shared 14-page `Week 2 memo.pdf` identified in `PROJECT_CONTROL_REGISTRY.md`. Week 3 is closed as immutable release evidence. Do not replace released artifacts through filename ambiguity or silent overwrite.

## Working rule for ChatGPT, Bullpen, Mercer, Memo OS, Novel OS, and visual production

1. Load the Project Mission and Control Registry.
2. Resolve the correct subsystem authority.
3. Verify the freshest league evidence required for the task.
4. Resolve character and world state before narrative or visual execution.
5. Route substantial work through the smallest competent Bullpen team and inherited counterweights.
6. Execute with real tools; do not substitute plans, personas, or “board meetings” for evidence.
7. Test and independently audit the result.
8. Bind release claims to current evidence.
9. Persist material changes in the owning repository.
10. Preserve one-world continuity into future weeks.

## Public repository boundary

This repository is intentionally public by Commissioner decision.

Do not commit secrets, credentials, private-only material, or Mercer-private competitive intelligence. Public production surfaces must contain only information appropriate for public repository storage.

---

**North-star test:** Did a real league event enter one canonical world, become meaningful story across multiple publication forms, and leave behind consequences that the universe will remember?

If not, the system is not operating as intended.
