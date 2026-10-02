# Librarian Learning — Current Authority Hardening

**Date:** 2026-10-02  
**Authority:** The Librarian (CKO) + Umpire / Closer review  
**Trigger:** PR #99 stale-authority stress test and repair cycle  
**Status:** DURABLE LEARNING / ACTIVE

## Incident class

Schemin can contain multiple artifacts that are all historically valid while only one is current for the user's task.

The failure mode is not necessarily false data. It is **correct historical evidence winning the retrieval race against newer authority** because it is easier to retrieve, more frequently referenced, semantically similar, or historically labeled canon/gold standard.

## Durable authority model

Resolve current authority by:

`DOMAIN + TEMPORAL SCOPE + RELEASE STATE + PRODUCTION ELIGIBILITY`

These are separate dimensions.

Examples:
- Week 2 Memo remains canonical for Week 2 but is not the current/latest Memo benchmark.
- current character semantic canon does not itself prove renderer eligibility.
- current World authority outranks an older released render.
- current Novel canon outranks consultant copies and superseded manuscript candidates.
- a live-data claim requires freshness; a valid old snapshot is not live.

## Layered-router lesson

A new authority resolver must not replace unrelated control planes.

PR #99 initially improved temporal authority but accidentally dropped:
- Repository Architecture V2 references from the human session router;
- explicit Execution Control registry routing required for fresh-operator recovery;
- compatibility with existing orientation assertions.

Therefore router evolution must preserve all applicable layers:

`PROJECT CONTROL → TASK ORIENTATION → EXECUTION CONTROL → DOMAIN AUTHORITY RESOLUTION → EVIDENCE / RELEASE / PRODUCTION GATES`

No single layer subsumes the others.

## Test-design lesson

Regression tests must validate the semantic contract, not incidental string formatting.

Example:
- Novel authority routing correctly stored a full repository path to `WHOLE_BOOK_SOURCE_AUTHORITY_MATRIX_V1.md`.
- the first PR #99 test incorrectly expected a bare filename and failed despite correct routing.

Tests should allow canonical full paths while remaining strict about authority identity.

## Character retrieval lesson

For current character-render work, the first packet should prioritize:
1. `canon/_INDEX.md`;
2. `canon/characters/VISUAL_REFERENCE_AUTHORITY_V1.json`;
3. current source/hash authority.

Legacy prose and convenience composites may remain useful context, but they cannot outrank the active machine visual-authority layer.

## Memo retrieval lesson

Weekly Memo routing separates:
- exact historical publication identity;
- current/latest benchmark authority;
- production-system authority.

Current/latest publication identity resolves through Publication Manifest + deterministic Memo resolver.

Production workflow resolves through `memo-os/_INDEX.md`, which owns the V5.5/V5.6 relationship.

Do not hard-wire an RC reconciliation file as the universal current publication authority.

## Merge-gate lesson

A standalone green workflow is insufficient if the repository's protected merge contract depends on one required gate.

Cross-domain authority is therefore now included as an explicit `authority` suite in the Repository Merge Gate for authority-sensitive files.

This converts the policy from advisory CI into merge-blocking institutional memory.

## Acceptance evidence

PR #99 final head:
`4484e259e041aca39d6a51de5928bf9a3e00a5b7`

Passed before merge:
- Repository Merge Gate
- Cross-Domain Authority CI
- Weekly Memo Authority CI
- Novel OS CI
- Bullpen Runtime CI

Merged main:
`0c1c5cd76ae8dd188526f698ac1a59b28e2aa4b0`

Post-merge:
- Cross-Domain Authority CI — PASS
- Weekly Memo Authority CI — PASS
- Novel OS CI — PASS
- Bullpen Runtime CI — PASS

## Librarian operating rule

When a new current-authority layer is added:

1. preserve historical truth;
2. identify the new current resolver;
3. preserve architecture/execution/resilience routing;
4. fail closed when current authority is unavailable;
5. test clean-context retrieval;
6. test stale-input/adversarial retrieval;
7. route the test through the required merge gate;
8. update the Librarian checkpoint only after current-head evidence passes.

## Result

**LEARNED AND INSTITUTIONALIZED.**
