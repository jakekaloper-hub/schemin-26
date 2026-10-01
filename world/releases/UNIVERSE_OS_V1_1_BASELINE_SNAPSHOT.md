# UNIVERSE OS V1.1 — BASELINE SNAPSHOT

**Captured:** 2026-09-30 / pre-Universe OS V1.2 migration  
**Baseline commit:** `636221a9caecbf1c5c49bee277adef03325b04c1`  
**Branch:** `world/universe-os-v1-2-atlas-control-plane`  
**Status:** PHASE -1 BASELINE / IMMUTABLE REFERENCE

## Purpose

This snapshot freezes the exact active World Engine / Atlas operating state before Universe OS V1.2 changes its ontology, civilization model, memory model or spatial contracts.

Git history remains the byte-level rollback authority. The companion JSON exports provide focused machine-readable recovery surfaces.

## Controlling state at capture

- World Engine V1.1 — RELEASED / ACTIVE.
- Atlas V1 — ACTIVE / GOVERNING under World Engine V1.1.
- Atlas Phase 1 — expansion governance active.
- Atlas Phase 2 — Location Control Plane active.
- Atlas Phase 3 — structural environment grounding active.
- Atlas Phase 4 — read-only Interactive Atlas active.
- Atlas Phase 5 — dry-run-first Weekly World Evolution active.
- Weekly Memo OS V5.5 remains current Memo authority.
- Character Control Plane v2 remains release-candidate unless separately promoted.
- Canonical machine World Engine records remain JSON under `world/data/`.

## Captured source manifests

| Surface | Path | Blob SHA |
|---|---|---|
| locations | `world/data/locations.json` | `a7a0d34278ad22b494f087ef9d38c9a8b7a59e55` |
| routes | `world/data/routes.json` | `da418245708c1f9d2128775df0ce7d26e7eeaa18` |
| divisions | `world/data/divisions.json` | `c6f18fae9d4fec928a9b1b8917ff474379a01d57` |
| owners | `world/data/owner_domains.json` | `b9c5e52b1ad09611d15b6662d64d1ff79cb9aaf9` |
| ontology | `world/data/inhabitant_ontology.json` | `09cd97d610cc4b9a48372545176a2539bf05a734` |
| state | `world/data/current_world_state.json` | `6d0344ce9cf5a29f32a04b0bae5c8e50c7afc71a` |
| events | `world/data/world_state_events.json` | `12b21ccc2c651108eefc24d10106739e72b0b8f8` |
| zones | `world/data/physical_zones.json` | `3d06bb11b6dd48d1fab523cd886b5003df1c8651` |
| chars | `canon/characters/CHARACTER_REGISTRY.yaml` | `edde98341e37eed7d18704e650c2689008a87b45` |
| atlas | `world/atlas/ATLAS_V1.md` | `221a0867314878e605385a79724bb133faac5666` |
| lcp | `world/location-control-plane/_INDEX.md` | `d61d0d37206f67975fa2e6c77c211fc89004a980` |
| env | `world/environment-references/_INDEX.md` | `bb9a81fb69f90c7baf210bcf2dbeac6ca1e0e937` |
| interactive | `world/atlas/interactive/_INDEX.md` | `23e6abfa98c3ab8535cdcedb821e81c7134a69fe` |
| evolution | `world/evolution/_INDEX.md` | `ca6e436e1cc70738ff7ec352c5709a55e0b43a7b` |

## Counts

- active locations: **23**
- active routes: **18**
- physical regions: **7**
- divisions: **3**
- owner-domain records: **12**
- world-state events: **7**

## Reconstruction rule

To reconstruct this baseline exactly:
1. checkout commit `636221a9caecbf1c5c49bee277adef03325b04c1`;
2. load the source paths and blob SHAs above;
3. verify World Engine V1.1, Atlas Phases 1–5 and existing CI before applying any V1.2 migration.

## Phase -1 acceptance

- rollback authority exists: PASS
- controlling versions identified: PASS
- machine sources identified: PASS
- Atlas subsystem captured through Phase 5: PASS
- downstream authorities preserved: PASS

**GATE -1: PASS**
