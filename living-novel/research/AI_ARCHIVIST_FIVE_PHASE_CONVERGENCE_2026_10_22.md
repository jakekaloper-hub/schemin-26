# NOVEL OS × BULLPEN — FIVE-PHASE ARCHIVIST CONVERGENCE (2026-10-22)

**Authority:** Research and candidate-development packet only; this document changes no published canon.  
**Repository:** `jakekaloper-hub/schemin-26`. **Instruction:** Reuse existing Novel OS / Atlas / World Engine, never create a competing OS.  
**Source inspiration:** user-provided 28-minute transcript discussing AI as an archivist, chronology reconstruction, implied mythology, visual continuity, and reader-facing world bibles.

## Phase 1 — Historical excavation: completed repository reconnaissance
Confirmed existing materials (paths are authoritative pointers, not claims about full coverage):
- `world/history/HISTORICAL_ARCHAEOLOGY_INITIATION_LEDGER.md`
- `world/history/2025/2025_FACT_LEDGER.md`, recovery passes 2–4, team-alias map
- `data-gateway/chronicle/extract-pro-schemin-history.js` and `validate-history.js`
- `living-novel/history/{HISTORICAL_ERAS,CHAMPIONSHIP_SUCCESSION,OWNER_LINEAGE,TEAM_NAME_LINEAGE,PLAYOFF_ARCHAEOLOGY,HISTORICAL_PRESSURE_LEDGER}.md`
- `living-novel/os/adapters/flaim/PRO_SCHEMIN_HISTORICAL_INTELLIGENCE_LEDGER_V1.md`
- `living-novel/manuscript/` and `chronicles/proof-of-concept/` for pre-existing prose, not empty folders.

**Finding:** The ESPN historical extractor explicitly requires a caller-supplied `fetchHistoricalLeague` adapter; its comments state a starting target of 2025. Full verified matchups for every week 2015–2025 must not be asserted from extractor existence. Historical season gates remain **UNVERIFIED** until fact-ledger source/coverage audit.

## Phase 2 — Canon reconciliation: reuse established authority
- Characters: `canon/characters/CHARACTER_REGISTRY.yaml`, `TWELVE_CHARACTER_NARRATIVE_POV_REGISTER_V1.md`, reference manifests, and `living-novel/os/NOVEL_POV_CONSTITUTION_V1.md`.
- Geography: `world/data/locations.json`, `routes.json`, `location_relationship_graph.json`; Atlas foundation inventory records 23 locations, 18 routes, three divisions, and 12 owner-location relationships **as of 2026-09-30**. Recount live records before making a current total claim.
- Events: `world/data/world_state_events.json` has a sourced Week 2 LLC intrusion and multiple Week 3 continuity events.
- Mutation governance: `world/evolution/WEEKLY_WORLD_EVOLUTION_CONTRACT_V1.md` requires explicit Umpire and Closer approvals for APPLY, plus Commissioner for location candidate promotion. Never infer approvals. Dry-run by default.

## Phase 3 — Implied mythology: source-backed candidate discoveries (NOT newly accepted canon)
1. **The Bridge of Decisions**: `EVT-W3-BRIDGE` at `LOC-BRIDGE-MOUNTAIN-LAKE` records a remembered encounter and explicitly **no required physical destruction**. Candidate literary interpretation: a place where rivalry becomes civic memory. Investigate 2015–2025 rivalry sources before treating it as ancient.
2. **Scarred Mire**: `EVT-W3-MIRE-HILL` at `LOC-DK-MUD-HILL` records lasting scars and debris until cleanup. Candidate narrative pressure: the aftermath has witnesses, cleanup costs, and claims of victory.
3. **The Receipt Route**: `EVT-W3-ALPINE-WAGER` at `LOC-RED-SLOB-ALPINE-ROUTE` records a wager/summit receipt landmark. Candidate mythology: an object originally tied to a match becomes a recurring social proof and public memory.
4. **The Storm City**: `EVT-W3-LLC-STORM` at `LOC-LLC-STORM-CITY` remembers severe weather and ongoing storm-protection works. Candidate causal arc: infrastructure, merchants, and governance respond rather than resetting the city after each week.
5. **The Defiled Estate**: `EVT-W3-COUNTRY-CLUB-CHILI` at `LOC-COUNTRY-CLUB-JACKSON` explicitly requires cleanup before pristine reuse. Candidate arc: an insult to prestige becomes a material labor and restitution story.

**Evidence rule:** These are five **inference candidates from 2026 continuity events**, not proof of millennia-old eras or historical seasons. Do not fabricate ages, dynasties, battles, or league outcomes.

## Phase 4 — Manuscript production: existing working surfaces
Existing draft: `living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md`, Chapters 02–03, `PROLOGUE_DRAFT_V1.md`, plus rewrite candidates in `living-novel/production/full-rewrite-2026/manuscript/`.  
Production requirement for each proposed story scene:
`scene_id, season, week, source_matchup_ids, pov_owner_id, location_id, historical_claims[], narrative_inferences[], open_loops[], continuity_in[], continuity_out[], approval_status`.
Narrative should not pretend a successful phase 1 extraction where sources are missing. Preserve exclusive twelve-owner POV; do not resurrect Edrin/Edin.

## Phase 5 — Living Commonwealth: reuse deployed interfaces
- `world/atlas/interactive/SCHEMIN_ATLAS_INTERACTIVE.html` and `build_interactive_atlas.py`
- `world/evolution/WORLD_EVOLUTION_LEDGER.json`, `world/data/world_state_events.json`
- `living-novel/os/NOVEL_OS_PHASE_7_LIVE_SEASON_ENGINE_V1.md`
- `world/docs/UNIVERSE_OS_QUERY_PLAYBOOK_V1.md`
Reader-facing knowledge entries should link source claims, era, owner POV, and Atlas location; render **CANON**, **INTERPRETATION**, and **PROPOSAL** distinctly. Do not publish draft discoveries as encyclopedic truth.

## Independent Umpire acceptance checklist
- [x] Existing systems located and mapped to five phases (repository tree and selective file read)
- [x] Five source-backed narrative candidate threads isolated from world-state ledger
- [x] No silent canon/world mutation
- [ ] Full 2015–2025 week-by-week source and result verification
- [ ] Automated archive graph/index built and tested against complete source corpus
- [ ] All twelve POV manuscripts completed and independent literary acceptance
- [ ] Reader-facing Atlas/history/POV integration implemented, tested and deployed
- [ ] CI and independent Umpire green on implementation changes

**Current assessment:** Five-phase **repository audit and actionable evidence packet produced**; end-to-end implementation **NOT COMPLETE**. Do not report green until the above gates are backed by test and release receipts.
