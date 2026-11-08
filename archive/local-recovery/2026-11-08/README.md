# Local recovery — 2026-11-08

Owner: Bullpen Librarian. Canonical store: `jakekaloper-hub/schemin-26`.

This is preservation, **not** a new Memo OS or proof of historical review, rendering, source acceptance, or publication. Archived workers/scripts are not registered, scheduled, or executed. `PASS`, `approved`, and similar claims inside historical payloads remain historical unverified assertions.

`MANIFEST.json` maps each local source to a byte-verified repository destination or an explicit exclusion. Files already present on main are linked rather than duplicated. Source copies are retained until remote-main readback. Raw Week9 direction consultations were copied into the existing `memo-os/week-9/production-evidence/direction-2026-11-08/` lane. Unreal first-party bridge/config/custom maps reside under `world/atlas/integration/unreal-prototype/`.

Excluded: TLS keys/certificates, `.env`/credentials, dependencies, OS metadata, engine caches/builds, unreviewed third-party Unreal template assets and their external actor files. Existing Unreal contract also excludes exported images/videos. These excluded local files are not deleted. This is not a claim that the entire Unreal installation/project is now reproducible from GitHub alone.

Librarian software-role advisory is saved as `LIBRARIAN_STORAGE_ADVISORY.json`; advice was checked against files. Final remote verification and retirement outcomes belong in the closeout receipt.

Next work after storage: continue existing Week9 P05 golf collage and P20 paintball proof-page inputs, preserving all production gates.

## Unpushed branch history

Two Week7 branches were neither reachable from current main nor present as remote heads. Their unique commits are preserved as incremental Git bundles, verified against the available main-history prerequisites; hashes are in WORKTREE_REACHABILITY.json. To recover, use a full clone of the canonical repository, `git bundle verify <bundle>`, then `git fetch <bundle> <recorded branch>:refs/heads/recovered/<branch-name>`. Do not merge this historical code into active production automatically.

Raw historical logs/configurations retain source whitespace byte-for-byte. Whitespace-only `git diff --check` warnings in these recovered payloads are intentionally not normalized, because normalization would destroy their source hashes. Newly authored indexes/receipts are checked separately.

## Completed preservation / cleanup

PR #283 merged at `0199166f4d7851fb1e5db96380c63a1098594266`. All 275 source mappings and both history bundles were read back from that fetched main commit with matching hashes. [CLOSEOUT.json](./CLOSEOUT.json) records the five retired folders and retained working installations. Untracked originals and standalone staged folders went to recoverable Trash only after verification; no forced worktree removal or branch deletion was used. The active Week9 continuation is the same existing worktree, not an additional folder.
