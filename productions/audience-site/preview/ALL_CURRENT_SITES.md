# All current Atlas sites — candidate rendering coverage

This is an additive extension of the existing observer renderer, not a new World or Atlas OS.

## Runtime scope

The three existing Southern Wetlands candidates stay in `regional-assets.mjs`. `atlas-site-assets.mjs` supplies explicit, differentiated local model candidates for the other 20 current `world/data/locations.json` entries. The renderer mounts both factories and suppresses generic substitute landmarks for their exact supported IDs. No principal actors or autonomous simulation is supplied.

A model includes the source landmark names, status, and ID without promoting its authority. Local shapes, materials, relative dimensions, terrain-contact supports, and viewpoints are **CANDIDATE_NOT_APPROVED**. Terrain remains illustrative; no geometry is written back into the Atlas. Camera framing follows actual candidate bounds. Closely spaced sites are scaled locally without moving source anchors.

## Reproduce and inspect

Use the existing `preview/README.md` build instructions and pinned vendor preparation. The standard build excludes private memo images. Explicit private editions keep their hash-verified original folios. The new models do not overwrite published artwork.

```sh
npm --prefix productions/audience-site test
node --test productions/audience-site/preview/tests/*.test.mjs
python3 -m unittest discover -s productions/audience-site/preview/tests -p 'test_*.py'
node productions/audience-site/scripts/report-observer-site-coverage.mjs
```

The report is internal, derived production coverage. It distinguishes the **23 current locations** from the **48 proposal records**, including held and rejected entries. It reports missing mappings explicitly and never activates candidate locations or adds invented history. Keep the proposal report outside the public render bundle.

## Still open at each site

These modeled candidates are not final cinematic environment art. Required next work includes source-reference art review, site-specific material and landscape refinement, recorded-state reconciliation, appropriate inhabited-life production, real-device performance, and independent/Founder acceptance. Current league and regional weather inputs remain disconnected. Historical state stays as recorded by its source. No public release, merge, paid service, or canon mutation is implied by technical tests.

Foreground execution preserved the concurrent graphics-fallback history improvements from `4fea081beeed5f562a5fae26525df43455377cb8` and the earlier Wetlands shaders. Source/implementation was executed inline; no separate Director, artist, or independent Umpire attendance is claimed.
