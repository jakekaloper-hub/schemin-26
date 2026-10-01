# SCHEMIN ’26 — RENDERING PROVIDER PHASE 0 DECISION

**Date:** 2026-10-01  
**Status:** PHASE 0 COMPLETE / ARCHITECTURE DECIDED  
**Decision owner:** Bullpen — Closer + Architect  
**Counterweights:** Umpire + Warden + Librarian + Groundskeeper  
**Scope:** rendering-provider strategy only; no production renderer is activated by this decision.

## Executive decision

Schemin will be **provider-neutral and renderer-optional at the project architecture level**.

No paid or credit-metered third-party plugin is allowed to become a required dependency for:

- Character Canon;
- character reference authority;
- World / Atlas authority;
- Weekly Memo production state;
- Living Novel production state;
- Publication Manifest;
- release evidence;
- Story Lock;
- Page Lock;
- publication eligibility.

Creative Claw is therefore **NOT an official Schemin production dependency**.

It may be used only as optional/ad-hoc tooling when explicitly available and useful. Its absence must never block canonical Schemin work.

## Why

A required paid renderer would couple Schemin production readiness to:
- credit balance;
- vendor pricing;
- account state;
- provider availability;
- provider-specific attachment semantics;
- provider-specific asset storage.

Those are infrastructure concerns, not Schemin authority.

The project must remain able to:
- ingest evidence;
- resolve canon;
- build page/scene packets;
- validate character/world authority;
- prepare render requests;
- run QA;
- preserve publication state;
- defer rendering safely;

without purchasing rendering credits.

## Architecture law

```text
SCHEMIN AUTHORITY
  ↓
PROVIDER-NEUTRAL RENDER REQUEST
  ↓
OPTIONAL EXECUTION ADAPTER
  ↓
ARTIFACT + EXECUTION RECEIPT
  ↓
SCHEMIN QA
  ↓
PUBLICATION GATE
```

The adapter is replaceable.

The authority, request contract, and QA are not.

## Provider classes

### A. REQUIRED CORE
None.

There is no required external renderer.

### B. OPTIONAL EXTERNAL PROVIDER
Examples may include:
- Creative Claw;
- Runway;
- OpenArt;
- future image/video providers.

Rules:
- optional;
- disabled by default;
- no authority ownership;
- no canon promotion;
- no source-of-truth storage;
- no release authority;
- project remains functional without them.

### C. OPTIONAL LOCAL / SELF-HOSTED EXECUTION
Future candidate.

May include:
- local image/video tooling;
- code-driven composition;
- self-hosted model/runtime;
- deterministic HTML/raster composition.

Promotion requires separate security, quality, runtime-cost, and maintainability review.

### D. NO-RENDER MODE
First-class supported state.

If no eligible renderer exists:
- render request may still be compiled;
- generation state = `GENERATION_BLOCKED` or `RENDER_DEFERRED`;
- no canon is lost;
- no publication state is corrupted;
- task may continue through all non-rendering stages.

## Character-reference consequence

Character authority is provider-independent.

The mandatory chain is:

`CHARACTER ID → APPROVED SOURCE HASH → AUTHORITY RECEIPT → PROVIDER-NEUTRAL MOUNT INTENT → OPTIONAL ADAPTER → MOUNT/BINDING RECEIPT → RENDER → CHARACTER QA`

A provider may transport the bytes.

It may not decide which bytes are canon.

## Asset-store consequence

No provider media library is canonical storage.

Creative Claw asset names, tags, URLs, generated previews, and composites are convenience metadata only.

The authoritative identity remains:
- Character ID;
- source filename/provenance;
- approved SHA-256;
- explicit Commissioner supersession state.

## Cost doctrine

Before any external renderer can be recommended for repeat production, its adapter must expose:
- expected monetary cost;
- cost unit;
- free/local fallback state;
- failure behavior;
- retry ceiling;
- cancellation path.

A workflow that silently consumes credits is not production-safe.

## Phase 0 acceptance criteria

Phase 0 is complete when:

1. no paid provider is required by project control;
2. Render Adapter contract is provider-neutral;
3. character authority is independent of provider asset names;
4. no-render mode is explicitly supported;
5. provider-specific receipts are adapter outputs, not project truth;
6. cost/failure semantics are part of provider admission;
7. Creative Claw is classified OPTIONAL / NON-AUTHORITATIVE;
8. CI proves no provider becomes required by configuration drift.

## Phase 0 result

**PASS.**

## Phase 1 recommendation

Do not select a new provider yet.

Next build should be:

**Provider-Neutral Render Adapter Baseline**

Deliverables:
- stable provider interface;
- no-render adapter;
- local deterministic composition adapter;
- optional external adapter interface;
- cost/capability registry;
- character-source authority integration;
- adapter conformance tests;
- one closed historical render fixture.

Only after that baseline should Bullpen compare any actual renderer providers.
