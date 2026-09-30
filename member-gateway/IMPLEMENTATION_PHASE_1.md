# Member AI Gateway — Implementation Phase 1

**Status:** RUNNING  
**Branch:** `feat/member-ai-gateway-phase1`  
**Authority:** Member AI Gateway Master Execution Contract V1 + current Schemin project-control documents.

## Phase objective
Establish the smallest transport-independent service-core skeleton required to prove identity/scope/capability semantics before connecting live providers or exposing an MCP transport.

## Bullpen ownership
- Architect / Setup Man: service-core contracts.
- Warden: fail-closed authorization boundary.
- Librarian: capability/provenance semantics.
- Scout: later Truth Plane attachment; no duplicate ESPN/Flaim acquisition logic.
- Groundskeeper: later run lifecycle/idempotency.
- Umpire: independent executable certification.

## Implemented in this first commit
- durable member/client principal contract;
- authorization-aware capability registry;
- semantic, read-only capability IDs;
- common response envelope;
- explicit `NOT_WIRED` behavior instead of fabricated authoritative results;
- contract tests for scope filtering, fail-closed unknown capabilities, no Director-call API, read-only Phase 1 surface, Mercer exclusion and non-certification.

## Next checkpoint
Run the tests in an executable environment. Fix failures before adding Truth Plane or SCK adapters. Then add Jake/Pitts fixture policy, freshness propagation, idempotency and outflow tests. Do not claim TEST PASS until fresh execution evidence exists.
