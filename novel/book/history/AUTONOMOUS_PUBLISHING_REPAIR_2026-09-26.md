# AUTONOMOUS PUBLISHING REPAIR — 2026-09-26

## Bullpen finding
The production contract named a canonical Living Book source and HTML path that did not actually exist in the repository. The legacy master also falsely described itself as synchronized through Week 3 while the approved publication boundary remains Week 2.

## Repairs completed
- Created and persisted `novel/book/SCHEMIN_LIVING_BOOK.md`.
- Enforced Week 2 as the released boundary.
- Excluded Chapter Three+ / Week 3 state from the Living Book source.
- Created and persisted the stable consumer path `novel/book/SCHEMIN_LIVING_BOOK.html`.
- HTML now renders only released material.
- Week 3 remains production-only.
- Existing legacy manuscript/release files remain provenance; they are not publication truth.

## Remaining production distinction
The stable HTML container now exists and is correct as publication infrastructure. Its current visual treatment is a functional consumer shell, NOT a claim that the full bespoke page-factory illustration mandate has been completed. Bespoke spread artwork must still pass the Page Factory Contract before it can be called final illustrated publication.

## Umpire
Publication-state integrity: PASS.
Canonical-path integrity: PASS.
Week-3 leakage: PASS (none in Living Book).
Full bespoke visual completion: NOT YET CLOSED.
