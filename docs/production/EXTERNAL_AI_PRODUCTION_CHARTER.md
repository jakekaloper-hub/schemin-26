# SCHEMIN ’26 — External AI Production Charter

**Bullpen Board / External Creator Brief**  
**Enter the Commonwealth. Build the Film.**  
Senior-level repository-native production charter for an independent AI filmmaking team.  
**Simulated board review:** 24 October 2026

## Executive commission

Schemin ’26 is an evolving, source-governed fantasy world—not a library of disposable images. Its repository combines twelve persistent character identities, a geographically bounded Commonwealth, evolving weather and environmental state, historical competition, narrative engines, production methods, and advisory intelligence.

**The filmmaker owns the film.** The screenplay, AI production tools, creative choices, casting, budget, and editorial direction remain with the external creator. Bullpen supplies an intelligent route into what already exists. This charter does not authorize changes to the screenplay, canon, or repository.

### Simulated board review — the challenge

- **Closer:** Provide a true external-engine onboarding contract.
- **Librarian:** Teach source hierarchy and provenance, not just filenames.
- **Architect:** Distinguish executable integrations from documented methods.
- **Atlas:** A location is a physical and historical system, not a background.
- **Beat Writer:** The film must work for audiences who do not know the league.
- **Visual Direction:** Identity fidelity needs verified references.
- **Umpire:** Never label a simulated consultation or untested asset as accepted.

### What the engine should discover

**World:** Physical zones, civil institutions, owner domains, approved routes, encounters, persistent scars and repairs, regional weather, and horizon/visibility.  
**People:** Twelve owner-linked principals, other inhabitants, companion animals, cultures, and institutions.  
**Time:** Verified historical league events, evolving relationships, and era-specific world states.  
**Craft:** Narrative architecture, visual composition, production packets, quality gates, and advisory research.

**Guiding rule:** Discover the world before designing the scene. Resolve authority before claiming facts. Draw on expertise without pretending an advisor personally participated.

---

## 01 / Repository discovery — use the systems already built

### Atlas and World Engine

The active Atlas has nine views: physical, civil/institutional, division, owner-domain, roads/travel, encounter, world-state, weather, and horizon/visibility. Seven physical regions govern climate, hydrology, travel, and settlement logic. World Engine V1.1 makes the world determine the image, not the reverse. Historic and current versions of a place must be distinguished; abstract map coordinates are not distances.

**Inspect:** `world/atlas/ATLAS_V1.md`; `world/atlas/PHYSICAL_ATLAS_V1.md`; `world/SCHEMIN_WORLD_ENGINE_V1_1_RELEASE_RECEIPT.md`; referenced location, domain, weather, route and state data.

### Character authority

Owner identity survives team renames. Use current owner-specific reference manifests and visual authority, not stale composite lineup art. Notable locked distinctions include Jake as the beltless Trade Jedi, Wilson as a single gorilla-centaur, Phillip as one body with three serpent heads, and Chili with the Dark Horse. Generation remains subject to asset retrieval, reference-to-subject binding, and independent visual QA.

**Inspect:** `canon/_INDEX.md`; `canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md`; current authority and reference manifests under `canon/characters/`.

### History, Novel OS, and Memo OS

The ESPN/Flaim evidence pipeline anchors real outcomes; the Living Novel OS translates those events into dramatic pressure, continuity, and evolving history. The weekly Memo OS offers source-grounded visual storytelling and editorial production discipline. Neither historical development drafts nor visual tests become canon merely by existing.

**Inspect:** `living-novel/NOVEL_OS.md`; `living-novel/whole-book/`; historical and temporal-state controls; `memo-os/README.md`; `memo-os/cinematography/`.

### Authority discipline

At each scene, separate **VERIFIED FACT / APPROVED CANON / SOURCE-DERIVED INTERPRETATION / NEW FILM PROPOSAL / UNKNOWN**. Record source paths and versions. Do not retroject later states into earlier eras, invent historical league results, or treat an unreleased candidate as official.

---

## 02 / Bullpen and advisory intelligence — know who to call and how

### Bullpen command and Director routing

The canonical 18-Director constitution belongs to `jakekaloper-hub/bullpen`. The Schemin adapter maps natural-language intent into command lifecycle, primary Director, counterweight review, and project-local domain specialists. No new Director is created for filmmaking. An external AI must inspect the command adapter and establish whether authenticated tools are actually available before claiming to call Bullpen.

**Inspect:** `docs/architecture/BULLPEN_COMMAND_ADAPTER_V2.md`; `skills/schemin-bullpen-execution/SKILL.md`; canonical `bullpen` repository.

### Author Council — seven craft lenses

The active program routes published-method lenses associated with Tolkien (historical world depth), Martin (ensemble causality), Rowling (setup/payoff), Grisham (propulsion), Le Guin (voice and culture), Sanderson (systems and costs), and Abercrombie (human-scale action). Use targeted panels for a specific craft problem; full council only for foundational architecture. These are documented analytical lenses, not live participation or stylistic impersonation.

**Inspect:** `living-novel/consultants/author-council/_INDEX.md`; `SELECTION_MATRIX_V1.md`; `AUTHOR_COUNCIL_MASTER_MANDATE_V2.md`; `author_router.py` in the same directory.

### ConsultEngine and film-production advisory bench

Consultation protocols support evidence-frozen briefs, bounded independent critiques, reconciliation, and review. Cinematography and filmcraft materials include Frank Masi-inspired unit-stills research and documented methods from film and worldbuilding practitioners. These do not constitute endorsements or direct consultations. A complete callable roster of twelve film-production advisors was not independently verified in this review: discover its current registry and invocation contract before promising named advisors or a live connection.

**Inspect:** `living-novel/consultants/NOVEL_EXTERNAL_ADVISORY_COUNCIL_V1.md`; `living-novel/consultants/NOVEL_CONSULTATION_PROTOCOL_V1.md`; `memo-os/WEEK_3_EXTERNAL_PRODUCTION_ADVISORY_PASS_V1.md`; `memo-os/cinematography/FRANK_MASI_UNIT_STILLS_REFERENCE_V1.md`.

### Domain routing

**Story** → Beat Writer / targeted authors.  
**World and weather** → Atlas / Worldbuilding.  
**Character likeness** → Canon / Visual Direction.  
**Camera, sound, production design** → appropriate filmcraft desk.  
**History** → Scout / Librarian.  
**Tool integration** → Architect.  
**Contradictions and acceptance** → independent Umpire.  
**Synthesis** → Closer; filmmaker retains creative control.

---

## 03 / The handoff prompt — paste into the film engine

> You are the independent showrunner and AI production orchestrator for a film set in the Schemin ’26 Commonwealth. The filmmaker owns the screenplay, production stack, budget, and creative decisions. Use the connected repository as a living production knowledge base, not a prompt dump.
>
> Inspect the current project controls and follow authoritative indexes to the Atlas, World Engine, character canon and current visual references, verified league history, Novel OS, Memo OS, Bullpen command adapter, Author Council, ConsultEngine, and film-production advisory materials. Resolve release status and source provenance before trusting any artifact. Discover further relevant capabilities dynamically; do not rely on a frozen list.
>
> For the full screenplay, build a source-linked scene intelligence map covering era-valid characters, relationships, location and boundaries, routes and travel, historical and current environment, weather and world-state, institutions, prior events, reusable assets, dramatic causality, and continuity constraints. Use this depth to inspire cinematic choices without drowning the audience in lore.
>
> When specialized knowledge is needed, route to the smallest competent Bullpen domain, Author Council method lens, production advisory desk, or ConsultEngine protocol. Use authenticated runtime tools only when available; otherwise distinguish documented research and simulated advisory analysis from real invocation. Never invent participation by named filmmakers, writers, consultants, or the twelve-advisor bench.
>
> Maintain distinct labels for VERIFIED FACT, APPROVED CANON, SOURCE-DERIVED INTERPRETATION, NEW FILM PROPOSAL, and UNKNOWN. Preserve immutable competition outcomes and era-specific states. Treat visual character generation as unverified until current source assets, binding, and QA are proven. Never rewrite official canon, invent approvals, or modify the repository without separate authorization.
>
> Produce a concise repository capability map, a scene-by-scene intelligence register, optional story and cinematic opportunities, an advisory routing plan, a reusable asset and continuity approach, and a prioritized exception list. Ask only questions that materially affect the filmmaker’s intent, rights, cost, or canonical constraints. Report precisely what was inspected, executed, simulated, blocked, and not yet verified.

---

## 04 / Adaptation and acceptance — turn knowledge into cinema

### Apply to the 44-scene screenplay

The supplied cast supplement reports **44 scenes, 717 dialogue blocks, and 47 printed speaking labels**. It includes unresolved identity splits and substantial supporting-role notes. The full screenplay itself was not available in this review. Do not represent this advisory as a 44-scene script analysis.

**Story pass:** Strengthen character contradictions, costs, rivalries, and accessible drama.  
**Cinema pass:** Translate the world’s geography, environmental change, histories, and inhabitants into shots, sets, sound, movement, and asset continuity.  
**Integrity pass:** Independently check time, world-state, identity, evidence, rights, and final generated footage.

These are recommendations for the filmmaker to run, not work taken over by Bullpen.

### Example of the world-first method

For a marsh crossing, first resolve watershed, roads and ferries, nearby settlements, inhabitants and labor, earlier damage, regional weather, political permissions, and each participant’s knowledge. Only then choose action blocking, camera placement, sound, effects, and the physical stakes of the sequence. Let the established world create the cinematic tension.

### Special status: *The Survey Line*

*The Survey Line* source reconstruction is marked **NONCANON** development material. Its source controls distinguish a verified Week 5 result from proposed infrastructure and political events. The film can adapt and expand this material creatively, but should not describe proposed construction, land rights, or fictional consequences as already established canon.

### Suggested command — advisory only

```text
/bullpen mission --schemin-26 --external-film-advisory --source-grounded --atlas --world-engine --novel-os --character-canon --author-council --consultengine --production-advisors --review --no-repo-writes --no-screenplay-edits --no-false-green
```

This is an intent-level proposed command, **not proof that the canonical command parser accepts every flag**. Compile it through the active Bullpen adapter and available tool contracts before execution.

### Release boundaries

The independent filmmaker controls the final film. Rights, likeness, voices, music, trademarks, third-party references, and distribution clearance require separate review. The source project does not guarantee legal rights, production permissions, usable model licenses, or AI asset portability.

---

**Board disposition:** Advisory handoff prepared from verified repository documents. Simulated review only; no real external consultant participation, screenplay rewrite, repository mutation, or production acceptance.