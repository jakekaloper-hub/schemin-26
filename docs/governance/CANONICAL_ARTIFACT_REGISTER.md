# Schemin '26 — Canonical Artifact Register

**Authority / owner:** The Librarian  
**Version:** 1.0  
**Status:** ACTIVE — INITIAL SWEEP REGISTER  
**Effective date:** 2026-09-27  
**Review cadence:** after material subsystem changes and each major weekly publication cycle

| Artifact / domain | Canonical path | Status | Authority | Validation / note |
|---|---|---|---|---|
| Project entry point | `PROJECT_CONTROL_REGISTRY.md` | active | Librarian / SCK | controls navigation |
| Standing operating contract | `docs/governance/SCHEMIN_26_STANDING_OPERATING_CONTRACT_V1.md` | active control | Jake / Bullpen / Librarian / Closer | standing BTS execution contract |
| Source-of-truth policy | `docs/governance/SOURCE_OF_TRUTH.md` | active | Librarian / Data | hierarchy + publication override |
| Authority matrix | `docs/governance/AUTHORITY_MATRIX.md` | active | Umpire / Librarian | mixed-domain boundaries |
| FLA boundary | `docs/architecture/FLA_INTEGRATION.md` | active | Architect / Librarian | upstream-only relationship |
| Character canon | `canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md` | active canon | Character QA | owner → character → current team |
| Memo V5 base | `memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_GOLD_STANDARD_STUDIO_PATCH.md` | controlling layer | Memo OS | read with subsequent patches |
| Memo V5.2 RC | `memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_2_RC_MUTUAL_IMPLEMENTATION_PATCH.md` | RC architecture | Memo OS | not permanently certified by existence |
| Memo V5.3 | `memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_3_CHARACTER_REFERENCE_ENFORCEMENT_PATCH.md` | active patch | Memo OS / Character QA | character reference enforcement |
| Memo V5.4 | `memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_4_ACCEPTANCE_TEST_HARDENING_PATCH.md` | active patch | Memo OS / QA | acceptance hardening |
| Week 3 production bible | `memo-os/WEEK_3_MEMO_PRODUCTION_BIBLE_V1.md` | active week-3 control | Memo OS | week-specific |
| Week 3 evidence/register set | `memo-os/week-3/` | active production state | Memo OS / Closer | evidence, continuity, Fact Lock, QA |
| ESPN reliability doctrine | `data-gateway/SCHEMIN_26_ESPN_INGESTION_RELIABILITY_PATCH_v1.0.md` | active | Data Gateway | freshness contract |
| ESPN runtime policy | `data-gateway/OPERATIONAL_PATCH_v1.0.md` | active | Data Gateway | operational/fallback rules |
| Scheduled ESPN snapshot workflow | `.github/workflows/espn-cold-standby.yml` | active workflow | Groundskeeper / Data | 30-minute schedule + manual |
| Novel OS regression workflow | `.github/workflows/novel-os-ci.yml` | active workflow | Novel OS / Groundskeeper | Python 3.12 unittest suite |
| ZeroGPU smoke workflow | `.github/workflows/novel-os-zerogpu-smoke.yml` | active workflow | Novel OS / Groundskeeper | external render smoke |
| Bullpen runtime CI | `.github/workflows/bullpen-runtime-ci.yml` | active workflow | Groundskeeper | Node 22 / npm test |
| Mercer spec | `mercer/JACK_MERCER_FRONT_OFFICE_V2_SPEC.md` | active | Mercer | read with operating contract |
| Mercer operating contract | `mercer/OPERATING_CONTRACT.md` | active | Mercer | privacy / authority boundary |
| Migration ledger | `MIGRATION_LEDGER.md` | historical + recovery control | Librarian | preserves unresolved original artifact |
| Repository integrity control | `docs/governance/REPOSITORY_INTEGRITY_SWEEP_CONTROL_V1.md` | active sweep control | Librarian | governs current sweep |

## Known non-canonical / unresolved reference

`SCHEMIN_26_WEEKLY_MEMO_OS_V5_1_DATA_HARDENING_PATCH.md` remains a referenced-but-not-retrieved original according to the migration ledger. Do not fabricate an "original" replacement; recover verbatim if found and update the ledger.
