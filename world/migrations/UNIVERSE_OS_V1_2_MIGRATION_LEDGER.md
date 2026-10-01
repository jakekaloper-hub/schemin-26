# UNIVERSE OS V1.2 — MIGRATION LEDGER

**Baseline:** World Engine V1.1 / Atlas V1 at `dea507983bc1ce8b3cf6393d41eec1bd5b7efd0e`
**Rule:** no active V1.2 mutation without provenance, tests and rollback.

| ID | Entity/System | Previous state | New state | Source | Affected systems/layers | Status |
|---|---|---|---|---|---|---|
| MIG-0001 | Wilson Look / D0nkey K0ng | historical Arsenal Centaur | Arsenal Gorilla Warrior | Commissioner correction 2026-09-29 | Character Control, Universe, Atlas Owner Domain, Memo, Novel, Art | MIGRATED |
| MIG-0002 | ObiWan / Jedi ontology | human mountain population; Jedi community implicit | principal ObiWan coexists with an explicit Jedi Order/community and non-Jedi humans | Commissioner correction 2026-09-30 | Ontology, Domain, Atlas Civil/Owner, Novel, Art | MIGRATING IN V1.2 |
| MIG-0003 | TDS body canon | older single-head reptile visual treatment | one body / three serpent heads | Commissioner correction | Character Control, Universe, Memo, Novel, Art | MIGRATED |
| MIG-0004 | TDS + Chili residence | division affiliation could be misread as separation | explicit cross-divisional shared coexistence | Commissioner directive 2026-09-29 | Atlas Division/Owner/Civil, Universe | MIGRATED |
| MIG-0005 | Atlas architecture | renderer/reference family under World Engine V1.1 | governed spatial control plane inside Universe OS V1.2 | Commissioner execution prompt 2026-10-01 | Universe, Atlas, Memo, Novel, Art | IN_PROGRESS |

## Rollback

Rollback restores consumers to V1.1/V1 files without deleting V1.2 history. A failed migration remains recorded with status `ROLLED_BACK` and defect receipt.

## Migration gate

Any future mutation must record:
MIGRATION_ID, CURRENT_STATE, PROPOSED_STATE, SOURCE, REASON, AFFECTED_SYSTEMS, AFFECTED_ATLAS_LAYERS, TESTS, ROLLBACK, RESULT.
