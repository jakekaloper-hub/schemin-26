#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
python3 "$ROOT/cinema/scripts/preflight.py"
API="$ROOT/cinema/runtime/api/wan22-animate.json"
if [ ! -f "$API" ]; then
  echo "BLOCKED: Load the vendored Filmclusive workflow in local ComfyUI, resolve nodes/models, then export API format to cinema/runtime/api/wan22-animate.json"
  exit 2
fi
python3 "$ROOT/cinema/scripts/render_local.py" --workflow "$API"
