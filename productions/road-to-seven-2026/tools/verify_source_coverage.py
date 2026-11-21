#!/usr/bin/env python3
"""Source-contract QA for The Road to Seven. No graphic or model-calibration approval.

Run from the repository checkout:
  python3 productions/road-to-seven-2026/tools/verify_source_coverage.py
"""
import json
import hashlib
import re
from decimal import Decimal, ROUND_HALF_UP
import sys
import subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
REPO = BASE.parents[1]
FOLIOS = BASE / "folios"
EVIDENCE = BASE / "evidence"
ISSUES = []


def test(condition, label):
    if not condition:
        ISSUES.append(label)


def load_json(name):
    path = EVIDENCE / name
    test(path.is_file(), "Missing evidence " + name)
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def run():
    live = load_json("FFHUB_LIVE_W11_2026-11-18_SUMMARY.json")
    forks = load_json("FFHUB_FUTURE_FORKS_2026-11-18.json")
    lineup_path = REPO / "canon/characters/APPROVED_LINEUP_2026_10_18.json"
    test(lineup_path.is_file(), "Approved character lineup JSON not in checkout")
    canon = json.loads(lineup_path.read_text(encoding="utf-8")) if lineup_path.is_file() else {}
    ids = {x["character_id"] for x in canon.get("individuals", [])}
    test(len(ids) == 12, "Expected exactly 12 approved characters")

    players = (EVIDENCE / "FLAIM_CURRENT_ROSTERS_2026-11-18.md").read_text(encoding="utf-8")
    games = (EVIDENCE / "FLAIM_W12_W14_PROVISIONAL_PROJECTIONS.md").read_text(encoding="utf-8")
    market = (EVIDENCE / "NFL_WEEK11_NEWS_AND_MARKET_CONTEXT_2026-11-18.md").read_text(encoding="utf-8")

    test(len(re.findall(r"^## .+ — ESPN team ID \d+$", players, re.M)) == 12,
         "Flaim roster snapshot must contain twelve teams")
    test(len(re.findall(r"^\| (?:Bench|IR|QB|RB|WR|WR/TE|TE|FLEX|D/ST|K|OP|WR/RB|RB/WR) \|", players, re.M)) >= 210,
         "Flaim snapshot does not have complete roster player rows")
    test(len(re.findall(r"^## Week (12|13|14)$", games, re.M)) == 3,
         "Must have 3 future-week projections")
    test(len(re.findall(r"^\| .+ vs .+ \| [0-9.]+ \| [0-9.]+ \| -?[0-9.]+ \|$", games, re.M)) == 18,
         "Must have 18 future-week matchup projections")
    test(market.count("|") >= 100 and "cbssports.com" in market and "2026" in market,
         "Market context missing dated source table")
    teams = live.get("teams", [])
    test(len(teams) == 12 and len({x.get("team") for x in teams}) == 12, "Live Week11 summary not twelve distinct teams")
    test(live.get("source_site", "").startswith("https://theffhub.com/PlayoffTool"), "Missing FFHub source")
    test(len(live.get("sweeps", [])) == 4 and live.get("captured_runs") == 16,
         "Week11 source lacks 12 single-game plus four winout scenarios")
    test(len(forks.get("cases", [])) == 10 and forks.get("run_count") == 20,
         "Week12-14 source lacks 20 conditional results")
    for case in forks.get("cases", []):
        for side in ("a", "b"):
            values = case.get("full_league_" + side, {})
            test(len(values) == 12, "Bad team coverage: " + str(case.get("tag")))
            test(abs(sum(values.values()) - 700) < 0.10, "Bad seven-berth mass: " + str(case.get("tag")))
        test(case.get("week") in (12, 13, 14), "Unexpected future week")

    all_chars = []
    count = 0
    for i in range(1, 8):
        p = FOLIOS / ("RT7-P%02d" % i) / "PAGE_PACKET.md"
        test(p.exists(), "Missing folio " + p.as_posix())
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8")
        count += 1
        chars = set(re.findall(r"CHAR-[A-Z0-9-]+", t)) & ids
        if i == 1:
            test(not chars and "Cover — News" in t, "Cover contains characters or lacks source update")
        else:
            test(len(chars) == 2, "Folio %02d missing two canonical characters" % i)
            all_chars.extend(chars)
            test("Live FFHub revalidation" in t and "Extended production intelligence" in t,
                 "Folio %02d missing live and roster future evidence" % i)
            test("approved crop" in t.lower(), "Folio %02d lacks visual ref binding" % i)
    test(count == 7, "Not exactly seven folios")
    test(len(all_chars) == len(set(all_chars)) == 12, "Twelve character appearances must each be unique")

    # Separate scene.json contracts bind page facts to immutable visual source assets.
    indexed = {x["team"]: x for x in live.get("teams", [])}
    image_pairs = 0
    for i in range(1, 8):
        path = FOLIOS / ("RT7-P%02d" % i) / "scene.json"
        test(path.is_file(), "Missing machine scene contract " + path.as_posix())
        if not path.is_file():
            continue
        scene = json.loads(path.read_text(encoding="utf-8"))
        art = scene.get("artifact", {})
        test(scene.get("id") == "RT7-P%02d" % i, "Bad scene ID")
        test(art.get("width") == 1080 and art.get("height") == 1920 and art.get("format") == "PNG",
             "Bad PNG geometry or format for page %02d" % i)
        rig = scene.get("lighting_contract", {})
        test(rig.get("method") == "BAKED_IN_MOTIVATED_LIGHTING_BEFORE_RENDERING",
             "Missing baked lighting method on page %02d" % i)
        test(len(scene.get("visual_studio", {}).get("specialist_lenses", [])) >= 2,
             "Missing page-specific visual specialist lens routing on page %02d" % i)
        test(scene.get("writing_contract", {}).get("copy_path", "").endswith("INKLINGS_TWELVE_POV_EDITORIAL_COPY.md"),
             "Missing parallel Inklings copy source page %02d" % i)
        for field in ("time", "text_safe", "forbidden"):
            test(bool(rig.get(field)), "Lighting rig missing %s page %02d" % (field, i))
        if i > 1:
            for side in ("left", "right"):
                for field in ("key", "fill", "rim", "air"):
                    test(bool(rig.get(side, {}).get(field)),
                         "Lighting rig missing %s.%s page %02d" % (side, field, i))
            test("## Publication copy lock — November 18 FFHub cohort" in (FOLIOS / ("RT7-P%02d" % i) / "PAGE_PACKET.md").read_text(),
                 "Publication cohort lock missing on %02d" % i)
        panels = scene.get("character_panels", [])
        test(len(panels) == (0 if i == 1 else 2), "Bad scene panel count on %02d" % i)
        for p in panels:
            image_pairs += 1
            test(p.get("character_id") in ids, "Unknown scene character " + str(p.get("character_id")))
            crop = REPO / p.get("approved_crop_path", "")
            test(crop.is_file(), "Missing reference crop " + str(crop))
            if crop.is_file():
                test(hashlib.sha256(crop.read_bytes()).hexdigest() == p.get("approved_crop_sha256"),
                     "Character crop SHA mismatch " + str(crop))
            card = REPO / p.get("atlas_card_path", "")
            plate = REPO / p.get("atlas_structural_plate_path", "")
            test(card.is_file() and plate.is_file(), "Missing semantic card or geometry plate " + str(p.get("team")))
            if card.is_file():
                card_obj = json.loads(card.read_text(encoding="utf-8"))
                test(p.get("character_id") in card_obj.get("owner_character_ids", []),
                     "Atlas owner mismatch " + str(p.get("team")))
            folio_copy = (FOLIOS / ("RT7-P%02d" % i) / "PAGE_PACKET.md").read_text(encoding="utf-8")
            # Publication text is checked separately from source JSON. Legacy Nov17 narrative sections remain archival.
            if i < 7:
                round1 = lambda value: Decimal(str(value)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
                expected_line = "PLAYOFF OUTLOOK %s%% (FFHUB, NOV 18)" % round1(p.get("ffhub_baseline_pct", -1))
                test(expected_line in folio_copy,
                     "On-image baseline no longer matches Nov18 scene source for " + str(p.get("team")))
                expected_win = "WIN W11 %s%%" % round1(p.get("ffhub_w11_win_pct", -1))
                expected_loss = "LOSE W11 %s%%" % round1(p.get("ffhub_w11_loss_pct", -1))
                test(expected_win in folio_copy and expected_loss in folio_copy,
                     "On-image conditional odds do not match Nov18 for " + str(p.get("team")))
            else:
                expected = "FFHUB NOV 18 %.2f%%" % float(p.get("ffhub_baseline_pct", -1))
                test(expected in folio_copy,
                     "P07 source cohort does not match Nov18 for " + str(p.get("team")))
            record = indexed.get(p.get("team"))
            test(record is not None, "Missing live FFHub current team for " + str(p.get("team")))
            if record:
                for field, key in (("ffhub_baseline_pct", "baseline_pct"),
                                   ("ffhub_w11_win_pct", "win_pct"),
                                   ("ffhub_w11_loss_pct", "loss_pct")):
                    test(abs(float(p.get(field, -1)) - float(record[key])) < .001,
                         "FFHub scene source drift " + str(p.get("team")) + " " + field)
    # Explicit authored manuscripts and visual-lighting workflows must cover every page.
    manuscript_path = BASE / "reviews/INKLINGS_TWELVE_POV_EDITORIAL_COPY.md"
    visual_path = BASE / "reviews/VISUAL_STUDIO_LIGHTING_BIBLE.md"
    test(manuscript_path.is_file() and visual_path.is_file(),
         "Missing parallel Inklings or visual studio deliverable")
    if manuscript_path.is_file() and visual_path.is_file():
        manuscript = manuscript_path.read_text(encoding="utf-8")
        visual_doc = visual_path.read_text(encoding="utf-8")
        titles = re.findall(r"^\*\*(?:Left|Right) / #(\d+) (.*?) — ", manuscript, re.M)
        test(len(titles) == 12 and len({int(rank) for rank, _ in titles}) == 12,
             "Inklings draft must have 12 individually numbered character POVs")
        original_pairs = [panel for page_id in range(2, 8) for panel in
                          json.loads((FOLIOS / ("RT7-P%02d" % page_id) / "scene.json").read_text(encoding="utf-8")).get("character_panels", [])]
        expected_map = {panel["official_week10_seed"]: panel["team"] for panel in original_pairs}
        for rank, name in titles:
            test(expected_map.get(int(rank)) == name.strip(),
                 "Wrong Inklings seed/name binding #" + rank)
        for page_id in range(1, 8):
            test(("RT7-P%02d" % page_id) in visual_doc, "Missing visual studio lighting page %02d" % page_id)
    test(image_pairs == 12, "Exactly 12 official character/image bindings required")
    approved_lineup = REPO / canon.get("stored_repository_path", "")
    test(approved_lineup.is_file(), "Missing approved master lineup PNG")
    if approved_lineup.is_file():
        test(hashlib.sha256(approved_lineup.read_bytes()).hexdigest() == canon.get("sha256"),
             "Master approved lineup SHA mismatch")

    # Full film production: weather/character/set/camera contracts fail closed.
    stage_compiler = BASE / "tools/build_staging.py"
    call_sheet_compiler = BASE / "tools/write_call_sheets.py"
    for tool in (stage_compiler, call_sheet_compiler):
        test(tool.is_file(), "Missing staging producer " + str(tool))
        if tool.is_file():
            result = subprocess.run([sys.executable, str(tool), "--dry-run"],
                                    capture_output=True, text=True, timeout=25)
            test(result.returncode == 0,
                 "Staging contract/call sheet stale: " + (result.stderr or result.stdout)[-700:])
    stage_manifest = BASE / "STAGING_MANIFEST.json"
    test(stage_manifest.is_file(), "Missing full-seven STAGING_MANIFEST")
    staged_images = []
    direct_practitioners = set()
    if stage_manifest.is_file():
        stage_records = json.loads(stage_manifest.read_text(encoding="utf-8"))
        test(stage_records.get("staged_pages") == 7 and stage_records.get("specialists") == 12,
             "Seven pages and all 12 specialized methods must be assigned")
        test(stage_records.get("no_new_weather_event_asserted") is True,
             "Global weather story must not assert a new source-unknown event")
        for i in range(1, 8):
            p = FOLIOS / ("RT7-P%02d" % i) / "STAGING.json"
            test(p.is_file(), "Missing film staging RT7-P%02d" % i)
            if not p.is_file():
                continue
            stage = json.loads(p.read_text(encoding="utf-8"))
            test(stage.get("page_id") == "RT7-P%02d" % i, "Wrong staging page ID")
            test(stage.get("world_state_record_as_of") == "end_of_week_3_2026",
                 "Unexamined later world state date")
            specialists = stage.get("staging_crew", [])
            test(len(specialists) == 12 and len(set(s["reference_profile"] for s in specialists)) == 12,
                 "Missing or duplicate film specialist-method profiles")
            direct_practitioners.update(s["reference_profile"] for s in specialists if s["direct_page_assignment"])
            cast = stage.get("characters", [])
            test(len(cast) == (0 if i == 1 else 2), "Staging cast count wrong page %02d" % i)
            if i == 1:
                test(stage.get("cover_staging", {}).get("weather") == "SYMBOLIC_ATLAS_COMPOSITE",
                     "Cover cannot assert a real cross-continent storm")
            for actor in cast:
                staged_images.append(actor["character_id"])
                test(actor.get("el_nino_attribution") not in
                     ("CONFIRMED_CONTINENTAL_STORM", "ASSUMED_GLOBAL"),
                     "Unverified continental Niño event asserted")
                weather = actor.get("weather_role")
                location = actor.get("location_id")
                if location == "LOC-STORM-BOWL":
                    test(weather == "EMBODIED_AT_STORM_BOWL" and
                         actor.get("el_nino_attribution") == "EMBODIED_APPROVED",
                         "El Niño direct manifestation missing at his source")
                elif weather == "EMBODIED_AT_STORM_BOWL":
                    test(False, "El Niño embodiment wrongly placed in another homeland")
                if location == "LOC-CHILI-STABLE":
                    test(weather == "WESTERN_DRY_RAIN_SHADOW", "Chili western weather changed")
                    test("BROWN cowboy hat" in actor.get("shoot_costume_dressing", ""),
                         "Chili's current brown hat must survive costume staging")
                if location in ("LOC-MUD-DOGS-SWAMP", "LOC-TDS-WATERFALL-TEMPLE",
                                "LOC-COUNTRY-CLUB-JACKSON"):
                    test(weather == "INDEPENDENT_SOUTHERN_HYDROLOGY",
                         "Southern wetlands cannot be relabeled Niño flood")
                if actor["character_id"] == "CHAR-WILSON-LOOK":
                    test("four-legged" in actor["approved_costume_visual"]["subject_morphology"],
                         "DK approved four-legged presentation lost")
                if actor["character_id"] == "CHAR-BOBBY-MITCHELL":
                    test("four-legged" in actor["approved_costume_visual"]["subject_morphology"],
                         "Mud's quadrupedal body lost")
                test(all(x in actor.get("motived_lighting", {}) for x in ("key","fill","rim","air")),
                     "Weather+lighting sources missing "+actor["character_id"])
        test(len(staged_images)==len(set(staged_images))==12,
             "Twelve canonical inhabitants must each receive their own staging")
        test(len(direct_practitioners)==12, "All twelve film specialties must own actual assignments")
    # Verify the derived image-production inputs against the frozen underlying sources.
    compiler = BASE / "tools/compile_render_inputs.py"
    test(compiler.is_file(), "Missing deterministic render-input compiler")
    if compiler.is_file():
        result = subprocess.run([sys.executable, str(compiler), "--dry-run"],
                                capture_output=True, text=True, timeout=25)
        test(result.returncode == 0,
             "Render manifest or per-page inputs stale: " + (result.stderr or result.stdout)[-700:])

    print(json.dumps({
        "source_qa": "PASS" if not ISSUES else "FAIL",
        "errors": ISSUES,
        "folio_count": count,
        "source_bound_scene_count": 7,
        "staged_heroic_folios": 7,
        "visual_specialist_method_assignments": len(direct_practitioners),
        "physical_weather_canon": "CHECKED_SEPARATE_FROM_SYMBOLIC_STORM_MOTIF",
        "character_and_atlas_byte_checks": image_pairs,
        "canonical_characters": len(set(all_chars)),
        "week11_teams": len(teams),
        "week11_conditional_runs": live.get("captured_runs"),
        "future_conditional_runs": forks.get("run_count"),
        "week12_14_projection_matchups": 18,
        "scope": "SOURCE-CONSISTENCY ONLY — no new live refresh, exact model calibration, pixels, or independent Umpire signoff",
        "independent_visual_gate": "NOT_RUN",
        "final_pngs": "NOT_GENERATED"
    }, indent=2))
    return 0 if not ISSUES else 1


if __name__ == "__main__":
    sys.exit(run())
