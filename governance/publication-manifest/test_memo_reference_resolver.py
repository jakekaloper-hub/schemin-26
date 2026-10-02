#!/usr/bin/env python3
import copy
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("resolver", HERE / "memo_reference_resolver.py")
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
manifest = json.loads((HERE / "PUBLICATION_MANIFEST_V1.json").read_text())

def week(q, m=manifest):
    return r.resolve_memo_reference(q, m)["source_interval"]["weeks"][0]

assert week("Week 2 memo") == 2
assert week("reference the Week 3 memo") == 3
assert week("latest memo") == 3
assert week("current memo") == 3
assert week("use the benchmark") == 3
assert week("most recent memo") == 3
assert week("the memo") == 3

for q in ("Week 4 memo", "Week 9 memo"):
    try: week(q)
    except r.MemoReferenceError as e: assert "REQUESTED_WEEK_ARTIFACT_NOT_VERIFIED" in str(e)
    else: raise AssertionError(q + " must fail closed")

sim = copy.deepcopy(manifest)
for p in sim["publications"]:
    if p["publication_id"] == "memo.2026.week-03":
        p["metadata"]["benchmark_status"] = "HISTORICAL_CANON"
    if p["publication_id"] == "memo.2026.week-04":
        p["release_state"] = "RELEASED"
        p["canonical_artifact"] = "SIMULATED_WEEK_4.pdf"
        p["metadata"]["benchmark_status"] = "CURRENT_BENCHMARK"
assert week("latest memo", sim) == 4

bad = copy.deepcopy(manifest)
for p in bad["publications"]:
    if p["publication_id"] == "memo.2026.week-02":
        p["metadata"]["benchmark_status"] = "CURRENT_BENCHMARK"
    if p["publication_id"] == "memo.2026.week-03":
        p["metadata"]["benchmark_status"] = "HISTORICAL_CANON"
try: week("latest memo", bad)
except r.MemoReferenceError as e: assert "STALE_BENCHMARK_AUTHORITY" in str(e)
else: raise AssertionError("stale Week 2 benchmark must fail closed")

print("memo reference resolver acceptance: PASS")
