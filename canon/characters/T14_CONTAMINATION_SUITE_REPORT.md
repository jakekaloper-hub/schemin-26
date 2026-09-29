# T14 — MULTI-CHARACTER CONTAMINATION SUITE

Required pair attacks:
1. Jake receives Austin belt → REGENERATE.
2. Brandon's Dark Horse assigned to Wilson → REGENERATE.
3. Ben's raccoon assigned to Zach → REGENERATE.
4. Jordan's pit-bull assigned to Bobby → REGENERATE.
5. Wilson axe/tankard assigned as Pitts identity props → REGENERATE.
6. Zach duck anatomy transferred to Manning → REGENERATE.

Six-character contract: six unique Character IDs; six independent packets; duplicate ID/ambiguous alias → HUMAN_REVIEW_REQUIRED.
Twelve-character contract: exactly 12 unique immutable IDs; reference assignment remains one-to-one; scene variables shared only when environmental, never identity traits.
Reference ordering attack: shuffled image/reference order may not determine ownership; ownership derives from Character ID mapping.
Missing one reference: affected character → HUMAN_REVIEW_REQUIRED; no neighboring reference substitution.

AUDIT: compiler rejects duplicate IDs and owner-scopes packet paths; QA contract explicitly checks NO_CROSS_CHARACTER_CONTAMINATION.
RED TEAM: PASS semantic contamination contract.
VISUAL DIRECTOR: PASS at pre-render layer.
UMPIRE: PASS; image-level contamination testing remains mandatory T15 after G1.
CLOSER: T14 COMPLETE / PASS_WITH_G1_DEPENDENT_VISUAL_RETEST.
