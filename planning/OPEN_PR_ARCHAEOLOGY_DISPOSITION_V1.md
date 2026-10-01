# Schemin '26 — Open PR Archaeology & Disposition Ledger V2

**Document class:** review / repository hygiene  
**Authority / owner:** Librarian + The Closer  
**Version:** 2.0  
**Status:** ACTIVE — 2026-10-01 reconciliation  
**Baseline main:** `be0c59a76418c13bbbb530da7027a33db41e9e82` after character-reference portability / renderer-binding hardening

## Governing rule

Open PRs are work surfaces, not alternate sources of truth.

Current merged `main`, `PROJECT_CONTROL_REGISTRY.md`, current release-evidence records, and explicit supersession decisions outrank stale PR prose.

Current dispositions:
- **ACTIVE_NEXT** — current candidate allowed to advance after its normal gates;
- **BLOCKED** — contains surviving value but cannot advance until named dependency/reconciliation closes;
- **EXPERIMENT** — future/product R&D with no current authority;
- **PARKED** — intentionally inactive; preserve only as a source for later current-main rebuild;
- **SUPERSEDED** — no longer a current merge candidate; close after durable value is recovered or remains safely recoverable from Git.

## Current open Schemin PRs

| PR | Subject | Disposition | Current ruling |
|---:|---|---|---|
| #61 | Novel: North-Star whole-book rebuild V3 | **ACTIVE_NEXT** | Single current Novel rebuild candidate. Starts from current main and explicitly supersedes #21. Keep draft until release gates close. |
| #47 | Atlas Phases 0–5 P1 hardening | **BLOCKED** | Unique hardening survives, but branch is far behind released Universe/Atlas main. Selectively rebuild/rebase against Universe OS V1.2; never merge stale branch wholesale. |
| #38 | Memo OS V5.6 RC | **BLOCKED** | V5.5 remains ACTIVE. V5.6 remains blocked on real Week 4 publication acceptance/final QA and requires current-main reconciliation before promotion. |
| #34 | Member AI Gateway Phase 1 | **EXPERIMENT** | Unique future product/service work, explicitly NOT CERTIFIED. No current control-plane authority. Rebuild on current Truth/Command contracts if resumed. |
| #6 | Commissioner Bot foundation | **PARKED** | Four unique architecture/privacy documents remain future-product research. Extremely stale; rebuild on current Member/Command/Truth contracts if revived. |
| #4 | Digital Universe Week 2 R&D | **PARKED** | Unique app/cinema prototype remains an incubator/reference source. Predates current Memo/World/Render architecture; selective rebuild only if product initiative resumes. |

## Closed in the 2026-10-01 reconciliation

| PR | Final disposition | Superseding/current authority |
|---:|---|---|
| #41 | **SUPERSEDED / CLOSED** | Universe OS V1.2 / Atlas Control Plane V2 released through later PRs #48/#51/#55. |
| #33 | **SUPERSEDED / CLOSED** | Canonical 18-Director rule and project command/counterweight consumption now live through Bullpen Command Adapter V2 and merged PRs #35/#36. |
| #32 | **SUPERSEDED / CLOSED** | Character fail-closed authority advanced through merged R2 enforcement #54 and reference-portability hardening #60. |
| #21 | **SUPERSEDED / CLOSED** | PR #61 is now the current Novel rebuild candidate and preserves #21 as literary provenance. |
| #12 | **SUPERSEDED / CLOSED** | Its recovery targets are now represented through Data R1 #50, release evidence #56, merge gate/branch-protection target #57, and current README/control reconciliation #59. |

Earlier closed/superseded branches from V1 remain historical Git provenance and are not reactivated by this ledger.

## Changed rulings from V1

### PR #12

V1 said **KEEP / REBUILD ON CURRENT MAIN** because durable ESPN persistence, health checking, repository merge gating and branch-protection controls had not yet been recovered.

That recovery is now complete enough to close the stale branch:
- Data R1 is operationally verified;
- durable `data/live` persistence exists;
- SHA-bound release evidence exists;
- the repository merge gate exists;
- the branch-protection target is explicit, with admin enforcement tracked separately.

Therefore #12 is now **SUPERSEDED**, not an active recovery PR.

### PR #21

V1 designated #21 as the active Novel consolidation target.

PR #61 was subsequently created from current main, rebuilt the whole-book source graph, and explicitly supersedes #21 while retaining its literary provenance.

Therefore #61 is now the single active Novel candidate and #21 is closed.

## Current dependency graph

- #61 is independent of #21 for merge authority; #21 remains provenance only.
- #38 cannot promote above V5.5 until real Week 4 publication acceptance/final QA closes and its branch is reconciled with current main.
- #47 cannot merge until surviving Atlas hardening is rebuilt/revalidated against released Universe OS V1.2 / Atlas Control Plane V2.
- #34, #6 and #4 have no current project authority and may not become active merely because their branches remain open.
- Character-bearing work on any open PR remains subject to the current fail-closed Character Generation Boundary and blocked character-production state.

## Closer rule

After this reconciliation:
- current operating truth lives on `main`;
- #61 is the only active Novel candidate;
- no stale repository-integrity, character-lock, organizational-design or obsolete Universe branch remains open as competing authority;
- incubator/product branches remain clearly non-canonical;
- BLOCKED branches must be rebuilt against current main rather than forcing old branch history forward.

Cross-project reconciliation record:
`jakekaloper-hub/bullpen/governance/CROSS_PROJECT_OPEN_PR_AUTHORITY_RECONCILIATION_2026-10-01.md`.
