# Cross-System Integration Contract — Playoff Context Intelligence V1

**Status:** BUILD CANDIDATE / NOT ACTIVE

**2026-11-17:** The weekly capture runner and Memo consumer are implemented and
exercised on finalized Week 10 data. Global forecast activation remains held.
`run_weekly.py --memo-output` invokes `memo-os/playoff_context_adapter.py`;
optional previs input produces existing page attachments. The adapter rechecks
freshness and league/season/page identity and removes model forecast fields
while `editorial_probability_eligible` is false. See `ACCEPTANCE_REPORT.md`.

## Core authority

Data Gateway owns the normalized, freshness-valid league-state snapshot. Playoff Context owns derived postseason analytics only.

## Consumer boundaries

### Weekly Memo OS
May consume HIGH-priority editorial candidates after result lock. Memo OS retains page architecture, voice, story hierarchy and publication authority. Analytics annotations must remain optional.

### Jack Mercer
May consume playoff probability, seed distribution, remaining schedule difficulty and leverage as situational context for win-now/keeper/trade decisions. Mercer must not confuse playoff probability with player value or power ranking.

### Living Novel / Story Room
May consume evidence-classed consequences such as exact elimination, exact clinch, or large probabilistic leverage. It may not infer motive, emotion, theme or character psychology from the number.

### Weekly Production / GOTW planning
May use leverage ranking as one input for identifying consequential matchups. It must not automatically select Game of the Week or override narrative/canon priorities.

### Future postseason specials
May support bracket/path visualizations and scenario-tree reporting after exact tiebreak semantics and postseason rules are fully validated.

## Shared invariants

- Freshness and result-lock state travel with every input.
- `EXACT`, `PROBABILISTIC`, and `EDITORIAL_INFERENCE` never collapse into one class.
- Monte Carlo 0/100 never becomes clinched/eliminated.
- No consumer publishes machine wording automatically.
- Every published number must trace to snapshot + model version + seed/run receipt + candidate + QA decision.
