# Character Visual Reference Authority — Incident Repair V1

**Date:** 2026-10-01
**Status:** ACTIVE FAIL-CLOSED SAFETY LAYER
**Incident class:** authority-routing / stale-reference leakage

## Root cause

Schemin had correct semantic canon and a strong mount/binding firewall, but there was still an upstream gap:

**a renderer asset could look authoritative because of its filename, tag, prompt or composite placement without proving byte lineage to the current Commissioner-approved source.**

That allowed a generated convenience image named like `CANON_*_ACTIVE_REF` to be mistaken for source authority.

## Correct law

`Character ID → current Commissioner source record → expected SHA-256 → actual renderer input bytes → mount receipt → subject binding → generation eligibility → render → independent Character QA`

No earlier shortcut is valid.

## What is no longer authority

The following are never production identity authority by themselves:

- the 12-character master lineup;
- generated “canon” previews;
- rendered comparison sheets;
- old Memo/Novel character matrices;
- historical pages;
- filenames containing CANON or ACTIVE;
- Creative Claw tags;
- prompt text;
- team names.

## Master-lineup status

The current lineup plate is **PARTIAL_STALE_REFERENCE_ONLY**.

It is stale for:
- Wilson Look — current Arsenal Gorilla Warrior supersedes centaur;
- Phillip Pitts — current one-body / three-serpent-head lock;
- Austin Byars — current Commissioner Belt Keeper source outranks the panel.

The lineup may remain for historical/human convenience, but it cannot seed character-bearing generation.

## Current three source authorities

- Wilson Look: `IMG_7866(1).jpeg`, SHA-256 `d6279c5c...`
- Phillip Pitts: `IMG_2178.jpeg`, SHA-256 `31b9d7be...`
- Austin Byars: `IMG_2179.jpeg`, SHA-256 `eedfaaf0...`

## Overview rebuild rule

A corrected 12-character overview is useful, but it is a **derived convenience artifact**.

It may be rebuilt only from the current 12 owner-scoped source records. It must carry:
- source Character ID;
- source SHA-256;
- source version;
- generated overview hash;
- explicit `DERIVED_OVERVIEW_NOT_PRIMARY_AUTHORITY` status.

If any of the 12 exact source bytes cannot be resolved, overview rebuild is BLOCKED rather than inferred from prose.

## Current external gate

The exact Commissioner files remain visible in Library search, but this execution context cannot materialize the three required raw files into a renderer/container path. Therefore:
- do not ask Jake for all 12 again;
- do not synthesize replacements from descriptions;
- do not use the stale lineup as fallback;
- keep character-bearing generation blocked for any unresolved source input.

## Immediate consequence

The current LLC × HMB publication-fidelity fixture is **REJECTED / NON-AUTHORITATIVE CHARACTER TEST** because its HMB input did not prove lineage to the active `IMG_2179.jpeg` source.

The page-concept work may survive; its character render does not.
