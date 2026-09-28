# Schemin '26 — Release Manifest Contract V1

**Document class:** control
**Authority / owner:** Memo OS + The Closer + Librarian
**Version:** 1.0
**Status:** ACTIVE
**Effective date:** 2026-09-28

## Rule

A file, artifact, memo, PDF, chapter, production package, or publication may not claim machine-recognized **RELEASED** status merely because its filename says FINAL/OFFICIAL or its prose describes it as complete.

A RELEASED claim must have a record in `governance/enforcement/RELEASE_REGISTRY_V1.json`.

Each release record requires:
- `artifact_path`
- `status: RELEASED`
- `source_commit`
- `released_at`
- `authority`
- `qa_gates` (non-empty)

The release registry is not retroactive proof of historical artifacts whose exact bytes are unavailable. Such artifacts remain historical publication references until exact evidence is recovered.

## Release-marker syntax

The enforcement scanner recognizes explicit release markers such as:
- `**Status:** RELEASED`
- `**Publication status:** RELEASED`
- `PUBLICATION_STATUS: RELEASED`

Draft, candidate, approved-for-composition, fact-locked, and QA-passed are not synonyms for RELEASED.
