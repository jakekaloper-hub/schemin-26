#!/usr/bin/env bash
set -euo pipefail

LEAGUE_ID="${LEAGUE_ID:-1417621}"
REMOTE="${SCHEMIN_DATA_REMOTE:-origin}"
BRANCH="${SCHEMIN_DATA_BRANCH:-data/live}"
SNAPSHOT_SRC="${SCHEMIN_SNAPSHOT_SRC:-data/snapshots/${LEAGUE_ID}}"
VERIFY_REF="refs/remotes/${REMOTE}/schemin-data-live-verify"
ROOT="$(git rev-parse --show-toplevel)"

cd "$ROOT"

if [[ ! -f "$SNAPSHOT_SRC/latest.json" || ! -f "$SNAPSHOT_SRC/manifest.json" ]]; then
  echo "No complete snapshot state exists; nothing durable can be persisted."
  exit 0
fi

if git ls-remote --exit-code --heads "$REMOTE" "refs/heads/$BRANCH" >/dev/null 2>&1; then
  git fetch "$REMOTE" "+refs/heads/$BRANCH:refs/heads/$BRANCH"
else
  git branch "$BRANCH" HEAD
  git push "$REMOTE" "refs/heads/$BRANCH:refs/heads/$BRANCH"
fi

WORKTREE="$(mktemp -d)"
VERIFY_DIR="$(mktemp -d)"
cleanup() {
  git worktree remove --force "$WORKTREE" >/dev/null 2>&1 || true
  rm -rf "$WORKTREE" "$VERIFY_DIR"
}
trap cleanup EXIT

git worktree add "$WORKTREE" "$BRANCH" >/dev/null
rm -rf "$WORKTREE/data/snapshots/$LEAGUE_ID"
mkdir -p "$WORKTREE/data/snapshots"
cp -R "$SNAPSHOT_SRC" "$WORKTREE/data/snapshots/$LEAGUE_ID"

(
  cd "$WORKTREE"
  git add "data/snapshots/$LEAGUE_ID"
  if git diff --cached --quiet -- "data/snapshots/$LEAGUE_ID"; then
    echo "Snapshot state unchanged; durable branch already matches."
  else
    git config user.name "schemin-data-gateway"
    git config user.email "actions@users.noreply.github.com"
    git commit -m "data: refresh ESPN $LEAGUE_ID snapshot" >/dev/null
    git push "$REMOTE" "HEAD:$BRANCH"
  fi
)

git fetch "$REMOTE" "+refs/heads/$BRANCH:$VERIFY_REF"
git show "$VERIFY_REF:data/snapshots/$LEAGUE_ID/latest.json" > "$VERIFY_DIR/latest.json"
git show "$VERIFY_REF:data/snapshots/$LEAGUE_ID/manifest.json" > "$VERIFY_DIR/manifest.json"

cmp "$SNAPSHOT_SRC/latest.json" "$VERIFY_DIR/latest.json"
cmp "$SNAPSHOT_SRC/manifest.json" "$VERIFY_DIR/manifest.json"

python3 - "$VERIFY_DIR/latest.json" "$LEAGUE_ID" <<'PY'
import json
import sys
path, league_id = sys.argv[1], sys.argv[2]
payload = json.load(open(path))
meta = payload.get("meta", {})
if str(meta.get("league_id")) != str(league_id):
    raise SystemExit("remote verification failed: league_id mismatch")
for field in ("fetched_at", "stale", "failure_reason", "snapshot_age_seconds"):
    if field not in meta:
        raise SystemExit(f"remote verification failed: missing meta.{field}")
print("Durable remote snapshot verified:", meta.get("fetched_at"))
PY
