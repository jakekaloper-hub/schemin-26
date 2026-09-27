# MANUSCRIPT LINEAGE MANIFEST V1
**Status:** ACTIVE / REQUIRES PROGRAMMATIC EXPANSION
## Prologue
`PROLOGUE_MANUSCRIPT_V1.md` → initial generation.
`PROLOGUE_MANUSCRIPT_V2_AUDITED.md` → audited revision.
`PROLOGUE_MANUSCRIPT_V3_REBUILD.md` → rebuild.
`PROLOGUE_MANUSCRIPT_V4_CONSULTANT_REVISION.md` → current consultant-revised literary master candidate.
## Rule
V4 is the current production parent unless a later explicit approved manuscript supersedes it. Earlier versions remain recoverable and must not be deleted.
## Required implementation fields
version_id; parent_id; path; blob_sha; status; reason; authoring role; created/observed time; canon implications; approval; child production artifacts.
## Gate
No future V5 may silently overwrite V4. It must declare V4 as parent (or document a different lineage), enumerate material changes, and pass literary/continuity/canon gates.
