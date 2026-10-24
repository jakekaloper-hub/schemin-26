# Playoff Context Intelligence Layer V1

**Status:** BUILD CANDIDATE / NOT ACTIVE

Reusable Schemin analytics capability beneath publication systems. It converts verified league-state snapshots into probabilistic playoff context plus conservative exact W/L-bound proofs, then emits a small editorial-candidate set. It does not publish prose or mutate canon.

## Authority boundary

`Flaim / ESPN evidence -> Data Gateway-normalized snapshot -> playoff-context engine -> editorial candidates -> owning publication/editorial gate`

- Data Gateway owns live/current truth and freshness.
- This package owns derived playoff analytics only.
- Memo OS / Living Novel / Mercer remain owners of their presentation and decision surfaces.
- Monte Carlo 0%/100% never becomes `ELIMINATED`/`CLINCHED` automatically.
- Current-week production requires a final-result lock.

## V1 surfaces

1. Probability engine: playoff probability, seed distribution, expected wins.
2. Exact engine: safe clinch/elimination proofs from W/L bounds; otherwise `ALIVE/UNKNOWN` rather than false certainty.
3. Conditional leverage: win-vs-loss playoff probability delta.
4. Editorial restraint filter: no more than configured high-value candidates.
5. Provenance-ready deterministic seed and normalized snapshot contract.

## Reuse

This capability is intentionally publication-agnostic and can feed:

- Weekly Memo page packets;
- Mercer GM situational context;
- Living Novel / Story Room consequence packets (fact class only, never motive/theme);
- weekly production planning and GOTW selection support;
- future playoff/championship special issues.

## Run tests

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```
