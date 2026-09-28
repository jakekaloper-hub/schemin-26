# Schemin '26 — Repository Sweep Unresolved Register

**Document class:** review  
**Authority / owner:** The Librarian  
**Version:** 0.2  
**Status:** ACTIVE  
**Created:** 2026-09-27  
**Last sweep update:** 2026-09-27  
**Review trigger:** every substantive sweep sprint

| ID | Severity | Question / defect | Evidence | Owner | Blocking? | Next action | Disposition |
|---|---|---|---|---|---:|---|---|
| RIS-001 | P1 | Should `schemin-26` remain public if all project activity lives here? | GitHub reports public visibility; governance separates private Mercer intelligence; Roadmap previously claimed private | Warden + Jake | Yes for sensitive artifacts | resolve Issue #10; document visibility/private-storage policy | OPEN |
| RIS-002 | P2 | How should `main` be protected without breaking the trusted ESPN snapshot writer? | GitHub reports `protected: false`; snapshot workflow writes to default branch | Umpire + Groundskeeper | No | resolve Issue #11 with ruleset/bypass design | OPEN |
| RIS-003 | P2 | Which of PRs #7, #8, #9 remains meaningful? | #7 failed Novel OS CI; #8/#9 passed; all were certification-only and current main is >90 commits ahead | Novel OS + Closer | No | none | CLOSED — #7/#8/#9 closed with evidence comments |
| RIS-004 | P2 | Does CI provide evidence for current core subsystems? | Bullpen Runtime green at baseline main; recent Novel OS green; ZeroGPU smoke green; Data Gateway CI green | Groundskeeper | No | maintain evidence doc | CLOSED — see `planning/REPOSITORY_SWEEP_CI_EVIDENCE_2026-09-27.md` |
| RIS-005 | P2 | Is any local developer work uncommitted/unpushed? | GitHub connector cannot inspect arbitrary local clone | Setup Man / authorized local environment | No for GitHub-side sweep | attest through authorized filesystem/desktop environment when needed | NOT_ATTESTABLE |
| RIS-006 | P2 | Can the exact original V5.1 data-hardening patch be recovered? | `MIGRATION_LEDGER.md` records referenced-but-not-retrieved artifact | Librarian | No | recover verbatim only if authoritative source appears | OPEN |
| RIS-007 | P2 | Are active workflow purposes and outcomes mapped? | four original workflows inspected; Data Gateway CI added; run evidence normalized | Groundskeeper | No | periodic review | CLOSED |
| RIS-008 | P2 | Do high-value control/index paths resolve? | tree/path audit of project registry, root docs, subsystem indexes | Librarian | No | keep canonical path checks lightweight | CLOSED — unresolved artifacts promoted separately |
| RIS-009 | P1 | ESPN workflow can validate live data but default branch currently lacks durable `data/snapshots/1417621/latest.json` | successful schedule log + missing tree path; root cause is pre-stage `git diff --quiet` ignoring untracked files | Data Gateway + Groundskeeper | Yes for durable snapshot certification | merge tested repair, then require one successful post-merge scheduled/manual persistence proof | OPEN — repair + regression CI PASS on sweep branch |
| RIS-010 | P2 | Exact official published `Week 2 memo.pdf` is referenced but absent from repository | control registry names artifact; 440-file tree lacks it; Library search found only non-canonical substitutes | Librarian + Commissioner | No for current Week 3 work | recover exact authoritative bytes; do not substitute later/test PDFs | OPEN — tracked on Issue #5 |
| RIS-011 | P2 | Top-level Project Control Registry lagged Memo OS controlling stack | registry said V5.2-RC while Memo OS index says V5.4/V5.3 are binding | Librarian + Memo OS | No | none after merge | CLOSED — corrected on sweep branch |

## Warden scan

Targeted searches for common committed-secret patterns did not surface an obvious credential. Matches were prose or runtime environment-variable references. This is a targeted repository search, not a claim that a dedicated secret scanner has exhaustively certified all history.

## Closure rule

An item closes only when evidence is recorded in the sweep review or a durable decision/control document. Silence, age, or "looks resolved" is not closure.
