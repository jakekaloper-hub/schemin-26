# T06 GATE REPORT — DETERMINISTIC RESOLVER

BUILD: `cccp_resolver.py`.
TEST MATRIX: 12 owner names + 12 current teams + canonical identities + known aliases.
Required adversarial resolutions:
- Baker Moore Purdy → CHAR-WILSON-LOOK / Arsenal Gorilla Warrior.
- Arsenal Centaur / Philosopher-Warrior → same active Wilson ID with SUPERSEDED_ALIAS warning; cannot seed retired render.
- The Immortal / That's Fantasy → CHAR-AUSTIN-BYARS / Belt Keeper.
- The LLC and The LLC. → CHAR-DAVID-BABB.
- Fart Star / Win Ugly → CHAR-JORDAN-HOLLINGSHEAD / Frat-Bro Berserker.
- unknown/ambiguous input → HUMAN_REVIEW_REQUIRED.
AUDIT: resolver returns identity/version before downstream prose; team names are aliases only.
POLISH: punctuation normalization for curly apostrophes and LLC punctuation alias.
BUGFIX: retired Wilson identity is forward-resolved rather than treated as active design.
RETEST: contract cases PASS by inspection against registry map; runtime CI execution is required again at T16.
ARCHITECT: PASS.
LEAGUE HISTORIAN: PASS.
UMPIRE: PASS WITH T16 runtime-CI dependency.
CLOSER: T06 COMPLETE / PASS. T07 AUTHORIZED.
