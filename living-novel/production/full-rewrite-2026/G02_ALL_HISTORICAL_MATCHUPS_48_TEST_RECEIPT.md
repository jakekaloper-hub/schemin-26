# G2 — 2015–2025 Historical Author Context Hydration

2026-10-18. Existing Novel OS adapter `living-novel/os/adapters/hydrated_author_memory.py` now reads the complete source-backed 2015–2025 matchup archive. For each target scene it loads prior-year and through-scene-week matchup records. Historical personal team identity remains UNKNOWN without explicit verified mapping; public archive records are not direct POV personal memories. Current 2026 World Memory access is constrained by event year and week, and historical division binding remains unknown absent seasonal source.

Added two regressions `living-novel/os/qa/test_hydrated_author_memory.py`: sourced pre-2019 history with explicit historical slot licensing is time-limited, and no historical self-attribution occurs without such license.

Actual Mac isolated checkout `/tmp/schemin-novel-gate`: `python3 -m unittest discover -s living-novel/os/qa -p 'test_*.py' -q` → **Ran 48 tests; OK**. Source implementation and tests are committed on PR #188 branch.

G2 remains PARTIAL: connector to actual persistent Bullpen memoryStore not implemented; object/promises/manuscript provenance and 2026 live matchup ingest incomplete; older 2015–2017 roster delta source unreliable; period division assignments and owner lineage outstanding. G4–G10 author-led manuscript, visuals, independent Umpire, merge and publication are NOT complete.
