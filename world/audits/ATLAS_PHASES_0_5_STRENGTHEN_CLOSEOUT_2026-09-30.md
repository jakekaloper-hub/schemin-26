# BULLPEN STRENGTHEN CLOSEOUT — ATLAS PHASES 0–5

**Local operating date:** 2026-09-30 EDT  
**UTC execution window:** 2026-10-01  
**Release vehicle:** PR #47  
**Command:** `/bullpen strengthen`  
**Board ruling:** APPROVED FOR RELEASE / FOUR P1 FINDINGS CLOSED

## Mission

Close the four P1 findings from the full-board Atlas audit without redesigning the released World Engine / Atlas architecture.

Required loop for each remediation:

IMPLEMENT → TEST → AUDIT → FIX → RETEST → APPROVE

---

## P1-01 — Phase 2 derived-card drift

### Audit finding
Phase 2 Location Cards were derived snapshots with no executable deterministic regeneration path. After Phase 3 changed reference authority, all 23 cards could drift from the central reference registry.

### Remediation
- added `world/location-control-plane/compiler/generate_cards.py`;
- compiler deterministically owns:
  - 12 Homeland Cards;
  - 23 Location Cards;
  - Homeland Card Registry;
  - Location Card Registry;
  - Parent/Sub-location Registry;
- regenerated cards at schema/compilation version 1.1;
- location reference snapshots now compile from `LOCATION_REFERENCE_REGISTRY.json`;
- CI runs `generate_cards.py --check` and fails on derived-card drift;
- Phase 5 rebuild fanout now calls `generate_cards.py --write` followed by `--check`.

### Defects found during strengthening
1. malformed newline serialization in the new compiler;
2. literal backslash-n output after first correction;
3. generated_from ordering mismatch;
4. global vs embedded sublocation `source` field mismatch.

Each defect was fixed and retested.

### Ruling
**CLOSED.**

---

## P1-02 — Phase 3 renderer-addressability overclaim

### Audit finding
The repository contained real deterministic structural SVG bytes, but there was no proof that an external image renderer had actually consumed/mounted those bytes. The phrase `renderer-addressable` therefore exceeded demonstrated capability.

### Remediation
Reference authority now distinguishes:
- `repo_byte_status = VERIFIED_REPO_PATH`;
- `renderer_injection_status = UNPROVEN`;
- `renderer_ready = false`.

Added:
- `world/environment-references/verify_repo_byte_portability.py`;
- fresh-checkout path/file/media/hash verification for all 23 structural plates;
- compiler blocker `RENDERER_INJECTION_UNPROVEN`;
- Visual + STRUCTURAL/CINEMATIC reference requests fail closed until injection is actually proven;
- project/control documentation now says **repo-addressable structural grounding**, not renderer-addressable grounding.

### Capability boundary
This closes the **release-integrity P1**: the system can no longer claim READY_FOR_RENDER on unproven reference injection.

It does **not** claim external renderer injection has been implemented. That remains a controlled future capability and is explicitly fail-closed.

### Ruling
**CLOSED AS SAFETY/CLAIM DEFECT. EXTERNAL INJECTION CAPABILITY REMAINS OPEN BY DESIGN.**

---

## P1-03 — Phase 5 schema and candidate-promotion enforcement

### Audit finding
The published evolution JSON schema existed but was not enforced by runtime. Candidate promotion planning also omitted Phase 1 lifecycle, event, technology and prerequisite rules.

### Remediation
`world_evolution.py` now:
- loads and enforces the published request schema before semantic validation;
- rejects malformed transaction IDs, unexpected top-level fields, bad types/ranges/enums, and missing required schema fields;
- enforces candidate lifecycle status;
- enforces `rejection_reason`;
- enforces candidate `event_eligibility`;
- blocks `REJECTED_TECH_DRIFT`;
- requires a verified technology unlock for `REQUIRES_TECH_UNLOCK`;
- requires declared candidate prerequisites to be resolved;
- preserves route, zone, collision and approval gates;
- preserves championship-only verification/finalist locks.

Adversarial tests now include:
- rejected modern stock-car candidate;
- held literal skyport;
- event-class mismatch;
- malformed schema envelope;
- championship before event/finalists;
- promotion without Commissioner approval.

### Ruling
**CLOSED.**

---

## P1-04 — Phase 5 rebuild fanout was descriptive only

### Audit finding
Phase 5 declared that accepted state/history evolution would rebuild Location Cards, structural references and the Interactive Atlas, but `apply_to_repo()` only wrote primary state/event/ledger files.

### Remediation
Added:
- `world/evolution/engine/rebuild_world_derivatives.py`;
- executable fanout:
  1. regenerate Phase 2 cards;
  2. verify card determinism;
  3. regenerate Phase 3 structural plates;
  4. regenerate Phase 4 Interactive Atlas;
- `CANDIDATE_EVIDENCE_LEDGER.json` for evidence persistence without candidate promotion;
- candidate evidence apply requires verified release + Umpire + Closer;
- atomic primary JSON writes;
- rollback of primary files if derivative rebuild fails;
- rebuild receipt;
- manifest corrected so Memo/Novel are explicitly pull-on-read consumers rather than nonexistent hydration caches;
- CI executes the real rebuild orchestrator and fails if deterministic derivatives differ from committed state.

### Ruling
**CLOSED.**

---

## Additional hardening completed

- Phase 2 active index reconciled with Phase 3 reference reality.
- Project Control Registry no longer says merged PR #40 is merely pending merge.
- Phase 4 invalid Python escape warning removed.
- Memo OS and Novel OS evolution handoffs explicitly use pull-on-read hydration from rebuilt Location Control Plane cards.
- Candidate promotion remains plan-only; no strengthen work promoted any CAND-* site.
- The Last Field remains championship-only and inactive.

---

## Regression evidence

Strengthened World Engine CI passes:
- compile;
- world validation;
- World Engine regressions;
- Universe V1.1;
- Location Control Plane Phase 2;
- deterministic Phase 2 card check;
- Environment Reference Phase 3;
- Phase 3 repo-byte portability;
- Interactive Atlas Phase 4;
- Weekly World Evolution Phase 5 adversarial suite;
- executable Phase 5 derivative rebuild + git diff;
- Atlas publication convergence;
- Memo OS V5.5 acceptance;
- Week 4 preproduction smoke;
- deterministic Atlas render.

Independent checks:
- World Engine QA — PASS;
- Bullpen Runtime CI — PASS;
- Schemin Project Mission CI — PASS;
- Novel OS CI is required on the final activation head because Novel handoff wording changed.

---

## Remaining non-blocking gaps

### Phase 3 external renderer injection
Still intentionally UNPROVEN and fail-closed. This is no longer a release-integrity defect because no runtime path claims it is ready.

### Phase 4 browser interaction acceptance
The Interactive Atlas has deterministic artifact tests but still lacks a real browser/DOM interaction suite (click/filter/state-toggle/editorial-query smoke). This remains a P2 test-coverage opportunity, not a P1 release blocker.

### Cinematic environment plates
0/23 human-approved cinematic environment references remain expected. Structural references are not substitutes for cinematic approvals.

---

## Umpire

**PASS.**

All four P1 audit findings have enforceable remediations and regression coverage.

## Closer

**APPROVE PR #47 FOR MERGE once the final activation-head World / Bullpen / Mission / Novel suites are green.**

## Governing conclusion

The strengthened Atlas stack now distinguishes three concepts that were previously too easy to blur:

1. **derived truth must be regenerable;**
2. **repository bytes are not automatically renderer-mounted bytes;**
3. **declared transaction fanout must execute, not merely appear in a manifest.**

The architecture is preserved. The weak contracts are hardened.
