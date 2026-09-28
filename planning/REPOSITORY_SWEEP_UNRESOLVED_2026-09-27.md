# Schemin '26 — Repository Sweep Unresolved Register

**Document class:** review  
**Authority / owner:** The Librarian + Bullpen second-line review  
**Version:** 0.3  
**Status:** ACTIVE  
**Created:** 2026-09-27  
**Last sweep update:** 2026-09-27  
**Review trigger:** material PR #12 head change, merge, post-merge data-plane proof, or visibility disposition

| ID | Severity | Question / defect | Evidence | Owner | Blocking? | Next action | Disposition |
|---|---|---|---|---|---:|---|---|
| RIS-001 | P1 | Should `schemin-26` remain public if all project activity lives here? | GitHub reports public visibility; governance separates private Mercer intelligence; durable ESPN persistence is pending | Warden + Jake | Yes for PR #12 release | resolve Issue #10; Bullpen target is private repo unless a redacted public snapshot contract is approved | OPEN |
| RIS-002 | P2 | How should `main` be protected without breaking ESPN persistence? | Operational writes moved to `data/live`; always-on Repository Merge Gate added | Umpire + Groundskeeper | No | authorized admin applies `docs/governance/BRANCH_PROTECTION_TARGET_V1.md` | ARCHITECTURE CLOSED / ADMIN SETTING OPEN — Issue #11 |
| RIS-003 | P2 | Which of PRs #7, #8, #9 remains meaningful? | #7 failed Novel OS CI; #8/#9 passed; all were certification-only | Novel OS + Closer | No | none | CLOSED — #7/#8/#9 closed with evidence comments |
| RIS-004 | P2 | Does CI provide stable repository-level merge evidence? | Repository Merge Gate + Data Gateway CI + Bullpen Runtime CI all PASS at PR #12 head `015cd9d82cd793760e126892457990ba2b1056c4` | Groundskeeper | No | preserve always-on gate as required-check surface | CLOSED |
| RIS-005 | P2 | Is any local developer work uncommitted/unpushed? | GitHub connector cannot inspect arbitrary local clone | Setup Man / authorized local environment | No for GitHub-side sweep | attest through authorized filesystem/desktop environment when needed | NOT_ATTESTABLE |
| RIS-006 | P2 | Can the exact original V5.1 data-hardening patch be recovered? | `MIGRATION_LEDGER.md` records referenced-but-not-retrieved artifact | Librarian | No | recover verbatim only if authoritative source appears | OPEN |
| RIS-007 | P2 | Are active workflow purposes and outcomes mapped? | workflows audited; Data Gateway CI and Repository Merge Gate added | Groundskeeper | No | periodic review | CLOSED |
| RIS-008 | P2 | Do high-value control/index paths resolve? | control/index tree audit completed | Librarian | No | periodic path audit | CLOSED — unresolved artifacts promoted separately |
| RIS-009 | P1 | Is durable ESPN state end-to-end operational? | first-write defect repaired; operational writes isolated to `data/live`; LKG hydration added; contract tests and merge gate green | Data Gateway + Groundskeeper | Yes for final certification | after visibility disposition + merge, require scheduled/manual run that persists `data/live:data/snapshots/1417621/latest.json` and passes health check | OPEN — CODE/CI PASS, RUNTIME PROOF PENDING |
| RIS-010 | P2 | Exact official published `Week 2 memo.pdf` is referenced but absent | tree audit + Library recovery search found only non-canonical substitutes | Librarian + Commissioner | No | recover exact authoritative bytes; never substitute later/test PDFs | OPEN — tracked on Issue #5 |
| RIS-011 | P2 | Top-level Project Control Registry lagged Memo OS controlling stack | registry said V5.2-RC while subsystem index said V5.4/V5.3 | Librarian + Memo OS | No | none | CLOSED |
| BPA-002 | P1 | Failed ESPN refresh could not mark durable LKG stale because LKG was not hydrated before refresh | Bullpen workflow audit | Data Gateway | No after merge | post-merge failure-path certification when practical | CLOSED IN CODE — regression guard added |
| BPA-003 | P2 | Runtime docs claimed mirror behavior not implemented by code | operational patch audit | Librarian + Data Gateway | No | none | CLOSED — executable contract corrected |
| BPA-004 | P1 | Structurally incomplete ESPN payloads could pass validation | validator audit | Data Gateway | No after merge | monitor upstream contract changes | CLOSED IN CODE — tests added |
| BPA-005 | P1 | No stable always-on status check suitable for branch protection | workflow audit | Groundskeeper | No | admin applies required check to main | CLOSED IN CODE — Repository Merge Gate green |

## Current PR-head evidence

At PR #12 head `015cd9d82cd793760e126892457990ba2b1056c4`:

- Repository Merge Gate / Schemin Repository Integrity — PASS
- Data Gateway CI — PASS
- Bullpen Runtime CI — PASS

## Warden scan

Targeted searches for common committed-secret patterns did not surface an obvious credential. Matches were prose or runtime environment-variable references. This is a targeted repository search, not a full-history secret-scanner certification.

## Closure rule

An item closes only when evidence is recorded in the sweep review or a durable decision/control document. Final repository-sweep closure still requires the visibility disposition and post-merge ESPN `data/live` persistence proof.
