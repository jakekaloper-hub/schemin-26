# SCHEMIN' '26 LIVING NOVEL — TWELVE-PRINCIPAL POV MIGRATION PROGRAM V1

**Status:** PROPOSED GOVERNING MIGRATION / FOUNDER-DIRECTED
**Founder directive:** retire Edrin/Edin as a POV character and convert the Living Novel to an exclusively Twelve-principal POV engine.
**Reader contract:** a reader may choose which of the Twelve principal character paths to follow through the shared chronology without requiring an institutional narrator.
**Applies to:** Living Novel OS, whole-book architecture, manuscript, worldbuilding interfaces, character/POV packets, Author Room workflow, QA, future chapters, visual/story continuity.

## 0. NON-NEGOTIABLE TARGET STATE

The Twelve are the only licensed POV principals.

Supporting inhabitants, archivists, officials, merchants, witnesses, couriers, crowds and institutions may exist, speak, act, carry evidence and affect causality, but they do not own narrative interiority or function as bridge narrators.

Edrin/Edin is retired from active canon as a narrative principal. No future scene may require Edrin to explain, certify, observe or connect story material.

Master Oren and other supporting world inhabitants remain support characters only unless separately reauthorized by Founder canon.

The Archive/Record House may remain an institution. Its functions must be dramatized through:
- one of the Twelve encountering records, testimony or officials;
- documents/artifacts presented inside a Twelve POV;
- public action visible to a Twelve POV;
- bounded non-interior interstitial material only if Novel OS expressly permits it and it cannot become a hidden narrator class.

## 1. PROGRAM AUTHORITY

### Executive
- **The Closer** — program chair, sequencing, conflict resolution, release gate.
- **Founder/Jake** — canon authority for the migration directive and any unresolved identity redesign.

### Internal Directors / desks
- **Narrative Director / Beat Writer / Lead Novelist** — Twelve-POV architecture and manuscript reconstruction.
- **Character Director** — Twelve principal identity/voice/knowledge profiles.
- **Librarian / Loremaster** — dependency inventory, provenance, supersession and canon transaction.
- **Architect** — Novel OS schema, routing, reader-path architecture and validation.
- **Continuity Editor** — chronology, cross-POV event consistency, duplicated-scene control.
- **World Architect** — preserves secondary-world depth after removal of institutional narrator.
- **Analyst** — causal consequence coverage and event significance.
- **Umpire** — independent regression audit and veto.
- **Red Team** — hunts narrator leakage, unsupported interiority and continuity drift.

### Author Council
This is a narrator constitution change + major canonical manuscript rewrite. Per active selection doctrine, use **Full Seven** as independent published-method lenses, then reconcile internally:
- Tolkien — secondary-world depth after narrator removal.
- Martin — ensemble causality, multi-POV architecture, path interlock.
- Rowling — reader onboarding, path legibility, setup/payoff.
- Grisham — propulsion and duplicate-event compression.
- Le Guin — POV legitimacy, distance, knowledge, culture from inside.
- Sanderson — reader-facing system legibility and rules.
- Abercrombie — tight voice differentiation, embodied consequence.

No author is a coauthor; no distinctive prose imitation. Consultants advise; Bullpen governs.

## 2. ARCHITECTURAL PRINCIPLES

1. **Twelve and only Twelve principals.**
2. **No neutral narrator substitute.** Deleting Edrin must not create an unnamed omniscient Edrin.
3. **Shared chronology, divergent experience.** The same event may appear in multiple paths only when each view adds materially different knowledge, cost, bias or consequence.
4. **Path independence.** A reader following one principal should understand that principal's arc without reading all eleven others.
5. **Path interlock.** Reading multiple principals should reveal contradictions, blind spots and larger causality, not merely duplicate scenes.
6. **No week=chapter constraint.** Chapter architecture follows story causality and character consequence, not fantasy schedule.
7. **Fictional interiority firewall.** Principal interiority is Schemin fiction, never a claim about the real owner's private thoughts.
8. **Evidence-bound knowledge.** Every POV packet owns verified knowledge, acquired-on-page knowledge, unknowns, uncertain beliefs and prohibited knowledge.
9. **World remains larger than the Twelve.** Non-POV people/institutions act independently and generate consequence; they simply do not narrate.
10. **Artifacts replace exposition where possible.** Records, receipts, broadsheets, rulings, standings, wagers and objects can convey institutional truth inside character experience.

## 3. READER-SELECTABLE POV ENGINE

### Core data model
Each scene receives:
- `scene_id`
- `story_time`
- `event_id`
- `principal_pov_id` — exactly one of Twelve
- `knowledge_before`
- `knowledge_acquired`
- `knowledge_after`
- `objective`
- `cost`
- `decision`
- `consequence_out`
- `cross_path_dependencies`
- `spoiler_boundary`
- `duplicate_event_rule`
- `world_state_in/out`

### Reader modes
The architecture must support:
- **Canonical Book Order** — editorially selected sequence across the Twelve.
- **Single-Principal Path** — follow one principal chronologically.
- **Multi-Principal Path** — select a subset of principals.
- **Event Crosscut** — optionally inspect all licensed viewpoints on one event after reaching it in chronology.

These are presentation/routing modes over one canonical event graph, not twelve separate contradictory novels.

### Scene eligibility test
A principal owns a scene only if at least one is true:
- they pay the highest new cost;
- they make a decision that changes downstream causality;
- their knowledge limitation produces meaningful uncertainty;
- their bias/voice changes interpretation;
- the scene changes their relationship/state;
- they uniquely expose an important part of the world.

Participation alone is insufficient.

## 4. SPECIAL CANON GATE — MANNING / EL NIÑO

Current world canon treats El Niño as a mobile elemental storm and historically prohibits interior POV.

The new Founder directive requires Twelve selectable principal paths.

Therefore Bullpen must resolve, before final POV Constitution V2 release, a lawful **Manning/El Niño principal-path implementation** that:
- preserves El Niño's elemental identity unless Founder canon explicitly changes it;
- does not create a thirteenth narrator;
- does not silently grant a weather system generic omniscience;
- provides a bounded, recognizable principal viewpoint/experience model;
- is reviewed by Character Director + World Architect + Le Guin lens + Umpire;
- receives explicit canon transaction before manuscript use.

Until resolved, Manning/El Niño is a named migration blocker, not an excuse to retain Edrin.

## 5. PHASED EXECUTION

### PHASE 0 — Directive Freeze + Dependency Census
**Goal:** establish exact blast radius before edits.

Actions:
- search entire repository for `Edrin`, `Edin`, `Edrin Vale`, Archive POV, institutional POV, bounded witness POV and narrator-class language;
- classify every hit: manuscript / architecture / OS / QA / consultant record / superseded historical record / visual brief / test;
- identify canonical vs historical artifacts;
- create migration ledger with action: DELETE / REASSIGN / REWRITE / RETAIN-AS-HISTORICAL-EVIDENCE / SUPERSEDE;
- freeze new Edrin-dependent prose.

Exit:
- 100% repository hit inventory;
- no unknown active dependency.

### PHASE 1 — Author Council + Internal Architecture Review
**Goal:** test the new constitution before prose rewrite.

Independent reviews:
- Full Seven author-method memos;
- Narrative Director proposal;
- Character Director Twelve-profile proposal;
- World Architect secondary-world preservation plan;
- Architect reader-routing/data model;
- Continuity Editor duplication/chronology policy.

Closer reconciliation produces:
- `TWELVE_POV_ARCHITECTURE_DECISION_V1.md`
- dissent ledger;
- accepted/rejected advice with rationale.

Exit:
- no unresolved load-bearing architecture disagreement.

### PHASE 2 — Novel OS / Constitution Rewrite
**Goal:** remove all non-Twelve POV licenses at system level.

Required changes:
- supersede `NOVEL_POV_CONSTITUTION_V1.md` with V2;
- update Master Directive ensemble doctrine;
- update Author Room hydration standard;
- update causal chapter architecture;
- update continuation contract;
- update POV templates/schema;
- add narrator leakage lint rule;
- add exact `principal_pov_id in TWELVE` validation.

Exit:
- system cannot authorize Edrin/Oren/witness/anonymous omniscient POV.

### PHASE 3 — Twelve Character/POV Packets
**Goal:** make each principal actually writable and distinct.

For each of the Twelve:
- identity + current canon state;
- physical/sensory attention;
- strategy/values in fictional world;
- knowledge map;
- blind spots;
- metaphor domains;
- humor/pressure pattern;
- sentence/voice tendencies without author imitation;
- relationship graph;
- homeland/world familiarity;
- artifact/institution interaction;
- current burdens/promises;
- forbidden real-owner inference;
- weekly delta interface.

Exit:
- 12/12 approved packets;
- no interchangeable voices;
- Manning/El Niño gate closed.

### PHASE 4 — Whole-Book Story Graph Re-architecture
**Goal:** convert existing material from narrator-spine to principal-causality graph.

Build:
- canonical chronological event graph;
- Twelve path graph;
- event-to-POV ownership matrix;
- cross-path dependency matrix;
- duplicate-event policy;
- onboarding policy;
- reveal/spoiler matrix;
- unresolved promise register.

Reassign institutional functions formerly carried by Edrin:
- evidence certification;
- historical context;
- outsider explanation;
- artifact interpretation;
- transitions;
- public consequence.

Exit:
- every necessary narrative function has a Twelve-compatible carrier/mechanism.

### PHASE 5 — Backward Manuscript Migration
**Goal:** repair all written book material, beginning at the earliest text.

Order:
1. Prologue
2. Chapter I
3. Chapter II
4. Chapter III
5. any Week 4 draft/architecture created before migration closes

For every Edrin scene:
- DELETE if nonessential;
- REASSIGN if another principal legitimately owns the consequence;
- REBUILD if the scene exists only because institutional narrator architecture required it;
- convert necessary record/exposition into artifact/action/dialogue witnessed by a principal;
- preserve causal facts and strong world objects where still valid.

Do not perform mechanical name replacement.

Exit per unit:
- zero active Edrin/Edin occurrences in current manuscript;
- no hidden narrator substitution;
- causal continuity preserved;
- POV knowledge audit PASS;
- prose read independently as a novel, not a fantasy recap.

### PHASE 6 — Reader-Path Assembly
**Goal:** prove the selectable-path concept works.

Generate:
- Canonical Book Order manifest;
- 12 principal reading manifests;
- scene routing metadata;
- cross-path encounter markers;
- event crosscut rules;
- minimal context injection for single-path readability.

Acceptance tests:
- choose any principal → valid chronological path;
- no scene leaks another principal's private interiority;
- no required Edrin-only bridge;
- single-path reader receives enough context;
- multi-path reader gains additional information rather than repetitive recap.

### PHASE 7 — Continuity, Literary + Systems QA
**Goal:** independently attack migration quality.

Required gates:
- repository text scan for active Edrin/Edin dependency;
- POV ID validation;
- knowledge leakage test;
- chronology test;
- duplicate-scene test;
- Twelve voice differentiation review;
- real-owner firewall;
- world-depth regression;
- artifact/exposition regression;
- onboarding test by outsider reader lens;
- current league truth regression;
- Character Canon regression;
- World Engine / location regression.

Umpire assigns PASS / HOLD with exact failures.

### PHASE 8 — Canon Transaction + Future Enforcement
**Goal:** make regression impossible.

On PASS:
- mark Edrin/Edin active-narrative role RETIRED;
- release POV Constitution V2;
- transact Twelve-reader engine into Novel OS;
- update project control registry;
- supersede stale architecture docs;
- retain old artifacts only as historical records with explicit SUPERSEDED headers;
- update chapter-production templates;
- add future pre-prose gate: exactly one licensed Twelve principal POV per scene;
- update Week 4+ handoff.

Final state:
`TWELVE_PRINCIPAL_POV_ENGINE = RELEASED / ACTIVE`
`EDRIN_ACTIVE_POV_DEPENDENCY = 0`
`NON_TWELVE_POV_LICENSES = 0`
`TWELVE_POV_PACKETS = 12/12 PASS`
`READER_PATH_MANIFESTS = 12/12 PASS`
`EXISTING_MANUSCRIPT_MIGRATION = PASS`

## 6. MIGRATION QA — FAILURE CONDITIONS

Automatic HOLD if any of the following remain in active canon:
- Edrin/Edin owns POV, interiority or required connective narration;
- Oren/supporting inhabitant becomes replacement POV;
- unnamed omniscient voice performs former Archive function;
- a scene lacks one principal POV;
- a principal knows facts not available under their packet;
- the same event is repeated without additional consequence/knowledge;
- one path is unintelligible without reading another;
- world depth collapses into twelve isolated teams/kingdoms;
- institutional truth becomes exposition dump;
- real-person private motives are invented as factual biography;
- Manning/El Niño path is unresolved.

## 7. FIRST KNOWN DEPENDENCY SET

Confirmed active/relevant hits already include:
- `living-novel/os/NOVEL_POV_CONSTITUTION_V1.md`
- `living-novel/os/NOVEL_CAUSAL_CHAPTER_ARCHITECTURE_V1.md`
- `living-novel/world/AUTHOR_ROOM_UNIVERSE_HYDRATION_STANDARD_V1.md`
- `living-novel/whole-book/CHARACTER_POV_TEMPORAL_STATE_MATRIX_V1.md`
- `living-novel/narrative/CHAPTER_01_ARCHITECTURE.md`
- `living-novel/narrative/CHAPTER_02_ARCHITECTURE.md`
- `living-novel/manuscript/PROLOGUE_DRAFT_V1.md`
- `living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md`
- `living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md`
- multiple historical editorial audits and Chapter III hydration/consultant artifacts.

Historical audits/consultant records should generally be retained as evidence and explicitly superseded rather than falsified retroactively.

## 8. BULLPEN COMMAND CHAIN

`/bullpen mission — migrate Living Novel to Twelve-principal selectable POV architecture; retire Edrin/Edin active POV; execute Phases 0–8 autonomously until PASS or isolate an irreducible Founder-only canon decision.`

Internal sequence:
`/bullpen investigate → /bullpen board → /bullpen consult full-seven → /bullpen architecture → /bullpen strengthen → /bullpen execute → /bullpen verify → /bullpen audit → /bullpen reconcile → /bullpen canonize → /bullpen next`

Do not return to Founder merely to shuttle questions between Directors. Route internally. Escalate only an actual canon choice with no existing authority.

## 9. DEFINITION OF DONE

This migration is complete only when the repository, Novel OS, current manuscript and future production path all agree on the same rule:

> **The Schemin' '26 Living Novel is experienced only through the Twelve principal characters. The world may contain countless other people and institutions, but none of them narrates the story. Readers may follow the canonical crosscut or choose any one of the Twelve principal paths through the same causal world.**
