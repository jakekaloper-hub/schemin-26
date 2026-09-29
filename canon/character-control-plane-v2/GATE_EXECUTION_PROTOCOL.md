# BULLPEN v2 GATE EXECUTION PROTOCOL
Status: BINDING

Every R0–R15 gate is a state machine. No step may be implied.

1. PLAN — inputs, authority, dependencies, acceptance criteria.
2. BUILD — smallest production artifact that can satisfy criteria.
3. AUDIT — independent desk inspects build against authority and external architecture principles.
4. TEST — executable where technically possible; otherwise gate cannot receive final technical approval.
5. BUG_ID — every material defect gets stable BUG-Rx-NNN identifier and severity P0/P1/P2/P3.
6. BUGFIX — change must identify which bug it addresses.
7. RETEST — original failing test plus relevant regression set.
8. PREAPPROVAL — domain owner confirms evidence is sufficient for polish, not release.
9. POLISH — simplify APIs/docs, remove ambiguity/duplication, improve diagnostics; no unreviewed semantic change.
10. APPROVAL — Umpire verifies evidence; Closer assigns PASS / HOLD / HUMAN_REVIEW_REQUIRED.
11. LEDGER — commit state, receipts, residual risks, next authorized gate.

Separation of duties: builder cannot self-certify release. Character Director owns identity; Narrative Director owns POV; Librarian owns provenance; Architect owns runtime; Visual Director owns render fitness; Red Team attacks; Umpire vetoes; Closer sequences. Jake alone approves genuine canon redesign/master-reference promotion.

Stop rules: P0/P1 unresolved; missing primary evidence; failed/absent required executable test; unknown identity ambiguity; illegal layer mutation; missing Jake approval for canon promotion. A HOLD is successful governance, not a reason to skip.
