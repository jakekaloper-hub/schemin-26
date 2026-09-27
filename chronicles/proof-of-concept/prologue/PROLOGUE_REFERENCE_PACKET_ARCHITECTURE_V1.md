# PROLOGUE ENVIRONMENT & OBJECT REFERENCE-PACKET ARCHITECTURE V1
**Status:** AUDITED / CANONICAL PACKET CONTRACT

## Packet rule
No production image begins from prompt prose alone. A brief resolves dependencies into versioned packets.

## Environment packet schema
`packet_id, name, authority, manuscript_anchors, establishing_description, geography_known, geography_unknown, architecture, materials, climate/weather, light, recurring_landmarks, scale_refs, allowed_variation, forbidden_inventions, approved_refs[], rejected_refs[], continuity_notes, status, version`.

Required Prologue packets:
ENV-ARCHIVE, ENV-FORTRESS, ENV-DUCKHOOK-WATER, ENV-TRADE-JEDI-MOUNTAINS, ENV-TDS-JUNGLE-ARMORY, ENV-SLOB-QUARTERS, ENV-LLC-BOARDROOM, ENV-MUD-SWAMP, ENV-CHILI-STABLE, ENV-RED-RUINS, ENV-ELNINO-FLOOD, ENV-CENTAUR-SHELTER, ENV-CHINS-ROADSIDE.

## Object packet schema
`packet_id, name, authority, physical_description, material, scale, wear/history, readable_text_allowed, narrative_meaning, associated_characters, beats, forbidden_inventions, approved_refs[], status, version`.

Required objects:
OBJ-OLD-LEDGER, OBJ-2026-CLEAN-LEDGER, OBJ-BELT, OBJ-POINT4-SLIP, OBJ-EMPTY-HOOKS, OBJ-GREEN-BLADE, OBJ-MARKER-PAPERS, OBJ-CHAIN, OBJ-BRIEFCASE-FOLDERS, OBJ-DARK-HORSE-TACK, OBJ-HAMMER-TABLE, OBJ-DRAFT-BOARD, OBJ-BRASS-CLOCK, OBJ-BLACK-EDGED-NOTICE.

## Packet states
MISSING → DRAFT → REFERENCE_RESOLVED → QA_PASS → LOCKED.
Only QA_PASS/LOCKED packets may support final production. DRAFT may support layout placeholders.

## Source priority
Founder correction > owner-approved individual reference > locked twelve-character plate > written Master Canon > manuscript/environment inference. Inference may fill ordinary non-identity detail only and must be recorded.

## Artifact text
Generated text is prohibited where exact readability matters. Typeset/compose exact artifact text after image creation or construct artifact separately.

## Ensemble rule
B040 requires 12 environment packets + board/clock objects. If recognizable principals appear, each needs its own locked character packet. Prefer environmental simultaneity over twelve-face collage.

## Directory recommendation
`chronicles/production/reference-packets/{environments,objects,characters}/<packet-id>/`
Each packet contains `PACKET.md`, `refs/`, `approved/`, `rejected/`, and provenance metadata where supported.

**Audit:** Librarian PASS · Creative Direction PASS · Architect PASS · Umpire PASS.
