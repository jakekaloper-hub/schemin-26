# ONE WORLD MODEL — UNREAL / OPEN-WORLD REINFORCEMENT RESEARCH V1

**Status:** RESEARCH GATE COMPLETE / IMPLEMENTATION NOT YET PROMOTED
**Date:** 2026-10-02
**Authority:** Schemin Project Mission + One World Model + World Engine V1.1
**Budget:** ZERO INCREMENTAL SPEND

## Executive decision
Do not create a new World Engine, Atlas, world-state database, or Unreal-owned authority. Current Schemin already has the One World Model, spatial control plane, World Evolution, Location Control Plane, Visual World Packet V2, provider-neutral RenderRequest, and fail-closed Character Reference Mount.

External repositories are architectural teachers. Default classification is ADAPT or LEARN-ONLY.

## Capability findings
| Capability | State | Finding |
|---|---|---|
| One world/spatial authority | EXISTS | Active; do not duplicate. |
| Geography/location/routes | EXISTS | World Engine + Atlas + Location Control Plane. |
| World mutation | EXISTS | Governed mutation protocol delegates active state/history to World Evolution. |
| Cross-publication hydration | EXISTS | Memo/Novel/visual consumers share world authority. |
| Renderer neutrality | EXISTS | Provider-neutral RenderRequest + optional adapter + no-render mode. |
| Character identity/binding contract | EXISTS | CharacterReferenceMount requires source/mounted hashes, Git blob, receipts and subject binding. |
| Renderer-addressable source bytes | BLOCKED | Existing Character Native Render program remains held on authorized durable source-byte portability/provider proof. |
| Version-aware persistent-state reconstruction | PARTIAL | Schema versions exist, but research did not locate an executable world snapshot/replay/migration contract equivalent to SPUD/PersistenceLab version-aware restoration. |
| Scene-instance linkage | PARTIAL | Visual World Packet and RenderRequest exist; a thin event/scene-instance envelope may reduce handoff ambiguity without becoming authority. |
| Deterministic procedural geography | PARTIAL / NOT CURRENTLY REQUIRED | Useful research patterns exist; no current production gap justifies importing a PCG dependency. |

## External pattern decisions
### sinbad/SPUD — ADAPT
Source review found explicit GUID/object-reference persistence, saved-property boundaries, chunk/save versioning, fallback load paths and restoration logic. Schemin should learn from version-aware restoration and stable-reference semantics; do not import an Unreal plugin into core Schemin.

### fallintodusk/alis — ADAPT / LEARN-ONLY
Source review found stable placement identity, deterministic seeds, canonical-cell realization, regeneration boundaries, mutation locks, automated restoration and tests. Adapt its contract discipline and deterministic realization concepts only where a proven Schemin gap exists. Do not import its Unreal world runtime.

### PCGEx/PCGExtendedToolkit — LEARN-ONLY FOR NOW
Source review confirms deterministic graph/selection behavior and rich topology algorithms. Schemin already has routes/topology authority and has no proven need for an Unreal PCG dependency. Revisit only for a concrete procedural-world prototype.

### GameForgeStudio/Unreal-Open-World-Starter — LEARN-ONLY
Useful architecture reference for World Partition, deterministic PCG and editor/runtime separation. Do not treat target/design documentation as implemented proof and do not import it into Schemin core.

### ZKShao-EpicGames/Sample-PersistenceLab — ADAPT
Source review found persisted custom-version metadata applied before deserialization, explicit serialization boundaries and persistence examples. Strong evidence for a future Schemin state-version/migration contract.

## Evidence-backed gaps
### OWM-GAP-001 — Version-aware world-state reconstruction
**State:** PROVEN PARTIAL / DESIGN AUTHORIZED, IMPLEMENTATION REQUIRES TARGETED PROTOTYPE.
Current world files carry schema versions and World Evolution governs mutation, but no equivalent executable snapshot/replay/migration restoration contract was located.
**External teachers:** SPUD + PersistenceLab.
**Remediation candidate:** renderer-independent state envelope with schema version, authority revision, event range, source hashes, migration path and reconstruction test.
**Must not:** become a second state store.

### OWM-GAP-002 — Cross-domain scene-instance envelope
**State:** PROVEN PARTIAL / SMALL EXTENSION CANDIDATE.
Visual World Packet V2 and provider-neutral RenderRequest already exist. A thin immutable envelope may link EVENT_ID + world packet ref + character packet refs + publication/storyboard ref + renderer request + provenance.
**Decision:** Scene Manifest Option B — extend existing contracts; do not create a new canonical scene database.

### OWM-GAP-003 — Deterministic procedural realization
**State:** HOLD / NO CURRENT PRODUCTION NEED.
ALIS and PCGEx demonstrate useful deterministic seeds, graph operations and regeneration boundaries. Current Schemin environment references are sufficient for active production. Do not build until a concrete renderer/world prototype requires it.

### OWM-GAP-004 — Character source-byte execution
**State:** EXISTING BLOCKER / NOT SOLVED BY THIS MISSION.
Persistent-identity patterns reinforce architecture but do not supply missing approved source bytes or prove provider subject binding. Existing Character Native Render gate remains authoritative.

## One World Model reinforcement law
League Truth -> verified event -> canonical world/character authority -> governed mutation/persistence -> canonical state -> existing hydration/packet contracts -> Memo | Novel | Atlas | Image | future Unreal -> independent QA -> accepted artifact -> World Evolution.

Unreal remains downstream and replaceable.

## Scene Manifest decision
**OPTION B — existing contracts need a small extension.**
Do not create a new authority store. If prototyped, the scene-instance envelope must contain references/receipts, not copied canon, and must fail closed on stale/missing authority.

## Character Control crossover
Can improve: stable identity semantics, versioned bindings, explicit state/asset references, provenance, stale-reference rejection, renderer handoff receipts.
Cannot solve: missing raw source bytes, provider attachment capability, provider subject-binding proof, or model-level likeness fidelity.

## Next prototype gates
1. **OWM-PROT-001:** version-aware reconstruction fixture over a closed historical world-state mutation. Prove serialize -> mutate -> restore/replay -> identical accepted state and explicit migration failure.
2. **OWM-PROT-002:** thin scene-instance envelope over one closed historical Memo/Novel event using existing packet references. Prove Memo, Novel, Atlas and no-render adapter consume the same authority without copied canon.
3. Do not prototype PCG or Unreal client until 1–2 pass and a concrete production requirement exists.

## Unreal feasibility
**HOLD / STRUCTURALLY FEASIBLE AS A FUTURE DOWNSTREAM CLIENT.**
The provider-neutral architecture can support a future adapter conceptually, but there is no evidence yet that installing Unreal improves Schemin enough to justify operational cost.

## Cost/dependency result
PASS: no paid service, API credit, SaaS backend, Unreal install, Marketplace/Fab purchase or new premium account is required by these findings.

## Gate
Research phase: **PASS**.
New world foundation: **NO-GO**.
One World Model reinforcement: **GO, TARGETED ONLY**.
Scene contract: **OPTION B**.
Version-aware reconstruction prototype: **GO**.
Scene-instance envelope prototype: **GO**.
Procedural geography implementation: **HOLD**.
Unreal client implementation: **HOLD**.
Character source-byte blocker: **UNCHANGED / OWNED BY EXISTING PROGRAM**.
