# Schemin '26 Knowledge Inventory

**Authority:** The Librarian (CKO)  
**Version:** 1.0  
**Created:** 2026-09-25  
**Currency target:** Review monthly during active season and after major subsystem changes.

## Registry

| Path | Class | Authority | Status | Review trigger |
|---|---|---|---|---|
| `README.md` | navigation | Librarian | active | repository structure change |
| `PROJECT_CONTROL_REGISTRY.md` | control | Executive Control | active | authority / build change |
| `MIGRATION_LEDGER.md` | provenance | Librarian | active | source recovery / migration |
| `docs/CATALOG.md` | knowledge architecture | Librarian | active | new folder / index |
| `docs/SESSION_CONTEXT.md` | session routing | Librarian | active | routing / subsystem change |
| `docs/governance/SOURCE_OF_TRUTH.md` | governance | Data / Executive | active | source hierarchy change |
| `docs/governance/AUTHORITY_MATRIX.md` | governance | Executive Control | active | responsibility change |
| `docs/governance/DOC_STANDARD.md` | governance | Librarian | active | documentation policy change |
| `docs/architecture/REPOSITORY_ARCHITECTURE.md` | architecture | Executive / Librarian | active | structure change |
| `docs/architecture/FLA_INTEGRATION.md` | integration | Schemin Executive | active | FLA boundary change |
| `memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_GOLD_STANDARD_STUDIO_PATCH.md` | controlling patch | Weekly Memo OS | active | superseding Memo OS patch |
| `memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_2_RC_MUTUAL_IMPLEMENTATION_PATCH.md` | controlling RC patch | Memo OS + SCK | active RC | acceptance result / supersession |
| `memo-os/SCHEMIN_26_WEEKLY_MEMO_GOLD_STANDARD_PRODUCTION_MANUAL.md` | runbook | Weekly Memo OS | active | production method change |
| `memo-os/SCHEMIN_26_WEEKLY_MEMO_MASTER_INITIATION_PROMPT.md` | prompt | Weekly Memo OS | active reference | prompt replacement |
| `canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md` | canon | Character authority / Jake | binding | explicit approved canon change |
| `canon/league.json` | structural config | Data / Commissioner | active | league structural change |
| `data-gateway/OPERATIONAL_PATCH_v1.0.md` | runbook | Data Gateway | active | acquisition/fallback change |
| `data-gateway/SCHEMIN_26_ESPN_INGESTION_RELIABILITY_PATCH_v1.0.md` | architecture | Data Gateway | active | reliability design change |
| `schemas/freshness.schema.json` | schema | Data Gateway | active | envelope contract change |
| `mercer/JACK_MERCER_FRONT_OFFICE_V2_SPEC.md` | product spec | Mercer | active | Front Office version change |
| `mercer/OPERATING_CONTRACT.md` | operating contract | Mercer | active | Mercer doctrine change |
| `bullpen/SCHEMIN_26_BULLPEN_FULL_PROJECT_REVIEW.md` | review snapshot | Bullpen | historical-current reference | new full-board review |
| `bullpen/SCHEMIN_26_SUBAGENT_V5_1_ENGINE_ROOM_RESPONSE.md` | architecture proposal | Subagent OS | adopted in later RC where stated | supersession |
| `planning/ROADMAP.md` | roadmap | Executive Control | active | monthly / milestone |
| `docs/decisions/ADR-0001-knowledge-architecture.md` | ADR | Executive + Librarian | accepted | architecture reversal |
| `archive/_INDEX.md` | archive registry | Librarian | active | archival event |

## Known gap

The exact original `SCHEMIN_26_WEEKLY_MEMO_OS_V5_1_DATA_HARDENING_PATCH.md` is referenced by migrated evidence but has not yet been recovered verbatim. Do not create a counterfeit original. Recover and register it when available.

## Orphan rule

A durable Markdown or machine-readable governance file added to this repository without a corresponding inventory/index update is considered an **orphan** and should be repaired before the workstream is closed.
