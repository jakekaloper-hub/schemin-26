# Memo Release Registry Spec V1 — SUPERSEDED POINTER

**Status:** SUPERSEDED / DO NOT IMPLEMENT AS A SEPARATE REGISTRY

PR #38 proposed a Memo-local release registry to prevent draft/test/replay artifacts from replacing published issues.

The requirement remains valid. The storage architecture does not.

Use:
- `governance/publication-manifest/PUBLICATION_MANIFEST_V1.json` for derived publication identity, archive and supersession relationships;
- `governance/release-evidence/registry.json` for machine release/acceptance evidence;
- the owning Weekly Memo release gate for actual publication authorization.

## Preserved invariants

- a candidate cannot silently overwrite a released issue;
- one canonical release identity is maintained per season/week unless explicit supersession occurs;
- immutable artifact identity is required for a released artifact;
- tests/replays/reconstructions remain non-canonical unless explicitly promoted;
- benchmark designation requires explicit authority;
- changing a canonical artifact requires an explicit supersession event.

## Anti-fork law

Do not create or maintain a second active Memo release registry.

This file exists only to preserve the design intent and document its migration into the canonical Publication Manifest + Release Evidence architecture.
