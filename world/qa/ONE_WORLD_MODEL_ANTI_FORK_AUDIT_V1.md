# ONE WORLD MODEL — ANTI-FORK AUDIT V1

**Status:** COMPLETE / CONSOLIDATION CANDIDATE
**Scope:** repository-wide active geography, route, state and consumer surfaces.

## Governing axiom
**One World Model. One Spatial Control Plane. Many Views. No Forked Geography.**

## Findings

| Surface | Classification | Source of truth | Why it exists | Drift risk | Remediation |
|---|---|---|---|---|---|
| `world/data/locations.json` | AUTHORITATIVE | self | active LOC identity/geography | LOW | retain |
| `world/data/routes.json` | AUTHORITATIVE | self | active route topology | LOW | retain |
| `world/data/physical_zones.json` | AUTHORITATIVE | self | active macro physical zones | LOW | retain |
| `world/data/current_world_state.json` | AUTHORITATIVE STATE | governed evolution | current persistent deltas | LOW | retain |
| `world/data/world_state_events.json` | AUTHORITATIVE HISTORY | governed evolution | evidence-backed state history | LOW | retain |
| `world/data/divisions.json` | AUTHORITATIVE OVERLAY | self | League cultural/home overlay | LOW | retain |
| `world/data/owner_domains.json` | AUTHORITATIVE RELATIONSHIP | self | owner→place relationships | LOW | retain |
| `living-novel/os/geography/world_travel_graph_v1.json` | DERIVED CACHE | locations + routes | novel travel query convenience | MEDIUM | enforce source parity; never edit as authority |
| `world/location-control-plane/**/CARD.json` | DERIVED | World Engine JSON | addressable production packets | MEDIUM | regenerate only |
| `world/environment-references/plates/**` | DERIVED | Location Cards | deterministic structural grounding | LOW | regenerate only |
| `world/atlas/interactive/SCHEMIN_ATLAS_INTERACTIVE.html` | VIEW | active World Engine JSON | interactive visualization | LOW | build-only; read-only |
| `world/data/atlas_location_candidates.json` | EDITORIAL CANDIDATE STORE | candidate governance | future location proposals | MEDIUM | never resolve as active LOC until promotion |
| Memo world packets | CONSUMER / DERIVED | active world JSON | publication hydration | MEDIUM | stable IDs only |
| Novel scene geography | CONSUMER / DERIVED | active world JSON | prose hydration | MEDIUM | stable IDs only |
| Canonical World Plate | VIEW | Atlas layers | curated visual composite | HIGH if treated as truth | explicitly non-authoritative |
| legacy YAML compatibility files | SUPERSEDED POINTERS | JSON authorities | compatibility | LOW | preserve pointer-only role |
| published memo scenery | HISTORICAL EVIDENCE | release artifact + provenance | source evidence | HIGH if auto-canonized | require location/evolution governance |

## Material audit conclusion

No second active location database is required. The existing apparent duplicates are primarily healthy derived products: travel graph, Location Cards, structural plates and Interactive Atlas.

The material fork risk is **behavioral**, not primarily file-count:
1. editing the Novel travel graph directly;
2. treating a Location Card as a new authority;
3. promoting candidate/scenery through rendering;
4. manually patching Memo/Novel state after a world mutation instead of rebuilding.

## Consolidation action
- preserve World Engine JSON as authoritative storage;
- treat Atlas Control Plane as the sole spatial representation/QA layer;
- keep all downstream world copies explicitly DERIVED/CACHE/VIEW;
- add executable parity tests;
- make mutation fanout the only supported update path.

**AUDIT RESULT: PASS WITH ENFORCEMENT PATCH REQUIRED**
