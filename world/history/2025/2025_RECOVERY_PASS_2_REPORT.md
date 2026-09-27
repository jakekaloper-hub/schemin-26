# 2025 RECOVERY PASS 2 — REPOSITORY EVIDENCE REPORT

**Status:** ACTIVE
**Date:** 2026-09-26
**Owners:** Scout + Umpire + Librarian

## New Evidence Located

Source:
`jakekaloper-hub/fantasy-league-artworks/scripts/heal-pro-schemin-week1.js`

The script identifies:
- Pro Schemin' Football League internal UUID `2489cdd4-7141-45ff-bd0c-7f46c6a0baa9`
- season 2025
- Week 1
- a 12-entry `TEAMS` array containing historical team labels and provider-facing owner handles.

### 12-team historical identity leads
1. Baker Moore Purdy — owner handle: Wilson Epworth
2. Dr. Duckhook — MasterZ69
3. El Niño — manningwelty
4. Mud Dogs — Bobbyfb4
5. ObiWan Jacoby — Hydro cF
6. Red Leopards — KevinZeek
7. Seven Deadly Chins — ESPNFAN6994197599
8. Slob on my Dobb — BigHolli58
9. The Chili Cheesers — Brandon Pryor12
10. The Immortal — abyars12
11. The LLC — David Babb
12. Three Dreaded Snake — Philpittsy

These names align strongly with the current owner/character map, but provider handles are not treated as legal/real-name authority. Librarian resolves them to known owner identities only where Character Master / approved project canon supplies the mapping.

## Umpire Quarantine — MATCHUPS Array

The same repair script contains a `MATCHUPS` array labeled "12 canonical 2025-season matchups (from DB — week 1 results)."

It MUST NOT be promoted into Recorded History.

Reasons:
- a 12-team H2H league should have six weekly pairings, not twelve;
- several teams appear more than once;
- entries include `The Blew Waffle's`, `The King`, and `Looks Don't Lose`, which are absent from the script's own 12-team TEAMS array;
- therefore the array is internally inconsistent with a single Week 1 league schedule and appears to be repair/prompt scaffolding, mixed-era data, or otherwise unsuitable as a canonical matchup export.

**Ruling:** QUARANTINED. Individual scores from this array cannot enter the historical Fact Ledger without independent verification.

## Additional Provenance Located

`scripts/backfill/proschemin-audit-report.json` preserves canonical/duplicate weekly-run IDs and operational states for 2025. This strengthens evidence that the 2025 production corpus existed week-by-week, but run-state metadata is not sporting history.

## Historical Identity Upgrade

The following 2025 team labels are upgraded from TO VERIFY to **STRONG REPOSITORY EVIDENCE / awaiting independent season-source confirmation**:
- Baker Moore Purdy
- Dr. Duckhook
- El Niño
- Mud Dogs
- ObiWan Jacoby
- Red Leopards
- Seven Deadly Chins
- Slob on my Dobb
- The Chili Cheesers
- The Immortal
- The LLC
- Three Dreaded Snake

This is enough for Librarian to begin the temporal alias registry, but not enough to lock standings/playoff history.

## Recovery Direction
Repository archaeology has now yielded:
- league UUID;
- 2025 season corpus existence;
- 17-week run evidence;
- 204-snapshot existence;
- a coherent 12-team historical identity list;
- canonical weekly-run metadata;
- schema for exact historical numerical snapshots.

What remains unavailable in committed source is the clean 204-row numerical payload.

### Next retrieval target
Use a clean season source to recover:
- six pairings per week;
- scores;
- cumulative records;
- standings;
- playoff path.

Preferred authority remains canonical ESPN historical data / validated Data Gateway or an unambiguous retained database export.

## Senior Lesson
Code comments that say "canonical" are not canon. Internal consistency and provenance outrank labels.
