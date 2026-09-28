# Schemin '26 — Cross-Repository Source-of-Truth Matrix

**Authority / owner:** The Librarian  
**Version:** 1.0  
**Status:** ACTIVE  
**Effective date:** 2026-09-27  
**Review trigger:** repository-boundary, platform, or major subsystem change

| Domain | Canonical repository | Canonical path / control | External/derived relationship | Primary owner | Validation |
|---|---|---|---|---|---|
| Project control | `schemin-26` | `PROJECT_CONTROL_REGISTRY.md` | none | Librarian / SCK | control-registry review |
| Source hierarchy | `schemin-26` | `docs/governance/SOURCE_OF_TRUTH.md` | none | Librarian / Data authority | governance review |
| Authority boundaries | `schemin-26` | `docs/governance/AUTHORITY_MATRIX.md` | Bullpen roles may inform, not supersede | Umpire / Librarian | governance review |
| Weekly Memo OS | `schemin-26` | `memo-os/` | FLA may supply reusable creative patterns | Weekly Memo OS | Memo acceptance gates |
| Week 3 production state | `schemin-26` | `memo-os/week-3/` | no external canonical copy | Memo OS / Closer | Fact Lock + registers |
| Character canon | `schemin-26` | `canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md` | upstream tools must consume, not redefine | Character QA | canon gate |
| League data / ESPN | `schemin-26` | `data-gateway/`, snapshots, schemas | external providers are evidence sources | Data Gateway | freshness + schema checks |
| Jack Mercer | `schemin-26` | `mercer/` | generic Bullpen can advise | Mercer | operating contract |
| Living Novel / Novel OS | `schemin-26` | `living-novel/`, `chronicles/` | external render/tool providers are replaceable dependencies | Novel OS | Novel OS CI + QA |
| Schemin-specific Bullpen evidence | `schemin-26` | `bullpen/`, `bullpen-runtime/` | reusable Bullpen OS may live upstream | Closer / Librarian | runtime CI + governance |
| Reusable FLA platform capability | `fantasy-league-artworks` upstream | upstream implementation | Schemin records requirement + upstream ref | FLA owner | upstream CI + Schemin integration evidence |
| Reusable generic Bullpen capability | `bullpen` upstream | upstream implementation | Schemin consumes via explicit boundary | Bullpen owner | upstream CI + Schemin adapter evidence |
| Published weekly artifact identity | `schemin-26` control record | Commissioner-designated artifact references | binaries may be externally stored only if explicitly registered | Commissioner / Release Auditor | publication lock |
| Repository integrity records | `schemin-26` | this file + sweep review/unresolved registers | no external canonical copy | Librarian | Closer audit |

## Rule

No Schemin '26 league fact, canon rule, weekly production state, release decision, or project-control artifact is canonical merely because a similar copy exists in FLA, Bullpen, ChatGPT conversation history, or an external tool.
