# Week 4 Prepublication Hardening — FLA Anti-Regression Addendum

**Status:** BINDING FOR WEEK 4 READINESS REVIEW  
**Purpose:** prevent Schemin-26 from repeating control failures observed in the private Fantasy League Artworks repository.

## Why this exists

The Week 4 publication system must not confuse:
- documented intent with enforced behavior;
- a green checklist with a proven execution path;
- caller-supplied observations with independent QA;
- an unmerged hardening patch with active protection;
- a successful component with end-to-end readiness.

The FLA repository contains examples of these failure classes, including:
- false-green behavior from checks that could miss untracked state;
- QA that trusted caller observations rather than independently proving output state;
- hardening work that existed but was not yet merged/active;
- real multi-character identity-preservation failure despite surrounding control language.

These are treated here as anti-patterns.

## Schemin-26 anti-regression rules

### 1. No documentation-only PASS
Markdown can explain a gate. It cannot satisfy the gate.

### 2. No caller-trust QA
A producer may submit evidence, but Umpire/validator must independently inspect the controlled artifact or machine receipt.

### 3. No unmerged-control assumption
A protection is not active merely because it exists on a branch or PR. Active authority must be explicit.

### 4. No false-green from incomplete state inspection
Validators must inspect the complete controlled manifest/artifact set, not only changed/tracked subsets.

### 5. No component-pass equals system-pass
A page can pass Character QA and still fail Publication Design or Continuity QA. A subsystem PASS does not imply release readiness.

### 6. No stale PASS reuse
Evidence must be bound to current bytes/state/freshness. Historical PASS cannot silently satisfy current Week 4.

### 7. No bypass around the production graph
Every page must traverse:
fact/world/character authority → validated packet → render eligibility → output QA → page lock → assembly → Umpire → release transaction.

### 8. No hardening deferred past publication
Any internally solvable bypass discovered before release is a publication blocker until fixed/tested or explicitly classified as an external capability hold.

## Week 4 enforcement implication

The target state is not "mostly ready."

It is:

**WAITING_ON_MNF / PUBLICATION PIPELINE HARDENED / INTERNAL CONTROLS PASS / EXTERNAL HOLDS EXPLICIT**

Anything less is HOLD.
