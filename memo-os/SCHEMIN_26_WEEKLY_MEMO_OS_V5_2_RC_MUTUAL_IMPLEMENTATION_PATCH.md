# SCHEMIN '26 --- WEEKLY MEMO OS ↔ SUBAGENT OS

## V5.2-RC COLLABORATION KERNEL --- OFFICIAL MUTUAL IMPLEMENTATION PATCH

**Version:** 5.2-RC\
**Status:** OFFICIAL / CONTROLLING CROSS-OS PATCH\
**Applies to:** Weekly Memo OS Engine Room, Schemin '26 Subagent OS,
Weekly Memo specialist agents, League Data Platform, QA, production
workflows, Research Lab, and release control\
**League:** Pro Schemin' Football League --- ESPN League ID `1417621`\
**Purpose:** Establish one agreed operating contract between the Weekly
Memo OS and Subagent OS before V5 acceptance testing.

------------------------------------------------------------------------

# 0. INSTALLATION DIRECTIVE

This patch is the synchronization contract between the two governing
systems.

The Weekly Memo OS retains authority over: - weekly memo production
architecture; - publication quality; - editorial workflow; - data
requirements; - page states; - release requirements; - acceptance
testing.

The Subagent OS retains authority over: - specialist organization; -
staffing; - agent contracts; - agent execution; - domain ownership; -
handoff behavior; - orchestration mechanics; - internal improvement
proposals.

Neither system is subordinate in every domain.

Where the two interact, this patch is controlling.

The goal is one production organization with explicit jurisdiction, not
two competing operating systems.

------------------------------------------------------------------------

# 1. MUTUALLY AGREED ARCHITECTURE

The organization now operates as five cooperating planes:

``` text
OWNER / COMMISSIONER INTENT
          ↓
CONTROL PLANE — SCK
          ↓
TRUTH PLANE — LEAGUE DATA PLATFORM
          ↓
PRODUCTION PLANE — V5 GOLD-STANDARD STUDIO
          ↓
GOVERNANCE PLANE — INDEPENDENT QA / RELEASE CONTROL
          ↓
LEARNING PLANE — REGRESSION SUITE / RESEARCH LAB / MEMORY
```

## Production Plane

**V5 Gold-Standard Studio**

Owns how verified evidence becomes a premium Pro Schemin' publication.

## Truth Plane

**V5.1 League Data Platform**

Owns acquisition, validation, freshness, lineage, snapshots, diffs,
quarantine, identity reconciliation, and Fact Lock inputs.

## Control Plane

**Schemin Collaboration Kernel (SCK)**

Owns request compilation, workflow graph, dependency state, handoffs,
acknowledgements, checkpoints, artifact versions, routing, scoped
context, and targeted recovery.

## Governance Plane

**Independent domain QA + Release Auditor**

Owns vetoes and release certification.

## Learning Plane

**Regression Suite + Research Lab + Institutional Memory**

Owns failure capture, experiments, accepted/rejected improvements,
benchmarks, and controlled OS evolution.

No plane may silently assume another plane's authority.

------------------------------------------------------------------------

# 2. GOVERNING PRECEDENCE

For Weekly Memo production:

1.  V5 Gold-Standard Studio Patch
2.  This V5.2-RC Mutual Implementation Patch for cross-OS orchestration
3.  V5.1 Data Hardening + Domain Authority Patch
4.  Gold-Standard Production Manual
5.  canonical Character Packets / approved references
6.  current verified league evidence
7.  Weekly Memo Playbook
8.  compatible V4 controls
9.  prior completed memos as benchmark/continuity references
10. generic defaults

For internal Subagent mechanics, the Subagent OS governs unless its
behavior would violate a higher Weekly Memo production, evidence, QA,
firewall, or release contract.

------------------------------------------------------------------------

# 3. REQUEST COMPILER --- ADOPTED

Every material Weekly Memo request is compiled before specialist
execution.

``` yaml
request:
  run_id:
  owner_intent:
  assignment_class:
  deliverables:
  constraints:
  source_policy:
  benchmark_policy:
  required_evidence:
  required_domains:
  staffing:
  dependencies:
  qa_gates:
  release_criteria:
  owner_decisions_required:
```

The compiled contract becomes the execution source of truth.

If two independent downstream specialists would materially disagree
about: - assignment class; - required deliverable; - permitted
sources; - benchmark restrictions; - gates; - completion definition;

the request is not ready and returns to Executive Control.

Do not solve ambiguous orchestration by allowing each agent to interpret
Jake independently.

------------------------------------------------------------------------

# 4. CENTRAL SUPERVISOR ROUTING --- ADOPTED

Executive Control / ECS is the normal routing authority.

Agents do not default to uncontrolled peer-to-peer conversation.

``` text
EXECUTIVE CONTROL
      │
      ├── DATA PLATFORM
      ├── RESEARCH / HISTORIAN / NFL INTEL / STATISTICS
      ├── NARRATIVE / EDITORIAL
      ├── CHARACTER / ART / DESIGN
      └── QA / RELEASE
```

Direct specialist-to-specialist communication is allowed only when: -
workflow permits it; - receiver is known; - artifact is versioned; -
handoff is recorded; - provenance is preserved.

Do not create a permanent new orchestration department at this stage.

SCK is initially owned by Executive Control / ECS.

A permanent orchestration specialist may be proposed only if metrics
demonstrate a recurring ECS bottleneck.

------------------------------------------------------------------------

# 5. TYPED HANDOFF ENVELOPE --- ADOPTED FOR V5.2-RC

Consequential handoffs use:

``` yaml
handoff:
  run_id:
  assignment_id:
  from:
  to:
  artifact:
  artifact_version:
  source_authority:
  source_snapshot:
  status:
  verified_facts:
  interpretations:
  assumptions:
  unavailable:
  unresolved:
  confidence:
  qa_already_performed:
  prohibited_inferences:
  dependencies:
  next_required_action:
  next_gate:
```

A receiver must not silently reconstruct missing critical context.

Malformed handoffs are rejected upstream.

------------------------------------------------------------------------

# 6. ACKNOWLEDGEMENT PROTOCOL --- RC ENFORCEMENT

Lifecycle:

``` text
ASSIGNED
→ ACKNOWLEDGED
→ RUNNING
→ HANDOFF_READY
→ RECEIVED
→ VALIDATED
```

Failure:

``` text
RECEIVED
→ HANDOFF_REJECTED
→ REASON CODE
→ RESPONSIBLE UPSTREAM NODE
→ FIX
→ RESEND
```

Initial reason codes:

-   MISSING_PROVENANCE
-   STALE_INPUT
-   INVALID_STATE
-   MISSING_DEPENDENCY
-   CONTRACT_VIOLATION
-   SOURCE_NOT_APPROVED
-   BENCHMARK_LEAKAGE
-   CHARACTER_PACKET_MISMATCH
-   UNSUPPORTED_CLAIM
-   QA_NOT_PERFORMED
-   WRONG_ARTIFACT_VERSION
-   MERCER_FIREWALL_VIOLATION

ACK is active for acceptance testing.

Permanent promotion requires successful RC evaluation.

------------------------------------------------------------------------

# 7. WORKFLOW STATE KERNEL --- ADOPTED

Workflow nodes use:

``` text
WAITING
READY
RUNNING
BLOCKED
QA_RETURNED
PASSED
SUPERSEDED
```

Rules:

-   READY requires dependencies satisfied.
-   PASSED requires designated independent gate.
-   BLOCKED identifies exact missing dependency.
-   QA_RETURNED routes to the responsible checkpoint.
-   SUPERSEDED remains traceable but cannot feed production.
-   "Done" from the producing agent is not a valid state transition.

This kernel complements, rather than replaces, V5 page and issue state
machines.

------------------------------------------------------------------------

# 8. CHECKPOINT MODEL --- ADOPTED

Required checkpoints:

``` text
CANONICAL_SNAPSHOT_LOCK
FACT_LOCK
STORY_LOCK
CHARACTER_PACKET_LOCK
ART_LOCK
COPY_LOCK
PAGE_LOCK
RELEASE_DATA_FREEZE
```

A defect returns to the nearest responsible checkpoint.

The Dependency Graph determines downstream invalidation.

Example:

``` text
late ESPN stat correction
→ canonical snapshot changes
→ affected Fact Lock fields superseded
→ affected Story Card / copy / page reopen
→ unrelated locked pages remain locked
→ affected gates rerun
```

Full-issue restart is prohibited when targeted recovery is sufficient.

------------------------------------------------------------------------

# 9. FAN-OUT / FAN-IN --- RC ENFORCEMENT

Parallel work is encouraged only where dependencies permit it.

Example:

``` text
FACT LOCK
   ├── HISTORIAN
   ├── NFL INTELLIGENCE
   └── STATISTICS
          ↓
ACKNOWLEDGED EVIDENCE FAN-IN
          ↓
STORY CARDS
```

Fan-in waits until required branches are: - PASSED; - explicitly
UNAVAILABLE; - or formally removed/reframed by the owning Director.

Silence is not completion.

------------------------------------------------------------------------

# 10. IDEMPOTENCY / DUPLICATE-WORK PROTECTION --- RC ENFORCEMENT

Expensive tasks should use deterministic work keys derived from their
material inputs.

Example:

``` text
2026_W03
+ MATCHUP_04
+ SNAPSHOT_V7
+ STORY_CARD_V2
+ CHARACTER_PACK_V5
+ PAGE_BRIEF_V3
```

If the contract and dependencies have not changed: - valid existing
artifacts may be reused; - duplicate expensive generation should not
occur.

If an upstream dependency changes: - only affected work keys are
invalidated.

Permanent promotion depends on observed reduction in duplicate work
without stale-artifact leakage.

------------------------------------------------------------------------

# 11. EVENT VOCABULARY --- RC ENFORCEMENT

Initial events:

``` text
CANONICAL_SNAPSHOT_PROMOTED
SOURCE_LOCKED
FACT_LOCKED
STAT_CORRECTION_DETECTED
STORY_CARD_APPROVED
STORY_CARD_REJECTED
CHARACTER_PACKET_UPDATED
ART_APPROVED
ART_REJECTED
COPY_LOCKED
PAGE_LOCKED
MOBILE_QA_FAILED
DEFECT_OPENED
DEFECT_RESOLVED
RELEASE_DATA_CHANGED
RELEASE_BLOCKED
RELEASE_CERTIFIED
```

Agents subscribe only to events relevant to their jurisdiction.

Events do not replace artifact state or QA evidence.

------------------------------------------------------------------------

# 12. TRACEABILITY --- ADOPTED

Required identifiers:

``` text
RUN_ID
ASSIGNMENT_ID
SNAPSHOT_VERSION
ARTIFACT_ID
ARTIFACT_VERSION
DEFECT_ID
EXPERIMENT_ID
RELEASE_ID
```

Target release lineage:

``` text
RELEASE
→ PAGE
→ COPY
→ STORY CARD
→ EVIDENCE PACKET
→ FACT LOCK
→ CANONICAL SNAPSHOT
→ RAW EVIDENCE
```

For art:

``` text
PAGE
→ APPROVED ART
→ PAGE BRIEF
→ STORY CARD
→ CHARACTER PACKET VERSION
```

For derived statistics:

``` text
VISIBLE STAT
→ DERIVED FIELD
→ FORMULA VERSION
→ VERIFIED INPUT FIELDS
→ SNAPSHOT
```

------------------------------------------------------------------------

# 13. CONTEXT FIREWALL --- ADOPTED

Each specialist receives only:

1.  governing contract;
2.  required artifacts;
3.  relevant evidence packet;
4.  relevant canon;
5.  relevant prior lessons;
6.  explicit prohibited inputs.

This is **scoped context**, not context starvation.

Continuity-critical league history must still reach the
Historian/Narrative roles.

Benchmark-only creative artifacts must remain hidden during blank-canvas
generation.

## Mercer firewall

Jack Mercer is strictly excluded from public Schemin Weekly Memo
production.

No evidence packet, Story Card, Page Brief, editorial conclusion,
ranking, trade discussion, opponent analysis, or public memo artifact
may contain Mercer-derived: - recommendations; - valuations; - private
roster reasoning; - trade strategy; - waiver strategy; - opponent
exploitation; - private conclusions.

Violation:

``` text
CRITICAL DEFECT
→ RELEASE BLOCK
→ contaminated artifacts SUPERSEDED
→ return to nearest clean checkpoint
```

------------------------------------------------------------------------

# 14. FAILURE-SPECIFIC ROUTING --- ADOPTED

``` text
TRANSIENT NETWORK FAILURE
→ bounded retry / alternate path

ENDPOINT FAILURE
→ failover / circuit breaker

PARSER FAILURE + VALID RAW JSON
→ raw normalization

SCHEMA DRIFT
→ quarantine + Schema Auditor

BAD HANDOFF
→ producing node

MISSING EVIDENCE
→ owning Data / Research domain

QA FAILURE
→ nearest responsible checkpoint

CHARACTER FAILURE
→ Character / Art

MOBILE FAILURE
→ Design / Layout

BENCHMARK LEAKAGE
→ Originality / Executive Control

OWNER-CONTROLLED POLICY EXCEPTION
→ Jake

RELEASE-CRITICAL CONFLICT
→ Executive + Standards / Release
```

No blind retry loops.

------------------------------------------------------------------------

# 15. BOUNDARY GUARDRAILS --- ADOPTED

Validate at each consequential boundary:

1.  ESPN acquisition → raw evidence
2.  raw evidence → normalized snapshot
3.  snapshot → canonical promotion
4.  canonical state → Fact Lock
5.  evidence packet → Story Card
6.  Story Card → Page/Art Brief
7.  Character Packet → generated art
8.  approved copy/art → layout
9.  layout → Page Lock
10. Page Lock → Asset Manifest
11. release refresh → dependency recheck
12. final PDF → Blind Release Audit

The objective is to catch defects near their source.

------------------------------------------------------------------------

# 16. COLLABORATION BUDGET --- ADOPTED

More agents are not automatically better.

Executive Control adds a specialist or parallel worker only when
expected information gain exceeds: - communication overhead; -
duplicate-work risk; - context complexity; - QA burden; - cycle-time
cost.

Temporary workers inherit: - Assignment Contract; - scoped context; -
handoff contract; - QA boundaries; - termination after handoff.

Do not create personas merely to appear agentic.

------------------------------------------------------------------------

# 17. DOMAIN AUTHORITY --- MUTUALLY CONFIRMED

Domain specialists have authority to block or return work when their
documented gate fails.

Examples:

-   Data Reliability may block Fact Lock.
-   Data Release Steward may refuse canonical promotion.
-   Historian may reject unsupported historical continuity.
-   Narrative may reject generic Story Cards.
-   Character Librarian may block art.
-   Art QA may force regeneration.
-   Editorial Design may reject repetitive/generic page architecture.
-   Mobile QA may force rebuild.
-   Copy/Fact QA may reopen visible facts/copy.
-   Blind Release Auditor may block release.

Routine documented failures do not require Jake's permission to correct.

Jake remains required for: - unresolved Commissioner Context; -
ambiguous canon not recoverable internally; - major creative
tradeoffs; - intentional policy exceptions; - final creative judgment
where V5 requires owner review.

------------------------------------------------------------------------

# 18. DOMAIN COUNCIL --- UPGRADED

Before Story Budget lock, domain leads challenge the issue.

Required questions:

**Data:** What evidence is weak, stale, partial, or likely to change?

**Historian:** What continuity or league history are we missing?

**Narrative:** Which stories could still be generic?

**Character:** Which canonical assets are missing or at risk?

**Art:** Which concepts are repetitive or visually weak?

**Design / Mobile:** Which planned pages may fail at phone width?

**Originality:** Where are we too close to prior work?

**Release:** What is most likely to escape into the final artifact?

**Orchestration:** Where could this issue fail because correct
information reaches the wrong agent, arrives too late, lacks provenance,
is never acknowledged, or advances before dependencies pass?

Credible risks become assignments, tests, or blocks.

------------------------------------------------------------------------

# 19. DATA PLATFORM --- MUTUALLY CONFIRMED

The Subagent OS formally adopts V5.1 League Data Platform behavior:

``` text
ACQUIRE
→ RETRY / FAILOVER
→ PRESERVE RAW
→ STRUCTURAL VALIDATION
→ NORMALIZE
→ SEMANTIC VALIDATION
→ DIFF
→ FRESHNESS CLASSIFICATION
→ QUARANTINE IF NEEDED
→ DATA RELEASE STEWARD
→ CANONICAL SNAPSHOT
→ FACT LOCK
```

Editorial/Creative agents may not independently improvise ESPN
retrieval.

A failed fetch is not equivalent to ESPN being unavailable.

Only affected domains degrade/block.

No fallback may impersonate live data.

------------------------------------------------------------------------

# 20. DATA × SCK EVENT-DRIVEN RECOVERY --- RC ENFORCEMENT

Promotion:

``` text
CANONICAL_SNAPSHOT_PROMOTED
→ dependency graph evaluates
→ eligible assignments become READY
```

Late correction:

``` text
STAT_CORRECTION_DETECTED
→ SNAPSHOT DIFF
→ dependency graph
→ affected artifacts SUPERSEDED
→ nearest clean checkpoint
→ targeted rework
→ independent re-QA
```

Acceptance target: - 100% of dependent artifacts identified in
controlled fixtures; - unrelated locked artifacts remain locked.

------------------------------------------------------------------------

# 21. REGRESSION SUITE ADDITIONS --- ADOPTED

``` text
COLLAB-001
handoff lacks provenance
→ receiver must reject

COLLAB-002
task starts before dependency PASS
→ scheduler must block

COLLAB-003
benchmark-only same-week creative material reaches blank-canvas agent
→ context firewall FAIL

COLLAB-004
unchanged expensive task is duplicated
→ idempotency FAIL

COLLAB-005
late stat correction affects one matchup
→ only dependent artifacts reopen

COLLAB-006
QA failure routes to unrelated department
→ routing FAIL

COLLAB-007
routine documented defect escalates to Jake
→ Executive interception FAIL

COLLAB-008
handoff sent but never acknowledged
→ assignment remains incomplete

COLLAB-009
SUPERSEDED artifact enters Asset Manifest / assembly
→ release FAIL

COLLAB-010
Mercer-derived private information enters public evidence packet
→ automatic critical FAIL

COLLAB-011
receiver silently fills missing handoff context
→ handoff integrity FAIL

COLLAB-012
event marks task READY while required dependency is BLOCKED
→ state-kernel FAIL
```

Failures become permanent regression cases after validation.

------------------------------------------------------------------------

# 22. RESEARCH-LAB PROMOTION PLAN --- BINDING

SCK components do not become permanent merely because they are
plausible.

## SCK-01 --- Typed Handoff + ACK

KEEP if: - first-pass handoff acceptance improves; - missing-context
defects decline; - cycle time does not materially worsen.

## SCK-02 --- Dependency States + Checkpoints

KEEP if: - QA return distance declines; - duplicate work declines; -
escaped defects do not increase.

## SCK-03 --- Scoped Context Firewall

KEEP if: - unsupported claims decline; - benchmark leakage declines; -
continuity quality does not materially decline.

## SCK-04 --- Event-Driven Rework

KEEP if: - affected-artifact detection reaches 100% on controlled
fixtures; - unrelated locked pages remain locked; - targeted re-QA time
improves.

Decision states:

``` text
KEEP
MODIFY
REVERT
INCONCLUSIVE
```

Successful experiments are versioned and promoted.

Failed experiments do not remain as permanent complexity.

------------------------------------------------------------------------

# 23. COMMUNICATION KPIs --- RC OBSERVATION

Track during acceptance testing:

``` text
handoff_acceptance_rate
first_pass_handoff_rate
handoff_rejection_rate
context_rejection_rate
duplicate_work_rate
upstream_return_rate
mean_qa_return_distance
checkpoint_recovery_rate
blocked_agent_time
fanout_completion_variance
unnecessary_escalation_rate
jake_intervention_rate
```

Do not optimize a single metric at the expense of publication quality.

Primary outcome remains: **fewer preventable defects discovered first by
Jake.**

------------------------------------------------------------------------

# 24. INTEGRATED V5.2-RC GOLDEN PATH

``` text
OWNER INTAKE
→ REQUEST COMPILER
→ ASSIGNMENT CONTRACT
→ WORKFLOW GRAPH
→ DATA PLATFORM HEALTH CHECK
→ MULTI-PATH ACQUISITION
→ CANONICAL SNAPSHOT
→ SOURCE LOCK
→ FACT LOCK
→ COMMISSIONER CONTEXT PASS
→ DOMAIN COUNCIL + ORCHESTRATION PRE-MORTEM
→ ISSUE THESIS
→ STORY BUDGET
→ PARALLEL EVIDENCE WORK
→ ACKNOWLEDGED EVIDENCE FAN-IN
→ STORY CARDS
→ ORIGINALITY CHECK #1 WHEN APPLICABLE
→ CHARACTER PACKETS
→ PAGE ARCHITECTURE
→ PAGE BRIEFS
→ PREMIUM PAGE PRODUCTION
→ JAKE VISUAL REVIEW WHERE V5 REQUIRES OWNER JUDGMENT
→ CHARACTER / FACT / STORY / ART / MOBILE QA
→ PAGE LOCK
→ REPEAT
→ UTILITY-PAGE HARMONIZATION
→ ASSET MANIFEST
→ RELEASE DATA REFRESH / FREEZE
→ SNAPSHOT DIFF
→ DEPENDENCY RECHECK
→ TARGETED REOPEN IF REQUIRED
→ ORIGINALITY CHECK #2 WHEN APPLICABLE
→ PDF ASSEMBLY
→ FULL-ARTIFACT AUDIT
→ DEFECT / CHECKPOINT RECOVERY
→ REASSEMBLE
→ BLIND RELEASE AUDIT
→ RELEASE CERTIFICATION
→ ARCHIVE
→ RETROSPECTIVE
→ METRICS
→ RESEARCH-LAB EXPERIMENTS
→ INSTITUTIONAL MEMORY UPDATE
```

------------------------------------------------------------------------

# 25. RELEASE MANIFEST --- V5.2-RC

Existing V5/V5.1 gates remain mandatory.

Add RC collaboration section:

``` yaml
collaboration_kernel:
  assignment_contract: PASS
  dependency_graph: PASS
  handoff_validation: PASS
  acknowledgement_integrity: PASS
  context_firewall: PASS
  artifact_version_integrity: PASS
  checkpoint_integrity: PASS
  supersession_check: PASS
  mercer_firewall: PASS
```

A Collaboration PASS never overrides a failed: - Data; - Story; -
Originality; - Character; - Art; - Design; - Mobile; - Copy; -
Assembly; - Release gate.

During RC testing, collaboration failures block validation of V5.2-RC.

After successful Research-Lab experiments, this section may be promoted
to permanent V5.2 doctrine.

------------------------------------------------------------------------

# 26. WEEK 2 ACCEPTANCE TEST --- MUTUAL TEST CONTRACT

The upcoming Week 2 test must evaluate both publication quality and
organizational behavior.

It must test:
### Truth

-   ESPN/live acquisition path;
-   canonical snapshot;
-   freshness;
-   semantic validation;
-   identity reconciliation;
-   Fact Lock.

### Coordination

-   Request Compiler;
-   Assignment Contract;
-   typed handoffs;
-   ACK;
-   dependencies;
-   fan-out/fan-in;
-   checkpoints;
-   scoped context;
-   artifact versions.

### Editorial

-   Issue Thesis;
-   Story Budget;
-   Story Cards;
-   specificity;
-   historical continuity;
-   originality isolation.

### Creative

-   canonical Character Packets;
-   Page Brief;
-   Premium Illustrated Page Mode;
-   Jake creative review;
-   character accuracy;
-   story-carrying illustration.

### Recovery

At least one controlled failure should be introduced or simulated: -
stale handoff; - missing provenance; - late score/stat correction; -
blocked character asset; - benchmark leakage attempt; - superseded
artifact.

The system must route the defect to the correct checkpoint without
unnecessary full-run restart.

### Release

The test is not successful merely because a strong page/PDF is produced.

It is successful when: - the product meets the gold-standard quality
floor; - the correct agents received the correct context; - gates
behaved correctly; - defects were caught near source; - targeted
recovery worked; - no critical private/Mercer contamination occurred; -
Jake did not have to discover basic preventable defects first.

------------------------------------------------------------------------

# 27. PERSONNEL DECISION

**No new permanent SCK department is authorized before testing.**

Existing Executive Control / ECS owns SCK during RC.

Temporary specialist workers may be spawned according to the
Collaboration Budget.

After testing: - if ECS handles orchestration without measurable
bottleneck → retain ownership; - if orchestration becomes a recurring
bottleneck → Research Lab may propose an Orchestration/Workflow
Reliability specialist.

Do not solve workflow problems by adding personnel before proving the
need.

------------------------------------------------------------------------

# 28. CROSS-OS CHANGE CONTROL

Either OS may originate an improvement proposal.

Cross-OS changes follow:

``` text
PROPOSED
→ DOMAIN REVIEW
→ CONFLICT CHECK
→ TEST PLAN
→ RC / EXPERIMENT
→ EVALUATION
→ KEEP / MODIFY / REVERT
→ VERSION
→ PROPAGATE TO BOTH OS THREADS
```

A change affecting both systems is not fully installed until both
governing threads receive the same controlling decision.

This patch satisfies that synchronization requirement for V5.2-RC.

------------------------------------------------------------------------

# 29. SUPERSEDED / MODIFIED RULES

## Superseded

-   uncontrolled conversational handoffs as sufficient coordination;
-   downstream reconstruction of missing critical context;
-   "done" as a workflow state;
-   full-run restart when dependency-aware targeted recovery is
    sufficient;
-   automatic escalation of routine domain defects to Jake;
-   unrestricted peer-to-peer agent collaboration.

## Modified

-   V5 one-page-at-a-time production remains controlling for flagship
    creative review, but parallel upstream evidence/research work is
    explicitly allowed.
-   V5.1 dependency-aware re-audit is now executed through SCK
    checkpoints/state.
-   context isolation is now a formal firewall but may not starve
    continuity-critical roles.
-   collaboration-kernel release gates are RC-blocking during acceptance
    testing but become permanent only after experiment success.

## Retained

-   V5 Gold-Standard Studio creative doctrine;
-   Commissioner Context Pass;
-   Premium Illustrated Page Mode;
-   exact canonical character dependencies;
-   Jake creative veto;
-   physical-world utility pages;
-   Asset Manifest;
-   final-PDF-as-truth;
-   V5.1 Data Platform;
-   source/fact locking;
-   semantic validation;
-   freshness/quarantine;
-   lineage;
-   snapshot diffs;
-   stat-correction watch;
-   domain authority;
-   QA vetoes;
-   benchmark isolation;
-   originality QA;
-   mobile QA;
-   blind release audit;
-   regression suite;
-   Research Lab;
-   Mercer firewall.

------------------------------------------------------------------------

# 30. FINAL MUTUAL DECLARATION

The Weekly Memo OS Engine Room and Schemin Subagent OS are to operate
from one agreed architecture before acceptance testing.

**Current build:**

`SCHEMIN '26 WEEKLY MEMO OS V5.2-RC`

**Composition:**

`V5 Gold-Standard Studio` + `V5.1 Hardened League Data Platform` +
`Schemin Collaboration Kernel RC` + `Independent Governance / QA` +
`Regression Suite + Research Lab`

**Testing status:** READY FOR CONTROLLED WEEK 2 ACCEPTANCE TEST once
this patch is installed in both governing threads.

**Permanent V5.2 status:** NOT YET CERTIFIED.

Certification requires successful evaluation of SCK-01 through SCK-04
and the V5/V5.1 acceptance criteria.

The organization succeeds when:

> reliable evidence enters once;\
> work advances only when dependencies permit;\
> specialists receive the context they actually need;\
> consequential handoffs are acknowledged;\
> defects return to the nearest responsible checkpoint;\
> late changes reopen only affected work;\
> premium Schemin identity never silently degrades;\
> private Mercer intelligence never enters public production;\
> independent QA---not the producing agent---controls PASS;\
> and Jake spends his time choosing among strong creative directions
> rather than rescuing preventable production failures.

**END OF OFFICIAL V5.2-RC MUTUAL IMPLEMENTATION PATCH**