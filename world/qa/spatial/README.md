# Spatial QA

Phase 9 intentionally begins with **topology**, not fake geographic precision.

Current executable checks:
- every route endpoint resolves;
- REGIONAL routes use adjacent physical zones;
- all 12 owner domains resolve to known zones;
- known-bad fixtures are rejected.

Future geometry may use GeoJSON + Turf.js after Atlas V1 gains stable shapes. That enhancement must not force premature coordinates into canon.
