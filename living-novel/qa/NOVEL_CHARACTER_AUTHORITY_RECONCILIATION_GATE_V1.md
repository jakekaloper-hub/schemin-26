# NOVEL CHARACTER AUTHORITY RECONCILIATION GATE V1

Status: HOLD RESOLVED FOR ARCHITECTURE / MANUSCRIPT RETROFIT STILL HELD
Date: 2026-09-29

## Finding
The Novel revision branch predates the current Character Canon Control Plane (CCCP). The repository default branch contains a newer owner-scoped registry and T04 character specifications that are absent from this Novel branch.

## Current authority
Novel OS must resolve current character identity from the repository's active owner-scoped CCCP before using older Living Novel copies.

Verified current examples:
- Jake Kaloper → The Trade Jedi → NO CHAMPIONSHIP BELT.
- Wilson Look → Arsenal Gorilla Warrior v2.0, effective 2026-09-29; centaur/equine state superseded for current identity.
- Phillip Pitts → The Podium Shadow → one reptilian humanoid body / THREE serpent heads; single-headed state rejected.
- Austin Byars → The Belt Keeper; team aliases do not redesign character.

## Temporal rule
Current identity authority and historical scene state are distinct.

A later Commissioner-approved redesign does not automatically rewrite what a character looked like in a scene whose Book-Time predates the redesign unless the Commissioner explicitly declares the new identity retroactive.

Therefore the POV/Pre-Book engine stores:
- CHARACTER_ID
- IDENTITY_AUTHORITY_VERSION
- EFFECTIVE_DATE
- BOOK_TIME
- HISTORICAL_SCENE_STATE
- CURRENT_RENDER_STATE

Any ambiguity between retroactive identity correction and in-world redesign must fail closed for visual production and be flagged for Commissioner resolution.

## Narrative-layer separation
1. IDENTITY CANON — CCCP.
2. EVIDENCE HISTORY — verified league facts.
3. TEMPORAL CAMPAIGN STATE — resources, record, availability, relationships, knowledge.
4. LITERARY INTERIORITY — fictional wants/beliefs/blind spots.
5. VISUAL CONTINUITY STATE — effective visual package at scene time.

No layer may silently overwrite another.

## Manuscript implication
Existing Prologue–III prose that hardcodes a superseded physical identity is revision-candidate text, not authority. The causal story may remain valid while physical description is corrected under the temporal identity rule.

GATE RESULT: PASS TO PRE-BOOK/POV BUILD. HOLD FINAL PROSE REVISION UNTIL TEMPORAL IDENTITY EFFECTIVITY IS RESOLVED.
