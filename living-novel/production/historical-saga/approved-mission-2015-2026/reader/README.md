# Local draft reader

Open `index.html` directly in a browser. New mission prose is embedded, so reading it needs no server, network, package installation or script execution. Preserved source archive links require GitHub access. The inventory and evidence links work within this checkout; copy the complete mission directory to preserve those links.

This is an isolated partial draft preview, not a publication or canonical reader replacement. It does not implement the twelve selectable owner pathways of the existing inkjs experiment, promote manuscript candidates, or certify browser accessibility. The existing experiment remains untouched. Legacy Prologue/Chapters I–II are indexed as preserved hard-canon sources, with their retired institutional POV risk explicit, and are not embedded as active reading text.

Rebuild and verify from this directory:

```sh
python build_reader.py
python -m unittest -v test_reader.py
```

`build_reader.py` discovers literary files named `manuscript/*/THE_*.md` in this mission. Add any differently named literary work deliberately before claiming reader coverage. Scene packets and revision records are not silently rendered as chapters. Its output manifest records each actual manuscript path and SHA-256. Markdown outside the supported heading/paragraph subset is preserved literally; source HTML is escaped.

The known Week 5 title `2026-week5/A_DOOR_WIDE_ENOUGH_NONCANON.md` is explicitly registered and tested, so it is included despite its different naming pattern. A missing explicitly registered manuscript fails assembly.

Story order is explicitly declared: `2026` (after Chapter III, before Week 4 results), `2026-week4`, `2026-week5`, then `2026-week6` (no Week 7 outcome). This is a mission-specific editorial mapping, not a claim that weeks must become chapters. Unknown lanes fail assembly until their scene-time placement is resolved; lexicographic folder sorting must not silently decide chronology. Individual scene packets remain the precise temporal authority.

The later historical binding audit supports two narrow historical lanes before 2026: `2024-title` (title aftermath, no 2025 knowledge) and `2025-reckoning` (named postseason events, no 2026 knowledge). These use event-specific fictional identity associations in preserved hard canon, not inferred ESPN account ownership. Raw human-owner fields remain UNKNOWN. Other historical lanes remain unlicensed unless separately audited; the reader does not grant season-wide permission. Historical text is counted and disclosed only when an actual literary file exists, never from a planned directory. The initial five-sequence, 2026-only tranche remains preserved in commit `321daf9`.

`2026-week6-wetland` is displayed after `2026-week6`, but occupies the same post-Week-6/pre-Week-7-result window. This display order does not prove which separate geographic event happened first. The two draft sequences retain independently proposed world-state deltas until continuity acceptance.

The source inventory records existing historical chronicle prose, R53 pilots, the manuscript tree (including superseded v3 sources), and full-rewrite manuscript/draft/reading candidates. It preserves each source hash and baseline Git blob. File counts and metadata-inclusive word counts diagnose corpus size only; assemblies may duplicate other entries, and neither count proves literary coverage or quality.

Technical tests verify frozen-source preservation, manifest hashes, actual manuscript inclusion, anchor links, explicit partial status, exclusion of legacy POV files from the active reader, and HTML escaping. They do not assert historical identity correctness, literary acceptance, complete saga coverage, or human review. No visual/browser inspection is claimed unless a later receipt supplies it.

`BROWSER_CHECK.json` records the browser attempt separately. Managed Chromium denied navigation to the local file with `net::ERR_BLOCKED_BY_ADMINISTRATOR`; no browser rendering or navigation acceptance is claimed. The attempt was not retried or routed through another scheme to bypass policy. `check_browser.py` is retained as the attempted technical smoke check, not evidence that it succeeded. Its Playwright/Chromium prerequisites are optional; the reader/build itself remains dependency-free.
