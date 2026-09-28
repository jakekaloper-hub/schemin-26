# Schemin '26 — Repository Synchronization Playbook

**Document class:** runbook  
**Authority / owner:** The Librarian  
**Version:** 1.0  
**Status:** ACTIVE  
**Effective date:** 2026-09-27  
**Review cadence:** monthly during the season and after major production changes

## Durable-work rule

Material Schemin '26 work is not durable until it is either:
1. committed to `jakekaloper-hub/schemin-26` in its canonical domain; or
2. explicitly registered as ephemeral, external, blocked, or unresolved.

A ChatGPT thread, plugin result, local draft, generated image, or upstream repository copy is not by itself durable Schemin state.

## Standard handoff

For material work:

1. **Identify** — state the artifact and domain.
2. **Resolve authority** — load `PROJECT_CONTROL_REGISTRY.md` and the domain index/control.
3. **Classify evidence** — verified fact, canon, interpretation, production asset, generated output, decision, or transient work.
4. **Choose canonical path** — use the existing subsystem; do not create parallel architecture casually.
5. **Validate** — run applicable canon/data/schema/build/test/QA gates.
6. **Commit** — use a meaningful atomic commit.
7. **Record provenance** — source, date/week, upstream dependency, version, and validation where material.
8. **Update indexes** — only when authority/navigation changed.
9. **Preserve SHA/PR** — consequential changes should be traceable.
10. **Close the loop** — supersede stale guidance and update unresolved registers.

## ChatGPT/Bullpen session start

For substantial work load, in order:
1. `PROJECT_CONTROL_REGISTRY.md`
2. `docs/governance/SOURCE_OF_TRUTH.md`
3. the relevant subsystem `README.md` / `_INDEX.md`
4. current week/production register if applicable
5. unresolved/blocker register for the workstream

## External repository changes

When Schemin exposes a reusable FLA/platform defect:
1. document the Schemin requirement here;
2. perform the reusable change upstream;
3. record upstream repo + PR/commit here;
4. keep league-specific state here;
5. test Schemin integration before calling the capability operational.

Do not mirror entire upstream repositories into Schemin.

## Generated artifacts

Generated media/PDF/output must have:
- canonical purpose;
- source inputs;
- producing workflow/tool when material;
- version/state;
- QA/release state;
- canonical path or registered external storage reference.

A generated artifact is not "official" merely because it exists.

## Weekly Memo special rule

Week-specific evidence, continuity, source snapshots, Fact Lock materials, page/QA registers, and publication records belong under the canonical Memo OS weekly production structure.

Published editions are immutable historical artifacts. Re-tests/reruns never silently replace them.

## Data special rule

Fresh/live claims require freshness metadata. Scheduled data acquisition must have both:
- successful acquisition/validation evidence; and
- proof that the durable snapshot was actually persisted.

Green CI without durable output is insufficient.

## Monthly Librarian sweep

Check:
- control/index paths still exist;
- open production PRs have dispositions;
- active docs reflect controlling versions;
- new domains have owners;
- missing canonical artifacts are registered;
- stale copies are marked/superseded;
- CI still validates the claims it is cited for;
- public/private boundary remains appropriate.

## Local workspaces

GitHub state does not prove a developer laptop is clean. If a local clone matters, attest it through an authorized filesystem/desktop environment and record status separately.
