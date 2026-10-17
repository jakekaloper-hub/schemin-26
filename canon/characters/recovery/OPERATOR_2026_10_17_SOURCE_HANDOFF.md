# Bullpen CHAR-PORT-002 — recovered source-byte deployment handoff

**State: LOCAL 12/12 SOURCE-IDENTITY PASS; GITHUB 12/12 PRIMARY STORAGE NOT YET VERIFIED; RENDERER STILL HOLD.**  
**Authority:** Existing Schemin Character Canon, Bullpen #133, draft PR #195. This is not a new OS, identity redesign or request for photographs.

## Discovery and evidence

On 2026-10-17, authorized Desktop Commander access to the connected Mac found the existing `~/Downloads/schemin26_12_character_reference_packet_20261012.zip`. It contained **twelve image binaries, one per canonical Character ID**, and `CHARACTER_UPLOAD_RECEIPTS.json`.

Fresh streaming SHA-256 from the ZIP matched the embedded uploaded-byte receipts for **12/12**, byte counts for **12/12**. The ZIP itself had SHA-256 `e132398eeb422fb859a756ccd2c461c4287c34960cb42c561654c7a2c4f2130a`.

An isolated recovery folder on the Mac holds all 12 extracted binaries, the same pinned source lock and the exact importer used in this PR. The importer was actually executed against the recovered ZIP in both verification and local-stage modes and passed 12/12, with fresh local readback. The immutable hash/Git-blob receipts are in `COMMISSIONER_2026_10_12_INGEST_RECEIPT.json`.

**Authority exception:** Austin Byars and Phillip Pitts are byte-identical to previously registered Sept 29 primary images. The other **ten October 12 Commissioner-supplied PNG references have distinct SHA-256s** from the Sept 29 approved JPEGs. They are genuine Oct 12 *source images*, but an exact-byte check cannot by itself assert that they are the same old binary or that the old visual-source registry has been superseded. Keep temporal/version provenance, do not silently overwrite the prior manifest.

## Why the direct push is not yet green

The authorized ChatGPT Library file handles were readable as metadata but denied raw-byte export. On the connected Mac the recovered 12 originals were readable; attempted direct cross-tool binary transmission into GitHub was disallowed by the connection safety boundary. Therefore this PR contains executable importer and authentic **text-only hash receipt**, not the JPEG/PNG binary payloads. Do not equate the receipt to a GitHub-stored binary.

## Repository-native import from the existing Mac archive

Use an isolated Git worktree; do **not** change the user's existing checkout, which already contains unrelated uncommitted work. The following is an operator runbook, not an instruction that has already executed:

```bash
set -euo pipefail
PROJECT="$HOME/Desktop/AI Project/schemin-26"
BRANCH="bullpen/next-2026-10-17-char-w6-reconcile"
WORKTREE="$HOME/Projects/schemin-character-upload-worktree-20261017"
ARCHIVE="$HOME/Downloads/schemin26_12_character_reference_packet_20261012.zip"

git -C "$PROJECT" fetch origin "$BRANCH"
git -C "$PROJECT" worktree add -b character-bytes-20261017 "$WORKTREE" "origin/$BRANCH"

python3 "$WORKTREE/canon/characters/recovery/ingest_commissioner_packet.py" \
  --archive "$ARCHIVE" --root "$WORKTREE" --stage

git -C "$WORKTREE" add canon/characters/assets canon/characters/recovery/COMMISSIONER_2026_10_12_INGEST_RECEIPT.json
git -C "$WORKTREE" diff --cached --stat
git -C "$WORKTREE" commit -m "fix(canon): persist 12 verified Commissioner reference binaries"
git -C "$WORKTREE" push origin "HEAD:refs/heads/$BRANCH"
```

**If the branch has advanced since fetch, STOP rather than force-push**; refresh/rebase before any retry. Require authenticated GitHub write access. No private credential contents, signed URLs or new photo uploads should appear in logs.

## Full acceptance gates after binary push

1. GitHub main/PR new commit readback: 12 exact uploaded-byte paths, Git blob IDs matching receipt, sizes, hashes (actual binaries).
2. Ten divergent October 12 visual-source versions reconciled against the existing 12-owner manifest/Commissioner visual locks with explicit version or supersession decisions. No wrong-character active mapping.
3. Machine/renderer fresh-context retrieval. Subject-slot identity binding evidence, not just image presence.
4. C1 12 independent character subject/crop comparison proof; then multicharacter contamination testing, actual independent Umpire T15, dependent T16.
5. Memo Week 6 only generates character-bearing final art after proven reference identity and output QA.

**Do not ask the Commissioner to resupply any of the twelve.** The bytes are already accessible through the recovered ZIP.
