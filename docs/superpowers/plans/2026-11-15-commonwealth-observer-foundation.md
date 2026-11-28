# Commonwealth Observer Foundation Implementation Plan

> For agentic workers: use superpowers:executing-plans inline. No subagent or autonomous Director invocation is available or claimed.

**Goal:** Turn the completed observer interview into tested presentation behavior inside the existing audience-site project.
**Architecture:** Pure browser ES modules plus a read-only source-derived catalog builder. No new OS, framework or authority files.
**Tech Stack:** Existing Node 22 built-in test runner, browser ES modules, existing Python CI suites; zero new third-party runtime dependencies.
**Spec:** docs/superpowers/specs/2026-11-15-commonwealth-observer-foundation.md

## Global constraints
Spectator only; unvisited does not mean hidden; no public release; no actual league/weather claims from synthetic fixtures; history unaffected by current weather; no edits to canonical World files or existing app.js.

## Review focus
Premature reveal, late asset failure, fake latest-result fallback, streak gaps, source/as-of drift, and editor-only location leakage all need explicit negative tests. No tested boolean is independent acceptance.

## Task 1 — Observer/Atlas state
- [x] Write observer-world.test.mjs; run and observe missing-implementation failures (15/15 RED).
- [x] Implement projectAtlas, createObserver, transitionObserver in src/observer-world.mjs.
- [x] Run 15/15 GREEN. Confirm source objects are unchanged; unsupported visitor powers fail.

## Task 2 — Weather/clock
- [x] Write observer-weather.test.mjs; run and observe 21/21 RED.
- [x] Implement resolveObserverWeather and observerClock in src/observer-weather.mjs.
- [x] Run combined 36/36 GREEN. Actual southeastern-US weather/league provider remains disconnected.

## Task 3 — Whole-Atlas source projection
- [x] Write observer-catalog.test.mjs; run and observe 6/6 RED.
- [x] Implement build-observer-catalog.mjs; combined 42/42 local GREEN.
- [ ] Execute verify-observer-sources.mjs on the full repository in CI; check all source records and hashes, retain source as-of.

## Task 4 — Verification/repository receipt
- [ ] Run full inherited audience-site and Story Graph suites on exact proposed HEAD.
- [ ] Read results, report any failures without self-certification, preserve draft review state.
- [ ] Attach verified artifacts and exact-HEAD receipt to existing #306/#309 work.

## Rulings
The user ended the interview and delegated unanswered decisions, then requested continuation. No further routine approval question is needed for this additive reversible tranche. Local workspace is an isolated patch overlay because git clone cannot resolve github.com; no local baseline claim is made. Use fresh branch atop #309, preserving #307/#309 heads. Canonical Bullpen routing is not reproduced with stubs and is not falsely counted as executed.
