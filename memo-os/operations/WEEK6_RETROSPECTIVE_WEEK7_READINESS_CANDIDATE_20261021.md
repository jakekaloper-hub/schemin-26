# Week 6 retrospective remediation — Week 7 integration candidate

**Status:** DRAFT / UNMERGED / NOT INDEPENDENTLY ACCEPTED

This work extends existing Memo OS controls; it does not create another operating system or amend the published 23-page Week 6 PDF.

## 1. Parallel character engineering exclusion

PR #223 and the separate Character Reference Pipeline Recovery mission own canonical binary asset ingestion, character resolver, renderer input attachment, subject binding, visual regression and clean-context portability. Character-bearing Memo OS acceptance remains BLOCKED until genuine verified receipts exist. Do not substitute prompt descriptions for images.

## 2. Publication manifest contract

The companion standard-library validator, `memo-os/tools/validate_publication_manifest.py`, accepts JSON with a nonempty `pages` array. Each page requires:

- `source_folio_id`: immutable source identity independent of physical position;
- `publication_position`: unique integer starting at 1 and consecutive;
- `asset_path`: root-relative path without traversal;
- `sha256`: digest of the exact local artifact bytes;
- `status`: CANDIDATE, REVIEWED, ACCEPTED, BLOCKED or SUPERSEDED.

PNG inputs must be 1024 × 1536. ACCEPTED additionally requires nonempty `editorial_receipt`, `raster_receipt`, and `independent_review_receipt`. **Presence of a receipt field alone is not evidence of independent QA**; issuer authentication and artifact binding remain follow-up integration requirements.

Usage:

```bash
python memo-os/tools/validate_publication_manifest.py path/to/manifest.json --root .
python -m unittest discover -s memo-os/tests -p test_publication_manifest.py -v
```

The validator is intentionally narrow; it does **not** assert image-copy accuracy, team-name spelling, source facts, character fidelity, or independent reviewer authenticity.

## 3. Deterministic typography — acceptance interface

Before authorizing release, the page production adapter must accept approved manuscript/version and structured factual data independently of cinematic background imagery. It must produce:
1. A text-layer source receipt bound to the page ID and copy SHA-256.
2. Controlled placement of scores, names, dialogue, headlines and statistics.
3. Exact-copy comparison (normalization rules require editorial signoff; never silently rewrite proper names or figures).
4. A 390px mobile legibility review receipt.
5. Output PNG and PDF byte/hash receipts.

No such production adapter is claimed implemented by this PR. Its absence remains P0 BLOCKED.

## 4. Story Room / cinematography pre-render contract

For every multi-folio matchup, approve before rendering: factual result/winner lock; immutable character IDs; home location; setup, escalation and payoff; camera axis, prop and weather continuity; original or approved revised copy. Retain superseded scripts. The Commissioner can override an approved story only through an explicit revision receipt.

## 5. Sports Desk evidence contract

Each sports claim records: league/season/week, transaction state, provider name, retrieval timestamp, actor/team/player IDs, exact numeric source values and editorial-cutoff timestamp. Injury reports additionally need contemporary dated NFL/team or trusted reporting, with medical privacy-aware, non-sensational wording. Bench hypotheticals require eligible lineup-slot checks before any claim that an alternate would change a matchup. Pending/unknown transactions must not appear as complete.

## 6. Atlas and physical-world preflight contract

Each illustrated scene references an existing Location Control Plane ID and authority state (established, candidate, temporary dressing). Spatial and physical review should use grounded roads, watersheds, structures, elevations and camera geography. Without executable spatial evidence, report *interpretation, not geographic certification*. Never auto-promote artwork as permanent Atlas canon.

## 7. Observability / Week 7 dry-run

Record page attempts, rejection reason, reference-mount status, copy mismatch count, score mismatch count, mobile readability decision, elapsed production gate durations and artifact hashes. Run dry-runs on:
- a narrative page (BLOCKED if native character references are not verified);
- a text-heavy factual page;
- a source-folio-to-publication-position assembly (manifest validator executable).

Regression anchor: the frozen, submitted 23-page Week 6 Memo. Keep original PDF and 21/22 earlier assembly candidates distinct, with immutable source receipts. No edits to the published file are authorized.

## 8. Remaining gates

- Confirm branch CI executing committed exact test files;
- integrate into existing Memo OS CI/release workflow without duplicating authority;
- implement true deterministic text layer and text extraction comparisons;
- implement authenticated independent QA receipts;
- verify factual source joins, temporal cutoffs and approved rendering adapters;
- demonstrate Week 7 multi-folio production dry-run;
- independent Umpire review and merge only when all release-critical gates pass.

**NO FALSE GREEN:** Local validator tests are not full production readiness.
