# Bullpen Full Lifecycle — Novel Author Consulting Program V2 Hardening

**Date:** 2026-10-01  
**Lifecycle:** status → research → spec → premortem → plan → execute → test → verify → audit → redteam → polish → retest → reconcile → handoff → retro → next  
**Status:** COMPLETE / ALL REQUIRED GATES PASS

## /bullpen status

Starting authority:
- Novel External Advisory Council V1 — RELEASED / ACTIVE.
- Author Consulting Program V2 — RELEASED / ACTIVE.
- Core Seven — active.
- Advisor/source registry tests — active.
- Four-round consulting charter — active.

## /bullpen research

Repository inspection found:
1. no executable resolver for named authors;
2. no executable resolver for named panels;
3. no deterministic default for generic "call the consultants";
4. no executable engagement-freeze builder;
5. no manifest validator enforcing evidence cutoff / independence;
6. panel composition existed only in documentation and would drift if duplicated in code.

## /bullpen spec

Required behavior:
- explicit author name routes to that author only unless a broader explicit council request is authoritative;
- named panels resolve deterministically;
- major book-architecture triggers may escalate to Full Seven;
- generic consultation uses the smallest general chapter-triage panel, not Full Seven;
- engagement selection must be frozen to a commit + temporal cutoff + decision question;
- pre-lock consultant cross-reading is forbidden;
- machine registry owns panel composition;
- CI must fail if routing or manifest rules regress.

## /bullpen premortem

Failure modes considered:
- every generic request invokes seven consultants and creates noise;
- different chats produce different panel membership;
- a panel changes in docs but runtime silently remains stale;
- a "full council" engagement omits one Core Seven seat;
- consultation begins without an evidence cutoff;
- advisors cross-read too early and synthetic consensus replaces independence;
- unknown consultant IDs enter an engagement;
- engagement routing works in prose but is not regression-tested.

## /bullpen plan

1. add repository-native deterministic router;
2. add canonical panel definitions to the machine registry;
3. make router consume registry rather than duplicate membership;
4. add engagement-manifest builder/validator;
5. add adversarial routing tests;
6. run router tests inside Novel OS CI;
7. audit against Author Council charter and advisory authority;
8. reconcile docs/index after proof.

## /bullpen execute

Implemented:
- `author-council/author_router.py`;
- `author-council/test_author_router.py`;
- Advisor Registry v2.1 panel definitions + aliases + default panel;
- Novel OS CI author-router gate.

Canonical panels:
- chapter triage;
- world depth;
- story architecture;
- POV / character;
- pacing / readability;
- fantasy logic;
- epic fantasy integrity;
- Full Seven via Core Seven registry.

## /bullpen test

Required test cases:
- explicit Grisham;
- multiple explicit authors;
- POV panel exact membership;
- Full Seven exact Core Seven order;
- book architecture escalation;
- generic consultation → three-seat chapter triage;
- registry owns panel composition;
- engagement manifest freezes evidence;
- missing evidence fails;
- pre-lock cross-reading fails.

## /bullpen verify

Acceptance criteria:
- existing Novel OS deterministic/adversarial tests remain green;
- advisor registry contract remains green;
- author-router suite green;
- Repository Merge Gate green;
- Bullpen Runtime CI green.

## /bullpen audit

Authority audit:
- router selects advisors only;
- router cannot promote canon;
- router cannot mutate manuscript/world/character state;
- engagement manifest records evidence and independence;
- author/source authority remains in registry;
- Novel OS / Author Room remain upstream.

## /bullpen redteam

Adversarial questions:
- Can "call the consultants" explode into Full Seven? **No; defaults to chapter triage.**
- Can a hard-coded panel drift from registry? **No; router consumes registry composition.**
- Can Full Seven differ from Core Seven? **Manifest validation and tests reject it.**
- Can an engagement omit temporal evidence? **Validator rejects it.**
- Can consultants cross-read before independent lock? **Validator rejects it.**
- Can a non-existent consultant enter the manifest? **Validator rejects it.**

Residual risk:
- public source URLs may later move or disappear; current CI validates registered provenance shape, not remote URL reachability.
- natural-language routing remains bounded heuristics; explicit names and panel commands are the deterministic preferred surface.

## /bullpen polish

Polish decisions:
- registry is the single machine authority for panel membership;
- the default panel is explicit in registry;
- router output includes selection mode, panel and reason for traceability;
- generic consults are intentionally narrow.

## /bullpen retest

Final pre-close proof on PR #69 head:
- Novel OS CI #318 — PASS;
- Repository Merge Gate #93 — PASS;
- Bullpen Runtime CI #2491 — PASS.

Novel OS CI includes:
- existing deterministic/adversarial Novel suite;
- advisor registry contract;
- deterministic Author Council router suite.

## /bullpen reconcile

No canon conflict introduced.

Reconciled hierarchy:
Bullpen command intent → Author Council router → frozen engagement manifest → independent consultant rounds → Bullpen reconciliation → existing Novel OS / canon gates.

## /bullpen handoff

Future session entry:
1. read `author-council/_INDEX.md`;
2. resolve advisor selection through `author_router.py`;
3. freeze an engagement before Round 1;
4. never infer panel membership independently of registry.

## /bullpen retro

Lesson:
A consulting program is not operational merely because dossiers and procedures exist. The selection decision and evidence freeze must themselves be executable, canonical and regression-tested.

## /bullpen next

**CLOSED.**

All required gates passed. No justified consulting-infrastructure work remains inside this lifecycle.

The next legitimate Novel step is an **actual consultant engagement against current manuscript/book architecture**, using the now-active router and frozen engagement manifest. Infrastructure expansion should occur only if a real engagement exposes a demonstrated gap.
