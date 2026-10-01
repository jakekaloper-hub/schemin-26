# ADR-004 — PLUGINS ARE REPLACEABLE, UNFUNDED-BY-DEFAULT ADAPTERS
**Status:** ACCEPTED / COST RECONCILED 2026-10-01

## Decision

Provider capability is separate from provider funding.

The Schemin baseline assumes only the user's existing ChatGPT Plus membership. GitHub/Flaim may be used at their already-available access level; no paid upgrade is implied.

Creative Claw, Higgsfield, OpenArt, Runway, Adobe paid services, fal.ai, Replicate, ElevenLabs, Cartesia and future metered providers are **UNFUNDED_EXTERNAL** unless Jake explicitly approves incremental spend.

## Rule

Provider failure, expired credits, trial exhaustion, account-plan limits, or lack of subscription must never corrupt or block canonical Schemin state.

Canon/reference packets, world state, release evidence, publication manifests, production manifests and QA exist independently of provider-specific assets.

Every critical workflow must either:
1. execute through the zero-incremental-spend baseline;
2. degrade to a supported native/local path; or
3. HOLD without falsely claiming completion.

## Character-specific rule

A provider-specific asset name, tag or ID is evidence only. It cannot substitute for the Commissioner-approved source hash and cannot become visual identity authority by convenience.
