# SCHEMIN '26 --- SUBAGENT RESPONSE TO ENGINE ROOM V5.1

## Collaboration Kernel + Data Platform Integration Proposal

**Status:** SUBAGENT PATCH-NOTE RECOMMENDATION TO WEEKLY MEMO ENGINE
ROOM\
**Target:** V5.x integration / evaluation\
**Basis:** Weekly Memo OS V4 Subagent Operating Patch + Engine Room V5.1
Live Data Hardening & Domain-Authority Patch + multi-agent
workflow-kernel research\
**Purpose:** Synchronize the Subagent organization with V5.1 and propose
the next collaboration/communication layer without creating a competing
operating system.

------------------------------------------------------------------------

# 1. EXECUTIVE RESPONSE

The Subagent organization recommends **accepting V5.1 Data Hardening as
the new data-plane baseline** and integrating a separate **Schemin
Collaboration Kernel (SCK)** as the communication/control plane.

These are complementary:

-   **V5.1 League Data Platform:** what information is trustworthy,
    current, validated, traceable, and safe to publish.
-   **Schemin Collaboration Kernel:** how verified work moves between
    agents without context loss, duplication, silent assumptions,
    premature advancement, or unnecessary Jake intervention.
-   **V4/V5 Production OS:** how the organization turns that information
    into the Weekly Memo.

``` text
JAKE / OWNER INTENT
        ↓
EXECUTIVE CONTROL
        ↓
SCHEMIN COLLABORATION KERNEL
        ↓
LEAGUE DATA PLATFORM
        ↓
DOMAIN WORKFLOWS
        ↓
INDEPENDENT QA / VETOES
        ↓
RELEASE CONTROL
        ↓
INSTITUTIONAL MEMORY / RESEARCH LAB
```

The SCK should not replace the V5.1 Golden Path, Source Lock, domain
authority, or release gates. It should become the coordination substrate
beneath them.

------------------------------------------------------------------------

# 2. V5.1 CHANGES ACCEPTED BY SUBAGENTS

## 2.1 League Data Platform

Adopt the hardened Source Lock:

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

Editorial, Narrative, Art, Design, and Release agents do not
independently improvise ESPN retrieval or repair missing league facts.

## 2.2 Failure taxonomy

A failed fetch is not equivalent to ESPN being unavailable.

Required classes:

-   TRANSPORT FAILURE
-   ENDPOINT FAILURE
-   PARSER FAILURE
-   SCHEMA DRIFT
-   PARTIAL RESPONSE
-   STALE SNAPSHOT
-   SEMANTIC DATA FAILURE
-   TRUE SOURCE UNAVAILABILITY

Only the affected domain degrades or blocks.

## 2.3 Multi-path acquisition

1.  Direct ESPN v3.
2.  Independent parser/client path.
3.  Valid raw-response fallback.
4.  Latest validated snapshot with explicit freshness.
5.  Commissioner evidence for fields unavailable through ESPN.

No fallback may impersonate live data.

## 2.4 Canonical snapshot + lineage

Only validated snapshots enter newsroom state.

``` text
VISIBLE CLAIM
→ NORMALIZED FIELD
→ SNAPSHOT VERSION
→ RAW ESPN RESPONSE / APPROVED RECEIPT
→ RETRIEVAL TIMESTAMP
```

Derived statistics retain formula/version.

## 2.5 Freshness + quarantine

``` text
LIVE_VERIFIED
RECENT_VERIFIED
STALE_VERIFIED
QUARANTINED
UNAVAILABLE
```

Suspicious state is quarantined rather than silently promoted.

## 2.6 Snapshot diff + stat-correction watch

Agents should consume changes rather than repeatedly rediscovering the
entire league.

``` text
ACTIVE
→ PROVISIONAL_FINAL
→ STAT_CORRECTION_WATCH
→ FACT_LOCKED
```

A late score change reopens only dependent statistics, stories,
standings, pages, and QA gates.

## 2.7 Domain authority

-   Data Reliability may block Fact Lock.
-   Character Librarian may block artwork.
-   Narrative may reject generic Story Cards.
-   Art QA may force regeneration.
-   Mobile QA may force page rebuild.
-   Blind Release Auditor may stop publication.

A documented gate failure does not require Jake's permission to correct.

------------------------------------------------------------------------

# 3. PROPOSED V5.x ADDITION --- SCHEMIN COLLABORATION KERNEL

Agents should communicate through **contracts, artifacts, state
transitions, acknowledgements, and events** rather than uncontrolled
conversational history.

> **PROMPT → CONTRACT → GRAPH → SCOPED CONTEXT → EXECUTE → ACK → VERIFY
> → CHECKPOINT → RELEASE → TRACE → LEARN**

------------------------------------------------------------------------

# 4. REQUEST COMPILER

Before specialist execution, Executive Control compiles Jake's prompt:

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

Two independent downstream agents receiving the contract should agree on
assignment type, deliverable, permitted sources, benchmark restrictions,
gates, and definition of completion. Otherwise the contract returns to
Executive Control.

------------------------------------------------------------------------

# 5. CENTRAL SUPERVISOR ROUTING

Executive Control remains normal routing authority. Agents do not
default to unrestricted peer-to-peer collaboration.

``` text
                    EXECUTIVE CONTROL
                           │
          ┌────────────────┼────────────────┐
          ↓                ↓                ↓
     DATA PLATFORM     RESEARCH        CREATIVE
          │                │                │
          └──────────── STRUCTURED ─────────┘
                       HANDOFFS
                           ↓
                     EDITORIAL MERGE
                           ↓
                    INDEPENDENT QA
```

Direct specialist communication requires an authorized workflow, defined
receiver, recorded handoff, and preserved provenance.

------------------------------------------------------------------------

# 6. TYPED COMMUNICATION ENVELOPE

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

This extends existing Schemin handoff doctrine.

------------------------------------------------------------------------

# 7. ACKNOWLEDGEMENT PROTOCOL

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

Suggested rejection codes: `MISSING_PROVENANCE`, `STALE_INPUT`,
`INVALID_STATE`, `MISSING_DEPENDENCY`, `CONTRACT_VIOLATION`,
`SOURCE_NOT_APPROVED`, `BENCHMARK_LEAKAGE`, `CHARACTER_PACKET_MISMATCH`,
`UNSUPPORTED_CLAIM`, `QA_NOT_PERFORMED`, `WRONG_ARTIFACT_VERSION`.

A receiver rejects malformed packets instead of silently reconstructing
missing context.

------------------------------------------------------------------------

# 8. WORKFLOW STATE KERNEL

``` text
WAITING
READY
RUNNING
BLOCKED
QA_RETURNED
PASSED
SUPERSEDED
```

`PASSED` requires the designated independent gate. `SUPERSEDED` remains
traceable but cannot feed new production. No downstream node advances
merely because upstream says "done."

------------------------------------------------------------------------

# 9. FAN-OUT / FAN-IN CONTROLLER

``` text
                   FACT LOCK
                       │
       ┌───────────────┼───────────────┐
       ↓               ↓               ↓
   HISTORIAN       NFL INTEL       STATISTICS
       │               │               │
       └───────────────┼───────────────┘
                       ↓
                 EVIDENCE FAN-IN
                       ↓
                  STORY CARDS
                       │
       ┌───────────────┼───────────────┐
       ↓               ↓               ↓
   MATCHUP 1        MATCHUP 2       ... ×6
       └───────────────┼───────────────┘
                       ↓
                 EDITORIAL MERGE
```

Fan-in waits until required branches are PASSED, explicitly UNAVAILABLE,
or formally removed/reframed by the owning Director.

------------------------------------------------------------------------

# 10. CHECKPOINT / RECOVERY MODEL

Minimum checkpoints:

-   CANONICAL_SNAPSHOT_LOCK
-   FACT_LOCK
-   STORY_LOCK
-   CHARACTER_PACKET_LOCK
-   ART_LOCK
-   COPY_LOCK
-   PAGE_LOCK
-   RELEASE_DATA_FREEZE

A downstream defect returns to the nearest responsible checkpoint.
V5.1's Dependency Graph determines what reopens.

------------------------------------------------------------------------

# 11. IDEMPOTENCY / DUPLICATE-WORK PROTECTION

Expensive tasks receive deterministic work keys, for example:

``` text
2026_W03
+ MATCHUP_04
+ SNAPSHOT_2026W03_V7
+ STORY_CARD_V2
+ CHARACTER_PACK_V5
+ ART_BRIEF_V3
```

If inputs and contract are unchanged, retries reuse valid artifacts.
Changed dependencies invalidate only affected keys.

------------------------------------------------------------------------

# 12. EVENT BUS

Initial event vocabulary:

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

Agents subscribe only to relevant jurisdictional events.

------------------------------------------------------------------------

# 13. TRACEABILITY

Required IDs:

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

Final-page trace:

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

This integrates directly with V5.1 Data Lineage.

------------------------------------------------------------------------

# 14. CONTEXT FIREWALL

Each agent receives only:

1.  governing contract;
2.  required artifacts;
3.  relevant evidence packet;
4.  relevant canon;
5.  relevant prior lessons;
6.  explicit prohibited inputs.

This reduces contamination, benchmark leakage, instruction collisions,
token overhead, and provenance ambiguity.

## Jack Mercer firewall

Jack Mercer remains completely outside Schemin public/editorial
production. No Schemin packet may contain Mercer recommendations,
valuations, private roster reasoning, trade/opponent strategy, or
Mercer-derived conclusions. Any violation is a critical failure and
automatic release block.

------------------------------------------------------------------------

# 15. FAILURE-SPECIFIC ROUTING

``` text
TRANSIENT NETWORK FAILURE → bounded retry / alternate path
ENDPOINT FAILURE → failover / circuit breaker
PARSER FAILURE + VALID RAW JSON → raw normalization
SCHEMA DRIFT → quarantine + Schema Auditor
BAD HANDOFF → producer
MISSING EVIDENCE → owning data/research domain
QA FAILURE → nearest responsible checkpoint
CHARACTER FAILURE → Character / Art
MOBILE FAILURE → Design / Layout
OWNER-CONTROLLED POLICY EXCEPTION → Jake
RELEASE-CRITICAL CONFLICT → Executive + Standards
```

No blind retries.

------------------------------------------------------------------------

# 16. BOUNDARY GUARDRAILS

Validate at:

1.  ESPN acquisition → raw evidence.
2.  Raw evidence → normalized snapshot.
3.  Snapshot → canonical promotion.
4.  Canonical state → Fact Lock.
5.  Evidence packet → Story Card.
6.  Story Card → Art Brief.
7.  Character Packet → generated art.
8.  Copy → layout.
9.  Layout → Page Lock.
10. Page Lock → release assembly.
11. Release refresh → dependency recheck.
12. Final artifact → Blind Release Audit.

Catch defects near their source.

------------------------------------------------------------------------

# 17. COLLABORATION BUDGET

More agents do not automatically improve output. Executive Control adds
agents only when expected information gain exceeds communication
overhead, duplicate-work risk, context complexity, QA burden, and
cycle-time cost.

------------------------------------------------------------------------

# 18. COMMUNICATION KPIs

Add:

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

------------------------------------------------------------------------

# 19. DATA PLATFORM × SCK INTEGRATION

``` text
ESPN ACQUISITION
↓
RAW PRESERVED
↓
SEMANTIC VALIDATION
↓
CANONICAL_SNAPSHOT_PROMOTED
↓ event
SCK DEPENDENCY GRAPH
↓
affected assignments become READY
```

Late correction:

``` text
STAT_CORRECTION_DETECTED
↓
SNAPSHOT DIFF
↓
DEPENDENCY GRAPH
↓
affected nodes → SUPERSEDED
↓
nearest valid checkpoint
↓
targeted rework
↓
independent re-QA
```

------------------------------------------------------------------------

# 20. DOMAIN COUNCIL UPGRADE

Keep V5.1 Domain Council / Red-Team and add:

> **Orchestration:** Where can this issue fail because the right
> information reaches the wrong person, arrives too late, lacks
> provenance, or is never acknowledged?

Credible risks become assignments/tests before Story Budget lock.

------------------------------------------------------------------------

# 21. NEW REGRESSION TESTS

``` text
COLLAB-001: handoff lacks provenance → receiver rejects
COLLAB-002: task starts before dependency PASS → scheduler blocks
COLLAB-003: benchmark-only same-week prose reaches blank-canvas agent → firewall fails
COLLAB-004: duplicate unchanged expensive generation → idempotency prevents
COLLAB-005: late stat correction affects one matchup → only dependent artifacts reopen
COLLAB-006: QA failure routes to unrelated department → routing fails
COLLAB-007: routine defect escalates to Jake → Executive intercepts
COLLAB-008: handoff sent but never acknowledged → assignment remains incomplete
COLLAB-009: superseded artifact enters assembly → release audit fails
COLLAB-010: Mercer-derived information enters evidence packet → auto-block
```

------------------------------------------------------------------------

# 22. RESEARCH-LAB EXPERIMENT PLAN

Do not promote the entire SCK at once.

## SCK-01 --- Typed Handoff + ACK

KEEP if first-pass acceptance improves, missing-context defects decline,
and cycle time does not materially worsen.

## SCK-02 --- Dependency States + Checkpoints

KEEP if QA return distance and duplicate work decline without increasing
escaped defects.

## SCK-03 --- Scoped Context Firewall

KEEP if unsupported claims/benchmark leakage decline without meaningful
loss of continuity.

## SCK-04 --- Event-Driven Rework

KEEP if affected-artifact detection reaches 100% on fixtures, unrelated
pages remain locked, and re-QA time improves.

Only successful experiments become permanent V5.x doctrine.

------------------------------------------------------------------------

# 23. PROPOSED INTEGRATED GOLDEN PATH

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
→ COMMISSIONER CONTEXT
→ DOMAIN COUNCIL + ORCHESTRATION PRE-MORTEM
→ ISSUE THESIS
→ STORY BUDGET
→ PARALLEL EVIDENCE WORK
→ ACKNOWLEDGED FAN-IN
→ STORY CARDS
→ CHARACTER PACKETS
→ PAGE ARCHITECTURE
→ PAGE BRIEFS
→ PREMIUM PAGE PRODUCTION
→ JAKE VISUAL REVIEW WHEN OWNER JUDGMENT IS REQUIRED
→ INDEPENDENT PAGE QA
→ PAGE LOCK
→ ASSET MANIFEST
→ RELEASE DATA REFRESH / FREEZE
→ SNAPSHOT DIFF
→ DEPENDENCY RECHECK
→ TARGETED REOPEN IF REQUIRED
→ PDF ASSEMBLY
→ FULL-ARTIFACT AUDIT
→ DEFECT / CHECKPOINT RECOVERY
→ BLIND RELEASE AUDIT
→ RELEASE CERTIFICATION
→ ARCHIVE
→ RETROSPECTIVE
→ METRICS
→ RESEARCH-LAB EXPERIMENTS
→ INSTITUTIONAL MEMORY
```

------------------------------------------------------------------------

# 24. RELEASE MANIFEST ADDITIONS --- ONLY AFTER TESTING

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

A Collaboration PASS never overrides a failed Data, Editorial,
Character, Art, Mobile, Copy, or Release gate.

------------------------------------------------------------------------

# 25. PERSONNEL IMPACT

Do **not** create a large new permanent department.

V5.1 already defines the necessary Data Platform functions:

-   League Data Engineer
-   Data Reliability / SRE
-   Schema & Contract Auditor
-   League Identity Resolver
-   Statistics Reconciliation Agent
-   Data Release Steward

The SCK should initially be owned by existing Executive Control / ECS.
Create a permanent Orchestration specialist only if experiments show ECS
is a measurable bottleneck.

Temporary parallel workers inherit the Assignment Contract, scoped
context, handoff requirements, QA boundaries, and terminate after
handoff.

------------------------------------------------------------------------

# 26. SUBAGENT SYSTEM UPDATE

## Adopt now

-   V5.1 League Data Platform behavior.
-   Multi-path ESPN resilience.
-   Canonical snapshots.
-   Semantic validation and quarantine.
-   Freshness states.
-   Snapshot diffs.
-   Stat-correction watch.
-   Data lineage.
-   Incident classification.
-   Domain authority.
-   Domain Council / Red-Team.
-   Canonical identity registry.
-   Dependency-aware re-audit.
-   Evidence packets.
-   Release refresh/freeze.
-   Chaos/regression testing.
-   Cost-of-change routing.
-   Golden datasets.

## Evaluate before permanent promotion

-   Request Compiler.
-   Typed communication envelopes.
-   ACK protocol.
-   workflow state kernel.
-   fan-out/fan-in controller.
-   checkpoints.
-   idempotency keys.
-   event bus.
-   trace IDs.
-   enforceable context firewall.
-   collaboration budget.
-   collaboration KPIs.

Follow:

> **PROPOSED → TESTED → APPROVED → VERSIONED → PROPAGATED**

------------------------------------------------------------------------

# 27. ENGINE ROOM REQUEST

The Subagent organization asks the Weekly Memo Engine Room to:

1.  Treat this as a **candidate V5.x integration proposal**, not an
    independent fork.
2.  Merge accepted V5.1 data-plane changes into permanent Subagent
    contracts.
3.  Evaluate the Collaboration Kernel through the Research Lab in the
    proposed sequence.
4.  Reject or modify any SCK component conflicting with the Engine
    Room's current V5 architecture.
5.  If tests pass, version the SCK into the controlling OS and propagate
    it to Subagent contracts, production workflows, regression suites,
    and release manifests.
6.  Return accepted/rejected/modified decisions so Subagents can
    synchronize to the final Engine Room build.

------------------------------------------------------------------------

# 28. FINAL RECOMMENDATION

V5.1 substantially hardens **truth acquisition**.

The next high-value improvement is hardened **coordination**, not more
personas.

> **Reliable data enters once.\
> Context reaches only agents that need it.\
> Every consequential handoff is acknowledged.\
> Dependencies control when work advances.\
> QA failures return to the correct checkpoint.\
> Late changes reopen only affected work.\
> Every final claim and page is traceable.\
> Jake is reserved for actual owner judgment.**

This is the recommended bridge from **Series A operational reliability**
toward **Series B institutional intelligence**.

------------------------------------------------------------------------

**Prepared by:** Schemin '26 Subagent Organization / Executive Control\
**For:** Weekly Memo OS Engine Room\
**Document class:** Candidate patch-note recommendation\
**Jack Mercer boundary:** STRICTLY EXCLUDED