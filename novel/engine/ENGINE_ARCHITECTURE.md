# Schemin' '26 Novel AI Engine — Bullpen Architecture Decision

**Status:** CANONICAL ENGINE BASELINE  
**Date:** 2026-09-26  
**Owners:** Bullpen — Architect + Librarian + Umpire + Scout + Setup Man  
**Human authority:** Jake  
**Scope:** `/novel`

## Decision

Build the Schemin' '26 Novel AI Engine as an **adapter-driven, Bookwright-inspired authoring system** inside this repository.

We do **not** replace the existing Schemin' novel bible, character canon, timeline, editorial gates, or human approval policy. External repositories are engineering references and optional adapters; Schemin' canon remains authoritative.

### Primary upstream reference
- **Bookwright** — https://github.com/jmorenobl/bookwright
- Adopt: spec-driven authoring; plain-text canonical artifacts; constitution/bible/outline/manuscript separation; deterministic continuity validation; knowledge-graph thinking; explicit unresolved/PENDING facts; provenance-first research.
- Why: this is the closest structural match to the Schemin' novel system already present in this repository.

### Secondary references
- **NovelForge** — https://github.com/sheengoa/novelforge
  - Borrow: auditor severity, plotline/deviation tracking, author-confirmed corrections, next-chapter closed loop.
- **Novel Studio AI** — https://github.com/YfengJ/novel-studio-ai
  - Borrow: character state, retrieval memory, confirmed-memory separation, graph facts.
- **Novel Agent** — https://github.com/HuangLeijiana/novel-agent
  - Borrow selectively: specialized multi-agent production roles and reader simulation. Do not blindly reproduce its 12-agent chain.
- **Long Novel Agent Kit** — https://github.com/mushroomfk/long-novel-agent-kit
  - Borrow: chapter contracts, debts/foreshadowing ledger, proposals-before-state-write, snapshots and audit trail.

## Schemin' authority order

1. Jake's explicit decisions.
2. `canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md`.
3. `novel/bible/STORY_CONSTITUTION.md`.
4. Approved files under `novel/bible/`.
5. Verified league-history/evidence ledgers.
6. Approved manuscript prose.
7. Working outlines/drafts.
8. External engine suggestions.

An external tool may identify a conflict. It may **never silently rewrite canon**.

## Engine layers

### 1. Source & evidence layer
Inputs: verified league history, matchup records, draft/trade history, approved character canon, owner-provided facts, memo artifacts.

Rule: fantasy-football reality is **story pressure**, not a literal plot transcript.

### 2. Canon graph
Represent:
- characters and aliases
- relationships
- desires/fears/secrets
- locations and factions
- chronology
- world rules
- objects/symbols
- unresolved promises/foreshadowing
- source/provenance
- temporal validity

Every fact has a status: `LOCKED`, `WORKING`, `PENDING`, `SUPERSEDED`, or `FICTIONALIZED`.

### 3. Narrative architecture
Maintain:
- series premise
- thematic argument
- macro arcs
- POV architecture
- relationship arcs
- act/sequence/chapter/scene plans
- setup/payoff ledger
- narrative debts
- future-result boundaries

The engine must never pre-author real future league outcomes.

### 4. Writers' room
Bullpen routes specialized passes:
- **Architect** — structural design and causality.
- **Librarian** — canon/context assembly and provenance.
- **Scout** — research and external craft/tool intelligence.
- **Analyst** — timeline, relationship, recurrence and pattern analysis.
- **GM / narrative strategist** — converts league events into possible dramatic pressure without literalizing them.
- **Writer** — scene prose.
- **Editor** — scene, chapter and line-level critique.
- **Umpire** — contradiction, authority and approval gate.
- **Closer** — delivery readiness.

Agents may disagree. Dissent is recorded; false consensus is prohibited.

### 5. Draft loop

`INTAKE → CONTEXT PACK → SCENE CONTRACT → 2–3 STORY OPTIONS → DRAFT → EDITORIAL PASSES → CONTINUITY AUDIT → REVISE → HUMAN GATE → CANON WRITE-BACK`

No draft writes directly into locked canon.

### 6. Quality gates
Before a chapter can become approved:
- canon contradictions: zero unresolved criticals
- chronology/location impossibilities: zero unresolved criticals
- POV/voice contract: pass
- character desire/agency: pass
- relationship-state continuity: pass
- setup/payoff ledger updated
- invented league facts clearly separated from verified history
- future league outcomes not leaked/invented
- prose approved by Jake

## Repository target

```
novel/
  engine/
    README.md
    ENGINE_ARCHITECTURE.md
    UPSTREAM_RESEARCH.md
    schemas/
      canon-fact.schema.json
      character-state.schema.json
      scene-contract.schema.json
      narrative-debt.schema.json
    state/
      canon-ledger.jsonl
      character-state.json
      narrative-debts.json
      decisions.jsonl
      proposals.jsonl
    prompts/
      architect.md
      writer.md
      editor.md
      continuity-guardian.md
      reader-simulator.md
    adapters/
      bookwright.md
    tests/
      continuity-cases.md
      future-leak-cases.md
      canon-authority-cases.md
```

Existing `novel/bible/` and `novel/editorial/` remain authoritative. The engine consumes them; it does not relocate them.

## Context-pack contract

Every drafting call should receive only the relevant subset:
1. immutable story constitution
2. POV character card + current state
3. involved-character relationship edges
4. location/world rules
5. verified chronology up to the scene's temporal boundary
6. unresolved narrative debts relevant to this scene
7. scene contract
8. voice/style constraints
9. previous-scene handoff
10. explicit forbidden inventions

This prevents dumping the entire repository into every prompt and reduces context drift.

## Schemin'-specific invariant

**League history drives pressure, consequence, symbolism and timing; it does not dictate a one-to-one fantasy-football retelling.**

A matchup can inspire conflict. A trade can alter trust. A losing streak can pressure identity. A rivalry can supply inherited history. But the novel must remain an original fantasy narrative with independent causality, geography, institutions, relationships and character choices.

## Integration strategy

Phase 1 — **Architecture lock**  
Create this decision record and preserve current canon.

Phase 2 — **Bookwright compatibility adapter**  
Map Schemin' artifacts to Bookwright concepts without making Bookwright the source of truth:
- Constitution ← `STORY_CONSTITUTION.md`
- Bible ← `novel/bible/*`
- Research/evidence ← verified league ledgers
- Outline ← Schemin' narrative architecture
- Manuscript ← working Markdown only
- Validation ← deterministic checks + Umpire

Phase 3 — **Durable state**  
Add structured canon facts, character state, narrative debts, decisions and proposals.

Phase 4 — **Writers' room runtime**  
Bullpen assembles context packs and runs planning/drafting/review roles.

Phase 5 — **Stress tests**  
Test identity drift, renamed teams, contradictory dates, future-result leakage, impossible travel/state, relationship asymmetry, abandoned setups, and unauthorized canon writes.

Phase 6 — **Author workbench**  
Only after the engine passes tests, consider a local UI. The UI is not the engine.

## Non-goals

- Fully autonomous novel publication.
- Letting an LLM decide permanent canon without Jake.
- Copying another author's distinctive prose.
- Turning weekly fantasy results directly into chapters.
- Forking several overlapping novel frameworks into an unmaintainable stack.

## Bullpen verdict

**Adopt Bookwright's architecture pattern; do not surrender Schemin' canon to Bookwright.**

The highest-value system is a Schemin'-native story engine with:
- Bookwright-style spec-driven truth,
- NovelForge-style auditing,
- Novel Studio-style durable character memory,
- Long Novel Agent Kit-style contracts/debts/proposals,
- Bullpen governance,
- Jake as final authorial authority.
