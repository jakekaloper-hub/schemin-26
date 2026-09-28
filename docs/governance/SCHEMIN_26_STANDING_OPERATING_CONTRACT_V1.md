# Schemin '26 — Standing Operating Contract

**Document class:** control  
**Authority / owner:** Jake / Commissioner intent; Bullpen execution; Librarian knowledge integrity; The Closer final integration  
**Version:** 1.0  
**Status:** ACTIVE — STANDING BEHIND-THE-SCENES OPERATING CONTRACT  
**Effective date:** 2026-09-28  
**Review trigger:** material architecture change, release-gate resolution, or explicit Commissioner supersession  
**Canonical repository:** `jakekaloper-hub/schemin-26`

## Prime directive

Resume work from the current GitHub state of `jakekaloper-hub/schemin-26`.

Do not restart discovery.

Do not reconstruct repository architecture from memory.

Do not create a parallel operating system.

Do not move Schemin '26 project state back into FLA, another repository, or ChatGPT-only context.

The Librarian repository-integrity sweep and Bullpen second-line audit are the governing behind-the-scenes baseline for subsequent Schemin '26 work.

---

## 1. Load the audited baseline first

Before substantial Schemin '26 work, resolve current repository state and load the relevant control documents.

Minimum control plane:

- `PROJECT_CONTROL_REGISTRY.md`
- `docs/governance/SOURCE_OF_TRUTH.md`
- `docs/governance/AUTHORITY_MATRIX.md`
- `docs/governance/CROSS_REPO_SOURCE_OF_TRUTH_MATRIX.md`
- `docs/governance/CANONICAL_ARTIFACT_REGISTER.md`
- `docs/governance/REPOSITORY_INTEGRITY_SWEEP_CONTROL_V1.md`
- `docs/governance/BRANCH_PROTECTION_TARGET_V1.md`
- `docs/architecture/REPOSITORY_DEPENDENCY_MAP.md`
- `docs/ops/REPOSITORY_SYNCHRONIZATION_PLAYBOOK.md`
- `planning/REPOSITORY_SWEEP_UNRESOLVED_2026-09-27.md`
- `bullpen/SCHEMIN_26_REPOSITORY_PLATFORM_SECOND_LINE_AUDIT_V1.md`

Then load only domain-specific material needed for the task.

Do not flood context with the entire repository unless the task requires it.

---

## 2. Preserve repository authority

Schemin '26 has one canonical project home:

`jakekaloper-hub/schemin-26`

This repository owns:

- league-specific truth;
- project governance;
- character canon;
- Memo OS;
- Week production;
- Novel OS;
- Living Novel;
- Mercer project state;
- Data Gateway contracts;
- Schemin-specific Bullpen operation;
- QA evidence;
- release records;
- production registers;
- project prompts;
- project decisions;
- durable artifacts.

External repositories may supply reusable capability. They do not become alternate project truth.

### FLA

`fantasy-league-artworks`

Treat as an upstream/reusable capability source.

Do not migrate Schemin-specific state there merely because FLA contains useful infrastructure.

### Bullpen upstream

Generic reusable Bullpen capability may live upstream.

Schemin-specific application, evidence, decisions, configuration, and operating state remain here.

---

## 3. Audited data architecture

The intended ESPN chain is:

```text
data/live last-known-good
        ↓
hydrate into workflow
        ↓
direct ESPN acquisition
        ↓
contract validation
   ┌────┴────┐
 success    failure
   ↓          ↓
fresh      preserve LKG
snapshot   + stale/failure metadata
   └────┬────┘
        ↓
persist to data/live
        ↓
consumer recomputes freshness at read time
```

### `main`

Owns:

- source code;
- governance;
- canon;
- Memo OS;
- Novel OS;
- Mercer;
- production state;
- tests;
- documentation.

### `data/live`

Owns:

- operational ESPN snapshot state;
- `data/snapshots/1417621/latest.json`;
- `data/snapshots/1417621/manifest.json`.

Do not use `data/live` as a general development branch.

Do not commit feature work, canon, prompts, or production documents there.

---

## 4. Data claims must carry freshness

No Bullpen member, Memo OS agent, Mercer workflow, Novel OS process, or downstream consumer may call ESPN-derived information "live" merely because snapshot data exists.

Every consumer must inspect:

- `fetched_at`;
- `stale`;
- `failure_reason`;
- `snapshot_age_seconds`;

and recompute effective snapshot age at read time.

Game-window workflows should use a tight SLO.

Historical/background workflows may use a broader SLO where appropriate.

If freshness exceeds the applicable SLO, state that explicitly.

Do not silently convert cached state into live state.

---

## 5. ESPN validation is a hard gate

Do not weaken Data Gateway validation without evidence.

Current contract includes:

- league ID `1417621`;
- 2026 season;
- exactly 12 teams;
- unique team IDs;
- non-empty schedule;
- valid settings/status structures;
- roster entries present;
- no empty team roster;
- settings-derived roster capacity;
- legitimate reserve/IR variance permitted;
- no roster exceeding configured capacity.

If ESPN changes upstream structure, investigate the contract change first.

Do not merely loosen tests until they pass.

---

## 6. Repository Merge Gate is the platform-wide safety net

The always-on workflow:

`.github/workflows/repository-merge-gate.yml`

is the intended stable merge-protection surface.

It validates:

- canonical control files;
- JSON integrity;
- Data Gateway compile;
- Data Gateway contract tests;
- Novel OS regression suite;
- Bullpen Runtime suite.

Domain-specific workflows may remain path-filtered.

Do not make path-filtered workflows the only universal protection mechanism.

If new major Schemin subsystems become mission-critical, evaluate whether deterministic tests should join the Repository Merge Gate.

Avoid turning the merge gate into a slow, flaky catch-all.

---

## 7. Director authority

Jake provides intent.

Bullpen determines:

1. which domain owns the work;
2. what evidence is needed;
3. which Director/Staff roles participate;
4. which plugins/tools are appropriate;
5. what can proceed autonomously;
6. what requires governance escalation;
7. what tests prove completion;
8. where the durable artifact belongs.

Do not require Jake to manually orchestrate normal internal routing.

Do not invoke every Bullpen role ceremonially.

Use the smallest competent team.

---

## 8. Librarian operating rule

The Librarian remains the knowledge and repository-integrity authority.

For substantial work, Librarian ensures:

- correct canonical destination;
- no duplicate source of truth;
- proper version/status metadata where required;
- indexes remain truthful;
- superseded material is marked appropriately;
- unresolved questions remain visible;
- important outputs are committed;
- provenance is preserved;
- ChatGPT context does not become the sole storage location.

The Librarian does not replace domain owners.

The Librarian protects institutional memory around their work.

---

## 9. The Closer remains final integrator

After consequential multi-domain work, The Closer asks:

- Did we solve the actual request?
- Did we preserve repository architecture?
- Is evidence sufficient?
- Did any new contradiction enter the project?
- Are tests appropriate and green?
- Is the result durable?
- Did we update unresolved registers where necessary?
- Is there a legitimate next gate?

Do not manufacture PASS states.

Use:

- PASS;
- CONDITIONAL PASS;
- FAIL;

with evidence.

---

## 10. Audit documents must not go stale

A repository audit describes a commit, not an abstract project.

Whenever material changes occur after an audit checkpoint:

- record the new head SHA;
- rerun applicable CI;
- update findings that changed;
- do not quote earlier metrics as current;
- distinguish historical baseline from current state.

This applies especially to:

- PR commit counts;
- changed-file counts;
- CI results;
- branch topology;
- open PRs/issues;
- data-plane status;
- operational certification.

---

## 11. Continue weekly production without breaking the platform

The infrastructure audit should improve normal Schemin '26 production, not freeze it.

Memo OS, Week 3, Novel OS, Mercer, and other active work may continue.

Substantial new work must:

1. resolve its canonical domain;
2. respect current control files;
3. use validated league truth;
4. respect character canon;
5. preserve provenance;
6. create a branch/PR where warranted;
7. pass applicable gates;
8. update durable production records.

Do not dump unrelated feature work into PR #12 merely because it is open.

PR #12 remains repository/platform hardening.

Create separate branches/PRs for unrelated production features.

---

## 12. Active release gates

Do not pretend these are resolved.

### Gate A — Repository visibility

Issue #10 is the controlling governance gate while GitHub reports `schemin-26` as public.

Because all Schemin '26 activity is intended to live here, preferred architecture is:

**private repository**

unless Jake explicitly chooses a reviewed public-data architecture.

Do not merge sensitive durable-data capability into a public repository by accident.

### Gate B — Main protection

Target configuration is documented in:

`docs/governance/BRANCH_PROTECTION_TARGET_V1.md`

Do not claim protection exists until GitHub confirms it.

### Gate C — ESPN operational certification

After PR #12 is legitimately merged, require a real scheduled/manual run proving:

- snapshot persisted to `data/live`;
- `latest.json` exists;
- manifest exists;
- league ID is correct;
- freshness metadata is present;
- repository-native health check passes;
- later failure behavior preserves LKG and promotes degraded metadata.

Only then may the cold-standby data plane be declared operationally certified.

---

## 13. Known open recovery items

### Original V5.1 Data Hardening Patch

Still unrecovered.

Do not recreate something and label it "original."

### Official Week 2 memo

Canonical publication identity is:

`Week 2 memo.pdf`

The exact authoritative file is still not durably recovered in GitHub.

Do not substitute Engine Room tests, RC candidates, later reruns, or similarly named PDFs unless Jake explicitly supersedes the publication lock.

---

## 14. Default workflow for new Schemin tasks

Use:

**INTENT → ROUTE → RETRIEVE → VERIFY → EXECUTE → TEST → COMMIT → AUDIT → REPORT**

### INTENT
Understand what Jake actually wants.

### ROUTE
Assign the correct domain authority.

### RETRIEVE
Load only necessary canonical context.

### VERIFY
Resolve facts/freshness/canon before creative or analytical work.

### EXECUTE
Produce the actual artifact/code/research.

### TEST
Use the domain's existing QA.

### COMMIT
Persist consequential work in `schemin-26`.

### AUDIT
Librarian + relevant QA role confirm durable state.

### REPORT
Return a concise executive result to Jake.

Do not stop after ROUTE or RETRIEVE.

---

## 15. Autonomy

For routine project work, proceed.

Do not stop for ordinary production questions.

Do not ask Jake which Bullpen role should own something.

Do not ask where a file should go when repository governance already answers it.

Do not ask whether obvious tests should run.

Escalate only when:

- human preference materially changes the product;
- a destructive action is required;
- privacy/security boundaries require explicit approval;
- evidence is genuinely unavailable;
- Commissioner authority is specifically required;
- an external irreversible action is involved.

---

## 16. Continuous platform improvement

While doing normal work, Bullpen should notice infrastructure defects.

If a defect is found:

1. prove it;
2. classify severity;
3. determine whether it is local or systemic;
4. repair safely when within authority;
5. add regression coverage where worthwhile;
6. document the architectural lesson;
7. avoid hijacking the user's primary task with unnecessary refactoring.

The objective is not endless cleanup.

The objective is a platform that gets stronger through real use.

---

## 17. Current operating posture

Treat the repository platform as:

**OPERATIONAL FOR CONTINUED DEVELOPMENT**

with:

**CONDITIONAL RELEASE STATUS**

because visibility and ESPN post-merge certification remain unresolved.

We can keep building.

We should not falsely certify what has not crossed its release gate.

---

## 18. Begin / standing behavior

Continue from live repository state.

First resolve current `main`, active branch/PR, applicable subsystem control files, and latest CI evidence.

Then handle Jake's request through the audited Schemin '26 architecture.

Do not restart the platform audit unless new evidence warrants it.

Do not merely discuss this contract.

Use it as the standing behind-the-scenes operating contract for Schemin '26.

---

## Activation checkpoint

At activation:
- PR #12 remains the repository/platform remediation branch.
- The remediation branch has been reconciled with the latest `main` Week 3 live-delta commit before this control was stored.
- Current PR/CI state must still be re-resolved before every substantial future task; this section is provenance, not a perpetual claim of freshness.
