# Schemin '26 — Open PR Archaeology & Disposition Ledger V1

**Document class:** review / repository hygiene  
**Authority / owner:** Librarian + The Closer  
**Version:** 1.0  
**Status:** ACTIVE — 2026-09-29 reconciliation  
**Baseline main:** `00ba525d955ee2017f0ddef77d2a636b3ab30c97` after Memo OS V5.5 merge

## Rule

Open PRs are not alternate sources of truth.

Each older PR is classified as:
- **KEEP / REBASE** — contains unique current value that is not durably represented elsewhere;
- **CONSOLIDATE** — newer branch subsumes the work and should become the only active PR;
- **SUPERSEDED / CLOSE** — current main/newer branch makes the PR operationally obsolete;
- **HISTORICAL / DO NOT MERGE** — useful provenance, but merging would reintroduce stale or contradictory authority.

## Disposition

| PR | Subject | Disposition | Reason |
|---:|---|---|---|
| #4 | Digital Universe Week 2 R&D | KEEP / REBASE LATER | 63-file app/cinema/toolchain prototype remains unique. Very far behind main; do not merge as-is. |
| #6 | Commissioner Bot foundation | KEEP / REBASE LATER | Four architecture/privacy docs remain unique future-product work. Not current operating authority. |
| #12 | Repository integrity + Data Gateway | KEEP / REBUILD ON CURRENT MAIN | Contains unique Data Gateway durability, health-check, merge-gate, and branch-protection work. Must be recovered onto current architecture rather than merged from stale base. |
| #13 | Week 3 pre-Fact Novel intelligence | SUPERSEDED / CLOSE | Week 3 is fact-locked and closed; newer Week 3 story/causal work lives in the consolidated Novel branch. |
| #15 | Librarian cleanup / old character lock | HISTORICAL / CLOSE | Valuable audit history, but character conclusions are superseded by 2026-09-29 Commissioner canon and CCP work. Official Week 2 recovery receipt has been recovered to current branch. |
| #16 | Novel causal retrofit | CONSOLIDATE INTO #21 | #21 contains the causal retrofit plus later Week 3/POV work. |
| #17 | Enforcement Plane V1 | HISTORICAL / CLOSE | Useful enforcement design, but stacked on #15 and contains obsolete canon assertions. Do not merge into current canon. Reusable enforcement ideas remain recoverable from Git history. |
| #18 | Week 3 Chapter III closure | CONSOLIDATE INTO #21 | #21 contains Chapter III, Week 3 ledgers, and later whole-book/POV work. |
| #19 | Pre-book POV foundation | SUPERSEDED / CLOSE | #21 contains the evolved POV foundation/schema and supersedes the earlier seed files. |
| #20 | CCP v2 CI trigger | SUPERSEDED / CLOSE | Only unique file is a CI trigger. Actual CCP CI is now observed green; current reconciliation branch also runs shadow reconciliation. |
| #21 | Whole-book story revision / Week 3→4 state | ACTIVE CONSOLIDATION TARGET | Retarget to current `main`; this becomes the single active Novel PR. |

## Recovery decisions

### PR #12
Do not close yet.
Required recovery candidates:
- `.github/workflows/data-gateway-ci.yml`
- `.github/workflows/espn-cold-standby.yml`
- `.github/workflows/repository-merge-gate.yml`
- `data-gateway/check_snapshot_health.py`
- `data-gateway/refresh_espn_snapshot.py`
- `tests/test_data_gateway_snapshot_contract.py`
- branch-protection / repository-governance controls that remain non-duplicative.

Recovery must use current V5.5/current-canon/current-main architecture and re-run tests.

### PR #4 / #6
These are product incubators, not current control-plane work. Keep open but explicitly treat as **needs-current-main rebase before implementation resumes**.

### PR #17
Do not cherry-pick old canon enforcement wholesale. If enforcement-plane concepts are revived, rebuild policy assertions from current CCP/current canon.

## Closer rule

After consolidation:
- current operating truth lives on `main`;
- one active Novel PR;
- one explicit stale Data Gateway recovery PR until rebuilt;
- incubator PRs are clearly non-canonical;
- no superseded branch remains open merely because it once contained useful work.
