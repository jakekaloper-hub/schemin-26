# Commissioner Bot — Librarian Index

**Steward:** The Librarian  
**Lifecycle:** proposal → prototype → operational → postseason archive

## Reading order
1. `README.md` — mission, authority, phases and invariants.
2. `ARCHITECTURE.md` — boundaries, memory partitions and event contract.
3. `PRIVACY_AND_CONSENT.md` — collection boundaries and participant rights.

## Classification
| Knowledge | Authority | Partition |
|---|---|---|
| ESPN roster/scoring/standings | Data Gateway / Scout | verified_league |
| League rules | canonical Schemin docs | verified_league |
| Group dialogue | source message event | shared_league |
| Direct messages | sender-specific source | owner_private |
| AI storyline extraction | Conversation Intelligence | derived_storyline |
| Character identity | Master Character Canon | existing canon |

## Librarian rules
- Never replace source messages with summaries.
- Preserve provenance from derived memory to source event IDs.
- Prefer append-only corrections over destructive historical rewrites.
- Team-renaming continuity follows existing Schemin canon.
- Mark superseded architecture rather than silently deleting institutional history.
- Production-ready additions must be registered in the repository catalog/inventory/session context.
