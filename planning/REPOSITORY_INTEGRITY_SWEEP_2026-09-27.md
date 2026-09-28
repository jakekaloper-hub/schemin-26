# Schemin '26 — Repository Integrity & Sync Sweep

**Document class:** review  
**Authority / owner:** The Librarian; final verdict by The Closer  
**Version:** 0.1 baseline  
**Status:** IN PROGRESS  
**Created:** 2026-09-27  
**Review trigger:** after each substantive remediation sprint  
**Baseline branch:** `main`

## Executive baseline

The sweep is being executed under the Master GitHub Repository Integrity, Sync & Provenance mandate, adapted to Schemin '26's actual single-project-repository architecture.

### Repository

- repository: `jakekaloper-hub/schemin-26`
- canonical role: Schemin '26 durable operating repository
- default branch: `main`
- baseline HEAD: `49194258ef60c3d467d6f1cdf9926c1a4cc84cc5`
- baseline commit: `Correct Week 3 TDS derived continuity under V5.3/V5.4`
- baseline visibility: **public**
- branch protection on `main`: **disabled**
- local workspace state: `NOT_ATTESTABLE_FROM_CURRENT_RUNTIME`

### Core structure observed

Durable domains present at baseline include:
- `canon/`
- `data-gateway/`
- `memo-os/`
- `memo-os/week-3/`
- `living-novel/`
- `chronicles/`
- `mercer/`
- `bullpen/`
- `bullpen-runtime/`
- `docs/`
- `planning/`

### Workflows observed

1. `bullpen-runtime-ci.yml` — push / pull request / manual; Node 22; `npm test`
2. `espn-cold-standby.yml` — manual + every 30 minutes; Python 3.12; refreshes validated ESPN snapshot and commits changed snapshot
3. `novel-os-ci.yml` — path-filtered push / PR / manual; Python 3.12 compile + unittest suite
4. `novel-os-zerogpu-smoke.yml` — path-filtered push / manual external-render smoke

The baseline HEAD has no GitHub combined-status contexts attached. This is not itself proof of CI failure because several workflows are path-filtered and GitHub Actions checks may be represented separately.

### Open PR state observed

Five open draft PRs were found:
- #9 Novel OS: Flaim CI certification
- #8 Novel OS Flaim certification v2
- #7 Novel OS Flaim certification
- #6 Commissioner Bot foundation
- #4 Digital Universe: Week 2 R&D foundation

PRs #7–#9 appear to represent successive certification attempts and require reconciliation so obsolete certification branches do not remain ambiguously active.

### Week 3 continuity

`memo-os/week-3/` is populated with durable evidence, continuity, character-packet, environment, data, Fact Lock, Monday exposure/close, composition, mobile, historical and QA artifacts. Recent main commits are actively updating Week 3 pre-Fact-Lock continuity.

This materially reduces the risk that current Week 3 state exists only in chat.

## Findings opened at baseline

| ID | Sev | Finding | Status |
|---|---|---|---|
| RIS-001 | P1 | Repository is public while governance anticipates private Mercer/sensitive project material | OPEN — tracked by issue #10 |
| RIS-002 | P2 | `main` has no branch protection | OPEN |
| RIS-003 | P2 | Three overlapping Novel OS/Flaim certification draft PRs are open | OPEN |
| RIS-004 | P2 | Current HEAD has no combined-status contexts; CI coverage needs workflow-run evidence by subsystem | INVESTIGATING |
| RIS-005 | P2 | Local developer workspace cleanliness cannot be attested through GitHub-only runtime | EVIDENCE LIMITATION |
| RIS-006 | P2 | Referenced original V5.1 data-hardening patch remains unretrieved | OPEN / preserved in migration ledger |

## Positive controls already present

- `README.md` explicitly defines `schemin-26` as canonical.
- FLA is explicitly upstream/reusable rather than league truth.
- `PROJECT_CONTROL_REGISTRY.md` provides subsystem navigation.
- `SOURCE_OF_TRUTH.md` defines evidence precedence.
- `DOC_STANDARD.md` defines durable-document metadata and closure discipline.
- Week 3 has a committed production evidence structure.
- CI exists for Bullpen Runtime and Novel OS.
- ESPN snapshot automation exists with a dedicated league ID and concurrency group.

## Next remediation sprint

1. inventory current branch/PR relationships and classify PRs #7–#9;
2. inspect recent workflow-run outcomes by workflow;
3. validate Bullpen Runtime package/test contract;
4. validate Novel OS deterministic suite inventory;
5. inspect ESPN snapshot freshness and scheduled-run health;
6. scan repository references for missing/renamed canonical paths;
7. update the unresolved register as findings close;
8. issue Closer checkpoint after evidence-backed repairs.

No destructive cleanup is authorized merely to improve appearance.
