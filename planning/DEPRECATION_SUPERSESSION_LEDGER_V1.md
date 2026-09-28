# Schemin '26 — Deprecation / Supersession Ledger

**Document class:** review / control support  
**Authority / owner:** Librarian  
**Version:** 0.1  
**Status:** ACTIVE — CHARACTER CANON TRANCHE  
**Effective date:** 2026-09-28

| Path | Domain | Previous role | Current classification | Replacement / current authority | Action | Reason |
|---|---|---|---|---|---|---|
| `canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md` | Character canon | mixed canonical titles/descriptors | CANONICAL_CURRENT | visual lock + normalized master canon | updated | retired descriptors were presented as competing titles |
| `canon/CHARACTER_REFERENCE_LAYER_V1.md` | Character packets | active reference candidate | ACTIVE_SUPPORTING | visual lock + exact title map | updated | mixed Slob/Wilson title strings could seed drift |
| `living-novel/os/adapters/flaim/PRO_SCHEMIN_IDENTITY_RESOLUTION_V1.json` | Machine identity | canonical-character registry | CANONICAL_CURRENT | exact 12-title map | updated | machine-readable contamination is high risk |
| `living-novel/os/adapters/flaim/registries/PRO_SCHEMIN_IDENTITY_RESOLUTION_V1.json` | Machine identity | duplicate runtime registry | ACTIVE_SUPPORTING | exact 12-title map | updated | aligned duplicate registry; future duplicate-removal review still needed |
| `memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_3_CHARACTER_REFERENCE_ENFORCEMENT_PATCH.md` | Memo OS | character enforcement | ACTIVE_SUPPORTING | visual lock + normalized titles | updated | active production path contained mixed titles |
| `memo-os/week-3/WEEK_3_CHARACTER_PACKET_REGISTER_V1.md` | Week 3 | current character packets | ACTIVE_SUPPORTING | visual lock + normalized titles | updated | current production must not inherit retired labels |
| `living-novel/characters/03_JORDAN_HOLLINGSHEAD.md` | Living Novel | active dossier | ACTIVE_SUPPORTING | **Win Ugly** | updated | retired descriptor was used as dossier title |
| `living-novel/characters/12_BEN_WHIPPLE.md` | Living Novel | active dossier | ACTIVE_SUPPORTING | **The People's Champ** | updated | retired descriptor was used as competing title |
| `living-novel/qa/STEP_4_CHARACTER_BIBLE_GATE.md` | Novel QA | closed gate | ACTIVE_SUPPORTING | revalidated exact titles | updated | prior PASS encoded obsolete labels |
| `living-novel/history/OWNER_LINEAGE.md` | History/control | current owner map | ACTIVE_SUPPORTING | normalized exact titles | updated | history index should not present retired labels as current |
| `living-novel/narrative/STATE_OF_THE_REALM_2026_OPENING.md` | Narrative canon | opening state | ACTIVE_SUPPORTING | normalized exact titles | updated | current opening canon should not seed old identity labels |
| `chronicles/production/reference-packets/characters/CHAR-SLOB/PACKET.md` | Chronicle packet | render packet | ACTIVE_SUPPORTING | Win Ugly | updated | render packet is high-risk prompt input |
| `chronicles/production/reference-packets/characters/CHAR-CHINS/PACKET.md` | Chronicle packet | render packet | ACTIVE_SUPPORTING | The People's Champ | updated | render packet is high-risk prompt input |
| `chronicles/production/CHARACTER_VISUAL_AUTHORITY_LOCK_2026-09-26.md` | Chronicle authority | older session plate pointer | SUPERSEDED_REFERENCE | `canon/SCHEMIN_26_MASTER_VISUAL_CANON_REFERENCE_LOCK_V1.md` | updated with supersession pointer | old conversation asset ID must not outrank newer Commissioner plate |
| `world/canon/SCHEMIN_26_MASTER_CHARACTER_CANON_V1_1.md` | historical/world canon | older master copy | UNRESOLVED / HIGH-RISK DUPLICATE | current canon | pending classification | duplicate-looking canon contains retired titles and can contaminate retrieval |
| `world/history/2025/2025_OWNER_TEAM_ALIAS_MAP.md` | historical evidence | 2025 mapping | ARCHIVE/HISTORY CANDIDATE | current owner/title map for 2026 | pending isolation | old labels may be legitimate history but must not appear current |
| `chronicles/proof-of-concept/prologue/*` matching retired titles | proof of concept | earlier production evidence | ARCHIVE/HISTORY CANDIDATE | current visual lock | pending classification | preserve provenance only if clearly historical/non-production |
| `XCODE_CHATGPT_HANDOFF.md` | handoff | legacy operational handoff | UNRESOLVED | standing operating contract / current controls | pending audit | highly retrievable legacy handoff may contain stale character/system rules |

## Canonical title rulings

- Jordan Hollingshead: **Win Ugly** is active. `Frat-Bro Berserker` is retired descriptor/history only.
- Wilson Look: **The Philosopher-Warrior** is active. `Arsenal Centaur` is a mandatory body-form descriptor, not a competing title.
- Ben Whipple: **The People's Champ** is active. `Blue-Collar Spoiler` is retired descriptor/history only.
- Jake Kaloper: **The Trade Jedi**, **NO championship belt**.
- Brandon Pryor: **The Chili Outlaw**, companion **The Dark Horse**.
- Austin Byars: **The Belt Keeper** across renames.

## Next tranche

The next repository-wide tranche must classify the unresolved duplicate/history candidates before any deletion:
1. `world/canon/`
2. `world/history/`
3. proof-of-concept prologue artifacts
4. legacy handoffs/prompts
5. duplicate identity registries
6. Memo OS older version lineage
