# Schemin '26 — Whole-Architecture Modernization Mission (20 November 2026)

**State:** EVIDENCE-FROZEN / INVENTORY CAPTURED / IMPLEMENTATION BACKLOG OPEN / NOT A RELEASE.
**Project authority:** SCHEMIN_26_PROJECT_MISSION.md and PROJECT_CONTROL_REGISTRY.md.
**Proposed coordination:** The Closer; primary architecture owner The Architect; independent audit The Umpire; Librarian provenance; Scout external research.
**Branch:** audit/all-subsystems-world-engine-20261120. Changes here do not modify active canon, world state or release status.

## Mission

Evaluate the *whole* Schemin platform, including seemingly minor subsystems, paths, scripts, skills, commands, adapters, production work, 18 Bullpen Directors, their Staff dispositions, and three modeled external consulting lenses. Identify demonstrable capability defects, prepare compatibility-preserving fixes and tests, and use existing public work as a **study-only donor** until licensing, costs, security and adaptation pass review. No new OS, 19th Director, recursive Staff authority, unsupported human consultation, paid dependency or speculative canonical write.

## Reproducible inventory receipts

- Schemin Git tree pinned: db559bc97ef105c981f1f3d346a2e5332a8b6c93 (main, observed November 20). **2,687 tracked files / 492 nested directories** indexed. The exhaustive directory and file-path index is [SCHEMIN_RECURSIVE_REPOSITORY_INVENTORY.json](SCHEMIN_RECURSIVE_REPOSITORY_INVENTORY.json). Inventory is comprehensive for this tree, not exhaustive *semantic review* of all 2,687 file contents.
- Separate private Bullpen tree pinned: f740977ed4c16a33f291f10969d004bc8ed39edc. Its path-level inventory and modeled advisory receipt are retained **inside the private Bullpen repository only**. Do not copy private paths or internal consulting content into the public Schemin repository.
- Main branch tracks 19 substantive top-level domains: archive; bullpen-runtime; bullpen; canon; chronicles; data-gateway; data; docs; governance; living-novel; memo-os; mercer; planning; productions; prompts; schemas; skills; tests; world. Every nested directory is enumerated in the JSON snapshot. No domain gets silently excluded due to a low file count.
- Public authority and version evidence: PROJECT_CONTROL_REGISTRY.md; docs/architecture/REPOSITORY_ARCHITECTURE_V2.md; governance/repository-architecture/FOLDER_DOMAIN_REGISTRY_V2.json; governance/repository-health/AUDIT_2026_11_20.md.
- Full private Bullpen registry: exactly 18 Directors and 46 canonical Staff capabilities. Existing zero-base Staff disposition is 15 CORE_PORTABLE, 24 PROJECT_ADAPTER, 6 MERGE_CANDIDATE, 1 REFERENCE_ONLY. Registered does not mean running. Historical TriggerEngagementAlertStaff is non-canonical.
- Existing release/control evidence and stacked PRs must be resolved under issue #332 rather than bypassed by this mission.

## Confirmed version asymmetry is NOT itself a defect

| Authority plane | Current authoritative state | Action |
|---|---|---|
| World Engine | V1.1 RELEASED / ACTIVE (September 29) | Assess contract, replay, evolution and provenance gaps; propose *new* version only on measured change |
| Universe OS | V1.2 RELEASED / ACTIVE | Reuse entity/domain ontology, memory, civilization and read-only query resolver |
| Atlas Control Plane | V2 RELEASED / ACTIVE via Universe receipt | Keep one geography source; no candidate promotion |
| Weekly Memo OS | V5.5 ACTIVE; V5.6 RELEASE CANDIDATE | Reconcile any command/prompt still treating V5.2-RC as top-level authority |
| Character Control Plane | V2 RELEASE CANDIDATE | Respect source-byte/subject-binding HOLD |
| Playoff Context Intelligence | V1 BUILD CANDIDATE | Forecast cannot publish until walk-forward evidence and league truth lock |
| Bullpen Runtime inside Schemin | V1 implementation | Real worker and persistence adapters remain incomplete; no pretend Director execution |
| Repository Architecture | V2 ACTIVE | No new top-level authority stores |
| World Evolution | Phase 5 ACTIVE, dry-run-first | New APPLY needs release, Umpire and Closer gates |

**Key source issue:** world/data/current_world_state.json remains end_of_week_3_2026 while Week 10/11 and 2026 postseason development exists in draft branches. The gap does not justify generating fictional intervening official events. Require verified league/memo release evidence, chronological event replay, dry-run diff, rollback and signed approval before APPLY.

**Character-history contradiction to reconcile prospectively:** the September World Engine / Universe release receipts describe Wilson Look's centaur morphology as superseded, whereas the October 18 Commissioner-approved lineup controls contain a newer Arsenal Gorilla Centaur Warrior clarification. Preserve historical receipts as historical evidence; resolve which current canon record commands new rendering before any art or universe projection.

## Review lanes — no minor subsystem omitted

| Review lane | Scope (including child paths) | Primary / counterweight | Target evidence |
|---|---|---|---|
| Authority, missions, registries | PROJECT_CONTROL_REGISTRY, governance/*, docs/governance/*, execution-control, branch ledger, release-evidence, publication-manifest | Librarian / Umpire, Closer | No ambiguous source-of-truth claims; timestamped statuses |
| World/Universe | world/engine, world/data, world/state, world/evolution, world/ontology, world/civilization, world/institutions, world/contracts, world/history, world/governance | Architect + Librarian / Umpire | Replay, schema crosswalk, transition/rollback, one-world proof |
| Physical Atlas/venues | world/atlas, location-control-plane, environment-references, encounters, divisions, domains, routes, travel, spatial and QA paths | Librarian + Architect / Scout, Umpire | Stable IDs, adjacency/route, chronology, noncanonical candidate separation |
| Character canon and rendering | canon/*, visual plate/reference portability, morphology, output provenance | Librarian + Pitching Coach / Umpire | Owner-ID joins, source bytes, subject binding and adversarial visual QA |
| Data and intelligence | data-gateway/* including ESPN/freshness, playoff-context and harvest adapters; data/* | Scout + Analyst / Librarian | ESPN lock, deterministic input, no stale-live claims, model calibration |
| Editorial Memo and media | memo-os/* including week folders, creative DNA, cinematography, post-production, production adapters and tests | Beat Writer + Pitching Coach / Scout, Umpire | Correct active V5.5 contracts, evidence-to-copy lineage, mobile/visual review |
| Novel/chronicle/reader | living-novel/* incl OS, manuscripts, historical chronicle, author council, consultants, QA; chronicles/* | Beat Writer + Librarian / Umpire | Twelve-POV continuity, source/fiction labels, world/league consistency |
| Front Office | mercer/* and any external front-office adapter | Scout + Analyst / Warden | Private-data firewall, keeper/transaction ledger and locked source truth |
| Cross-domain execution | bullpen/*, bullpen-runtime/*, skills/*, prompts/*, production DAG, command and agent adapters | Closer + Architect / Umpire, Warden | Actual worker receipts vs simulated roles; no phantom operations |
| Artifact lifecycle | productions/*, planning/*, archive/*, post-season candidates and deployment surfaces | Groundskeeper + GM / Librarian, Umpire | Draft/active boundaries, supersession, artwork and publication gates |
| Platform engineering | schemas/*, tests/*, docs/*, .github/*; package/CI security; scripts nested in each domain | Setup Man + Architect / Warden, Umpire | Exact-head checks, path coverage, bounded resources, rollback |
| Operations / research capability | all 46 Staff and their dispositions; private Bullpen plugin/skill/command/adapter/evaluation paths | Clubhouse Manager + Librarian / Umpire | Per-capability operational status, evidence, license/cost posture |

Every file-path row in the snapshot must ultimately be assigned to an owning lane and one of: VERIFIED_CURRENT, REPAIR_REQUIRED, BLOCKED, HISTORICAL_REFERENCE, or UNREVIEWED. This document does **not** automatically award VERIFIED_CURRENT.

## Priority deficiencies and constraints

1. **P0 Release truth:** main is reported unprotected in issue #332; preserve independent review and do not merge stacked drafts or deploy without proof. Coordinate, do not duplicate, the branch visibility mission.
2. **P0 World chronological continuity:** derive a replayable sequence from accepted production and league evidence. Verify Week 3 baseline and recent release state; preserve open weeks as unknown.
3. **P0 World / character contract:** reconcile the later Commissioner appearance authority with historical receipts via versioned read-only view, not retroactive overwrite.
4. **P1 World API integration:** prove cross-consumer contract between World Engine, Universe, Atlas, Memo, Novel, spectator viewer and renderer; zero parallel truth stores.
5. **P1 Version and command drift:** scan docs, skills, scheduled production prompts and adapters that refer to older controlling Memo/World versions. Update only consumers after confirming authority.
6. **P1 New-world proposals:** draft PRs #321, #322, #324 and #325 propose Championship Island, 147 dossiers and 44 new candidate sites. Keep candidate vs active location separate, Last Field supersession held, historical-owner/memorial uncertainty intact. Read the latest branch state before treating an issue-body mismatch as unfixed.
7. **P1 Character and graphics:** canonical references and GPU/device acceptance are separate gates; do not promise cinematic/world production from structural environment candidates alone.
8. **P2 Reliability:** test deterministic world evolution, route topology, archive provenance, missing-provider fail-closed behavior, release state, negative fixtures, latency and end-to-end spectator read/return.
9. **P2 Bullpen actuality:** 18 Director identities are registry data, 46 Staff require status reconciliation, and internal Phase Two should be reviewed as capability maturity—not created as an uncontrolled third level of authority. Record exact runtime worker invocations. No Staff recursion by default.
10. **P2 Documentation and estate:** high-volume week assets and historical files should be indexed and maintained without wholesale deleting, renaming or consolidating provenance sources.

## Public-repository research — study-only donor shortlist

- [Temporal TypeScript SDK](https://github.com/temporalio/sdk-typescript) and [versioning documentation](https://github.com/temporalio/documentation/blob/main/docs/develop/typescript/workflows/versioning.mdx): borrow *ideas* for deterministic replay, idempotency, resumability, safe version migrations; no mandatory Temporal service or new paid platform.
- [OpenTelemetry semantic conventions](https://github.com/open-telemetry/semantic-conventions): learn consistent trace/span/context field names for Memo, Bullpen, Atlas, data and release provenance; map to existing Trace v1.2 rather than replace it.
- [Khronos glTF Validator](https://github.com/KhronosGroup/glTF-Validator): candidate format validation for glTF/GLB visualization exports, not for Unreal uasset files or JPEG/PNG. Add only when an applicable asset pipeline and test fixture exist.
- [SchemaStore](https://github.com/SchemaStore/schemastore): examine JSON Schema test discipline, including strict-mode and negative fixture coverage. SchemaStore is **not** itself a validator for all arbitrary local schemas; use an appropriate supported local validator.
- [Godot navigation documentation](https://github.com/godotengine/godot-docs): compare region/map/agent semantics to the existing spatial travel graph; design study, **not** a mandate to migrate from current Unreal/Canvas/WebGL work.
- Existing publicly accessible Schemin project and approved FLA public-source content should be preferred to unrelated libraries where it already contains domain concepts. Search reuse before invention.

Before any import: record pinned URL/commit, file-level license/provenance, dependency and CVE review, security boundary, zero-incremental-spend posture, performance benchmark, maintenance owner, tests and a reversible migration.

## Bullpen and advisory operating sequence

The established Bullpen operating law is intent → orientation → route → counterweights → bounded Staff → evidence → independent QA → Closer synthesis. The review should be coordinated by **Architect** with Setup Man and GM counterweights; Librarian owns inventory and source cutoffs; Scout sources research; Analyst measures; Groundskeeper handles state; Warden checks security; Clubhouse Manager reconciles Staff; Beat Writer/Visual/Pitching Coach review narrative/visual consumers. Remaining Directors inspect their applicable domain scopes, without artificial all-18 model calls when no material question exists.

Three separate **modeled** ConsultEngine lens calls were executed on the connected local Mac, using the same pinned high-level evidence packet and a local model, and preserved privately as a traceable receipt. They are NOT human consultations or independent acceptance. Reconciled suggestions:
- Jeff Lunsford lens: prioritize value-producing Atlas/production reliability and avoid a feature explosion.
- John Ezzell lens: publish dependency maps, interface contracts and rollback proofs before migration.
- Tim Veil lens: reproduce world state, tighten branch/version hygiene, validate schemas/asset formats and third-party risks.

The advisory calls raised candidate tests; these have **not** been executed or automatically endorsed. The Closer's actionable synthesis should favor inexpensive checks, not speculative new platform installation.

## Program gates

**G0 — Capture:** pinned full public/private inventories, recorded versions/holds, mixed-domain authority. COMPLETE for path discovery; semantic coverage incomplete.

**G1 — Classification:** create machine-checkable directory/file-to-owner statuses, consume existing Staff disposition and mark unknowns UNREVIEWED. Do not equate path listing with review.

**G2 — Contract QA:** assemble world/atlas/data/character/memo/novel/observer compatibility tests, including negative cases and frozen historical read-only state. Require real checks.

**G3 — Implementation:** make minimal reversible patches in owner-controlled directories; no data fabrication, founder-gated canon activation, third-party copy, version bump or direct main write.

**G4 — Independent acceptance:** exact-head tests, failures/dissent recorded, Umpire independent challenge, Warden license/secrets review, domain-owner acceptance, rollback proof. A modeled self-review is not independent signoff.

**G5 — Promotion / learning:** Closer integrates only accepted patches in dependency order; PR/CI readback; release evidence and public-facing status updated; library and regression lessons retained.

### Explicit no-change boundaries

No direct main writes, no release/status inflation, no new geography IDs activated from drafts, no unauthorized model/media spend, no human endorsement claims, no private Bullpen path inventory exposed in this public repository, and no rewriting historical receipts to erase version drift.

### Next real implementation tranche

- Build a deterministic *status/classification layer* over the already captured recursive snapshot, not a second source of truth.
- Create a canonical cross-system version/reference drift test for active control document consumers.
- Build an evidence-backed World Engine V1.2/2.0 *candidate specification* with replay acceptance; version decision awaits compatibility diff and actual executed results.
- Reconcile current published week and World Evolution pending APPLY via current Data Gateway, without auto-changing world state.
- Request independent Umpire check only after those verifiable patches exist.

