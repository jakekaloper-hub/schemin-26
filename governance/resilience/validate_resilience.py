#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from resilience import ROOT, load_json, validate_conditioning_registry

def main() -> int:
    errors = []
    schema_path = ROOT / "schemas" / "production-checkpoint.schema.json"
    conditioning_path = ROOT / "governance" / "resilience" / "CREATIVE_CONDITIONING_REGISTRY_V1.json"
    harvest_path = ROOT / "governance" / "resilience" / "FLA_PATTERN_HARVEST_V1.md"
    handoff_path = ROOT / "governance" / "resilience" / "FRESH_OPERATOR_HANDOFF_GATE_V1.md"
    checkpoint_cli = ROOT / "governance" / "resilience" / "checkpoint_cli.py"
    checkpoint_store = ROOT / "governance" / "resilience" / "checkpoints" / "README.md"

    for path in (schema_path, conditioning_path):
        try:
            json.loads(path.read_text())
        except Exception as exc:
            errors.append(f"{path}: invalid json: {exc}")

    if conditioning_path.exists():
        errors.extend(validate_conditioning_registry(load_json(conditioning_path)))

    for path in (harvest_path, handoff_path, checkpoint_cli, checkpoint_store):
        if not path.exists():
            errors.append(f"missing resilience control: {path}")

    if harvest_path.exists() and "1494d7cb5342c186ac7f7ebfa84d75129ebc6496" not in harvest_path.read_text():
        errors.append("FLA harvest must pin inspected source revision")

    if errors:
        for error in errors:
            print(error)
        return 1
    print("Schemin resilience controls valid.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
