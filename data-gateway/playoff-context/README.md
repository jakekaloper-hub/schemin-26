# Playoff Context Intelligence Layer V1

**Status:** WEEKLY RUNNER IMPLEMENTED / DESCRIPTIVE CANDIDATES VERIFIED / ADDITIONAL CONSUMPTION REQUIRES CHECK / INTERNAL FORECAST PUBLICATION HOLD

The local November 17 Week 10 run reconciled the completed season history and
remaining fixtures. Its walk-forward diagnostic did not beat the 50/50 baseline.
The Memo adapter therefore emits descriptive statistics while withholding
probability and leverage fields. This branch contains code, synthetic tests and
operating documentation only. Authenticated inputs, league-specific rule
evidence, simulation receipts and the full Memo packet are retained separately
pending explicit approval to publish those records to this public repository.

The retained production audit found stale copy at PR #315 `96bf06f`; that
branch subsequently finalized its existing inputs at `14b1ad0`. Additional
analytics still require source-to-copy and render-mirror checks. The actual
recent FFHub harvest is also retained through `FFHUB_INTAKE_CONTRACT.md`.
See `memo-os/week-10/playoff-context/README.md` for the current handoff and the
distinction between existing final production and optional new analytics.

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

## Weekly execution

Run from the repository root with a fresh captured Flaim bundle and accepted
rule evidence in a private working directory. Replace the example paths below
with your actual local paths; no real capture is bundled in this branch.

```bash
python data-gateway/playoff-context/validate_model.py \
  /path/to/private/week-10-capture.json \
  --rules /path/to/private/accepted-rules.json \
  --output /path/to/private/model-validation.json

python data-gateway/playoff-context/run_weekly.py \
  /path/to/private/week-10-capture.json \
  --rules /path/to/private/accepted-rules.json \
  --validation /path/to/private/model-validation.json \
  --simulations 10000 --include-leverage --leverage-simulations 2000 \
  --output /path/to/private/report.json \
  --memo-output /path/to/private/MEMO_ANALYTICS_PACKET.json \
  --previs /path/to/private/issue-previs.json \
  --render-inputs /path/to/private/render-inputs
```

Optional `--previs <current-issue-previs.json>` attaches candidates to existing
page contracts without changing approved copy or release state. The locally
verified Week 10 packet used PR #315 at `96bf06fb164580e85e7985150e37ac7310e3f088`.
Later issues supply their own page bindings; Week 10 numbering is not inferred.

`--render-inputs` is optional and reads the existing per-page `request.json`
files without editing them. The Memo packet always includes a production
readiness result. Missing requests, unreconciled final sources, stale copy,
unselected analytics and mismatched prompts remain explicit holds. A verified
source/copy/render boundary still does not approve artwork or publication.

The 24-hour freshness SLO is recomputed at consumption. Reproduce an old run
using its recorded evaluation timestamp with `--as-of` in both commands;
outputs are then explicitly `HISTORICAL_REPLAY`. Do not restamp old captures.
The adapter consumes captured provider observations and never requests cookies.

## Current evidence and external reference

- `ACCEPTANCE_REPORT.md`: implementation disposition and forecast hold.
- `WEEK_10_DOMAIN_HANDOFF.md`: Analyst ownership and operating handoff.
- `../../memo-os/week-10/playoff-context/README.md`: local packet disposition and page bindings.
- `THEFFHUB_REFERENCE.md`: upstream features, methods, source and license review.

Local source captures and audit receipts are not attached to the public branch.
The code's tests use synthetic inputs and do not require those retained files.

TheFFHub is an external manual scenario source. The separate November 17
session produced the retained 18-scenario harvest and two baselines; it was
recovered and checked for Week 10 production. This engine's values remain
Schemin calculations. Vendor estimates, independent proofs and internal model
output keep their own provenance and acceptance boundaries. Neither analytics
source replaces official standings or owning publication gates.
