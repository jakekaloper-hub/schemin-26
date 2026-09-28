# Schemin '26 — Repository Sweep Unresolved Register

**Document class:** review  
**Authority / owner:** The Librarian  
**Version:** 0.1  
**Status:** ACTIVE  
**Created:** 2026-09-27  
**Review trigger:** every substantive sweep sprint

| ID | Severity | Question / defect | Evidence | Owner | Blocking? | Next action | Disposition |
|---|---|---|---|---|---:|---|---|
| RIS-001 | P1 | Should `schemin-26` remain public if all project activity lives here? | GitHub reports public visibility; governance separates private Mercer intelligence | Warden + Jake | Yes for sensitive artifacts | resolve issue #10; document visibility/private storage policy | OPEN |
| RIS-002 | P2 | Should `main` receive branch/ruleset protection? | GitHub reports `protected: false` | Umpire + Groundskeeper | No | determine appropriate required checks without breaking scheduled data writes | OPEN |
| RIS-003 | P2 | Which of PRs #7, #8, #9 remains meaningful? | three draft Novel OS/Flaim certification PRs open | Novel OS + Closer | No | compare against current main and CI history; close superseded PRs only with evidence | OPEN |
| RIS-004 | P2 | Does current CI provide sufficient evidence at HEAD? | no combined status contexts on baseline SHA; workflows are path/event dependent | Groundskeeper | No | inspect latest runs per workflow and record outcomes | INVESTIGATING |
| RIS-005 | P2 | Is any local developer work uncommitted/unpushed? | GitHub connector cannot inspect arbitrary local clone | Setup Man / Jake environment | No for GitHub sweep | use authorized local filesystem connector when available | NOT_ATTESTABLE |
| RIS-006 | P2 | Can the exact original V5.1 data-hardening patch be recovered? | `MIGRATION_LEDGER.md` records referenced-but-not-retrieved artifact | Librarian | No | preserve provenance; recover verbatim only if authoritative source appears | OPEN |
| RIS-007 | P2 | Are all current workflows healthy and non-duplicative? | four workflows identified; run history not yet normalized | Groundskeeper | No | inspect run history/jobs/logs as needed | OPEN |
| RIS-008 | P2 | Are all canonical paths referenced by indexes actually present? | control/index system exists; link/path sweep not yet complete | Librarian | No | perform repository path/reference audit | OPEN |

## Closure rule

An item closes only when evidence is recorded in the sweep review or a durable decision/control document. Silence, age, or "looks resolved" is not closure.
