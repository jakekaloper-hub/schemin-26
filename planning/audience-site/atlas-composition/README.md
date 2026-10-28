# Atlas composition guide

Reproduce from the repository root:

```sh
python planning/audience-site/atlas-composition/build_guide.py
python -m unittest discover -s planning/audience-site/atlas-composition -p 'test_guide.py'
```

`COMPOSITION_GUIDE.svg` is a 2000 × 1400 source-bound illustration planning sheet. It uses the exact website projection, retains all 23 location anchors and all 18 ordered route chains, and shows the seven existing abstract regional extents. It is deliberately not final artwork. The extents are neither surveyed boundaries nor coastline instructions.

`ANCHOR_MATRIX.json` carries each anchor's regional terrain, climate, landmarks, connected routes, ordinary activity where a visual packet exists, authoritative current state and SHA-256 source receipts. Existing canonical and interpretive statuses remain intact. No source file is changed and no geometric precision, property rights or new permanent scenery is asserted.

`ACCEPTANCE_CHECKLIST.md` requires every anchor to pass source binding, biome, landmarks, routes, desktop and phone review before painted terrain is combined with the live overlay. No automatic acceptance is awarded by this generator or its tests.

SVG groups are named for vector-editor use: `region-extents`, `route-chains`, `anchor-points`, `optional-inline-labels`, `anchor-register`, `region-register`. The optional inline labels begin hidden because the source locations are dense; the full register remains visible. Final label collision handling belongs to website composition, not this diagnostic guide.

Read `world/production/CANONICAL_WORLD_PLATE_SPATIAL_BLUEPRINT_V1.md` and its QA companion before commissioning. This guide preserves the source organization; it does not replace those authorities.
