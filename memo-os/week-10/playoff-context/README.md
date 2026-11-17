# Week 10 sports analytics handoff

**Status:** reusable adapter implemented; real Week 10 packet generated and
independently checked locally; forecast publication held. This public branch
contains code and documentation. The authenticated league capture, detailed run
receipts and full Memo packet are retained separately pending explicit approval
to publish those records to the public repository.

## Existing page bindings

The local derived packet binds P27 (standings), P28 (divisions), P29 (scoring
form), P30 (playoff picture), P31 (next-week preview) and P35 (GOTW stakes) from
PR #315 at `96bf06fb164580e85e7985150e37ac7310e3f088`. It preserves the original
previs content and release fields. The 34-page budget and omitted P32 remain
unchanged. No production artwork was modified or approved by this integration.

The adapter supplies official record/seed observations, scoring averages and
recent form, weekly all-play, weekly-median comparisons, schedule-neutral win
equivalents, descriptive schedule effects and remaining opponents' observed
scoring averages. Definitions travel with every value. Those comparisons
describe scores and schedules; they do not establish skill or future entitlement.

## Forecasts withheld

The local walk-forward diagnostic did not beat a 50/50 baseline. The adapter's
descriptive-field allowlist excludes probability, seed-distribution,
simulated-win, uncertainty and leverage fields while forecast acceptance is held.
The raw simulation remains available locally for Analyst review.

Exact division-clinch logic remains unresolved. Zero sampled successes is not
elimination. Older conditional witnesses cannot become an exact claim without
a reproducible proof.

## Reuse and ownership

Run `data-gateway/playoff-context/run_weekly.py` with the accepted local capture,
rules and diagnostic. Use `--memo-output` for the derived packet and optional
`--previs` for the current production copy. See the subsystem README for example
commands. Future weeks supply their own actual page bindings.

Scout/Data Gateway owns source acceptance; Analyst owns mathematics and model
quality; Beat Writer/Memo Editor selects useful content; independent Umpire and
the existing Memo gates review final output. Candidate generation does not
certify Fact Lock or authorize publication. Recheck freshness at consumption.
