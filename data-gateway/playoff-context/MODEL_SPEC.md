# Model Spec — V1

## Separation law

The model has two independent evidence classes:

- `PROBABILISTIC`: Monte Carlo estimates.
- `EXACT`: only claims proven by deterministic logic.

Editorial inference is downstream and must be labeled separately.

## Probability engine

Stdlib-only Monte Carlo replays the remaining regular-season schedule. Team scoring strength combines season scoring, recent scoring, limited regression toward league mean, and available future projections as a weak prior. Matchup outcomes are sampled from relative scoring-strength distributions; future points are sampled only as a probabilistic tiebreak proxy.

Default production target: 50,000 simulations; deterministic RNG seed recorded in receipt.

## Exact engine

V1 deliberately uses conservative win-bound proofs. It can prove some clinch/elimination states without needing uncertain future-points tiebreaks. When a statement cannot be proved, it does not infer certainty from simulation and remains `ALIVE`/`UNKNOWN`.

A later V1.x may add complete branch-and-bound/CP-SAT solving after tiebreak semantics are fully encoded and acceptance-tested.

## Result-lock law

A publishable weekly run must reject a current-week snapshot containing provider `UNDECIDED` matchups. Preview analysis may exist separately but must be labeled non-publishable.
