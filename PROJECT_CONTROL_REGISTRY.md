# Schemin '26 — Project Control Registry

**Status:** ACTIVE  
**Season:** 2026  
**League:** Pro Schemin' Football League — ESPN `1417621`

This file is the shortest authoritative entry point for substantial Schemin '26 work.

## Canonical project mission

**First read:** `SCHEMIN_26_PROJECT_MISSION.md`

The Project Mission is the Commissioner-approved north star above every subsystem. Weekly Memo OS, Living Novel OS, World Engine / Universe Atlas, Character Canon, visual production, data ingestion, publication control, and future Schemin systems must operate as surfaces of one persistent fictional reality.

Subsystem documents may specialize HOW their domain works. They may not redefine WHY the project exists or create an incompatible reality.

Machine-readable mission invariants: `governance/SCHEMIN_26_PROJECT_MISSION_CONTRACT.json`.

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

## Publication identity manifest

Derived cross-publication identity and relationship metadata lives at:

- `governance/publication-manifest/_INDEX.md`
- `governance/publication-manifest/PUBLICATION_MANIFEST_V1.json`

This manifest is **ACTIVE AS A DERIVED INDEX ONLY**. It may resolve publication identity, archive membership, related Memo/Novel installments, and authority references. It may not publish, promote, supersede, reopen, or mutate any artifact. Owning release/manuscript gates and `governance/release-evidence/registry.json` remain authoritative.

## Release evidence control

Machine release/acceptance applicability is resolved through:

- `governance/release-evidence/_INDEX.md`
- `governance/release-evidence/registry.json`
- `governance/release-evidence/release_evidence.py`

Historical PASS evidence remains preserved, but it cannot masquerade as current when controlled subsystem bytes changed or a required current check is red.

## Controlling domains

### Weekly Memo
Current controlling build: **V5.5 Integrated Preproduction Hardening**.

Read in this order:
1. `memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_5_INTEGRATED_PREPRODUCTION_PATCH.md`
2. `memo-os/LOCATION_CONTROL_PLANE_INTEGRATION_PATCH_V1.md`
3. `memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_4_ACCEPTANCE_TEST_HARDENING_PATCH.md`
4. `memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_3_CHARACTER_REFERENCE_ENFORCEMENT_PATCH.md`
5. `memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_GOLD_STANDARD_STUDIO_PATCH.md`
6. `memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_2_RC_MUTUAL_IMPLEMENTATION_PATCH.md`
7. `memo-os/SCHEMIN_26_WEEKLY_MEMO_GOLD_STANDARD_PRODUCTION_MANUAL.md`
8. `memo-os/SCHEMIN_26_WEEKLY_MEMO_MASTER_INITIATION_PROMPT.md`
9. `canon/_INDEX.md`

V5.5 passed the Week 3 retrospective acceptance suite (11/11 after bug-fix/polish/retest) and is binding above V5.4/V5.3. V5.6 publication-integrity controls have been selectively salvaged onto current main as additive safeguards, but **V5.6 remains RELEASE_CANDIDATE / NOT ACTIVE**; see `memo-os/V5_6_CURRENT_MAIN_RECONCILIATION_V1.md`. V5.2-RC remains part of the lower orchestration lineage; it is not the top-level production-hardening authority.

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

**Character generation enforcement:** the fail-closed runtime under `canon/characters/runtime/` is ACTIVE as an execution-safety boundary when present on `main`. It does not promote Character Control Plane v2. Character-bearing generation requires verified current asset/hash, reference mount, per-subject binding, proven provider capability, signed request-bound eligibility, governed renderer invocation, output-instance receipt, and independent Character QA. Missing evidence returns `GENERATION_BLOCKED`. Current durable 12-reference retrieval and real provider subject-binding proof remain production blockers.

### World Engine / Geography
Current controlling build: **SCHEMIN WORLD ENGINE V1.1 — RELEASED / ACTIVE (2026-09-29)**.

Read in this order:
1. `world/SCHEMIN_WORLD_ENGINE_V1_1_RELEASE_RECEIPT.md`
2. `world/PRO_SCHEMIN_WORLD_BIBLE_V1.md`
3. `world/encounters/ENCOUNTER_VENUE_RESOLVER_V1.md`
4. `world/civilization/INHABITANT_ONTOLOGY_V1.md`
5. `world/atlas/ATLAS_V1.md`
6. `world/atlas/phase-1/_INDEX.md`
7. `world/location-control-plane/_INDEX.md`
8. `world/environment-references/_INDEX.md`
9. `world/atlas/interactive/_INDEX.md`
10. `world/evolution/_INDEX.md`
11. `world/atlas/ROUTE_AND_TRAVEL_MODEL_V1.md`
12. `world/domains/OWNER_DOMAIN_REGISTER_V1.md`
13. `world/divisions/BURGERS_DIVISION_INDEX_V1.md`
14. `world/divisions/WINGS_DIVISION_INDEX_V1.md`
15. `world/divisions/PIZZA_DIVISION_INDEX_V1.md`
16. `world/state/WORLD_STATE_LEDGER_V1.md`
17. `living-novel/os/geography/world_travel_graph_v1.json`
18. `world/qa/WORLD_ENGINE_V1_1_ACCEPTANCE_REPORT.md`
19. `world/atlas/integration/_INDEX.md`

World Engine V1.1 owns persistent physical geography, division spatial/cultural identity, owner-domain placement, Encounter venue resolution, routes/travel topology, recurring locations, inhabitant ontology, environmental state and geography QA. It does not own fantasy-league truth or principal character body identity.

Binding laws:
- **The world determines the image; the image does not determine the world.**
- Ordinary regular-season/divisional Encounters default to the verified home team's established environment.
- Game of the Week, playoff and championship Encounters default to approved neutral Schemin locations.
- Away participants require an approved route/path to the venue.
- 2026 division truth is Burgers = ObiWan / D0nkey K0ng / TDS / Mud Dogs; Wings = Red Leopards / Slob / Chili / Duckhook; Pizza = LLC / HMB / El Niño / Seven Deadly Chins.
- Divisions are nonexclusive League-cultural/home-venue overlays, not biological or residential borders.
- Peopled kinds: ObiWan, D0nkey K0ng, Red Leopards, Slob, Mud Dogs, Seven Deadly Chins.
- Singular beings: Belt Keeper, Duckhook, El Niño, The LLC.
- TDS and Chili explicitly coexist across their division split.
- El Niño may be embodied or, when explicitly resolved, the natural storm/disaster itself; not every storm is El Niño.
- Burgers = burgers; Wings = **chicken wings**; Pizza = pizza.
- Canonical machine World Engine records are JSON under `world/data/`; legacy YAML duplicates are supersession pointers only.
- Renderers consume world data and never silently mutate canon.

World Engine V1 remains historical release evidence and is superseded by V1.1 for current world production.

**Atlas Phase 1 expansion governance:** when world/atlas/phase-1/_INDEX.md is present on main, these controls are ACTIVE for cultural deepening, future-location candidate lifecycle, rare/special-event venue policy and generation hydration. They do not supersede World Engine V1.1 physical authority or promote candidate geography automatically.

**Atlas Phase 2 / Location Control Plane:** when world/location-control-plane/_INDEX.md is present on main, it is ACTIVE as derived location-packet infrastructure beneath World Engine V1.1. It compiles homelands, active locations, routes, state, history and consumer overlays. It cannot promote CAND-* geography or override upstream canon.

**Atlas Phase 3 / Environment References:** when world/environment-references/_INDEX.md is present on main, 23 deterministic structural environment plates are ACTIVE as renderer-addressable structural grounding. Cinematic environment references remain separately human-gated.

**Atlas Phase 4 / Interactive Atlas:** when world/atlas/interactive/_INDEX.md is present on main, the standalone interactive Atlas is ACTIVE as a read-only canonical visualization. Editorial candidates remain non-spatial and non-active.

**Atlas Phase 5 / Weekly World Evolution:** when world/evolution/_INDEX.md is present on main, the dry-run-first weekly evolution engine is ACTIVE for governed post-release state/history transactions. Candidate promotion remains separately gated and never implicit.


**Universe / Atlas architectural lock:** one authoritative world model, one Atlas spatial control plane, many views/consumers. Memo OS, Novel OS, Interactive Atlas, Canonical World Plate and Art Pipeline may consume or render world truth but may not maintain competing active geography.

**Axiom:** **One World Model. One Spatial Control Plane. Many Views. No Forked Geography.**

**Architectural lock status:** **ACTIVE** — enforced by `world/qa/test_one_world_model_contract.py`; post-merge verification: `world/qa/ONE_WORLD_MODEL_POST_MERGE_VERIFICATION_V1.md`.

Read:
- `world/governance/WORLD_DATA_OWNERSHIP_MATRIX_V1.md`
- `world/governance/CANONICAL_WORLD_ID_CONTRACT_V1.md`
- `world/governance/DERIVED_WORLD_DATA_CONTRACT_V1.md`
- `world/evolution/WORLD_MUTATION_FANOUT_CONTRACT_V2.md`
- `world/qa/ONE_WORLD_MODEL_ANTI_FORK_AUDIT_V1.md`
- `world/qa/ATLAS_CONTROL_PLANE_CONSOLIDATION_REPORT_V1.md`
- `world/qa/test_one_world_model_contract.py`
- `world/qa/ONE_WORLD_MODEL_ARCHITECTURAL_LOCK_ACCEPTANCE_REPORT_V1.md`
- `world/ONE_WORLD_MODEL_ARCHITECTURAL_LOCK_RELEASE_RECEIPT_V1.md`

**Atlas Publication Convergence V1:** when `world/atlas/integration/_INDEX.md` is present on main, it is ACTIVE as the cross-OS authoring contract binding League Data, Character Canon, World Engine, Location Control Plane, Memo OS, Novel OS, visual grounding, Interactive Atlas, Weekly World Evolution and release control. It creates no second geography/canon store.

### Universe OS V1.2 / Atlas Control Plane V2 — RELEASED / ACTIVE

Branch implementation: `world/universe-os-v1-2-atlas-control-plane`.

This program **does not create a second geography store**. It layers Universe OS world/civilization/memory/query contracts over the existing World Engine V1.1 and Atlas Phases 1–5, while promoting Atlas into the governed spatial control plane.

Active entry points:
- `world/governance/UNIVERSE_OS_V1_2_PATCH_CONTROL_DOCUMENT.md`
- `world/atlas/ATLAS_CONTROL_PLANE_V2.md`
- `world/ontology/ENTITY_ONTOLOGY_V2.md`
- `world/domains/DOMAIN_ARCHITECTURE_V2.md`
- `world/history/WORLD_MEMORY_ENGINE_V1.md`
- `world/civilization/CIVILIZATION_DENSITY_ENGINE_V1.md`
- `governance/SCHEMIN_OS_CONTRACT_MAP_V1.md`
- `world/engine/universe_resolver.py`
- `world/qa/UNIVERSE_OS_V1_2_ACCEPTANCE_SUITE.md`

**Release receipt:** Universe OS V1.2 and Atlas Control Plane V2 are RELEASED / ACTIVE. See `world/UNIVERSE_OS_V1_2_RELEASE_RECEIPT.md` and `world/qa/UNIVERSE_OS_V1_2_ACCEPTANCE_REPORT.md`. World Engine V1.1 / Atlas Phases 1–5 remain active underlying infrastructure.

### Living Novel — External Advisory Council V1

**Status:** RELEASED / ACTIVE — ADVISORY ONLY (2026-10-01).**

Read:
- `living-novel/consultants/_INDEX.md`
- `living-novel/consultants/NOVEL_EXTERNAL_ADVISORY_COUNCIL_V1.md`
- `living-novel/consultants/NOVEL_CONSULTATION_PROTOCOL_V1.md`
- `living-novel/consultants/ADVISOR_REGISTRY_V1.json`
- `living-novel/consultants/SOURCE_REGISTRY_V1.json`
- `living-novel/os/NOVEL_EXTERNAL_ADVISORY_INTEGRATION_PATCH_V1.md`
- `living-novel/consultants/NOVEL_EXTERNAL_ADVISORY_COUNCIL_V1_RELEASE_RECEIPT.md`

The council provides research-grounded external craft perspective through published-method lenses and composite specialists. It is not a new control plane and has no canon authority. Author Room hydration remains upstream; independent consultant reads are reconciled by Bullpen before any implementation enters the normal Novel OS editorial/continuity/canon gates.

Natural-language requests such as "Bullpen, call the Novel consultants on this" route through Bullpen's shared external-advisory capability. Full-council review is reserved for cross-cutting architecture; targeted panels are the default.

### Living Novel — Author Consulting Program V2

**Status:** RELEASED / ACTIVE — ADVISORY ONLY (2026-10-01).**

This program is the named author-method layer beneath the active Novel External Advisory Council.

**Core Seven:** J.R.R. Tolkien; George R.R. Martin; J.K. Rowling; John Grisham; Ursula K. Le Guin; Brandon Sanderson; Joe Abercrombie.

Read:
- `living-novel/consultants/author-council/_INDEX.md`
- `living-novel/consultants/author-council/_PROGRAM_CHARTER.md`
- `living-novel/consultants/author-council/AUTHOR_COUNCIL_MASTER_MANDATE_V2.md`
- `living-novel/consultants/author-council/SELECTION_MATRIX_V1.md`
- `living-novel/consultants/author-council/BULLPEN_EXECUTION_PROMPT_V2.md`
- `living-novel/consultants/author-council/NOVEL_AUTHOR_CONSULTING_PROGRAM_V2_RELEASE_RECEIPT.md`

Operating model: informed pre-work → independent specialist rounds → Bullpen cross-examination → implementation between rounds → adversarial re-review → final synthesis → audit → durable learning.

The names identify published-method lenses only. They do not imply live participation, endorsement or permission to imitate prose. Author Room hydration, verified evidence, canon and Novel OS remain upstream authority.

### Living Novel — Causal Story Architecture V1 / Book Architecture V2

**Status:** RELEASED / ACTIVE PROSPECTIVELY FROM CHAPTER III (2026-10-01).**

Promoted from the first complete Full Seven Author Council production engagement: `NOVEL-AUTHOR-CONSULT-2026-10-01-001`.

Read in this order:
1. `living-novel/os/NOVEL_CAUSAL_CHAPTER_ARCHITECTURE_V1.md`
2. `living-novel/os/NOVEL_BOOK_ARCHITECTURE_V2.md`
3. `living-novel/os/NOVEL_POV_CONSTITUTION_V1.md`
4. `living-novel/os/NOVEL_PROMISE_AND_OPEN_LOOP_LEDGER_V1.md`
5. `living-novel/os/NOVEL_SCORE_ARTIFACT_FOREGROUNDING_DOCTRINE_V1.md`
6. `living-novel/os/templates/MINIMUM_PRE_PROSE_GATE_V1.md`
7. `living-novel/os/templates/CHAPTER_DOSSIER_V2.md`
8. `living-novel/os/state/CURRENT_OPEN_LOOP_LEDGER_V1.json`
9. `living-novel/os/state/READER_RULE_LEDGER_V1.json`
10. `living-novel/consultants/author-council/engagements/NOVEL-AUTHOR-CONSULT-2026-10-01-001/RELEASE_RECEIPT.md`

**Binding literary law:** **A source week is evidence. A chapter is causality.** Verified league truth remains complete in evidence/state, but a scoring period is not automatically a chapter and equal matchup coverage is not required in long-form prose.

Chapter III+ is significance-gated, causality-first, geography-aware, open-loop aware, and normally carries 1–3 primary POVs chosen by causal ownership. Exact scores enter foreground prose only when they materially change action, relationship, interpretation, rule application, resources, or later causality.

The Prologue, Chapter I and Chapter II remain HARD MANUSCRIPT CANON / CLOSED. This promotion does not reopen or rewrite them. Week 3 is not automatically Chapter III; its six matchups are evidence packets first, with story units selected only after significance and causal architecture.

### Living Novel — Chapter III Canon

**Status:** HARD MANUSCRIPT CANON / CLOSED (Founder-approved 2026-10-01).**

Canonical manuscript:
- `living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md`
- approved blob SHA: `49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc`

Authority / evidence:
- `living-novel/qa/CHAPTER_03_FINAL_CANON_GATE_V1.md`
- `living-novel/qa/CHAPTER_03_CANON_PROPOSAL_V1.md`
- `living-novel/qa/CHAPTER_03_CANON_RELEASE_RECEIPT_V1.md`
- `living-novel/qa/CHAPTER_03_STATE_TRANSACTION_RECEIPT_V1.md`
- `living-novel/production/chapter-03/_INDEX.md`

Chapter III inaugurates Movement II — **CLAIMS HARDEN**. Its causal spine is the aftermath of Mire Hill: Wilson Look / D0nkey K0ng becomes the sole 3-0 competitive power, places his standard below the neutral-ground summit, and refuses to convert victory into sovereignty while public crown/ownership interpretation begins attaching itself to the record.

Binding limits:
- no Belt transfer;
- no sovereignty or territorial transfer;
- summit remains unclaimed;
- no Week 4 outcome;
- fictional Wilson POV is not a factual claim about Wilson Look's real-world private psychology;
- Arsenal Gorilla Warrior is current character canon; Centaur anatomy remains retired.

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

## Current operating checkpoint — 2026-09-30

- Atlas Phases 3–5 production cycle completed: structural environment grounding, interactive canonical Atlas, and weekly world-evolution transaction system.


- Atlas Foundation Reconciliation V1 merged through PR #37.
- Atlas Phase 1 merged through PR #39 and is active beneath World Engine V1.1.
- Phase 2 Location Control Plane has completed board/QA review in PR #40; when merged, it becomes active derived production infrastructure.

### Prior checkpoint — 2026-09-29

- Week 3 facts are locked and the 21-page Week 3 Memo is immutable release evidence.
- Week 3 post-production is complete; its accepted controls were integrated into Memo OS V5.5.
- Week 4 is the next Memo production cycle; use V5.5 rather than recreating Week 3 process manually.
- Living Novel Chapter III — `THE HILL IS NOT THE KINGDOM` — is HARD MANUSCRIPT CANON / CLOSED after Founder approval on 2026-10-01. It interprets selected Week 3 consequence without establishing Week = Chapter.
- Character Control Plane v2 is advancing but remains RELEASE_CANDIDATE / NOT ACTIVE.
- Schemin World Engine V1.1 is RELEASED / ACTIVE on `main`; PR #29 closed the Encounter-geography, travel-graph and inhabitant-ontology gaps and repaired stale division assignments.
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
