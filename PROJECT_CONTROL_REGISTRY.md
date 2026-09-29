# Schemin '26 — Project Control Registry

**Status:** ACTIVE  
**Season:** 2026  
**League:** Pro Schemin' Football League — ESPN `1417621`

This file is the shortest authoritative entry point for substantial Schemin '26 work.

## Canonical publication lock

**Official Week 2 Memo (league-shared September 23, 2026): `Week 2 memo.pdf`.** It is the 14-page illustrated issue beginning with Red Leopards “SPECIAL DELIVERY.” This is the canonical Week 2 published artifact and gold-standard benchmark. No similarly named Week 2 “final,” test, replay, rerun, or RC candidate may replace it without explicit Commissioner supersession.

## Five-plane architecture

```text
JAKE / COMMISSIONER INTENT
          ↓
CONTROL — SCHEMIN COLLABORATION KERNEL (SCK)
          ↓
TRUTH — LEAGUE DATA PLATFORM / DATA GATEWAY
          ↓
PRODUCTION — DOMAIN SYSTEM (MEMO OS / MERCER / CREATIVE)
          ↓
GOVERNANCE — INDEPENDENT QA / RELEASE CONTROL
          ↓
LEARNING — REGRESSION / RESEARCH / VERSIONED MEMORY
```

## Controlling domains

### Weekly Memo
Current controlling build: **V5.5 Integrated Preproduction Hardening**.

Read in this order:
1. `memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_5_INTEGRATED_PREPRODUCTION_PATCH.md`
2. `memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_4_ACCEPTANCE_TEST_HARDENING_PATCH.md`
3. `memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_3_CHARACTER_REFERENCE_ENFORCEMENT_PATCH.md`
4. `memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_GOLD_STANDARD_STUDIO_PATCH.md`
5. `memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_2_RC_MUTUAL_IMPLEMENTATION_PATCH.md`
6. `memo-os/SCHEMIN_26_WEEKLY_MEMO_GOLD_STANDARD_PRODUCTION_MANUAL.md`
7. `memo-os/SCHEMIN_26_WEEKLY_MEMO_MASTER_INITIATION_PROMPT.md`
8. `canon/_INDEX.md`

V5.5 passed the Week 3 retrospective acceptance suite (11/11 after bug-fix/polish/retest) and is binding above V5.4/V5.3. V5.2-RC remains part of the lower orchestration lineage; it is not the top-level production-hardening authority.

### League truth / ESPN
Read:
- `data-gateway/SCHEMIN_26_ESPN_INGESTION_RELIABILITY_PATCH_v1.0.md`
- `data-gateway/OPERATIONAL_PATCH_v1.0.md`
- `schemas/freshness.schema.json`

No downstream system may imply live ESPN verification unless freshness metadata supports that claim.

### Character canon
Read:
- `canon/_INDEX.md`
- `canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md`
- `canon/characters/CHARACTER_REGISTRY.yaml`

Rule: **OWNER → CANONICAL CHARACTER → CURRENT TEAM NAME**.

Latest explicit Commissioner-approved corrections outrank older visual plates and historical production. Current examples include Wilson Look's 2026-09-29 Arsenal Gorilla Warrior redesign and Phillip Pitts' one-body/three-serpent-head lock.

The typed Character Control Plane v2 under `canon/character-control-plane-v2/` is **RELEASE_CANDIDATE / NOT ACTIVE** until its release gates close. Do not treat v2 existence as runtime promotion.

### World Engine / Geography
Current controlling build: **Schemin World Engine V1** once this receipt is present on `main`.

Read in this order:
1. `world/SCHEMIN_WORLD_ENGINE_V1_RELEASE_RECEIPT.md`
2. `world/PRO_SCHEMIN_WORLD_BIBLE_V1.md`
3. `world/atlas/ATLAS_V1.md`
4. `world/divisions/DIVISION_INDEX_SCHEMA_V1.md`
5. `world/state/WORLD_STATE_LEDGER_V1.md`
6. `world/qa/WORLD_GEOGRAPHY_ACCEPTANCE_SUITE_V1.md`
7. `world/data/README.md`

World Engine owns persistent physical geography, division spatial/cultural identity, owner-domain placement, routes, recurring locations, environmental state and geography QA. It does not own fantasy-league truth or character identity.

Binding semantic locks include:
- Burgers = burgers.
- Wings = **chicken wings**.
- Pizza = pizza.
- Renderers consume world data; they do not silently create canon.

Memo OS and Living Novel consume the same World Engine location/state IDs rather than maintaining parallel geography.

### Jack Mercer
Read:
- `mercer/JACK_MERCER_FRONT_OFFICE_V2_SPEC.md`
- `mercer/OPERATING_CONTRACT.md`

Mercer owns football decision analysis for ObiWan Jacoby. Mercer does not own Weekly Memo publication or league-data freshness.

### Bullpen / FLA
Read:
- `bullpen/SCHEMIN_26_BULLPEN_FULL_PROJECT_REVIEW.md`
- `bullpen/SCHEMIN_26_SUBAGENT_V5_1_ENGINE_ROOM_RESPONSE.md`
- `docs/architecture/FLA_INTEGRATION.md`

FLA Bullpen is a selective specialist/governance adapter. It is not a sixth Schemin control plane and is not the source of current fantasy league truth.

## Current operating checkpoint — 2026-09-29

- Week 3 facts are locked and the 21-page Week 3 Memo is immutable release evidence.
- Week 3 post-production is complete; its accepted controls were integrated into Memo OS V5.5.
- Week 4 is the next Memo production cycle; use V5.5 rather than recreating Week 3 process manually.
- Living Novel Week 3 is closed on the active Novel branch and carries a Week 3 → Week 4 state handoff.
- Character Control Plane v2 is advancing but remains RELEASE_CANDIDATE / NOT ACTIVE.
- Schemin World Engine V1 has completed the 12-phase build/QA cycle and becomes controlling persistent-world authority when merged to `main`.
- Repository is intentionally public by Commissioner decision; secrets/private-only material and Mercer-private intelligence remain prohibited from public committed surfaces.

## Non-negotiable execution rules

- Evidence before inference.
- Stale data never masquerades as live.
- Canon blocks visual publication when unresolved.
- Same-week benchmark material is isolated during blank-canvas originality tests.
- Production agents may not self-certify release.
- File existence is not release readiness.
- A late correction reopens only dependent artifacts when possible.
- Private Mercer intelligence must not leak into public memo production.
- Material operating changes belong in Git history.
