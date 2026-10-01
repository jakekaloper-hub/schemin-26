# BUILD ARTIFACT — Character Reference Portability Mission

**Status:** BUILT / RELEASE GATE NOT CLOSED
**Date:** 2026-09-30

Implemented without redesigning Character Control Plane v2 and without adding renderer dependencies:

1. `canon/characters/reference_sources_v1.json`
   - exact 12-character approved source registry;
   - expected SHA-256, filename, original file ID, observed Library byte size and target repository path.

2. `canon/characters/runtime/source_byte_integrity.py`
   - fail-closed repository byte verification;
   - SHA-256 + Git blob SHA + byte-size receipt generation;
   - missing bytes => `SOURCE_BYTES_REQUIRED`;
   - corrupt/mismatched bytes => `GENERATION_BLOCKED`.

3. 12/12 `REFERENCE_MANIFEST.yaml`
   - owner-scoped explicit portability state;
   - no manifest may imply a durable asset while bytes are absent.

4. Runtime receipt hardening
   - reference mount requires approved/mounted hash equality, repository path, Git blob SHA, byte size, mount receipt and provider capability receipt;
   - eligibility binds those receipts to request, character, route and subject;
   - renderer output must echo exact reference/binding execution receipt before Character QA.

5. `renderer_capabilities_v1.json`
   - evidence-backed capability registry;
   - current available image-rendering route classified unproven for Schemin deterministic binding.

6. Render Adapter candidate reconciliation
   - Character profile consumes upstream source-integrity and mount/binding receipts;
   - Render Adapter remains NOT ACTIVE.

7. Active boundary CI and adversarial tests
   - source-byte corruption/missing cases;
   - capability-evidence cases;
   - 2/6/12 subject-binding cases;
   - known character-drift cases.

No binary reference was generated, approximated or substituted.
