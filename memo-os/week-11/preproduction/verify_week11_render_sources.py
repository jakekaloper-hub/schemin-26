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
# This check is intentionally a RELEASE HOLD, not a source-assembly failure:
# the prior Week10 local copy was found to have a DIFFERENT SHA-256, and was
# removed from the canonical path. Human production may audition with the
# approved Oct18 lineup crop plus Commissioner Oct22 semantic correction;
# the exact Oct22 approved bytes are still required for canonical identity release.
RELEASE_HOLDS = []
if observed != expected:
    RELEASE_HOLDS.append({
        "gate":"BRANDON_CURRENT_OVERRIDE_EXACT_SOURCE",
        "status":"BLOCKED",
        "expected_sha256":expected,
        "observed_sha256":observed,
        "action":"Do not treat prior Week10 local-copy bytes as Oct22 approved original."
    })
# Week 11 G01 Founder correction: detect character substitutions and loss
# of the existing three-stage duel / fall / alive-water-surface outcome.
g01 = load(ISSUE / "W11_G01_HMB_DK_BRIDGE_F09_F11_RESULT_LOCKED_RENDER_PACKET_2026-11-24.json")
seq = g01["three_scene_continuity"]
g01_ids = ["F09","F10","F11"]
master_g01 = {page["internal_folio_id"]:page for page in render["pages"] if page["internal_folio_id"] in g01_ids}
check("g01_beat_and_winner_locked",
      g01["source_outcome"]["winner"] == "His Majesty's Blood" and
      g01["source_outcome"]["away_points"] == 168.2 and
      g01["source_outcome"]["home_points"] == 129.75 and
      all(word in seq["middle"].lower() for word in ["austin","strike","four","skid"]) and
      all(word in seq["ending"].lower() for word in ["wilson","lake","alive","bridge"]),
      "Austin causes four-hoof slide; Wilson alive after lake fall; 168.20–129.75")
for scene in g01["pages"]:
    old = master_g01.get(scene["id"],{})
    override = old.get("active_matchup_override",{})
    check("g01_integrated_"+scene["id"],
          old.get("exact_reader_publication_copy_markdown") == scene["exact_print_copy"] and
          override.get("source", "").endswith("W11_G01_HMB_DK_BRIDGE_F09_F11_RESULT_LOCKED_RENDER_PACKET_2026-11-24.json") and
          override.get("no_folio_ids_on_print") is True and
          override.get("wilson_old_native_handle_blocked") is True and
          "GLOWING RED EYES" in old.get("camera_scene_and_design",{}).get("approved_character_override",""),
          "exact selected scene and all print/identity restrictions preserved")
hmb = g01["character_identity"]["Austin_Byars"]
hmb_reference = ROOT / hmb["commissioner_correction"]
hmb_seen = digest(hmb_reference) if hmb_reference.is_file() else "MISSING"
check("g01_hmb_approved_commissioner_visual_bytes",
      hmb_seen == hmb["commissioner_correction_sha256"],
      "expected=%s observed=%s" % (hmb["commissioner_correction_sha256"],hmb_seen))
if g01["character_identity"]["Wilson_Look"]["legacy_handle_state"].startswith("BLOCKED"):
    RELEASE_HOLDS.append({"gate":"G01_WILSON_CURRENT_SOURCE_SUPERSESSION",
                          "status":"BLOCKED_FOR_FINAL_CANON",
                          "action":"Do not attach biped historical primary as four-hoof current active source."})
# Founder-directed Week11 G01 stunt/identity regression check. This is a source
# preflight, not evidence of a finished image or independent character approval.
duel = load(ISSUE / "W11_G01_MOUNTAIN_LAKE_FIGHT_SEQUENCE_V2_2026-11-24.json")
scenes = duel["sequence"]
g01_ids = ["F09", "F10", "F11"]
check("g01_three_page_order", [x["folio"] for x in scenes] == g01_ids,
      "Verbal conflict/charge, choreographed fighting, fall/survivor")
check("g01_seven_story_frames", [len(x["frames"]) for x in scenes] == [2,3,2],
      "2 + 3 + 2 distinct shot beats")
austin = duel["cast"]["austin"]
wilson = duel["cast"]["wilson"]
for character, info in [("austin",austin),("wilson",wilson)]:
    for alias, path_field, sha_field in [
        ("crop","approved_lineup_crop_path","approved_lineup_crop_sha256")]:
        target = ROOT / info[path_field]
        actual = digest(target) if target.is_file() else "MISSING"
        check("g01_%s_%s_verified" % (character,alias), actual==info[sha_field],
              "%s actual_sha=%s" % (target.relative_to(ROOT),actual))
hmbpath = ROOT/austin["approved_hmb_correction_path"]
hmb_sha = digest(hmbpath) if hmbpath.is_file() else "MISSING"
check("g01_austin_commissioner_oct18_correction",hmb_sha==austin["approved_hmb_correction_sha256"],
      "approved current source must be attached for candidate render: %s" % hmb_sha)
for item in scenes:
    id = item["folio"]
    folio = by_id[id]
    reqpath = ISSUE / "render-inputs" / ("W11-P" + id[-2:]) / "request.json"
    req = load(reqpath)
    check("g01_reader_exact_vs_packet_"+id,
          folio["exact_reader_publication_copy_markdown"].endswith(item["print_copy"]),
          "G01 exact printed source copied into all-35 packet")
    check("g01_render_request_copy_"+id,
          req["exact_full_publication_copy"]["body"] == item["print_copy"] and
          req["page_id"] == "W11-P" + id[-2:] and
          len(req["performance_and_choreography"]["frames"]) == len(item["frames"]) and
          not req.get("image_generation_executed") and not req.get("publication_approved"),
          "Complete integrated type/script/stunt beats; image not yet generated")
    check("g01_image_character_overrides_"+id,
          "HOODED" in folio["active_matchup_override"]["austin_current_character"].upper()
          and folio["active_matchup_override"]["source_binding_requirement"] if "source_binding_requirement" in folio["active_matchup_override"] else
          folio["camera_scene_and_design"].get("source_binding_requirement","").startswith("Must visually reference"),
          "HMB red-eyed correction must outrank generic human resemblance")
check("g01_lake_hydrology_not_silently_changed",
      duel["stage"]["water_handle"].endswith("::LAKE"),
      "Raging wave effect OK; literal river requires Atlas amendment")

# Founder 2026-11-24 photographic reality / 4K composition-source gate.
# A PASS certifies instructions are present, never that an image looks photoreal.
photo = load(ISSUE / "W11_ALL35_HYPERREAL_PHOTOGRAPHY_CONTROL_2026-11-24.json")
actii_photo = load(ISSUE / "W11_ACTII_P09_GOLD_STANDARD_14_FOLIO_ART_DIRECTION_2026-11-24.json")
photo_map = {x["id"]:x for x in photo["all_folios"]}
check("photo_standard_all_35", len(photo_map)==35 and set(photo_map)==set(expected_ids),
      "35 distinct page-specific photographic material and lens treatments")
check("photo_reference_is_quality_not_geography",
      photo["reference_photo"]["source_role"].startswith("Photographic realism") and
      photo["reference_photo"]["pixels"]==[941,1672] and
      photo["reference_photo"]["sha256"]=="ab3a5d5b1bff74eb961ca185357a0c177031240db0d39de0180630fcc06bb7e2",
      "Founder photo reference is 941x1672; must not overwrite other Atlas locations")
for page in render["pages"]:
    pid = page["internal_folio_id"]
    phot = page.get("photographic_realism_contract",{})
    check("photographic_handoff_"+pid,
          phot.get("physical_reality_anchor")==photo_map[pid]["photographic_reality_anchor"] and
          phot.get("source")=="W11_ALL35_HYPERREAL_PHOTOGRAPHY_CONTROL_2026-11-24.json" and
          "4K" in phot.get("finishing",""),
          "Quality and physical site material attributes are kept separate from original source copy")
check("actii_photo_all_14",len(actii_photo["folios"])==14 and
      all(x.get("photographic_finish_anchor")==photo_map[x["id"]]["photographic_reality_anchor"] for x in actii_photo["folios"]),
      "Six narrative matchups carry 14 distinct shot/material directions")
for id in ["F09","F10","F11"]:
    request = load(ISSUE / "render-inputs" / ("W11-P"+id[-2:]) / "request.json")
    check("g01_photo_render_request_"+id,
          request.get("photographic_finish",{}).get("reference_photo_sha256")==photo["reference_photo"]["sha256"] and
          "PHOTOGRAPHIC REALISM HARD GATE" in request["prompt"],
          "Actual render request includes physical photo realism rather than only generic high resolution")

result = {
  "status":"WORKING_ART_SOURCE_PREFLIGHT_PASS" if not ERRORS else "WORKING_ART_SOURCE_PREFLIGHT_FAIL",
  "publication_approved":False,
  "render_bound_subjects_attested":False,
  "approved_cinematic_plates_in_current_registry":0,
  "accepted_final_png_count":0,
  "release_holds":RELEASE_HOLDS,
  "errors":ERRORS,
  "checks":REPORTS,
}
print(json.dumps(result, indent=2))
sys.exit(1 if ERRORS else 0)
