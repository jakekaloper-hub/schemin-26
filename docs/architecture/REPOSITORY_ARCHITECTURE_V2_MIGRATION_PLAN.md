# Repository Architecture V2 Migration Plan

## Decision

**No P0 or P1 file moves are approved for V2.** The current domain-first structure is sufficiently coherent; the material defects are missing entry points, stale architecture metadata and unenforced placement boundaries.

## P0 — authority-risk corrections
None requiring relocation.

## P1 — structural ambiguity corrections
Close in place:
- formalize `governance/` vs `docs/governance/` boundary;
- formalize `living-novel/` vs `chronicles/` vs `productions/` boundary;
- define planning graduation law;
- add missing root entry points;
- register all top-level directories.

## P2 — future cleanup candidates
- root `XCODE_CHATGPT_HANDOFF.md`;
- root `XCODE_HANDOFF_PRO_SCHEMIN_WORLD.md`.

These are visible root clutter but not current authority hazards. V2 leaves them untouched to avoid path churn.

## P3 — cosmetic
No action.

## Premortem

| Failure | Mitigation | Detection | Rollback |
|---|---|---|---|
| Broken links from moves | no V2 relocations | architecture/reference tests | revert commit |
| CI path breakage | path-scoped validator tests | Repository Merge Gate | revert batch |
| stale Task Orientation | validate context-source paths | orientation suite | restore prior matrix |
| stale Execution Control authority | existing execution-control validator | merge gate | restore registry refs |
| Publication Manifest/release evidence break | no relocation; run suites | publication/release CI | revert |
| Canon/Novel/Memo read-order break | update navigation only; run domain suites | domain CI | revert |
| historical identity ambiguity | no artifact relocation in V2 | publication/release tests | n/a |

Future moves must be small coherent batches with atomic reference updates and post-batch regression.