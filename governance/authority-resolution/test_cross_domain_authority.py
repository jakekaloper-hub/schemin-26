#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT=Path(__file__).resolve().parents[2]
errors=[]

def read(p): return (ROOT/p).read_text(encoding="utf-8")

# Memo: historical/current separation and fail-closed resolver.
manifest=json.loads(read("governance/publication-manifest/PUBLICATION_MANIFEST_V1.json"))
memos=[p for p in manifest["publications"] if p.get("family")=="weekly_memo"]
current=[p for p in memos if p.get("release_state")=="RELEASED" and p.get("metadata",{}).get("benchmark_status")=="CURRENT_BENCHMARK"]
if len(current)!=1 or current[0]["publication_id"]!="memo.2026.week-03":
    errors.append("MEMO_CURRENT_AUTHORITY")
w2=next(p for p in memos if p["publication_id"]=="memo.2026.week-02")
if w2.get("metadata",{}).get("benchmark_status")!="HISTORICAL_GOLD_STANDARD":
    errors.append("MEMO_WEEK2_HISTORICAL")

# Session and Memo entrypoints must distinguish historical from current.
session=read("docs/SESSION_CONTEXT.md")
memo_readme=read("memo-os/README.md")
for label,txt in [("SESSION",session),("MEMO_README",memo_readme)]:
    if "Historical benchmark is not current authority" not in txt and "historical gold standard" not in txt.lower():
        errors.append(label+"_TEMPORAL_SEPARATION")
if "Pro_Schemin_Week_3_Memo_Final.pdf" not in memo_readme:
    errors.append("MEMO_README_WEEK3")

# Task router must send current Memo and visual tasks to machine authority surfaces.
matrix=json.loads(read("governance/task-orientation/TASK_CONTEXT_MATRIX_V1.json"))
routes={r["id"]:r for r in matrix["routes"]}
if "governance/publication-manifest/PUBLICATION_MANIFEST_V1.json" not in routes["weekly-memo"]["context_sources"]:
    errors.append("ROUTER_MEMO_MANIFEST")
if "canon/characters/VISUAL_REFERENCE_AUTHORITY_V1.json" not in routes["character-visual"]["context_sources"]:
    errors.append("ROUTER_VISUAL_AUTHORITY")

# Character: known stale composite subjects must be explicitly stale and forbidden as production seed.
visual=json.loads(read("canon/characters/VISUAL_REFERENCE_AUTHORITY_V1.json"))
lineup=visual["master_lineup"]
expected={"CHAR-WILSON-LOOK","CHAR-PHILLIP-PITTS","CHAR-AUSTIN-BYARS"}
stale={x["character_id"] for x in lineup["stale_for"]}
if not expected.issubset(stale): errors.append("CHAR_STALE_SET")
if lineup.get("production_seed_allowed") is not False: errors.append("CHAR_LINEUP_SEED")
if visual.get("status")!="ACTIVE_FAIL_CLOSED": errors.append("CHAR_FAIL_CLOSED")

# Master prose must explicitly fence legacy lineup doctrine behind machine visual authority.
master=read("canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md")
if "CURRENT VISUAL AUTHORITY NOTICE" not in master: errors.append("CHAR_MASTER_FENCE")
if "PARTIAL_STALE_REFERENCE_ONLY" not in master or "production_seed_allowed=false" not in master:
    errors.append("CHAR_MASTER_STALE_LINEUP_FENCE")

# Canon index must make newer corrections outrank master prose and block unproven generation.
canon_index=read("canon/_INDEX.md")
if "latest explicit Commissioner-approved character correction" not in canon_index:
    errors.append("CHAR_PRECEDENCE")
if "GENERATION_BLOCKED" not in canon_index:
    errors.append("CHAR_GENERATION_BOUNDARY")

# World: current engine must outrank old world releases/renderers.
world=read("world/governance/UNIVERSE_OS_AUTHORITY_HIERARCHY_V2.md")
if "Current Character Canon" not in world or "Art / map renderers" not in world:
    errors.append("WORLD_HIERARCHY")
if "Generated scenery is evidence only until governed promotion" not in world:
    errors.append("WORLD_RENDER_NONAUTHORITY")

# League truth: freshness must be propagated and Flaim cannot become parallel truth.
dg=read("data-gateway/_INDEX.md")
if "A payload existing does not prove freshness" not in dg: errors.append("DATA_FRESHNESS")
if "not a second source of truth" not in dg: errors.append("DATA_FLAIM_BOUNDARY")

# Novel: task routing must retain authority matrix for canon-bearing work.
novel_matrix=json.loads(read("living-novel/os/TASK_CONTEXT_MATRIX_V1.json"))
if not any(
    any(str(src).endswith("WHOLE_BOOK_SOURCE_AUTHORITY_MATRIX_V1.md") for src in route.get("context_sources", []))
    for route in novel_matrix.get("routes", [])
):
    errors.append("NOVEL_AUTHORITY_ROUTE")

if errors:
    print("CROSS_DOMAIN_AUTHORITY_FAIL", *errors, sep="\n- ")
    sys.exit(1)
print("CROSS_DOMAIN_AUTHORITY_PASS")
print("memo=current Week 3; Week 2 historical")
print("character=owner-specific current authority; stale composite blocked")
print("world=current governed model outranks renders")
print("data=freshness required")
print("novel=authority matrix routed")
