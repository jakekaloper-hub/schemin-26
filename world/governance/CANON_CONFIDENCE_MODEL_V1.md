# CANON CONFIDENCE MODEL V1

Universe OS separates **truth status** from **detail confidence**.

Allowed confidence states:
- `LOCKED` — explicit Commissioner/current control-plane authority.
- `APPROVED` — reviewed production/world standard.
- `INFERRED` — causal worldbuilding consistent with authority but not independently locked.
- `HISTORICAL` — valid evidence of a past publication/version.
- `SUPERSEDED` — intentionally retired from current production.
- `UNKNOWN` — unresolved; cannot be promoted by renderer inference.

Required fields:
`status`, `source`, `last_verified`, `review_owner`, optional `supersedes`, `superseded_by`, `notes`.

Examples:
- Wilson Gorilla Warrior — LOCKED.
- Wilson Centaur — SUPERSEDED + HISTORICAL.
- Wings = chicken wings — LOCKED.
- TDS–Chili coexistence — LOCKED.
- exact unverified village placement — INFERRED.
- generated scenery with no approval — UNKNOWN / NON-CANONICAL.

**Rule:** inferred lore cannot masquerade as locked canon.
