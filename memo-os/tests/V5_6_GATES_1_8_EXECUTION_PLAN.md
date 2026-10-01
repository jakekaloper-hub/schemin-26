# V5.6 Publication Integrity — Gates 1–8 Execution Plan

**Status:** EXECUTION PLAN  
**Authority:** Weekly Memo OS / Bullpen  
**Branch:** `memo-os/v5-6-publication-integrity`  
**Promotion target:** V5.6 only after all mandatory promotion evidence passes.

## Operating loop

Each gate follows:

`PLAN → BUILD → RUN → AUDIT → BUG-FIX → POLISH → RETEST → LOCK / BLOCK`

A gate may finish as PASS or BLOCKED. BLOCKED is valid completion when the missing evidence is external or deliberately unavailable; blocked gates may not be mislabeled PASS.

## Gate 1 — Acceptance Harness Construction

**Bullpen owners:** Architect, Setup Man, Umpire, Librarian.

**Build**
- executable V5.6 suite;
- release/page/canon/world/fact/publication fixtures;
- retained V5.5 suite invocation;
- machine-readable summary.

**Pass**
- test runner exits zero;
- every declared V5.6 control has at least one positive and one negative path where applicable;
- no test simply asserts `True` for a release-critical invariant.

## Gate 2 — V5.5 Regression Preservation

**Bullpen owners:** Umpire, Librarian.

**Build**
- invoke retained V5.5 suite unchanged;
- compare expected 11 groups to current result;
- detect accidental authority or fixture mutation.

**Pass**
- 11/11 retained V5.5 groups pass;
- V5.6 does not rewrite V5.5 historical acceptance evidence.

## Gate 3 — Controlled Failure Injection

**Bullpen owners:** Umpire, Pitching Coach, Scout, World/Canon domain owners.

**Inject**
- wrong character body/species;
- rename-driven redesign;
- stale fact;
- wrong score;
- world-location conflict;
- wrong artifact class;
- missing mounted reference;
- unaddressable asset.

**Pass**
- each injected defect is rejected by the nearest responsible gate;
- no downstream gate can override an upstream hard fail.

## Gate 4 — Dependency Reopen / Targeted Recovery

**Bullpen owners:** Architect, Setup Man, Umpire.

**Build**
- dependency graph for page → fact/canon/world/asset/release dependencies;
- late-correction event processor;
- reopen only dependent pages/modules.

**Pass**
- affected pages reopen;
- unaffected locked pages remain locked;
- provenance/event trace records why.

## Gate 5 — Controlled Publication Simulation

**Bullpen owners:** Groundskeeper, Beat Writer, Architect, Umpire.

**Build**
A synthetic five-page issue:
1. cover;
2. matchup feature;
3. scoreboard;
4. Pittsy-style ledger placeholder using deterministic test data only;
5. Final Word.

The simulation uses fake test facts and cannot be mistaken for a real Week 4 issue.

**Pass**
- complete page contracts;
- deterministic-data boundary;
- release registry candidate record;
- final-PDF audit flag required;
- publication cannot become RELEASED without final artifact identity and final audit.

**Important:** this proves orchestration only. It does not satisfy real-media promotion evidence.

## Gate 6 — Independent Bullpen Audit

**Bullpen owners:** Librarian, Umpire, Warden, Pitching Coach, Groundskeeper, Closer.

Independent review domains:
- authority/load order;
- character/canon enforcement;
- world/encounter enforcement;
- fact/story/myth separation;
- generation intent;
- reference mounting;
- renderer-addressable asset contract;
- privacy/Mercer firewall;
- release identity;
- anti-bureaucracy / duplicate-control risk.

**Pass**
- zero unresolved critical engineering defects;
- all remaining blockers explicitly classified as engineering, evidence, or production-media blockers.

## Gate 7 — PR #38 Hardening

**Bullpen owners:** Architect, Setup Man, Closer.

**Actions**
- run all repo CI;
- confirm branch mergeability;
- inspect changed files for unintended authority promotion;
- keep V5.5 controlling until Gate 8 passes;
- resolve code/test defects;
- record non-Memo deployment/check failures separately when unrelated.

**Pass**
- Memo-specific tests and acceptance workflow green;
- no unresolved review-blocking defect in changed Memo files;
- PR remains draft until promotion evidence is complete.

## Gate 8 — Promotion Decision

**Bullpen owners:** Umpire + Closer; production systems cannot self-promote.

**Mandatory evidence**
- Gates 1–7 complete;
- controlled Week 2 reconstruction against release-time evidence;
- real Week 4 page acceptance against current Truth/Canon/World state;
- actual generated-media proof of reference mounting;
- renderer-addressable exact bytes + hash + independent inspection;
- final-raster Character/World/Intent QA;
- independent release audit;
- zero critical defects.

**Decision**
- PASS → update Project Control Registry and promote V5.6.
- BLOCKED/FAIL → V5.5 remains ACTIVE; V5.6 remains RC.

No partial evidence may silently promote V5.6.
