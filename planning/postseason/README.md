# Championship Island — Bullpen / Inklings production entry point

**Current authority:** [Founder decisions](FOUNDER_CHAMPIONSHIP_ISLAND_DECISIONS_2026-11-18.md) govern the creative direction. The 2015–2025 actual league results are immutable. All island physical designs, arena assignments, causeway edges, camps, historical story scenes and memorial-site arrangements remain **unpromoted editorial proposals**.

## What is installed in this branch

- Eleven historical seasons; 56 verified championship-bracket fixtures and 67 annual playoff entries.
- A fixed-round arena model: three quarterfinal sites in the modern seven-team format, two semifinal sites, one permanent championship site.
- The island's proposed 23-node / 41-link causeway and precinct network.
- A deterministic Inklings production compiler that emits **56 scenario cards / 168 multi-stage creative beats**.
- A cross-OS preproduction exporter for Memo OS, Novel OS, Atlas, Commonwealth site preview and future 2026 postseason context.
- Positive and negative validation plus [GitHub Actions](../../.github/workflows/postseason-island-validation.yml) on changes to this folder.

## One command

From the repository root:

```sh
node planning/postseason/run_postseason_island_pipeline.mjs --check
```

This **compares** the stored cards and cross-OS export to freshly compiled inputs and refuses drift. It writes nothing.

To intentionally regenerate *only* the two generated **noncanon** preview files after editing source proposals:

```sh
node planning/postseason/run_postseason_island_pipeline.mjs --refresh
```

Then re-run:

```sh
node planning/postseason/test_postseason_inklings_packets.mjs
node planning/postseason/test_postseason_cross_os_preflight.mjs
node planning/postseason/run_postseason_island_pipeline.mjs --check
```

No script edits live world files, publishes pages, deploys sites, or authorizes 2026 results.

## Precedence

1. **Real results:** ESPN/Flaim season-specific historic matchups, including the 2015–16 two-week playoff periods.
2. **Founder creative authority:** `FOUNDER_CHAMPIONSHIP_ISLAND_DECISIONS_2026-11-18.md`.
3. **History source:** `HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json`.
4. **Physical proposal:** `ISLAND_SITE_EVOLUTION_2015_2025.founder_v2.json` and `ISLAND_CAUSEWAY_TOPOLOGY.founder_v2.json`.
5. **Creative production:** `INKLINGS_2015_2025_COMPILED_PRODUCTION_CARDS.proposal.json` and `INKLINGS_ELEVEN_SEASON_ISLAND_CHRONICLE_V1.md`.
6. **Derived preview:** `POSTSEASON_CROSS_OS_PREPRODUCTION_EXPORT.founder_v2.json`.

Earlier rotating-arena files are retained as history, explicitly superseded for venue staging.

## Bullpen / Inklings operating boundary

Inklings is a Founder-authorized **project-local creative production unit**, led under Beat Writer and subject to Scout/Librarian provenance review, Atlas physical authority, Character Canon, and independent Umpire acceptance. The scripts above make the creative production **reproducible**, but do not establish that autonomous model-writing agents are independently running. Eight published-author lenses remain review methods, never claims of human participation.

## Outstanding release gates

- Atlas engineering: causeway approach, island geometry, maritime/road connections and Last Field location supersession.
- Modern broadcasting canon: locally approved conceptual direction, but global technology compatibility and actual power/distribution require world verification.
- Historic ownership and memorial chronology: no unverified owner-specific permanent camps or fabricated Michael Farrell history.
- Character visual QA, independent review and publication evidence.
- Official 2026 seven-team bracket lock after Week 14; no 2026 team can be depicted as champion before its verified result.

**Result:** An installed, testable **draft preproduction pipeline**, not a fully operational independent AI writing team, released website, or promoted island.
