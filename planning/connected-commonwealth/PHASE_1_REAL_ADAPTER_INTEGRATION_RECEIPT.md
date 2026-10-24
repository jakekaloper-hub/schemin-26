# Mission #175 — Existing Location Control Plane Adapter Integration

**Status:** IMPLEMENTED / LOCAL TESTED / CI CONFIGURED BUT NOT RUN ON GITHUB.
**Review authority:** simulated Director/Umpire lenses only; no authenticated consultation or independent acceptance.

## Existing entrypoints identified and changed
- `world/location-control-plane/adapters/memo_adapter.py::compile_memo_location_packet`
- `world/location-control-plane/adapters/novel_adapter.py::compile_novel_location_packet`

Both now call the read-only civilization resolver for packets already eligible for semantic QA or rendering, attach a shared interpretive `civilization_context` and `civilization_context_status=INTERPRETIVE_NON_PROMOTING`, and fail closed with `CIVILIZATION_CONTEXT_UNRESOLVED` if the context fails. They do not elevate readiness or bypass existing character/venue gates.

## Evidence
- `world/qa/test_civilization_location_adapters.py` — 4/4 PASS: direct existing adapter calls, three Basin anchors, unknown locations, injected broken context.
- `python -m unittest discover -s world/qa -p 'test_civilization*.py' -q` — 25/25 PASS.
- `python world/qa/test_central_basin_pilot.py` — 5/5 PASS.
- Universe V1.2 and One World Model suites PASS.
- Existing Location Control Plane suite run locally after changes; PASS.
- Existing `.github/workflows/world-engine-ci.yml` updated to run new suites for future pushes/PRs; **no remote CI run yet**.

## Scope boundary
The actual Location Control Plane adapters are integrated. Full weekly Memo publication and Novel manuscript compilation still require proving that their orchestration calls these adapters on the active workflow. No published issue, chapter, new canon or imagery was produced.
