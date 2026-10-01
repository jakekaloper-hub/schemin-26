# ATLAS PHASE 5 — WEEKLY WORLD EVOLUTION ENGINE

**Status:** ACTIVE PRODUCTION GATE

## Mission
Turn every released weekly memo into a governed world-state reconciliation cycle without allowing publication artwork or unverified story treatment to mutate canon automatically.

## Transaction model

RELEASE EVIDENCE
→ SCOUT EXTRACTION
→ EVOLUTION REQUEST
→ DRY-RUN PLAN
→ VALIDATION
→ UMPIRE
→ CLOSER
→ APPLY STATE/HISTORY DELTAS
→ REBUILD PHASE 2/3/4 DERIVATIVES
→ REGRESSION
→ RELEASE RECEIPT

## Mutation classes

### Class A — State/history mutation
Examples:
- damage;
- cleanup;
- contamination;
- memorialization;
- repaired-with-scar;
- route closure memory;
- recurring landmark history.

May be applied by the engine only when:
- release evidence is verified;
- source provenance exists;
- active LOC exists;
- Umpire PASS;
- Closer PASS.

### Class B — Candidate evidence
May attach evidence to a CAND-* record in a transaction plan.
Does not activate geography.

### Class C — Candidate promotion
Never occurs implicitly.
Requires:
- Phase 1 promotion prerequisites;
- Umpire PASS;
- Closer PASS;
- Commissioner approval;
- a complete proposed LOC payload;
- route/zone compatibility.

Championship-only candidates additionally require:
- event_class = CHAMPIONSHIP;
- championship_verified = true;
- finalists_verified = true.

## Phase 5 deliverables
- machine-readable request schema;
- world-evolution planner/applicator;
- immutable transaction ledger;
- dry-run output format;
- rebuild dependency manifest;
- Memo post-release handoff;
- Novel post-release handoff;
- executable adversarial regression suite;
- CI integration;
- acceptance/release receipts.

## Anti-automation laws
- a renderer cannot call APPLY;
- a Memo draft cannot call APPLY;
- a candidate appearance in art is not promotion;
- failed validation produces no mutation;
- approval fields are inputs, not inferred;
- active-world files are changed only by explicit apply mode.

## Rebuild fanout after an accepted active-state transaction
1. current_world_state.json
2. world_state_events.json
3. Location Cards
4. structural environment plates where displayed state text changes
5. Interactive Atlas
6. Novel/Memo hydration caches
7. QA suites
