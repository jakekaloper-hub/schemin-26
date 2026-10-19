# R51 — External GitHub Reuse Audit for R50 Saga Blueprint
**Date:** 2026-10-19. **Authority:** Consultant-style analysis for Bullpen; NOT an authenticated Director meeting, installed integration, or approval. **Repo:** schemin-26 / PR #188.

## Reuse first: what this repository already owns
1. **Author Memory and source provenance:** existing `living-novel/os/adapters`, 2015–2025 G01 archive, G04 11-season source packets, Character/World Memory engines, promises register, scene graph R39/R40/R41, 78+ Novel OS test coverage. Do not install a fiction canon database.
2. **Twelve selectable POV reader:** #130 owns migration; #149 owns **Ink/inkjs** prototype and progress persistence. Any third-party Ink package can only improve the existing reader. Do not build another route engine.
3. **Prose:** original Prologue–III, Chapter IV owning PR #128, R49/R50 book commission, multiple developmental manuscripts. **Substantial missing product is actual edited continuous literary prose**, not lack of orchestration tools.
4. **Atlas and visual canon:** the existing World OS location graph, owners/domains, Character Canon and image references. External image/world editors are assistants, never canon writers.
5. **Bullpen:** existing Director registry, lifecycle, knowledge/memoryStore and runtime; external agent frameworks would duplicate authority unless a narrow isolated capability proves otherwise.

## Verified GitHub opportunities (research, not installed)
| Repo | Previous project exposure | Useful capability | Integration strategy | Rank |
|---|---|---|---|---|
| [inkle/ink](https://github.com/inkle/ink) and [inkle/inky](https://github.com/inkle/inky) | **Acknowledged** via PR #149/Book Architecture | Author interactive routes, compile/playtest choices, cross-file narrative | Test sample owner pathway in existing `inkjs` project, preserve one shared canon | P0 proof |
| [y-lohse/inkjs](https://github.com/y-lohse/inkjs) | **Already prototyped** in PR #149 | Web reading, branching, save/load serialized progress | Validate compilation, 12-owner route IDs, spoiler redaction, refresh persistence; don't fork | P0 build |
| [guantoubaozi/novel-writing](https://github.com/guantoubaozi/novel-writing) | **Not found in Novel repo references; new investigation** | Six-axis chapter review, time-aware relationship and plot obligation checking, safe author/reader redaction | Borrow **test cases and review checklist only**. Compare with existing Novel OS checks; no competing state store | P1 spike |
| [CSandbatch/novelgraph](https://github.com/CSandbatch/novelgraph) | **Not found in Novel repo references; new investigation** | Series/book/run scoped graph, approval separation, source-bound continuity and supervised drafting | Evaluate concepts against existing R39/R40/Novel memory; do not migrate schema absent measured concrete gap | P1 research only |
| [quarto-dev/quarto-cli](https://github.com/quarto-dev/quarto-cli) | **Not found in Novel repo references; new investigation** | Multi-document book building and web/print-like output via Pandoc | Isolated candidate render from accepted Markdown with manuscript hashes; compare existing publisher before adoption | P1 spike |
| [jgm/pandoc](https://github.com/jgm/pandoc) | **Not found in Novel repo references; new investigation** | Markdown to EPUB/DOCX/HTML and other formats | Existing pipeline adapter only; explicit candidate watermark and bibliography/source manifests | P1 spike |

### Exclude or defer
- **LangGraph/n8n:** useful to Bullpen-wide orchestration but *not needed to write the manuscript*; adopting would duplicate already-existing lifecycle/job system. Don't block novel prose on them.
- **New novel-writing OS, new knowledge graph, or new vector DB:** overlaps authenticated Bullpen memory + Novel Continuity. Adopt test patterns rather than runtime.
- **Generated historical “owner truth” or automated lore promotion:** unacceptable. Sports source and fictional proposal classes remain separate.
- **Quarto as main narrative source editor:** unnecessary; current Markdown/Git files stay source of truth.
- **Inky/Ink full overhaul:** don't overwrite PR #149 or fork the reader; run bounded integration tests first.

## Simulated editorial engineering panel
**Closer:** prioritize prose productivity; tool integration must remove a verified blocker.
**Librarian:** novel-writing's deterministic citation, temporal, promise and spoiler tests merit inspection, but migration must not erase provenance.
**Architect:** #149 inkjs is the owner. Quarto/Pandoc should be tested as export adapters.
**Beat Writer:** a plotting/continuity tool improves revision, but it cannot produce characterization by itself; require one actual chapter improved as measurable proof.
**Visual/Atlas:** source reference bytes and period-state remain mandatory regardless of tools.
**Independent Umpire lens:** no tool is a substitute for real reader/edit review; license/version/security/CI and a failing negative test are mandatory before promotion.

## Ordered executable research gates
1. **Inkjs POC (existing PR #149):** fetch exact latest head; install existing lockfile in isolation; run its test/build; confirm twelve paths, state rehydration and one future-spoiler negative test. Fix defects only in owning branch.
2. **Chapter QA spike:** borrow test themes from `novel-writing` (six review dimensions, reader redaction, atomic write), map to existing `living-novel/os/qa`; introduce 1–3 small regression tests that fail on a genuine known manuscript defect, then fix within existing source authority. No new database.
3. **Export spike:** inspect current Schemin publisher. Compare Quarto vs Pandoc on a noncanonical 5k+ word development edition; produce EPUB/HTML only if installed/available; record measured output hashes and status. Do not claim final approved book.
4. **NovelGraph selective audit:** inspect series/book/run separation and conflict tests for a *specific* missing cross-book invariant. Reject implementation adoption if it only replicates Author Memory.
5. **Cost/maintenance:** capture pinned release/license, update cadence, dependency/security risk and backwards compatibility for anything actually installed. No paid service blocker.

## Acceptance and literary North Star
An accepted repo must accelerate at least one measurable output: more source-safe **revised continuous prose**, stronger continuity QA, tested 12-POV reader, authenticated source readbacks, correct image time-state, or independently reviewed book export. Engineering remains subordinate to the *multi-book epic*, no week-as-chapter shortcut.

**Status:** Research inventory delivered. Zero newly imported repositories, installed tools, passing external POCs, authenticated Director deliberations or canon promotions are asserted.
