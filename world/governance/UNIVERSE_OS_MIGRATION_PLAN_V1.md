# UNIVERSE OS V1.2 MIGRATION PLAN V1

## Migration strategy
Preserve V1.1 release evidence. Add V1.2 structures without deleting prior artifacts.

## Sequence
1. Snapshot baseline.
2. Add confidence/migration controls.
3. Normalize ontology.
4. Enrich domain profiles.
5. Build Atlas-native relationship graph.
6. Add memory classification.
7. Add civilization/institution data.
8. Add contracts/mutation/query layers.
9. Run acceptance and Week 1–3 replay.
10. Promote only after green release gates.

## Compatibility
Existing location IDs, route IDs, character IDs and division IDs remain stable unless an explicit migration record says otherwise.

## Rollback
Revert affected entity to baseline snapshot value; preserve the failed migration record and reason.
