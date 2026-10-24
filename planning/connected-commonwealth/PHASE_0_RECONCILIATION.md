# Mission #175 — Phase 0 baseline and local reconciliation

**Status:** IN PROGRESS / AUTHORITY RECONCILED PARTIALLY / IMPLEMENTATION HOLD.
**Baseline:** `origin/main` at `0a8b4f5186b5a99f8a3504d201908401d4104ef8`.
**Isolated branch:** `mission-175-connected-commonwealth-phase0`.
**Issue:** https://github.com/jakekaloper-hub/schemin-26/issues/175

## Workspace safety
The pre-existing checkout `/Users/jakekaloper/Desktop/AI Project/schemin-26` is on `commissioner-bot-foundation` with 21 top-level dirty status entries (25 individual files after expanding untracked directories). No reset, stash, clean, overwrite, or transfer was performed. The new worktree was created from fetched `origin/main`, initially clean.

## Local-material classification
Byte-level SHA-256 comparisons against the isolated canonical worktree:
- **Already identical in main (2):** `bullpen/PRO_SCHEMIN_WORLD_FOUNDATION_PHASE0_PASS1.md`, `bullpen/PRO_SCHEMIN_WORLD_FOUNDATION_WORK_PLAN.md`. Do not re-import.
- **Modified relative to main (4):** `PROJECT_CONTROL_REGISTRY.md`, `bullpen/_INDEX.md`, `docs/INVENTORY.md`, `planning/ROADMAP.md`. Require line-level provenance/authority review; do not wholesale overwrite.
- **Locally new relative to main (19):** `world/history/LEAGUE_HISTORY_EVIDENCE.md`; `bullpen/FOUNDATION_SOURCE_ARTIFACT_MANIFEST.md`, `bullpen/GITHUB_REFERENCE_LEARNING_PLAN.md`, `bullpen/PRO_SCHEMIN_WORLD_BULLPEN_MASTER_FOUNDATION_PLAN.md`; `docs/decisions/ADR-0002-continuity-kernel.md`; `docs/governance/AGENT_AND_DESK_REGISTRY.md`, `docs/governance/PHASE_BRIEFING.md`; `docs/operations/HANDOFF.md`, `docs/operations/SESSION_CLOSE.md`, `docs/operations/SESSION_START.md`; `planning/CURRENT_WORK.md`; `world/atlas/PLACE_EVIDENCE_REGISTER.md`; `world/canon/CANON_EXCAVATION.md`, `world/canon/PROVENANCE_LEDGER.md`, `world/canon/VISUAL_EVIDENCE_EXTRACTION.md`, `world/canon/WEEK_1_PAGE_EVIDENCE.md`, `world/canon/WEEK_2_PAGE_EVIDENCE.md`; `world/characters/CHARACTER_EVIDENCE_DOSSIERS.md`; `world/continuity/CONTINUITY_SCHEMA_DRAFT.md`. Treat as unpromoted historical/local material pending per-file assessment. No automatic import.

## Authority findings
- `PROJECT_CONTROL_REGISTRY.md` identifies **World Engine V1.1 RELEASED/ACTIVE** and **Universe OS V1.2 / Atlas Control Plane V2 RELEASED/ACTIVE**. Confirmed by `world/SCHEMIN_WORLD_ENGINE_V1_1_RELEASE_RECEIPT.md`, `world/UNIVERSE_OS_V1_2_RELEASE_RECEIPT.md`, and `world/atlas/ATLAS_V2_RELEASE_RECEIPT.md`.
- `world/atlas/ATLAS_CONTROL_PLANE_V2.md` still contains the pre-promotion text “RELEASE CANDIDATE” and its promotion condition. Interpret as stale source header; controlling project registry and release receipts establish active state. Propose a focused documentation correction in a later reviewed change.
- **Character conflict requiring canon-owner ruling:** `PROJECT_CONTROL_REGISTRY.md` explicitly cites Commissioner-approved 2026-10-02 D0nkey K0ng **Arsenal Gorilla Centaur Warrior** (single gorilla upper identity, four-legged equine lower body), while `world/PRO_SCHEMIN_WORLD_BIBLE_V1.md` and `world/civilization/INHABITANT_ONTOLOGY_V1.md` say **Arsenal Gorilla Warrior** and label older centaur material superseded. Do not silently resolve this by choosing an older prose file. Character owner and Librarian must reconcile controlling approved character registry and dated Commissioner decision before character-bearing rendering.
- Existing World Memory, Civilization Density, Domain Architecture, Atlas layers, location IDs, venue law and cross-OS contracts must be reused. Do not create duplicate control planes.
- 2026-onward Living Chronicle, ambient-only NPCs and season-scoped division overlay remain mission invariants. Historical 2015–2025 archaeology deferred.

## Baseline checks
- `git diff --check` on clean worktree: no output.
- `python3 world/qa/test_universe_os_v1_2.py`: **UNIVERSE OS V1.2 ACCEPTANCE: PASS**.
- `python3 -m unittest world.qa.test_universe_os_v1_2 -q` discovered zero tests: **not acceptance evidence**.

## Remaining Phase 0 gates
1. Reconcile all 19 local-only and four divergent files with canonical ownership and provenance; avoid imports unless specifically justified.
2. Verify actual Bullpen Director runtime, ConsultEngine and advisor registry; record authenticated calls or BLOCKED, never simulate execution.
3. Build current cross-OS consumer matrix and determine minimum compatible extensions.
4. Resolve principal-character anatomy discrepancy through authorized Character Canon control before visual work.
5. Run relevant broader baseline suites and independent Umpire review.
6. Advance to Phase 1 only on evidence-backed Phase 0 acceptance.

**Not performed:** Canon promotion, implementation of civilization features, authenticated Director consultation, independent Umpire acceptance, PR, merge.

## Phase 0 continuation — baseline and authority checks

### Current character precedence — verified
`canon/_INDEX.md` explicitly identifies the 2026-10-02 Commissioner clarification as the latest governing semantic correction. `canon/characters/CHARACTER_REGISTRY.yaml` records `CHAR-WILSON-LOOK`, version 2.1, effective 2026-10-02, as **Arsenal Gorilla Centaur Warrior**: one gorilla-upper/equine-four-legged hybrid. `canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md` sections around lines 58–64 agree; its older September 29 retirement note is superseded. Therefore the World Bible and inhabitant ontology's “centaur superseded” statements are stale and require narrowly scoped corrective documentation; no character image generation is authorized. The canonical asset/mount/binding gate remains separate and BLOCKED absent receipts.

### Existing cross-OS contract — verified
`governance/SCHEMIN_OS_CONTRACT_MAP_V1.md` already defines the authoritative dependency chain:
- Universe OS: world IDs, ontology, civilization context, institutions, memory, state and mutations.
- Atlas: derived containment, routes, travel, hydrology, visibility and spatial QA.
- Character Control: principal morphology, wardrobe, props and negative locks.
- Memo OS: verified weekly outcomes, home/away facts, release evidence and *proposed* world-state deltas.
- Novel OS: consumes Universe/Atlas context, memory, ontology, settlements, institutions and POV knowledge.
- Art Pipeline: consumes Visual World Packet, Atlas, environment tier, character packet and typography plan.
No consumer may fork active LOC/ROUTE/REG/DIV/CHAR identities. A same-scene cross-consumer compatibility test is required. No second store is justified.

### Existing civilization support — verified
`world/civilization/CIVILIZATION_DENSITY_ENGINE_V1.md` already defines unnamed confidence-tagged settlement context and placement reasons, explicitly disallowing named canon merely for scenery. This is the appropriate extension point; reconcile its stale RELEASE CANDIDATE header against Universe V1.2 release evidence before edits.

### Baseline test evidence (local isolated branch)
- `python3 world/qa/test_one_world_model_contract.py` → ONE WORLD MODEL CONTRACT: PASS.
- `python3 world/qa/test_world_engine.py` → 8 tests PASS.
- `python3 world/qa/test_universe_v1_1.py` → 11 tests PASS.
- `python3 world/qa/test_universe_os_v1_2.py` → UNIVERSE OS V1.2 ACCEPTANCE: PASS.
- `npm test` in `bullpen-runtime/` → 24 tests PASS.
- `python3 living-novel/consultants/test_advisor_registry.py` → 12 tests PASS.
These are **local baseline tests**, not independent Umpire acceptance, nor proof of live authenticated Bullpen invocation.

### ConsultEngine verification
The Schemin `bullpen-runtime/` exists and its 24 tests pass, including fail-closed unavailable specialists and independent-gate requirements. This does **not** establish access to the separately governed canonical Bullpen ConsultEngine or its authenticated Director runtime. The Living Novel advisor registry is ACTIVE/ADVISORY_ONLY, with published-method lenses and no unverified human advisor participation. Actual ConsultEngine calls and Director attestations remain **BLOCKED/NOT DEMONSTRATED** until runtime discovery and authenticated invocation.

### Outstanding Phase 0
- File-by-file provenance and suitability review for 19 local-only and four divergent files; all remain unimported.
- Narrow doc fixes for superseded DK anatomy and Atlas/Civilization Density stale release-candidate labels, only after verifying owning document authority.
- Verified authentic ConsultEngine / Director invocations and Umpire independent sign-off.
- Broader CI-level cross-OS consumer regression; no promotion until evidence.
