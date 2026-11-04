# Commonwealth Creative Production — StoryCraftr pattern adaptation (candidate)

Status: IMPLEMENTATION CANDIDATE / NOT ACTIVE / NOT RELEASED

## Decision
**Adapt** the pattern of separate context preparation and chapter production.
**Adapt** task receipts and role-scoped authoring only through the existing Bullpen
execution control, NOT by copying StoryCraftr's threading/job system.
**Reject** importing generic all-Markdown retrieval as an authority mechanism.
**Reject** introducing new agents, canon stores, world models, paid providers, or
independent publication gates.

## Executable vertical slice
`living-novel/os/creative_context.py` accepts an intent and prepares an
authority-ranked manifest using the current `TASK_CONTEXT_MATRIX_V1.json`,
source authority matrix and existing execution registry. It fails closed for
unknown tasks or absent referenced sources. It never generates prose or changes
canon. The output status is deliberately `CONTEXT_READY_NOT_APPROVED`.

Usage: `python living-novel/os/creative_context.py "write chapter"`

Regression tests:
`python -m unittest discover -s living-novel/os/tests -p 'test_creative_context.py'`

## Subsystem patch matrix
| Owner | Scope | Decision |
| --- | --- | --- |
| Novel OS / Author Council | Context selection before chapter drafting | Adapt; candidate code |
| Historical Saga / Archivist | Source-authority routing for historical narrative | Reuse Novel OS; no parallel store |
| Memo OS | Existing story-first editorial controls | Retain; integration deferred pending tests |
| World Engine / Universe OS / Atlas | Existing canonical location and world-state contracts | Retain; no mutation |
| Character Canon | Existing owner/character authority and release gates | Retain; no mutation |
| Visual/cinematic studio | Existing scene and character-bound production gates | Retain; no mutation |
| Reader/public audience | Existing publication manifest and release authority | Retain; no mutation |
| Bullpen | Existing execution lifecycle, job registry and counterweights | Retain; no duplicate runner |
| Data Gateway / Mercer | Verified source/derived analytics authority | Read-only; no mutation |

## Release hold
This branch is a first vertical slice, not complete cross-subsystem integration.
Test output, code review, inherited canonical Bullpen route/counterweight evidence,
and independent Umpire acceptance are still required before activation or merge.
External research: https://github.com/raestrada/storycraftr
