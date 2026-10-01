#!/usr/bin/env python3
"""Path-scoped repository merge gate for Schemin '26."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

SUITE_COMMANDS = {
    "mission": [
        "python -m py_compile governance/validate_project_mission.py",
        "python planning/character-native-render/validate_program_plan.py",
        "python -m unittest -v tests/test_character_native_render_program_plan.py",
        "python governance/capability-budget/validate_zero_spend.py",
        "python -m unittest -v tests/test_zero_incremental_spend.py",
        "python governance/validate_project_mission.py",
    ],
    "bullpen": ["cd bullpen-runtime && npm test"],
    "data": [
        "python -m py_compile data-gateway/refresh_espn_snapshot.py data-gateway/check_snapshot_health.py",
        "bash -n data-gateway/persist_snapshot_to_data_live.sh",
        "python -m unittest -v tests/test_data_gateway_snapshot_contract.py tests/test_data_gateway_snapshot_persistence.py",
    ],
    "character": [
        "python -m unittest discover -s canon/characters/tests -p 'test_*.py' -v",
        "! grep -R 'PORTABLE_REFERENCE_READY' canon/characters --include='*.py'",
        "! grep -R 'READY_FOR_SEMANTIC_QA' canon/characters --include='*.py'",
    ],
    "novel": [
        "python -m py_compile living-novel/os/engine/novel_os.py",
        "cd living-novel/os/evaluations && python -m unittest -v test_novel_os.py",
        "python living-novel/consultants/test_advisor_registry.py",
        "python living-novel/consultants/author-council/test_author_router.py",
        "python living-novel/os/evaluations/test_causal_chapter_architecture.py",
        "python living-novel/os/evaluations/test_author_council_book_architecture.py",
        "python living-novel/os/evaluations/test_pov_packet_validator.py",
        "python living-novel/consultants/author-council/test_engagement_001.py",
        "python living-novel/os/evaluations/test_chapter_03_minimum_gate.py",
        "python living-novel/os/evaluations/test_chapter_03_mission.py",
        "python living-novel/os/evaluations/test_chapter_03_canon_closeout.py",
        "python living-novel/os/evaluations/test_whole_book_convergence.py",
    ],
    "memo": [
        "python memo-os/tests/v5_5_acceptance_suite.py",
        "python -m unittest -v memo-os/tests/test_week4_preproduction_open.py",
        "python -m unittest -v memo-os/tests/test_v56_current_main_salvage.py",
    ],
    "world": [
        "python world/engine/validate_world.py",
        "python world/qa/test_world_engine.py",
        "python world/qa/test_universe_v1_1.py",
        "python world/location-control-plane/qa/test_location_control_plane.py",
        "python world/environment-references/test_environment_references.py",
        "python world/atlas/interactive/test_interactive_atlas.py",
        "python world/evolution/qa/test_world_evolution.py",
        "python world/atlas/integration/test_publication_convergence.py",
        "python world/qa/test_universe_os_v1_2.py",
        "python world/qa/test_one_world_model_contract.py",
    ],
    "release": [
        "python -m unittest -v governance/release-evidence/test_release_evidence.py",
        "python governance/release-evidence/release_evidence.py --head-sha \"$GITHUB_SHA\"",
    ],
    "publication": [
        "python -m py_compile governance/publication-manifest/validate_publication_manifest.py",
        "python governance/publication-manifest/validate_publication_manifest.py",
        "python -m unittest -v tests/test_publication_manifest.py",
    ],
}

ORDER = ["mission", "data", "character", "novel", "memo", "world", "release", "publication", "bullpen"]

def _starts(path: str, prefix: str) -> bool:
    return path == prefix.rstrip("/") or path.startswith(prefix)

def suites_for_path(path: str) -> set[str]:
    suites: set[str] = set()
    if _starts(path, "planning/character-native-render/"):
        suites.add("mission")
    if path in {
        "SCHEMIN_26_PROJECT_MISSION.md",
        "PROJECT_CONTROL_REGISTRY.md",
        "README.md",
        "living-novel/MASTER_DIRECTIVE.md",
    } or _starts(path, "governance/SCHEMIN_26_PROJECT_MISSION"):
        suites.add("mission")
    if _starts(path, "bullpen-runtime/") or path == "docs/architecture/BULLPEN_COMMAND_ADAPTER_V2.md":
        suites.add("bullpen")
    if (
        _starts(path, "data-gateway/")
        or path == "schemas/freshness.schema.json"
        or _starts(path, "tests/test_data_gateway_snapshot_")
        or path in {".github/workflows/data-gateway-ci.yml", ".github/workflows/espn-cold-standby.yml"}
    ):
        suites.add("data")
    if (
        _starts(path, "canon/characters/")
        or path == "memo-os/CCCP_INTEGRATION_CONTRACT_V1.md"
        or path == ".github/workflows/character-lock-ci.yml"
    ):
        suites.add("character")
    if (
        _starts(path, "living-novel/os/")
        or _starts(path, "living-novel/whole-book/")
        or _starts(path, "chronicles/proof-of-concept/prologue/")
        or path == ".github/workflows/novel-os-ci.yml"
    ):
        suites.add("novel")
    if _starts(path, "memo-os/"):
        suites.add("memo")
    if (
        _starts(path, "world/")
        or _starts(path, "living-novel/world/")
        or _starts(path, "living-novel/os/geography/")
        or path == "living-novel/os/engine/novel_os.py"
        or path in {
            "memo-os/WORLD_ENGINE_INTEGRATION_PATCH_V1.md",
            "living-novel/os/WORLD_ENGINE_INTEGRATION_PATCH_V1.md",
        }
    ):
        suites.add("world")
    if (
        _starts(path, "governance/release-evidence/")
        or path in {
            "memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_5_INTEGRATED_PREPRODUCTION_PATCH.md",
            "canon/_INDEX.md",
            "world/UNIVERSE_OS_V1_2_RELEASE_RECEIPT.md",
            ".github/workflows/release-evidence-ci.yml",
        }
    ):
        suites.add("release")
    if (
        _starts(path, "governance/publication-manifest/")
        or path in {
            "tests/test_publication_manifest.py",
            "docs/CATALOG.md",
            "docs/INVENTORY.md",
            "docs/SESSION_CONTEXT.md",
        }
    ):
        suites.add("publication")
    if _starts(path, "world/atlas/integration/"):
        suites.add("mission")
    return suites

def plan(changed_files: list[str]) -> list[str]:
    selected: set[str] = set()
    for path in changed_files:
        selected.update(suites_for_path(path))
    return [suite for suite in ORDER if suite in selected]

def run_suite(suite: str) -> None:
    for command in SUITE_COMMANDS[suite]:
        print(f"[merge-gate] {suite}: {command}", flush=True)
        subprocess.run(command, shell=True, check=True)

def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("plan", "run"):
        p = sub.add_parser(name)
        p.add_argument("--changed-file-list", required=True)
    args = parser.parse_args()
    changed = [line.strip() for line in Path(args.changed_file_list).read_text().splitlines() if line.strip()]
    selected = plan(changed)
    print(json.dumps({"changed_files": changed, "suites": selected}, indent=2))
    if args.command == "run":
        for suite in selected:
            run_suite(suite)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
