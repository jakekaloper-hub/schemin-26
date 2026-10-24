> **Historical candidate record (October 12–13):** Preserved for provenance, not current source or release authority. Current approved character registry, visual-reference authority and October 18 lineup prevail; older source supersession and 32-page planning claims below are not reactivated. Current release status resolves through `governance/publication-manifest/PUBLICATION_MANIFEST_V1.json`.

# Week 5 — Reader-Facing Full-Name Enforcement

**Commissioner directive (2026-10-12): No shorthand anywhere in reader-facing Week 5 Memo output.** Apply to headlines, captions, dialogue attribution, narrative, charts, scoreboard, playoff odds, tables, overlays, cover lines, image text and accessibility labels.

## Canonical names (from canon/characters/CHARACTER_REGISTRY.yaml)
| Owner (permitted first, last, or full name after clear identification) | Team name to print | Blocked short forms |
|---|---|---|
| Jake Kaloper | ObiWan Jacoby | ObiWan, Obi, OJ (as short-form team label) |
| Kevin Zeek | Red Leopards | Red (as team shorthand) |
| Jordan Hollingshead | Slob on my Dobb | Slob (as team shorthand) |
| David Babb | The LLC. | LLC as shorthand; full team brand spelling follows current registry |
| Wilson Look | D0nkey K0ng | DK, Donkey (use owner name Wilson Look, Wilson or Look as natural prose when appropriate) |
| Phillip Pitts | Three Dreaded Snake | TDS, Three Snakes |
| Brandon Pryor | Chili Cheesers | Chili (as team shorthand) |
| Manning Welty | El Niño | None; full two-word team name |
| Austin Byars | His Majesty's Blood | HMB, Majesty, His Majesty (as team shorthand) |
| Bobby Mitchell | Mud Dogs | Mud (as shorthand) |
| Zach Wilson | Dr. Duckhook | Duckhook (as team shorthand) |
| Ben Whipple | Seven Deadly Chins | Seven Chins, Chins (as team shorthand) |

**Typography and aliases:** Keep the canonical stylization **D0nkey K0ng** with zeros (a capitalized "Donkey Kong" may be a historical alias but current registry is authoritative). Owner's first name, surname, or first-and-last name can be used naturally and accurately if the person is clearly introduced. Character *titles* such as The Belt Keeper, The Trade Jedi, The Chili Outlaw, and The Dark Horse are story identities, not substitutes for formal team names in standings, score labels, publication navigation, probability tables or attribution. ESPN player acronyms, D/ST, Points For, Points Against, and statistical notation may appear as standard domain labels only when needed and clearly explained; this rule primarily prohibits shortening owner and team identities.

## Separation of private source keys from published typography
Machine-only keys such as `gotw`, `duck-dk`, `HMB`, `TDS`, `DK`, `P004`, `CHAR-*`, or Atlas `LOC-*` may continue existing **only in file paths, internal JSON keys, data joins, test fixture IDs and development metadata**. They must not leak into final visible copy or artwork lettering. Preserve existing historical source documents without rewriting them.

## Required prepublication validation
1. Check the manifest's user-visible `matchup`, `title`, `home`, `away` fields use full names; internal `key`, `slug`, `packet_path` may stay stable to avoid breaking links.
2. Check each page's final narrative, deterministic overlays, graphics, captions, numbers, alt text and cover text against the canonical name mapping. Do not replace words naively inside names, paths, historical citations, player names or text discussing older work.
3. Search and reject standalone shorthand team labels in the final text/PDF extraction including: `DK`, `TDS`, `HMB`, `LLC` (when not the full official team name), `ObiWan`, `Red`, `Slob`, `Chili`, `Duckhook`, `Chins`, `Seven Chins`; distinguish intentional narrative references to characters rather than team-name data labels.
4. Named owner-first/last-only references are valid prose after owner/team identity has been established, not an excuse to abbreviate labels.
5. The independent Umpire must verify page-level display text and assembled full-issue export. Any unauthorized shortened label is `NAME_CANON_QA_FAIL`, blocks Page Lock and Release Lock.

**Status:** Enforced as contract and manifest rule; actual PDF text-extraction and compositor enforcement **NOT YET TESTED**. No full publication green claim.
