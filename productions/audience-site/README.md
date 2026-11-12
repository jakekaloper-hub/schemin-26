# Commonwealth Audience Website V2

Read-only presentation consumer of the current Schemin Story Production Graph plus active Character, World and Publication authorities.

This directory owns **presentation only**. It cannot approve manuscripts, release memos, mutate world geography, promote canon, or authorize rendering.

## Architecture

```
Story Graph web_index.json + timeline.json
        +
current Character / World / Publication sources
        ↓
build_public_catalog.py
        ↓
dist/data.json
        ↓
static Commonwealth reader
```

The old `feat/commonwealth-audience-site-20261022` branch is a historical donor only. V2 does not inherit its branch ancestry or stale authority assumptions.

## Reproduce

Requirements: Python 3.12+ and Node 22+. No npm dependencies or model/API calls.

```bash
python3 productions/audience-site/tests/test_public_catalog.py
npm --prefix productions/audience-site test
python3 productions/audience-site/build_public_catalog.py --no-render
python3 planning/story-production-graph/build_downstream_consumers.py --check
```

The build copies the static source shell into `dist/` and writes a derived `data.json`.

## Current public behavior

- all nine 2026 memo issue records are listed with their Story Graph state;
- unavailable artifacts remain unavailable and never fall back to another week;
- the Chronicle exposes the 42 source-backed W3–W9 Events without authority promotion;
- current approved Twelve and canonical world records feed the reader/atlas;
- only `CANON_CLOSED` Living Novel manuscript editions are projected;
- progress is device-local and source-version/fingerprint specific.

## Public boundary

The catalog is allowlisted. Internal editorial fields such as location `open_questions` are not emitted. Public source links are revision-pinned. No Mercer-private analysis, credentials, editor controls or publication actions belong in this bundle.

## Accessibility

Automated static contracts cover skip navigation, focus visibility, reduced motion, keyboard map/menu behavior, mobile breakpoint and a 44px primary-target floor.

A full accessibility acceptance still requires rendered browser + assistive-technology testing.

## Hosting / release

**Current V2 state: NOT DEPLOYED.**

Merge, deployment, founder visual acceptance, rollback rehearsal and public smoke checks are separate gates. Do not infer a live website from a green build.

## Recovery evidence

See `planning/audience-site/V2_STORY_GRAPH_RECOVERY_RECEIPT.md`.
