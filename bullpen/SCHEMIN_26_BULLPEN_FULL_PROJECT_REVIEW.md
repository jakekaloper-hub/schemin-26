# SCHEMIN ’26 — FLA BULLPEN FULL-PROJECT REVIEW
## Full Board Audit + Closer Synthesis

**Date:** 2026-09-25  
**Status:** BOARD REVIEW COMPLETE / IMPLEMENTATION NOT AUTHORIZED BY THIS DOCUMENT  
**Project:** Schemin ’26  
**League:** Pro Schemin’ Football League — ESPN `1417621`  
**FLA Repository:** `jakekaloper-hub/fantasy-league-artworks`  
**FLA Integration Under Review:** Draft PR #3 — `Schemin '26 Bullpen Router v1`  
**Review Method:** FLA Bullpen Charter authority model applied to repo-grounded evidence and current Schemin ’26 project doctrine.

> **Important execution note:** This review did not fabricate a live FLA API board session. The current environment can inspect the connected FLA repository and Schemin project evidence, but it is not the deployed FLA Bullpen runtime with Supabase intel adapters and Anthropic calls. The board protocol below therefore uses the authoritative Director contracts, governance doctrine, live repository state, current PR/CI evidence, and Schemin project files.

---

# 1. Executive Board Synthesis

## The Closer — Board Resolution

Schemin ’26 does **not** need another operating system.

Its strongest current architecture is already defined:

```text
JAKE / COMMISSIONER INTENT
          ↓
CONTROL PLANE — SCHEMIN COLLABORATION KERNEL (SCK)
          ↓
TRUTH PLANE — V5.1 LEAGUE DATA PLATFORM
          ↓
PRODUCTION PLANE — V5 GOLD-STANDARD STUDIO
          ↓
GOVERNANCE PLANE — INDEPENDENT QA / RELEASE CONTROL
          ↓
LEARNING PLANE — REGRESSION SUITE / RESEARCH LAB / MEMORY
```

That structure is coherent and should remain controlling.

The FLA Bullpen should enter Schemin ’26 as a **selective specialist adapter and governance layer**, not as a sixth control plane and not as a replacement for SCK, Weekly Memo OS, Jack Mercer, ESPN truth, or Jake’s creative authority.

The most important project failure is no longer lack of architecture. It is the gap between **declared architecture and reliably executed architecture**.

Schemin ’26 now has strong doctrine for:

- live data acquisition and freshness;
- source hierarchy;
- benchmark isolation;
- character continuity;
- page-by-page production;
- domain authority;
- independent release control;
- targeted recovery;
- specialist handoffs;
- Mercer privacy;
- regression testing.

Yet recent production behavior has still exhibited:

- wrong or stale league context;
- same-week benchmark contamination during “blank canvas” testing;
- inaccurate or drifted characters;
- outputs that claimed to use the OS without actually reproducing the governing workflow;
- repeated need for Jake to identify defects that should have been caught upstream.

The FLA integration is promising but **not operationally complete**. Draft PR #3 introduces the correct broad concept — a deterministic Schemin-to-Bullpen router that reuses existing FLA Directors rather than inventing duplicate agents — but the branch is not merge-ready. As of the reviewed head commit `026f90617d81d93c6602112a5b6f418a59995be0`:

- Link Check: **PASS**
- Semgrep Code Quality Gate: **PASS**
- File Size Scan: **PASS**
- Main CI: **FAIL**
- PR state: **OPEN / DRAFT / MERGEABLE**
- Deploy preview: available
- Changed files: 7

The current CI failure is explained by a direct contradiction between the router implementation and its test contract:

```text
Objective:
"fix ESPN data and weekly memo"

TEST EXPECTATION:
cross_domain → The Closer

CURRENT ROUTER:
data_discrepancy → The Scout
because data-integrity terms override all other matched domains
```

That contradiction is exactly the kind of authority ambiguity the router exists to prevent.

## Board call

**Do not merge PR #3 yet.**

First resolve router semantics, turn the project’s acceptance doctrine into executable evidence, and prove one end-to-end Schemin workflow through the router without weakening the existing five-plane Schemin architecture.

---

# 2. Evidence & Source Inventory

## Schemin ’26 controlling evidence reviewed

### Weekly Memo / Production
- `SCHEMIN_26_WEEKLY_MEMO_OS_V5_GOLD_STANDARD_STUDIO_PATCH(1).md`
- `SCHEMIN_26_WEEKLY_MEMO_OS_V5_1_DATA_HARDENING_PATCH(1).md`
- `SCHEMIN_26_WEEKLY_MEMO_OS_V5_2_RC_MUTUAL_IMPLEMENTATION_PATCH(1).md`
- `SCHEMIN_26_WEEKLY_MEMO_GOLD_STANDARD_PRODUCTION_MANUAL(1).md`
- `SCHEMIN_26_WEEKLY_MEMO_MASTER_INITIATION_PROMPT(1).md`
- `SCHEMIN_26_SUBAGENT_V5_1_ENGINE_ROOM_RESPONSE(1).md`
- Week 1 production materials
- current Schemin ’26 Week 2 controlled-retest history and failure observations

### Character / Identity
- `SCHEMIN_26_MASTER_CHARACTER_CANON(1).md`
- current approved owner-character continuity rules
- current rename protocol

### Jack Mercer
- current Front Office V2 specification / redesign prompt
- current canonical league-state hierarchy for Mercer
- current Mercer isolation rules

## FLA repo evidence reviewed

- `docs/ops/governance/BULLPEN_CHARTER.md`
- `.claude/skills/bullpen/SKILL.md`
- `docs/agents/the-closer.md`
- `docs/ops/governance/PHASE_BRIEFING.md`
- `docs/ops/governance/DOCTRINE.md`
- `lib/bullpen/consultEngine.js`
- `pages/api/admin/bullpen/convene.js`
- `lib/executive-control/constants.js`
- `lib/executive-control/bullpenOrg.js`
- `docs/strategy/PRO_SCHEMIN_CASE_STUDY.md`
- `docs/ops/handoffs/PRO_SCHEMIN_SEASON_AUDIT_2025.md`

## Live FLA integration evidence reviewed

### Pull request
`PR #3 — Schemin '26 Bullpen Router v1`

Branch:
`schemin/bullpen-router-v1`

Head:
`026f90617d81d93c6602112a5b6f418a59995be0`

Changed files:

```text
docs/bullpen/SCHEMIN_BULLPEN_ROUTER_ACCEPTANCE_TESTS.md
docs/bullpen/SCHEMIN_BULLPEN_ROUTER_V1.md
docs/integrations/SCHEMIN_CHATGPT_INTEGRATION.md
lib/bullpen/__tests__/scheminRouter.test.js
lib/bullpen/index.js
lib/bullpen/scheminRouter.js
lib/workflow/publishScheduler.js
```

### CI state at review

| Gate | State |
|---|---|
| Link Check | PASS |
| FLA Semgrep — Code Quality Gate | PASS |
| File Size Scan | PASS |
| CI / `npm test` | **FAIL** |
| Netlify deploy preview | AVAILABLE |

### Important FLA governance drift found

The current authoritative Bullpen Charter defines **18 Directors**.

Legacy files still contain stale language such as:

```text
"all 8 directors"
```

inside board-meeting implementation comments and older synthesis paths.

The machine-readable organization has since been decomposed under:

```text
lib/executive-control/org/directorOrg.js
```

and the current facade explicitly describes **18 Directors + Staff arrays**.

This is documentation/runtime-era drift, not evidence that the current board contains only eight Directors.

---

# 3. Current Schemin ’26 Architecture

## Authoritative operating model

```text
                         JAKE
          Commissioner / owner / creative veto
                           │
                           ▼
                 CHATGPT CONTROL SURFACE
         request interpretation + synthesis interface
                           │
                           ▼
              SCHEMIN REQUEST / SCK CONTROL
      assignment class • dependencies • source policy
      handoffs • ACK • checkpoints • artifact versions
                           │
        ┌──────────────────┼───────────────────┐
        ▼                  ▼                   ▼
  LEAGUE DATA         DOMAIN EXECUTIVES      CANON
  PLATFORM            + SPECIALISTS          LAYER
  ESPN 1417621        Memo / Mercer /        Character
  snapshots           creative / QA          packets
        │                  │                   │
        └──────────────────┼───────────────────┘
                           ▼
                  PRODUCTION / DECISION
             memo • GM analysis • artwork • book
                           │
                           ▼
                 INDEPENDENT QA / GATES
     fact • freshness • canon • mobile • originality
                  firewall • release audit
                           │
                           ▼
                        OUTPUT
                           │
                           ▼
             REGRESSION / RESEARCH / MEMORY
```

## Where FLA belongs

```text
CHATGPT
   │
   ▼
SCHEMIN / SCK
   │
   ├── native Schemin authority
   │
   └── FLA BULLPEN ROUTER  ← selective adapter
             │
             ▼
     EXISTING FLA DIRECTORS / STAFF
             │
             ▼
      evidence-backed specialist input
             │
             ▼
      return to Schemin authority
```

FLA does **not** become:

- the source of live fantasy league truth;
- the Weekly Memo control plane;
- Jack Mercer;
- Jake’s creative authority;
- an automatic full-board call for routine work;
- a second league database;
- a second SCK.

---

# 4. System Health Matrix

| System | Status | Current authority | Board read | Immediate action |
|---|---|---|---|---|
| Weekly Memo OS V5 | YELLOW | Weekly Memo OS | Strong doctrine; reproducibility remains inconsistent | prove a fresh blank-canvas acceptance run |
| V5.1 League Data Platform | YELLOW | Data Platform / ESPN truth | Architecture is correct; operational use is not consistently demonstrated in every chat workflow | standardize one freshness/evidence receipt |
| V5.2-RC / SCK | YELLOW | Executive Control / SCK | Correct coordination model; explicitly not yet certified | execute SCK-01→04 acceptance tests |
| Character Canon | YELLOW | Character Librarian / canon file | Canon is strong; enforcement has still failed in generated art | machine-enforce character packet dependency before generation |
| Gold-Standard Creative Studio | YELLOW | Weekly Memo production | Week 2 proves quality ceiling; repeatability is still weak | test from facts without same-week creative leakage |
| Independent QA / Release | RED | QA + Release Auditor | Doctrine exists but Jake is still catching preventable defects first | require evidence ledger + release veto in every production run |
| Regression / Research Lab | YELLOW | Learning plane | Good test catalog exists; several critical behaviors still conceptual | turn highest-value failures into executable fixtures |
| FLA Bullpen Router PR #3 | RED | FLA engineering review | Correct direction, CI currently failing | resolve routing contract + turn CI green |
| FLA Bullpen as Schemin adapter | YELLOW | FLA + Schemin co-boundary | Feasible; currently branch-level integration rather than proven ChatGPT runtime | prove one selective consultation path |
| Jack Mercer | YELLOW | Jack Mercer | Product doctrine and data hierarchy are strong; current deployed functionality not fully reverified in this audit | perform separate live Front Office functional audit |
| Mercer firewall | YELLOW | SCK / QA | Explicit rule exists; must be tested, not assumed | add contamination fixture |
| Pittsy’s Book | YELLOW | Schemin editorial / verified lines | Functional concept; freshness dependency remains critical | consume same canonical league-state receipt |
| ESPN/Data Gateway | YELLOW | ESPN + Data Reliability | Correct failure taxonomy exists; live access remains a recurring practical dependency | prove direct + fallback path in controlled test |
| FLA repo documentation | YELLOW | Librarian | Rich institutional knowledge; some stale era comments remain | currency sweep for Bullpen count + integration state |
| FLA CI / engineering gate | RED for router branch | Architect / Setup Man / Umpire | 3 gates green, main CI red | fix failing contract and rerun |
| Security boundary of router | GREEN/YELLOW | Warden | Router is deterministic/read-only by design and explicitly denies destructive/publish/merge authority | keep constraints immutable; review before API/MCP exposure |

---

# 5. Full Director Findings

## The Closer — CEO

**Current read:** Schemin has sufficient architecture but too many places where written doctrine can be bypassed by conversational execution.

**What works:** Five-plane Schemin model, explicit source precedence, SCK contract model, FLA adapter strategy.

**Gap:** FLA integration risks becoming another authority layer if “FLA is the persistent operating platform” is interpreted too broadly.

**Call:** FLA is a reusable specialist workforce and institutional governance source. Schemin remains the project control architecture.

---

## The Setup Man — CTO

**Current read:** The adapter approach is technically sound because it reuses existing FLA infrastructure instead of creating a new agent runtime.

**Evidence:** PR #3 adds only a deterministic router, documentation, tests, index export, and one scheduler-related correction.

**Gap:** CI is red. The current implementation and acceptance test disagree about mixed-domain routing.

**Call:** No merge until `npm test` passes and mixed-domain semantics are resolved deliberately.

---

## The Scout — CDO

**Current read:** Data authority is one of Schemin’s strongest written systems.

**Evidence:** V5.1 distinguishes transport, endpoint, parser, schema, partial-response, stale, semantic, and true-source-unavailability states.

**Gap:** Correct architecture does not guarantee every ChatGPT workflow actually resolves live ESPN evidence before analysis.

**Call:** Every live football assignment should carry one machine-readable league-state receipt:

```yaml
league_id:
season:
week:
source_path:
fetched_at:
freshness_state:
snapshot_version:
stale:
failure_reason:
```

---

## The Umpire — Compliance

**Current read:** Schemin repeatedly defines excellent gates but sometimes allows the producing assistant to behave as if the gate passed.

**Gap:** “I used the OS” is not evidence that Source Lock, benchmark isolation, character QA, or release audit actually ran.

**Call:** Gate evidence must be attached to the artifact state. No evidence = gate not passed.

---

## The Beat Writer — CCO

**Current read:** The Week 2 Gold-Standard method is the correct editorial doctrine.

**What works:** Premium Illustrated Page Mode, Commissioner Context Pass, page-by-page review, league-specific visual storytelling.

**Gap:** Blank-canvas retests have sometimes recreated the old issue rather than generating a genuinely new issue from locked facts.

**Call:** Preserve Week 2 as evaluation benchmark only during blank-canvas tests.

---

## The Groundskeeper — COO

**Current read:** Complexity has grown faster than proven operational value.

**Gap:** Repeated patches, agents, and workflow concepts can increase coordination cost if not backed by measurable reduction in Jake intervention.

**Call:** Freeze new orchestration layers. Make the current SCK + Router prove value first.

Primary KPI:

```text
preventable_defects_discovered_first_by_jake
```

This number must decline.

---

## The GM — CPO

**Current read:** Jack Mercer has a clear product role and should remain the executive for ObiWan Jacoby football decisions.

**Gap:** A generic FLA Director must not supersede Mercer on roster/trade/waiver/lineup calls.

**Call:** Football operations route:

```text
Jake → Mercer → Scout/Analyst support → QA → Jake
```

not:

```text
Jake → generic full Bullpen → consensus football decision
```

---

## The Pitching Coach — CAIO

**Current read:** The project should route models/tools by task, but deterministic routing logic should decide authority before an LLM thinks.

**What works:** `scheminRouter.js` is intentionally deterministic with no LLM call and no writes.

**Gap:** Keyword precedence is currently too coarse for mixed-domain requests.

**Call:** Classification should distinguish:

- primary objective;
- incident type;
- affected artifact/domain;
- required authority.

Do not let one keyword seize the entire request.

---

## The Warden — CISO

**Current read:** The router’s current security posture is appropriate for a first adapter.

**Positive controls:**

```text
destructiveActionsAuthorized: false
publishAuthorized: false
mergeAuthorized: false
fullBoardByDefault: false
conversationMemoryIsCanonical: false
```

**Call:** Preserve these as hard constraints when an API/MCP boundary is eventually exposed.

No chat instruction should silently convert analysis authority into write/deploy/publish authority.

---

## The Commissioner — CSD

**Current read:** Schemin succeeds when the weekly rhythm is reliable, not merely when impressive one-off artifacts are possible.

**Gap:** Recent retests show the commissioner still has to intervene on basic correctness and continuity.

**Call:** Weekly operations should consume pre-validated league state and canon once, then reuse those artifacts across Memo, Pittsy, preview, and league-facing outputs.

---

## The Analyst — CAO

**Current read:** Schemin has many good metrics but the most important operating measurements are workflow quality metrics.

Priority measurements:

```text
freshness_failure_rate
wrong_character_escape_rate
benchmark_leakage_rate
first_pass_handoff_rate
duplicate_work_rate
qa_return_distance
jake_intervention_rate
final_artifact_blocking_defects
```

**Call:** Stop judging the system mainly by sophistication of prompts or number of subagents.

---

## The Librarian — CKO

**Current read:** Institutional knowledge is strong but authority metadata needs tightening.

**Drift found:**
- current Charter = 18 Directors;
- legacy board implementation/comments still say 8;
- V5.1 file is labeled “PROPOSED CONTROLLING ADDENDUM,” while V5.2 treats V5.1 as retained and adopted baseline;
- old FLA case-study material is useful history but must not become current Schemin doctrine.

**Call:** Every controlling Schemin file should declare:

```yaml
status:
version:
effective_date:
supersedes:
superseded_by:
scope:
```

---

## The Agent — CMO

**Current read:** The Pro Schemin identity is a product asset and should not be diluted by generic AI-dashboard aesthetics.

**Call:** Preserve the tactile fictional-sports-publication language for league-facing media while allowing Mercer to retain its separate private front-office visual identity.

No recommendation to broaden distribution is required for the current reliability mission.

---

## The Bookkeeper — CFO

**Current read:** The main cost risk in Schemin is not only token/image spend; it is repeated regeneration caused by upstream defects.

**Call:** Track rework cost:

```text
failed_generation_count
regeneration_due_to_wrong_fact
regeneration_due_to_wrong_character
full_restart_count
targeted_rework_count
```

Targeted recovery should replace full-run restart wherever dependencies allow.

---

## The Commissioner General — CLO

**Current read:** Canon images, generated art, private league information, and third-party sports data require clear provenance boundaries.

**Call:** Keep a per-artifact provenance ledger identifying:
- user-supplied reference;
- generated derivative;
- public league evidence;
- private Mercer analysis;
- publication authorization state.

---

## The Clubhouse Manager — CHRO

**Current read:** Schemin has enough named roles.

**Gap:** Adding more personas can hide accountability instead of improving execution.

**Call:** No new permanent specialist until a current owner repeatedly fails due to measurable capacity/domain mismatch.

Existing doctrine already says no permanent SCK department before testing; preserve that.

---

## The Scout Master — CRO

**Current read:** External growth and sales are outside the immediate Schemin reliability objective.

**Status:** `N/A` for current-season operating remediation.

**Call:** Do not allow monetization or growth work to distract from reliable weekly execution.

---

## The Architect — CEnO

**Current read:** PR #3 is directionally correct but fails its own executable contract.

### Concrete defect

Implementation:

```js
if (matches.includes('data_discrepancy')) {
  return 'data_discrepancy';
}
```

Test:

```js
classifyAssignment({
  objective: 'fix ESPN data and weekly memo'
}) === 'cross_domain'
```

These cannot both be correct.

**Call:** Decide the intended semantics first; then change code or test.

Recommended semantics:

```text
Pure ESPN/state discrepancy
→ data_discrepancy / Scout

Data discrepancy affecting a distinct governed deliverable
→ cross_domain / Closer
with Scout owning the data gate and the domain executive retaining output authority
```

This preserves data authority without allowing the data domain to seize publication or football-product authority.

---

# 6. Cross-System Conflicts & Drift

## Conflict A — SCK vs FLA Router

### Risk
Both could be interpreted as the “router.”

### Resolution
They are different layers.

```text
SCK = Schemin workflow/control plane
FLA Router = adapter selecting reusable FLA expertise
```

The FLA Router must operate **inside or beneath SCK authority**, not beside it as a competing supervisor.

---

## Conflict B — “FLA is the persistent operating platform”

The draft ChatGPT integration document says:

> FLA is the persistent operating platform and institutional knowledge layer for Schemin ’26.

That wording is too broad.

### Board correction

Use:

> FLA is a persistent **governance, specialist-contract, engineering, and selected canon/institutional-knowledge source** for Schemin ’26.

It is not the sole project source of truth.

Current fantasy state remains ESPN/Data Gateway.  
Weekly production remains Weekly Memo OS.  
Football strategy remains Mercer.  
Schemin cross-domain orchestration remains SCK.  
Jake remains final authority.

---

## Conflict C — Data-authority precedence vs cross-domain authority

Current router code makes any data-discrepancy keyword authoritative.

That is valid for a pure discrepancy, but not automatically for:

```text
"fix ESPN data and weekly memo"
```

A data incident may block another domain without owning the other domain.

### Correct pattern

```text
Scout owns truth/freshness gate
Closer resolves cross-domain workflow
Weekly Memo OS owns publication
```

---

## Conflict D — 18-Director Charter vs 8-Director legacy board code

Treat the 18-Director Charter / current `BULLPEN_ORG` as authoritative.

Legacy comments and synthesis code require a future currency cleanup but should not redefine the current organization.

---

## Conflict E — V5.1 status wording

V5.1 is labeled as proposed in its own file, while V5.2-RC explicitly adopts and retains the V5.1 Data Platform.

### Resolution

For current Weekly Memo operation, V5.2-RC’s cross-OS declaration makes the V5.1 data behavior part of the active RC architecture.

A documentation pass should make this explicit so later retrieval does not treat “PROPOSED” as inactive.

---

# 7. Preserve / Fix / Consolidate / Retire

| System / practice | Board disposition | Reason |
|---|---|---|
| Five-plane Schemin architecture | **PRESERVE** | clean authority separation |
| Weekly Memo V5 Gold Standard | **PRESERVE** | quality method proven |
| V5.1 Data Platform | **PRESERVE + PROVE** | correct data architecture |
| SCK | **PRESERVE + CERTIFY** | correct control model, still RC |
| Page-by-page creative approval | **PRESERVE** | critical to achieved quality |
| Jake creative veto | **PRESERVE** | league culture/taste is non-mechanical |
| Character canon master | **PRESERVE + ENFORCE** | strong identity contract |
| Mercer firewall | **PRESERVE + TEST** | prevents private-strategy leakage |
| FLA Bullpen Router | **FIX + KEEP AS ADAPTER** | useful integration pattern |
| Full-board-by-default routing | **REJECT** | expensive and unnecessary |
| Conversation memory as live truth | **REJECT** | stale/context contamination risk |
| New SCK department | **DEFER** | no proven need |
| Duplicate FLA agent registry for Schemin | **RETIRE / DO NOT BUILD** | existing Bullpen already provides contracts |
| Manual reinterpretation of missing ESPN data | **REJECT** | violates data doctrine |
| Same-week memo reuse during blank-canvas test | **REJECT** | benchmark contamination |
| “PDF exists = done” | **REJECT** | final rendered QA controls completion |

---

# 8. Risk Register

## P0 — Current blockers

| ID | Risk | Owner | Evidence | Impact | Remediation | Acceptance test |
|---|---|---|---|---|---|---|
| P0-01 | Bullpen Router CI is red | Setup Man + Architect | PR #3 `npm test` failure | cannot claim adapter is validated | resolve mixed-domain contract and rerun CI | all PR required checks green |
| P0-02 | Authority ambiguity in mixed data/domain requests | Closer + Scout + domain executive | router/test contradiction | incorrect executive ownership | model incident + affected-domain separately | ESPN+memo fixture routes cross-domain with Scout data ownership |
| P0-03 | Memo retest cannot yet be treated as certified V5.2 | Weekly Memo OS + Umpire | V5.2 explicitly says NOT YET CERTIFIED; recent controlled retests still required correction | false confidence in production system | run SCK-01→04 + blank-canvas acceptance | all acceptance fixtures pass with artifact evidence |
| P0-04 | Producing assistant can still bypass evidence gates | Umpire + SCK | repeated human discovery of factual/canon/benchmark defects | unreliable output despite good doctrine | bind gate receipts to workflow state | artifact cannot enter release state without receipts |

## P1 — Current-season stabilization

| ID | Risk | Owner | Remediation |
|---|---|---|---|
| P1-01 | Live league state resolved inconsistently across Memo/Mercer/Pittsy | Scout | shared canonical freshness receipt |
| P1-02 | Character canon exists but enforcement is not deterministic enough | Librarian + Pitching Coach | mandatory canonical character packet before image generation |
| P1-03 | Benchmark firewall is doctrine but not proven by fixture | Umpire + Beat Writer | controlled same-week leakage test |
| P1-04 | Mercer firewall unproven as executable test | Warden + GM | contamination fixture |
| P1-05 | FLA authoritative docs contain era drift | Librarian | current-governance currency sweep |
| P1-06 | Front Office functionality not verified in this audit | GM + Setup Man | live functional test, especially ESPN refresh |

## P2 — Quality / efficiency

- quantitative Jake-intervention metric;
- rework-cost tracking;
- provenance manifest automation;
- standardized artifact state machine across creative outputs;
- shared incident taxonomy between SCK and FLA adapter.

## P3 — Defer

- growth/revenue integrations;
- new permanent Schemin orchestration department;
- automatic full-board invocation;
- broad external FLA platform expansion for the sake of Schemin;
- new agent personas without proven domain gap.

---

# 9. Recommended Target Operating Model

## The simplest defensible model

```text
1. JAKE
   states goal / approves creative judgment / authorizes consequential actions

2. CHATGPT
   conversational control surface
   understands request but does not treat memory as canonical truth

3. SCHEMIN REQUEST COMPILER / SCK
   determines assignment class, source rules, dependencies, gates

4. DOMAIN EXECUTIVE
   Weekly Memo OS
   OR Jack Mercer
   OR Creative/Canon
   OR Engineering
   OR The Closer for genuine cross-domain work

5. CANONICAL SOURCES
   ESPN/Data Gateway
   Character Canon
   Commissioner ledger / approved receipts
   version-controlled Schemin + FLA doctrine

6. SELECTIVE SPECIALISTS
   Schemin native agents and/or FLA Bullpen adapter
   minimum sufficient team only

7. INDEPENDENT QA
   fact / freshness / canon / firewall / mobile / originality / release

8. OUTPUT

9. REGRESSION / LEARNING
   convert escaped defects into executable fixtures
```

## FLA Bullpen contract

FLA provides:

- Director/staff specialist definitions;
- repo-backed governance;
- engineering review;
- data-quality expertise;
- narrative/art/model expertise;
- security/compliance expertise;
- selective board synthesis when truly cross-domain.

FLA does not own:

- current ESPN truth;
- ObiWan Jacoby football strategy;
- Weekly Memo publication authority;
- Schemin request-state transitions;
- Jake’s final creative taste.

---

# 10. Remediation Sequence

## Step 1 — Fix the router contract

Resolve mixed-domain routing.

Recommended rule:

```text
one domain matched
→ domain route

multiple domains matched
→ cross_domain
UNLESS all matches are merely subordinate evidence terms inside one explicitly typed assignment
```

A data incident remains authoritative as a **gate**, not necessarily as the executive for the entire deliverable.

Then rerun CI until every required PR gate is green.

---

## Step 2 — Lock the authority map

Create one compact machine-readable authority table shared by Schemin and the adapter:

```yaml
weekly_memo:
  executive: weekly_memo_os
football_ops:
  executive: jack_mercer
artwork:
  executive: fla_creative_governance
data:
  executive: the_scout
engineering:
  executive: the_setup_man
cross_domain:
  executive: the_closer
```

Include explicit co-authority/gate relationships.

---

## Step 3 — Standardize source receipts

One data receipt format should serve Memo, Mercer, Pittsy, and Router QA.

Do not rebuild ESPN retrieval independently per thread.

---

## Step 4 — Execute the Schemin acceptance harness

Run controlled fixtures for:

- live ESPN refresh;
- stale snapshot rejection;
- roster/matchup correctness;
- character lock;
- benchmark isolation;
- blank-canvas Week 2 regeneration;
- one-page-at-a-time approval;
- late stat correction targeted reopen;
- Mercer leakage rejection;
- final rendered PDF audit.

---

## Step 5 — Certify or modify SCK

Evaluate:

```text
SCK-01 Typed Handoff + ACK
SCK-02 Dependency States + Checkpoints
SCK-03 Scoped Context Firewall
SCK-04 Event-Driven Rework
```

Each ends:

```text
KEEP
MODIFY
REVERT
INCONCLUSIVE
```
Do not leave an experimental feature permanently installed merely because it sounds useful.

---

## Step 6 — Prove one real FLA-routed Schemin assignment

Recommended first production proof:

```text
engineering or data discrepancy
```

not a Weekly Memo.

Reason: those domains have deterministic acceptance criteria and avoid creative ambiguity.

Only after that should the adapter be trusted for a full Memo workflow.

---

## Step 7 — Merge only after evidence

PR #3 is eligible for non-draft/merge consideration only when:

- all CI gates green;
- router acceptance suite aligned to actual semantics;
- no domain-authority contradiction;
- current 18-Director governance reference confirmed;
- adapter remains non-destructive;
- first controlled end-to-end Schemin route passes.

---

# 11. Acceptance Tests

## AT-01 — Live ESPN refresh

Given league `1417621`, obtain current required league state.

PASS requires:
- source path recorded;
- timestamp;
- freshness classification;
- no stale state presented as live;
- failure type classified if unavailable.

---

## AT-02 — Correct roster / matchup

Select one known team/week fixture.

PASS requires exact:
- team identity;
- matchup opponent;
- roster;
- relevant score/state;
- snapshot version.

---

## AT-03 — Character continuity

Generate or validate a fixture involving:

- ObiWan Jacoby → Trade Jedi, no championship belt;
- Donkey Kong → Arsenal Centaur;
- Slob on my Dobb → Fart Star;
- His Majesty’s Blood → Belt Keeper;
- Chili Cheesers → Chili Outlaw + Dark Horse.

PASS requires no rename-driven redesign.

---

## AT-04 — Blank-canvas memo

Use verified Week 2 facts.

Hide same-week approved creative prose/art/layout from generation context.

PASS requires:
- new issue thesis;
- new page concepts;
- correct facts;
- correct canon;
- quality assessed afterward against benchmark.

Benchmark similarity should not be achieved through copying.

---

## AT-05 — Benchmark firewall

Intentionally expose a benchmark-only artifact to the wrong context channel.

PASS = workflow rejects or quarantines it.

---

## AT-06 — Page-by-page approval

A flagship page may not advance:

```text
BRIEF
→ GENERATE
→ DISPLAY
→ REVIEW
→ CORRECT
→ QA
→ LOCK
```

until blocking defects are zero.

---

## AT-07 — Final PDF truth

PASS requires:
- rendered-page inspection;
- no crop/stretch;
- fact QA;
- character QA;
- mobile readability;
- duplication review;
- independent release signoff.

---

## AT-08 — Mercer firewall

Seed a private Mercer trade opinion.

Run a public Weekly Memo workflow.

PASS = no Mercer-derived strategic claim appears in any public evidence packet, copy, art brief, or final artifact.

---

## AT-09 — FLA provenance

A routed assignment must record:

```text
router version
selected executive
selected specialists
repo revision
canonical sources
freshness status
material disagreement
QA result
```

---

## AT-10 — Recovery test

Inject a late score/stat correction affecting one matchup.

PASS requires:
- dependent artifacts reopened;
- unrelated locked pages remain locked;
- targeted re-QA only;
- no full issue restart.

---

## AT-11 — Mixed-domain router

Input:

```text
fix ESPN data and weekly memo
```

PASS requires:
- cross-domain coordination;
- Scout controls the data/freshness gate;
- Weekly Memo OS retains publication authority;
- The Closer resolves sequencing/authority;
- no silent single-domain takeover.

---

# 12. Owner Decisions Required

The board identifies only two decisions that genuinely need Jake.

## Decision 1 — Confirm FLA’s Schemin role

Recommended wording:

> FLA Bullpen is an on-demand specialist and governance layer for Schemin ’26. It does not replace SCK, Weekly Memo OS, Jack Mercer, ESPN truth, or Jake’s final authority.

## Decision 2 — Router merge threshold

Recommended:

> PR #3 remains draft until all required CI gates pass and one end-to-end controlled Schemin route has produced evidence.

Everything else in the immediate remediation sequence is an engineering/governance issue and should not require repeated Jake intervention.

---

# 13. Board Resolution

## Final Closer synthesis

The project’s problem is **not insufficient intelligence** and not insufficient prompting.

Schemin ’26 has accumulated enough intelligence.

The problem is **execution integrity**.

The architecture says:

```text
verify → route → execute → QA → lock → release
```

but conversation-level production can still collapse into:

```text
remember → improvise → generate → declare done
```

That is the gap the next phase must close.

The Bullpen therefore resolves:

1. **Preserve the five-plane Schemin architecture.**
2. **Keep FLA as a selective adapter, not a new control plane.**
3. **Keep PR #3 draft until CI is green.**
4. **Resolve its mixed-domain authority contradiction before any merge.**
5. **Make gate evidence machine-visible instead of narrative claims.**
6. **Certify SCK-01 through SCK-04 with controlled fixtures.**
7. **Use the Week 2 memo as benchmark-only in blank-canvas tests.**
8. **Make character canon and live-data receipts hard dependencies.**
9. **Preserve Jack Mercer as football executive and keep the firewall testable.**
10. **Measure success by preventable defects Jake no longer has to catch.**

## What not to do

Do not:
- add another agent organization;
- create another league database;
- make the full Bullpen default;
- merge the router because the concept is good;
- treat conversation memory as league truth;
- let FLA own domains already governed by Schemin;
- use the official Week 2 creative work as generation input during blank-canvas testing;
- call an artifact complete before independent QA.

## Definition of done

This review’s remediation program is complete only when a real Schemin assignment can travel:

```text
JAKE
→ SCK
→ correct domain executive
→ canonical sources
→ minimum sufficient specialists / FLA adapter
→ independent QA
→ correct artifact
```

with provenance, freshness, canon, firewall state, and acceptance evidence — **without Jake having to discover the basic preventable defect first**.

---

# 14. Appendix — Evidence Ledger

## Schemin ’26 project artifacts
- `SCHEMIN_26_WEEKLY_MEMO_OS_V5_GOLD_STANDARD_STUDIO_PATCH(1).md`
- `SCHEMIN_26_WEEKLY_MEMO_OS_V5_1_DATA_HARDENING_PATCH(1).md`
- `SCHEMIN_26_WEEKLY_MEMO_OS_V5_2_RC_MUTUAL_IMPLEMENTATION_PATCH(1).md`
- `SCHEMIN_26_WEEKLY_MEMO_GOLD_STANDARD_PRODUCTION_MANUAL(1).md`
- `SCHEMIN_26_WEEKLY_MEMO_MASTER_INITIATION_PROMPT(1).md`
- `SCHEMIN_26_SUBAGENT_V5_1_ENGINE_ROOM_RESPONSE(1).md`
- `SCHEMIN_26_MASTER_CHARACTER_CANON(1).md`
- current Jack Mercer Front Office V2 specification
- current project-level Week 2 acceptance/retest history

## FLA repository
- `docs/ops/governance/BULLPEN_CHARTER.md`
- `.claude/skills/bullpen/SKILL.md`
- `docs/agents/the-closer.md`
- `docs/ops/governance/PHASE_BRIEFING.md`
- `docs/ops/governance/DOCTRINE.md`
- `lib/bullpen/consultEngine.js`
- `pages/api/admin/bullpen/convene.js`
- `lib/executive-control/constants.js`
- `lib/executive-control/bullpenOrg.js`
- `docs/strategy/PRO_SCHEMIN_CASE_STUDY.md`
- `docs/ops/handoffs/PRO_SCHEMIN_SEASON_AUDIT_2025.md`

## FLA Schemin Router PR #3
- `docs/bullpen/SCHEMIN_BULLPEN_ROUTER_ACCEPTANCE_TESTS.md`
- `docs/bullpen/SCHEMIN_BULLPEN_ROUTER_V1.md`
- `docs/integrations/SCHEMIN_CHATGPT_INTEGRATION.md`
- `lib/bullpen/__tests__/scheminRouter.test.js`
- `lib/bullpen/index.js`
- `lib/bullpen/scheminRouter.js`
- `lib/workflow/publishScheduler.js`

## Reviewed integration revision
`026f90617d81d93c6602112a5b6f418a59995be0`

---

**END OF FLA BULLPEN FULL-PROJECT BOARD REVIEW**