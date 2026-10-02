# Weekly Memo OS

Canonical home of the Schemin '26 Weekly Memo production system.

## Benchmark authority

**Current Memo benchmark is resolved dynamically, never hard-coded from historical prominence.**

Use `governance/publication-manifest/memo_reference_resolver.py` + `PUBLICATION_MANIFEST_V1.json`.

Current state:
- Week 2 `Week 2 memo.pdf` — canonical for Week 2; **HISTORICAL_GOLD_STANDARD**.
- Week 3 `Pro_Schemin_Week_3_Memo_Final.pdf` — **CURRENT_BENCHMARK**.
- Week 4 — unreleased/blocked and ineligible to satisfy latest/current until its release gate passes and benchmark promotion is transacted.

A historical gold standard remains useful for regression and craft comparison. It is not the default current reference. Search similarity, filename friendliness, prior prompt frequency, or an old “gold standard” label cannot override release authority.

## Fail-closed rule

Explicit week → exact released week only.  
latest/current/benchmark → highest released CURRENT_BENCHMARK.  
unreleased/unknown week → no substitution.

## Production lifecycle
1. Intake
2. Data verification/freeze
3. Rename + canon reconciliation
4. Pre-production
5. Page architecture
6. Copy
7. Art direction
8. Page production
9. Page-by-page QA
10. Final assembly
11. Mobile-readability audit
12. Publication package
13. Postmortem / OS patch

Historical outputs are regression evidence, not current-state defaults or templates to copy verbatim.
