# Acceptance Report — Initial Build Candidate

**Activation:** HOLD / NOT ACTIVE

## Gates

- G1 Data: PARTIAL PASS — normalized Flaim/ESPN contract implemented; production Week 4 lock intentionally blocked while provider results remain UNDECIDED.
- G2 Rules: PARTIAL PASS — canonical repo verifies 12 teams / 14 regular-season weeks / 7 qualifiers; Flaim reports `H2H_RECORD` playoff seeding. Exact tie-dependent clinch/elimination remains blocked until that rule is encoded and regression-tested.
- G3 Reproducibility: PASS — deterministic seed test.
- G4 Exactness: PARTIAL PASS — conservative exact W/L-bound proofs tested; historical clinch/elimination regression fixtures still required before activation.
- G5 Monte Carlo Stability: BUILD PASS — deterministic/stability mechanics in unit suite; real historical calibration pending.
- G6 No False Certainty: PASS — probability 0/100 is never promoted to exact status.
- G7 Editorial Restraint: PASS — candidate cap enforced.
- G8 Narrative Preservation: PASS BY ARCHITECTURE — output is optional candidate data; no publication dependency.
- G9 Provenance: PARTIAL PASS — deterministic seed, snapshot boundary and rule-evidence references are defined; runtime receipt wiring pending production adapter.
- G10 Umpire: HOLD — independent production QA required after finalized Week 4 fixture.

## Activation rule

Do not activate until Week 4 (or another finalized real fixture) passes end-to-end ingestion, exact/probabilistic classification, provenance receipt, editorial filtering, and independent QA.
