# Schemin '26 Organizational Design Program Charter V1
status: ACTIVE_REVIEW
branch: governance/schemin-org-design-v1
baseline_main: fe601dfc23730ca96ff16d0085d44d210358b0b0
program_sponsor: The Closer
governance_authority: The Umpire
knowledge_authority: The Librarian
operations: The Groundskeeper
principal: Jake / Commissioner

## Objective
Determine, from evidence, the smallest durable Bullpen organizational model that gives Schemin '26 deterministic authority, responsibility, independent QA, escalation, and runtime routing across league truth, canon, world, narrative, visual production, AI generation, publication and operations.

## Constitutional freeze
Until Phase 5 recommendation and Phase 10 ratification:
- Bullpen remains the canonical 18-Director project-agnostic organization.
- No project title is a Bullpen Director unless mapped to a canonical Director or explicitly ratified.
- No Visual Director, Character Director, Continuity Director, Memo OS Director, Novel Director or Visual Systems Director title acquires executive authority merely by appearing in a Schemin document.
- Existing released subsystem controls remain active unless explicitly superseded.
- Character Control Plane v2 remains RELEASE_CANDIDATE / NOT ACTIVE until its own gates close.
- Production agents may not self-certify release.
- Jake retains approval over constitutional changes and canon-changing decisions.

## Repository boundary
Universal Bullpen constitution and portable roles belong in jakekaloper-hub/bullpen.
Schemin-specific appointments, capability maps, role contracts, routing and operating rules belong in schemin-26 or a governed Bullpen Project Context Pack.

## Evidence hierarchy
Use PROJECT_CONTROL_REGISTRY.md and docs/governance/SOURCE_OF_TRUTH.md. Repository/runtime truth outranks conversation memory.

## Mandatory phase loop
Every phase executes:
BUILD -> DOUBLE_CHECK -> AUDIT -> BUG_ID -> BUG_FIX -> TEST -> POLISH -> RETEST -> DOMAIN_SIGNOFF -> LEDGER_UPDATE.
Missing evidence means HOLD, not PASS.

## Severity
P0: constitutional/source-of-truth/security/firewall violation.
P1: release-blocking authority, canon, evidence or QA defect.
P2: material ambiguity/operational weakness.
P3: polish/documentation issue.

## Phase gates
0 freeze/baseline; 1 capability inventory; 2 authority matrix; 3 failure attribution; 4 zero-base operating model; 5 gap resolution; 6 project command; 7 role contracts; 8 runtime design/integration contract; 9 adversarial acceptance; 10 ratification.

## Phase 0 audit
Double-check: Bullpen BULLPEN.md, BULLPEN_ARCHITECTURE.md, core/org/directorOrg.js; Schemin PROJECT_CONTROL_REGISTRY.md, SOURCE_OF_TRUTH.md, current open PRs and current main.
Bugs found:
- ORG-0001 P1: shadow project titles appear without normalized mapping to canonical 18-Director authority.
- ORG-0002 P2: no single Schemin organizational authority registry spans Memo, Novel, World, Character, AI and release.
Fix: constitutional freeze plus explicit project-role classification and forthcoming authority registry.
Test: no phase artifact may promote a project title to universal Director before Phase 10.
Polish: preserve existing subsystem controls rather than invent parallel governance.
Sign-off: The Closer APPROVED PROGRAM START; The Umpire APPROVED FREEZE; The Librarian APPROVED BASELINE, subject to branch review/CI.
