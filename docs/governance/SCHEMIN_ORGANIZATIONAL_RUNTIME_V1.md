# Schemin '26 Organizational Runtime V1
status: PHASE_8_CONTRACT_REVIEWED
implementation_scope: routing/governance contract; does not claim all downstream adapters are already wired

## Request compilation
INTENT -> PROJECT CONTEXT -> CAPABILITY CLASSIFICATION -> AUTHORITY RESOLUTION -> EVIDENCE REQUIREMENTS -> ASSIGNMENT GRAPH -> DEPENDENCY GATES -> EXECUTION -> DOMAIN QA -> UMPIRE GATE -> RELEASE.

## Required context packets
truth_packet: source, observed_at/fetched_at, stale, confidence, provenance.
canon_packet: Character ID/owner/team aliases, active version, invariants, negatives, reference IDs/hashes.
world_packet: event class, home/away, venue, location, route, entering world state, ontology.
story_packet: narrative thesis, POV, allowed invention, dialogue/copy requirements.
visual_packet: visual thesis, composition, camera, layers, environment, text/art allocation; cannot redefine canon.
render_packet: model/provider, authenticated references, mount receipts, invariants, negative locks.
qa_packet: expected checks, independent reviewer, result, defects, disposition.

## Fail-closed gates
- missing/stale-required league truth -> FACTUAL_BLOCK.
- unresolved canon conflict -> CANON_BLOCK.
- required visual reference without authenticated mount proof -> GENERATION_BLOCKED.
- unresolved world venue/path -> WORLD_BLOCK.
- producer attempting self-certification -> GOVERNANCE_BLOCK.
- Mercer-private input on public creative path -> FIREWALL_BLOCK.

## Routing examples
"Write Week 4 matchup story" -> Scout + Librarian/World + Beat Writer; Visual Lead only if visual artifact requested.
"Generate Week 4 GOTW art" -> truth/canon/world -> Beat Writer story intent -> Visual Lead brief -> Librarian reference proof -> Pitching Coach render/generation -> Umpire QA.
"Fix image-generation reference injection" -> Pitching Coach + Setup Man + Librarian; Visual Lead consulted, not accountable.
"Change Belt Keeper appearance" -> Librarian + Beat Writer/Visual consultation -> Jake approval; generation only after canon mutation.

## Phase 8 audit
Bug ORG-0801: documentary authority can be bypassed unless packets/gates are runtime-enforced.
Fix: define machine-enforceable packet/gate contract; implementation must attach to SCK/OS routing rather than parallel orchestration.
Bug ORG-0802: PR #32 is active and must not be overwritten by organizational work.
Fix: this branch defines interfaces; character-lock runtime implementation remains PR #32 until reconciled.
Tests: routing scenarios resolve correct A/R/QA; fail-closed cases defined.
Polish: interoperates with existing five-plane SCK architecture.
Sign-off: Setup Man APPROVED runtime contract; Architect APPROVED interface boundary; Pitching Coach APPROVED render boundary; Librarian APPROVED context packets; Umpire APPROVED fail-closed rules.
