# Schemin '26 — Repository Integrity Sweep Control

**Authority / owner:** The Librarian (CKO), with The Closer as final cross-domain auditor  
**Version:** 1.0  
**Status:** ACTIVE CONTROL FOR 2026-09-27 SWEEP  
**Effective date:** 2026-09-27  
**Review trigger:** completion of the sweep, repository visibility disposition, or material repository-boundary change  
**Supersedes:** none

## Purpose

This control adapts the Master GitHub Repository Integrity, Sync & Provenance Sweep to the actual Schemin '26 repository architecture.

## Canonical project home

`jakekaloper-hub/schemin-26` is the single durable operating repository for Schemin '26 project activity.

All league-specific durable work belongs here unless a controlling document explicitly classifies it as:
- upstream reusable platform work;
- external dependency evidence;
- generated/transient output;
- deliberately private material that cannot safely live in the current repository visibility state.

## External repository rule

External repositories such as `jakekaloper-hub/fantasy-league-artworks` and `jakekaloper-hub/bullpen` are upstream capability/reference sources, not alternate canonical homes for Schemin '26 state.

When an external reusable change is required:
1. record the Schemin requirement in this repository;
2. make the reusable change upstream under that repository's governance;
3. record the upstream commit/PR reference here;
4. keep league-specific configuration, evidence, canon, production state, and release decisions in `schemin-26`.

## Sweep lifecycle

DISCOVER → BASELINE → INVENTORY → CLASSIFY → RECONCILE → RECOVER → REPAIR → TEST → SECURITY → CI → COMMIT → VERIFY → AUDIT → REPORT

## Evidence discipline

A PASS claim requires a file path, commit SHA, test output, CI run, diff, configuration, repository metadata, or reproducible command/result.

Conversation history can help locate work but is not durable project state until represented or explicitly classified in this repository.

## Local workspace limitation

The current ChatGPT/GitHub connector runtime can attest GitHub state but cannot attest an arbitrary developer machine's local clone. Local workspace cleanliness must therefore be recorded as `NOT_ATTESTABLE_FROM_CURRENT_RUNTIME` unless an authorized filesystem/desktop connector is used.

## Security gate

At sweep start, GitHub reports this repository as public. Issue #10 tracks the required visibility/private-material disposition.

Until that gate is resolved, no credentials, private ESPN cookies, private messages, personal data, or sensitive Mercer-only intelligence should be committed here.

## Completion authority

The Librarian owns artifact/index integrity. The Architect owns structural findings. The Umpire validates claims. The Warden owns security findings. Groundskeeper/Setup Man own CI/reproducibility. The Analyst owns before/after metrics. The Closer issues the final PASS / CONDITIONAL PASS / FAIL.
