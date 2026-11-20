# Repository Health — Visibility, Not Promotion

This folder provides the discoverability layer for the current GitHub repository.

- **BRANCH_VISIBILITY_LEDGER.md**: current branch and PR listing committed to main, showing draft, review, merged and untracked states. It is a *derived inventory*, not a release or canon authority.
- **UNLINKED_BRANCH_TRIAGE_2026_11_20.md**: evidence-backed comparison and disposition for each of the 24 branch names without a matching PR in the dated snapshot.
- **AUDIT_2026_11_20.md**: 30-day audit summary and outstanding release/deployment gates.
- **visibility.py**: read-only GitHub REST inventory generator; it never merges, deletes, rebases, changes protection, or alters production metadata. Python standard library only.
- **test_visibility.py**: verifies visible stacked PRs, orphan branches, merged branches and fork semantics.
- **.github/workflows/repository-visibility.yml**: daily UTC or manual refresh generates only derived Markdown and proposes it through a **draft PR**. The workflow must never push directly to `main`; approval, required CI and branch rules control promotion. A GitHub setting that disallows GitHub Actions from creating PRs must produce an explicit failed run rather than a bypass.
- **test_workflow_safety.py**: guards against restoring direct-main pushes or exposing token write permission to PR jobs.

GitHub-created PRs using the default `GITHUB_TOKEN` may not automatically trigger all normal `pull_request` CI checks. An authorized reviewer must trigger/verify the relevant exact-head checks before merging a proposed ledger update. Do not auto-approve the bot's own proposal.

**Bullpen routing:** The Librarian owns inventory/provenance, The Setup Man owns workflow reliability, The Umpire independently challenges release-state inflation, and The Closer owns cross-domain resolution. These are domain ownership lenses; this file does not assert authenticated autonomous Director execution.

**Promotion boundary:** New work belongs on main only after applicable release, canon, provenance and exact-head validation. Draft branches must be visible, not mass-merged. Never interpret a successful workflow or listed branch as publisher acceptance.

**Audit start:** 2026-10-21 through 2026-11-20. The inventory enumerates all currently reachable branches so older orphan work is not silently excluded.
