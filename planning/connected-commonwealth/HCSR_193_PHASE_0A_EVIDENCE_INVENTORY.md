# HCSR #193 — Phase 0A Evidence Inventory (read-only)

> **Historical record — current authority check required (2026-10-24).** This October 16 inventory/topology record preserves findings from the inspected snapshot. Counts, missing-asset statements and the downstream DK conflict describe that snapshot, not a new current diagnosis or a requirement for fresh canon approval to preserve already approved morphology. Current authority remains PROJECT_CONTROL_REGISTRY.md, world/data and the governing character registry; this report promotes no geometry, character design or production approval.


**Date:** 2026-10-16. **Status:** EVIDENCE COLLECTED / NOT ACCEPTED. **Source:** default-branch GitHub file reads, not authenticated Bullpen Director or independent Umpire execution. **Scope:** machine authority census and 12-domain baseline; full per-location dossier, runtime test and cross-OS audit remain pending.

## Authority and anti-fork rule
Read `SCHEMIN_26_PROJECT_MISSION.md`, `PROJECT_CONTROL_REGISTRY.md`, `docs/architecture/REPOSITORY_ARCHITECTURE_V2.md`, `governance/SCHEMIN_OS_CONTRACT_MAP_V1.md`, `world/governance/WORLD_DATA_OWNERSHIP_MATRIX_V1.md`. No new active store. This file is a planning/evidence view, not canon.

## Machine counts (default branch)
- Registered top-level repository domains: **20** (7 owning domains, 2 runtime, remainder control/support/lifecycle).
- Physical regions: **7**; owner domains: **12**; registered Homeland Cards: **12**; registered Location Cards: **23**.
- Active locations in authoritative data: **23**; approved route records: **18**; editorial candidate records: **48**.
- Owner domains missing registered Homeland Card: **0**; missing primary Location Card: **0**; missing active primary location ID: **0**.
- Structural reference status: **23/23 APPROVED_STRUCTURAL_REFERENCE**; cinematic visual reference status: **23/23 MISSING_APPROVED_VISUAL_REFERENCE**. Structural approval is not proof of approved cinematic assets or metric geometry.
- Coordinate system: `schemin-local-v1 (abstract, non-metric)`. No metric distances inferred.

## All 12 domain parity baseline
| Team | Character ID | Primary LOC | Physical region IDs | Homeland registered | Location registered | Cinematic reference |
|---|---|---|---|---|---|---|
| ObiWan Jacoby | `CHAR-JAKE-KALOPER` | `LOC-TRADE-JEDI-MOUNTAIN-BASE` | `REG-UPPER-VALLEYS` | YES | YES | MISSING_APPROVED_VISUAL_REFERENCE |
| Red Leopards | `CHAR-KEVIN-ZEEK` | `LOC-RED-RUINS` | `REG-EASTERN-STORM-COAST` | YES | YES | MISSING_APPROVED_VISUAL_REFERENCE |
| Slob on my Dobb | `CHAR-JORDAN-HOLLINGSHEAD` | `LOC-SLOB-FOOTHILL-CAMP` | `REG-UPPER-VALLEYS` | YES | YES | MISSING_APPROVED_VISUAL_REFERENCE |
| The LLC | `CHAR-DAVID-BABB` | `LOC-LLC-BOARDROOM` | `REG-INNER-SEA-LITTORAL` | YES | YES | MISSING_APPROVED_VISUAL_REFERENCE |
| D0nkey K0ng | `CHAR-WILSON-LOOK` | `LOC-DK-HIGHLAND-STRONGHOLD` | `REG-UPPER-VALLEYS`, `REG-NORTHERN-SPINE` | YES | YES | MISSING_APPROVED_VISUAL_REFERENCE |
| Three Dreaded Snake | `CHAR-PHILLIP-PITTS` | `LOC-TDS-WATERFALL-TEMPLE` | `REG-SOUTHERN-WETLANDS` | YES | YES | MISSING_APPROVED_VISUAL_REFERENCE |
| Chili Cheesers | `CHAR-BRANDON-PRYOR` | `LOC-CHILI-STABLE` | `REG-WESTERN-TABLELANDS` | YES | YES | MISSING_APPROVED_VISUAL_REFERENCE |
| His Majesty's Blood | `CHAR-AUSTIN-BYARS` | `LOC-BELT-KEEPER-KEEP` | `REG-EASTERN-STORM-COAST`, `REG-NORTHERN-SPINE` | YES | YES | MISSING_APPROVED_VISUAL_REFERENCE |
| El Niño | `CHAR-MANNING-WELTY` | `LOC-STORM-BOWL` | `REG-EASTERN-STORM-COAST`, `REG-INNER-SEA-LITTORAL` | YES | YES | MISSING_APPROVED_VISUAL_REFERENCE |
| Mud Dogs | `CHAR-BOBBY-MITCHELL` | `LOC-MUD-DOGS-SWAMP` | `REG-SOUTHERN-WETLANDS` | YES | YES | MISSING_APPROVED_VISUAL_REFERENCE |
| Seven Deadly Chins | `CHAR-BEN-WHIPPLE` | `LOC-CHINS-ROAD-COMMONS` | `REG-CENTRAL-BASIN` | YES | YES | MISSING_APPROVED_VISUAL_REFERENCE |
| Dr. Duckhook | `CHAR-ZACH-WILSON` | `LOC-COUNTRY-CLUB-JACKSON` | `REG-SOUTHERN-WETLANDS` | YES | YES | MISSING_APPROVED_VISUAL_REFERENCE |

## Seven-region coverage
| Region | Adjacencies recorded | Source |
|---|---:|---|
| Northern Spine (`REG-NORTHERN-SPINE`) | 3 | `world/data/physical_zones.json` |
| Upper Valleys and Foothills (`REG-UPPER-VALLEYS`) | 4 | `world/data/physical_zones.json` |
| Central River Basin (`REG-CENTRAL-BASIN`) | 5 | `world/data/physical_zones.json` |
| Western Tablelands (`REG-WESTERN-TABLELANDS`) | 4 | `world/data/physical_zones.json` |
| Eastern Forest and Storm Coast (`REG-EASTERN-STORM-COAST`) | 4 | `world/data/physical_zones.json` |
| Southern Wetlands and Delta (`REG-SOUTHERN-WETLANDS`) | 3 | `world/data/physical_zones.json` |
| Inner Sea Littoral (`REG-INNER-SEA-LITTORAL`) | 3 | `world/data/physical_zones.json` |

## Registered repository surfaces (not proof of runtime availability)
| Directory | Class | Canonical entry point |
|---|---|---|
| `.github/` | support | N/A |
| `archive/` | lifecycle | `archive/_INDEX.md` |
| `bullpen/` | domain | `bullpen/_INDEX.md` |
| `bullpen-runtime/` | runtime | `bullpen-runtime/README.md` |
| `canon/` | domain | `canon/_INDEX.md` |
| `chronicles/` | lifecycle | `chronicles/README.md` |
| `data/` | support | `data/README.md` |
| `data-gateway/` | domain | `data-gateway/_INDEX.md` |
| `docs/` | support | `docs/README.md` |
| `governance/` | control | `governance/README.md` |
| `living-novel/` | domain | `living-novel/README.md` |
| `memo-os/` | domain | `memo-os/_INDEX.md` |
| `mercer/` | domain | `mercer/_INDEX.md` |
| `planning/` | lifecycle | `planning/README.md` |
| `productions/` | lifecycle | `productions/README.md` |
| `prompts/` | support | `prompts/README.md` |
| `schemas/` | support | `schemas/README.md` |
| `skills/` | runtime | `skills/README.md` |
| `tests/` | support | `tests/README.md` |
| `world/` | domain | `world/README.md` |

## Reconciliation and defects to investigate
1. **Do not duplicate existing work:** Commonwealth #175, G0 #186, G1–G4 #189, engineering HOLD #192; PR #187 and #190 require their own review/promotion gates. The prior single-character flagship design in #189 is *not* a substitute for 12-domain parity.
2. **Character conflict:** `world/data/owner_domains.json` contains `NO_CENTAUR_ANATOMY` for DK, while the 2026-10-02 governing character correction documented in `planning/connected-commonwealth/PHASE_0_RECONCILIATION.md` is Arsenal Gorilla Centaur Warrior. Treat this as a stale downstream guard requiring owner-approved correction, not a reason to rewrite character canon.
3. **Visual distinction:** structural reference tier exists for 23 locations, but approved cinematic references are missing for all 23 in the current registry. Keep exact-reference-required rendering on human-review gate.
4. **Unmeasured physical reality:** abstract coordinates and adjacency cannot be presented as acreage, travel miles, floor plans or surveyed heights. Keep UNKNOWN pending governed evidence.
5. **Unverified depth:** location cards, feature handles, route endpoints, hydrology, institutional population, architecture/interiors, environmental simulation, Memo/Novel adapter behavior, character image source bytes, and temporal state have not been exhaustively inspected or executed in this report.
6. **No authenticated runtime claim:** Director/ConsultEngine and independent Umpire have not been called; tests and CI have not been run in this evidence pass.

## Phase 0B acceptance work (next)
- Fetch and reconcile all 23 Location Cards and 12 Homeland Cards against authority; record individual completeness/UNKNOWN values.
- Verify route endpoint and regional adjacency integrity; include negative cases, watershed/visibility/travel classes and seasonal access.
- Audit civilization, institutions, economics, population, structures, interiors, history, environmental state, and all Memo/Novel/Art/data adapters.
- Reconcile PR #187/#190 changes against current default branch before asserting production availability.
- Run deterministic cross-OS same-scene and twelve-domain regressions; record exact command, commit SHA and outcome.
- Obtain authenticated Director/Umpire attestations or record BLOCKED. No promotion without gates.

## Source registry
- `governance/repository-architecture/FOLDER_DOMAIN_REGISTRY_V2.json`
- `world/data/owner_domains.json`
- `world/data/physical_zones.json`
- `world/location-control-plane/registries/LOCATION_CARD_REGISTRY.json`
- `world/location-control-plane/registries/HOMELAND_CARD_REGISTRY.json`
- `world/location-control-plane/registries/LOCATION_REFERENCE_REGISTRY.json`
- `world/data/locations.json`
- `world/data/routes.json`
- `world/data/atlas_location_candidates.json`
