#!/usr/bin/env python3
"""Verify source assets and complete per-page text handoff; does NOT approve final art."""
import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
ISSUE = ROOT / "memo-os/week-11/preproduction"
REPORTS = []
ERRORS = []

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check(name, passed, detail):
    REPORTS.append({"check": name, "pass": passed, "detail": detail})
    if not passed:
        ERRORS.append(name)

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

render = load(ISSUE / "W11_ALL_35_INTEGRATED_RENDER_INPUTS_2026-11-24.json")
lineup = load(ROOT / "canon/characters/APPROVED_LINEUP_2026_10_18.json")
native_refs = load(ROOT / "canon/characters/NATIVE_RENDER_REFERENCE_BINDING_V1.json")
reconcile = load(ISSUE / "WEEK11_PRE_RENDER_REFERENCE_RECEIPT.json")
text = (ISSUE / "W11_READER_LETTERING_2026-11-24.md").read_text(encoding="utf-8")
heads = list(re.finditer(r"^## (F\d\d) · ([^\n]+)$", text, re.MULTILINE))
expected_ids = ["F%02d" % i for i in range(1,36)]
found_ids = [p["internal_folio_id"] for p in render.get("pages", [])]
check("35_integrated_pages", found_ids == expected_ids, "%d integrated packets" % len(found_ids))
check("35_exact_reader_sections", [m.group(1) for m in heads] == expected_ids,
      "%d source reader sections" % len(heads))
by_id = {p["internal_folio_id"]:p for p in render["pages"]}
for i, m in enumerate(heads):
    page_id=m.group(1)
    raw = text[m.end(): heads[i+1].start() if i+1<len(heads) else len(text)].strip()
    page = by_id.get(page_id, {})
    ok = (page.get("exact_reader_publication_copy_markdown") == raw
          and page.get("final_page_headline") == m.group(2)
          and page.get("user_approved_print_controls",{}).get("visible_folio_reference") is False)
    check("exact_copy_"+page_id, ok, "source text/title unchanged; no visible folio label")
check("fourteen_performance_treatments",
      sum(bool(p.get("screenplay_for_performance_only")) for p in render["pages"]) == 14,
      "14 source scripts supplied only for the scene/performance layer")
lineup_people = lineup["individuals"]
check("twelve_approved_lineup_entries", len(lineup_people)==12, "12 visual identities registered")
for row in lineup_people:
    path=ROOT/row["crop"]
    seen=digest(path) if path.is_file() else "MISSING"
    check("lineup_"+row["character_id"], seen==row["crop_sha256"],
          "%s expected=%s observed=%s" % (row["crop"],row["crop_sha256"],seen))
register = {x["character_id"]:x for x in native_refs["characters"]}
check("native_file_id_register", len(register)==12 and all(x.get("renderer_reference_id") for x in register.values()),
      "12 exact native Library handles registered; presence is not a live renderer attachment receipt")
for match in reconcile["matchups"]:
    plate=ROOT/match["venue"]["structural_plate"]["path"]
    check("structural_plate_"+match["id"], plate.is_file(), str(plate.relative_to(ROOT)))
brandon = ROOT/"canon/characters/assets/CHAR-BRANDON-PRYOR/supplementary/COMMISSIONER_CHILI_OUTLAW_2026_10_22.png"
expected = "5812d9b62844368fdd1e23bb11657bbe47af101f7c026413eea6ce2bb8a3793f"
observed = digest(brandon) if brandon.is_file() else "MISSING"
check("brandon_oct22_override_exact_sha256",observed==expected,
      "expected=%s observed=%s" % (expected, observed))
result = {
  "status":"SOURCE_PREFLIGHT_PASS_ONLY" if not ERRORS else "SOURCE_PREFLIGHT_FAIL",
  "publication_approved":False,
  "render_bound_subjects_attested":False,
  "approved_cinematic_plates_in_current_registry":0,
  "accepted_final_png_count":0,
  "errors":ERRORS,
  "checks":REPORTS,
}
print(json.dumps(result, indent=2))
sys.exit(1 if ERRORS else 0)
