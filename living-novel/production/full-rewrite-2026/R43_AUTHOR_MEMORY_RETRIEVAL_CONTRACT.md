# R43 — Author Memory Retrieval Contract (integration into existing infrastructure)

**Owner recommendation:** Bullpen Librarian with Beat Writer, Scout, Atlas, Character Canon, ConsultEngine and Umpire. **State: DESIGN/ADOPTION PROPOSAL.** Do not create a new OS or a competing writable canon store.

## Audited existing components
- `jakekaloper-hub/bullpen/governance/BULLPEN_MEMORY_ARCHITECTURE.md` and `knowledge/memoryStore.js`: provenance, scoped recall, freshness, supersession, key resolution and conflict detection.
- `world/history/WORLD_MEMORY_ENGINE_V1.md` + `world/data/world_memory.json`: place/event memory overlay, not rewrite of base geography.
- `living-novel/os/NOVEL_OS_PHASE_4_CONTINUITY_INTELLIGENCE_V1.md`: temporal, object, relationship, identity, knowledge and manuscript-SHA checks.
- `docs/LONG_TERM_KNOWLEDGE_VISION.md`: seven knowledge categories and anti-bloat rule.
- Existing source/character registers, historical ledger, `living-novel/whole-book/`, Atlas and memoir-to-novel translation, draft PR #188 and owner PRs.

## Critical gap
The individual components answer narrow questions. A Beat Writer preparing a scene currently has no demonstrated *single authorized read path* joining: source event → year and chronology → verified owner ID → visual time-state → location and neighbors → what this POV knows → relationship state → story object possession → manuscript scene history → outstanding promise → continuity conflict → speculative inspiration.

**Solution:** read-only **Author Context Packet**, a projection of existing data with exact file/commit anchors. Build as an adapter or query, not an independent memory engine. No write-back except through existing owning registries and approval workflow.

## Retrieval request shape
`{character_id, scene_time, evidence_cutoff, location_id?, other_character_ids?, object_ids?, intended_scene_question, view:"AUTHOR_DRAFT"|"CANON_AUDIT"}`

## Expected answer: seven panels
1. **Immutable anchors:** what ESPN actually recorded, season/week and direct source. Historical team-slot aliases without proven owner continuity remain UNKNOWN.
2. **Authoritative identity and visual time-state:** one owner principal, correct morphology, name variants, hair/Belt state and applicable reference source. Resolve present from active registry, not stale old prose.
3. **World position:** place IDs, territory, known routes, travel impossibilities and prior physical-state changes. Never invent distance or transit time.
4. **Knowledge and relationships:** what this character has directly witnessed, credible received reports, merely believes, cannot know yet; co-present and remote owner interaction edges.
5. **Material story history:** every scene already written, accepted vs draft vs rejected, passage/blob SHA, source-derived outcome, object changes and obligations.
6. **Future dramatic promises:** open conflict, stakes, secrets, intended cost, planted object and anticipated payoff; clearly PROPOSED, with no guaranteed future ESPN result.
7. **Conflicts and uncertain items:** old/canonical text discrepancy, unsupported year attribution, disputed source, superseded manuscript, stale memory, reader-knowledge spoiler hazards.

## Retrieval precedence
Project Mission and authoritative canon > certified source events > approved World State > approved manuscript scene > noncanon draft > author proposals > speculation. This is not a license to treat all high-priority records as literal fictional narration; a novel's invented interiority is never a real person's documented thoughts.

## Manuscript memory: precise statuses
`SOURCE_EVENT`, `CANON_SCENE`, `NONCANON_DRAFT`, `PROPOSED_BEAT`, `REJECTED_IDEA`, `SUPERSEDED`, `UNKNOWN`.

Each memory card must supply minimum: `memory_id`, `scope`, `type`, `source_repo`, `source_path`, `source_ref_or_sha`, `observed_at`, `story_time`, `owner`, `confidence`, `status`, `supersedes`, `temporal_knowledge_boundary`. Optional: `characters[]`, `location_ids[]`, `object_ids[]`, `episode_id`, `consequence_links[]`, `open_loops[]`.

## Scene lifecycle
`READ AUTHORITY → FREEZE EVIDENCE/KNOWLEDGE → REQUEST AUTHOR PACKET → DRAFT SCENE → CHECK CONTINUITY → CONSULT METHOD LENS → RECORD REVISIONS → CANON PROPOSAL → INDEPENDENT UMPiRE/FOUNDER GATE → UPDATE AUTHOR CONTEXT`.

Explicitly maintain two navigations:
- **Retrospective:** “What happened, what did each witness know, which version was accepted, what is source-verified?”
- **Prospective:** “Which loose ends, objects, debts, relationships and regional pressures could make the next scene unavoidable?”

## Three proof queries (acceptance tests, not claims they pass now)
**A. TDS W3 viewpoint** → W2 barbershop as prior event, one three-headed serpent shorn after W2; 2023→2025 recovery as separate historical evidence and attribution check; known W3 Obi loss; no earlier memories of future W4/W5 results.
**B. Wilson immediately after W4** → one integrated Arsenal gorilla-centaur (four iron-shod equine hooves), W3 hill, W4 first loss, Byars keeps Belt, W5 second loss MUST be excluded from Wilson's prior knowledge; compare owner PR #128 and subsequent noncanon candidate.
**C. Red 2022 versus Red 2026** → 2022 13–1/third verified; any fictional experience or current 2026 visual morphology backdated only if historical owner and character state are grounded; 2026 returned parcel and wagers must not appear as 2022 events.

## Concrete implementation plan (no new architecture)
- Librarian inventories existing retrieval actions and whether authenticated ChatGPT/Codex path actually reaches memoryStore and repo read authorities.
- Architect writes a **read-only join/adapter** within the existing Novel OS or Bullpen memory client, keyed on canonical character IDs, source year, location and artifact SHA.
- Scout populates historical event joins with existing 2015–2025 sources and current certified 2026 snapshots; where absent, surface UNKNOWN.
- Beat Writer adds **memory questions** and proposed story leads to character brief without marking proposals as factual.
- QA executes A/B/C tests with fixture-based exact-source citations, rejected stale references and no temporal leakage.
- The Closer publishes one acceptance receipt naming real executed API reads, retrieved bytes and failing cases. Do not self-certify human/editorial acceptance.
- Never commit credentials or unverified memories; no external paid database necessary under zero-incremental-budget controls.

## Release posture
**FOUNDATION FOUND; INTEGRATION GAP OPEN.** No claim that Author Context Packet has been implemented. Keep the existing World Memory Engine, Bullpen memory architecture, Novel OS and Librarian as sole authorities for their domains. Reconcile stale Wilson 'no-centaur' register phrasing and superseded Edrin POV allowances through owning canonical processes rather than silently editing manuscripts.
