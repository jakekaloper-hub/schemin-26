#!/usr/bin/env python3
"""Static, fail-closed structural checks for Memo OS Commissioner Creative DNA packets.

This does NOT authenticate a renderer, facts, images, or Umpire. It validates
previsualization/page-packet contracts before existing QA and release gates.
"""
import argparse
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
PATTERN_IDS = {
    "power_rankings", "cinematic_sequence",
    "matchup_progression_receipt", "opening_drive",
}


def _filled(value):
    return isinstance(value, str) and bool(value.strip())


def _number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _record(obj):
    return (
        isinstance(obj, dict)
        and isinstance(obj.get("wins"), int)
        and not isinstance(obj["wins"], bool)
        and obj["wins"] >= 0
        and isinstance(obj.get("losses"), int)
        and not isinstance(obj["losses"], bool)
        and obj["losses"] >= 0
    )


def validate_registry(registry):
    errors = []
    if not isinstance(registry, dict):
        return ["registry is not an object"]
    patterns = registry.get("patterns")
    if not isinstance(patterns, list):
        return ["patterns missing"]
    ids = [p.get("id") for p in patterns if isinstance(p, dict)]
    if len(patterns) != 4 or set(ids) != PATTERN_IDS or len(ids) != len(set(ids)):
        errors.append("expected exactly four distinct approved patterns")
    for p in patterns:
        if not isinstance(p, dict):
            errors.append("invalid pattern")
            continue
        if not p.get("not_character_authority"):
            errors.append(f"{p.get('id')} must be explicitly non-authoritative for character identity")
        if not p.get("reference") or not p.get("qa") or not p.get("required_data"):
            errors.append(f"{p.get('id')} missing reference/QA/data")
    if registry.get("reuse_policy", {}).get("historical_pages") != "COMPOSITION_REFERENCE_ONLY":
        errors.append("historical reference images cannot become character identity authority")
    return errors


def validate_packet(packet, registry):
    """Return deficiencies, never a production/publication approval."""
    errors = validate_registry(registry)
    if errors:
        return errors
    if not isinstance(packet, dict):
        return ["issue packet missing"]
    patterns = {p["id"]: p for p in registry["patterns"]}
    pages = packet.get("pages")
    if not isinstance(pages, list) or not pages:
        return ["pages must be a nonempty array"]
    used = set()
    seen_page_ids = set()
    for idx, page in enumerate(pages):
        location = f"pages[{idx}]"
        if not isinstance(page, dict):
            errors.append(f"{location} must be an object")
            continue
        pid = page.get("page_id")
        if not _filled(pid) or pid in seen_page_ids:
            errors.append(f"{location} has missing or repeated page_id")
        seen_page_ids.add(pid)
        selected = page.get("creative_dna_patterns", [])
        if not isinstance(selected, list) or len(selected) != len(set(selected)):
            errors.append(f"{location} has invalid/duplicate creative_dna_patterns")
            continue
        for pattern_id in selected:
            if pattern_id not in patterns:
                errors.append(f"{location} has unknown pattern {pattern_id}")
                continue
            used.add(pattern_id)
            payload = (page.get("creative_dna") or {}).get(pattern_id)
            if not isinstance(payload, dict):
                errors.append(f"{location}/{pattern_id}: creative_dna payload missing")
                continue
            for required in patterns[pattern_id]["required_data"]:
                if required not in payload or payload[required] in (None, "", [], {}):
                    errors.append(f"{location}/{pattern_id}: missing {required}")
            if pattern_id == "power_rankings":
                _check_rankings(payload, errors, location)
            elif pattern_id == "opening_drive":
                _check_opening(payload, errors, location)
            elif pattern_id == "cinematic_sequence":
                _check_cinema(payload, errors, location)
            elif pattern_id == "matchup_progression_receipt":
                _check_receipt(payload, errors, location)
        if selected:
            for key in ("image_tells", "prose_tells", "data_tells"):
                if not _filled(page.get(key)):
                    errors.append(f"{location}: missing {key} for editorial complementarity")
    required = set(registry["production_bindings"]["required_issue_modules"])
    omissions = packet.get("explicit_module_omission_reasons", {})
    for pattern_id in sorted(required - used):
        if not isinstance(omissions, dict) or not _filled(omissions.get(pattern_id)):
            errors.append(f"issue missing required module {pattern_id} without explicit omission")
    return errors


def _check_rankings(data, errors, location):
    prefix = location + "/power_rankings"
    rows = data.get("ranking_rows")
    if not _filled(data.get("fact_lock_ref")) or not _filled(data.get("previous_published_rankings_ref")):
        errors.append(prefix + ": missing factual baseline references")
    if not isinstance(rows, list) or len(rows) != 12:
        errors.append(prefix + ": expected exactly 12 ranking rows")
        return
    ranks, teams, priors = set(), set(), set()
    for row in rows:
        if not isinstance(row, dict):
            errors.append(prefix + ": invalid row")
            continue
        rank, prior, move = row.get("rank"), row.get("prior_rank"), row.get("movement")
        if type(rank) is not int or not 1 <= rank <= 12:
            errors.append(prefix + ": invalid rank")
        if type(prior) is not int or not 1 <= prior <= 12:
            errors.append(prefix + ": invalid prior_rank")
        if type(move) is not int or (type(prior) is int and type(rank) is int and move != prior - rank):
            errors.append(prefix + ": movement not equal to prior_rank - rank")
        if rank in ranks or prior in priors:
            errors.append(prefix + ": duplicated rank/prior rank")
        ranks.add(rank)
        priors.add(prior)
        team = row.get("team_id")
        if not _filled(team) or team in teams:
            errors.append(prefix + ": missing/duplicate stable team_id")
        teams.add(team)
        if not _record(row.get("record")):
            errors.append(prefix + ": invalid W-L record")
        if not _filled(row.get("commentary")):
            errors.append(prefix + ": missing one-line rationale")
        if not _filled(row.get("portrait_asset_ref")):
            errors.append(prefix + ": missing approved portrait asset")
        if row.get("portrait_source") not in ("same_issue_accepted_matchup_crop", "exact_current_approved_canonical_asset"):
            errors.append(prefix + ": portrait source not approved")


def _check_opening(data, errors, location):
    prefix = location + "/opening_drive"
    for key in ("weekly_thesis", "narrative_text", "world_atlas_ref", "entry_world_state_ref"):
        if not _filled(data.get(key)):
            errors.append(f"{prefix}: {key} missing")
    refs = data.get("fact_evidence_refs")
    if not isinstance(refs, list) or not refs or any(not _filled(v) for v in refs):
        errors.append(prefix + ": missing event evidence refs")
    callouts = data.get("world_event_callouts")
    if not isinstance(callouts, list) or len(callouts) < 2:
        errors.append(prefix + ": need at least two verified event-to-world callouts")
        return
    for c in callouts:
        if not isinstance(c, dict) or any(not _filled(c.get(k)) for k in ("event_ref", "world_consequence", "location_ref")):
            errors.append(prefix + ": callout not linked to event and world location")


def _check_cinema(data, errors, location):
    prefix = location + "/cinematic_sequence"
    beats = data.get("sequence_beats")
    if not isinstance(beats, list) or len(beats) < 2 or any(not _filled(v) for v in beats):
        errors.append(prefix + ": at least two meaningful sequential beats needed")
    for key in ("narrative_text", "fantasy_causality_ref", "world_atlas_ref"):
        if not _filled(data.get(key)):
            errors.append(f"{prefix}: {key} missing")
    if data.get("text_treatment") not in ("integrated", "hybrid", "image_led_minimal"):
        errors.append(prefix + ": unknown text treatment")


def _check_receipt(data, errors, location):
    prefix = location + "/matchup_progression_receipt"
    accepted = data.get("accepted_character_assets")
    refs = data.get("scene_asset_refs")
    result = data.get("result")
    if not isinstance(refs, list) or not refs or any(not _filled(v) for v in refs):
        errors.append(prefix + ": missing accepted scene assets")
    if not isinstance(accepted, dict) or not isinstance(result, dict):
        errors.append(prefix + ": accepted assets or result missing")
        return
    sides = []
    for side in ("home", "away"):
        row = result.get(side)
        if not isinstance(row, dict):
            errors.append(f"{prefix}: {side} missing")
            continue
        team = row.get("team_id")
        if not _filled(team) or not _filled(row.get("portrait_asset_ref")):
            errors.append(f"{prefix}: {side} missing team/portrait")
        if not _record(row.get("record")) or not _number(row.get("score")) or row.get("score", -1) < 0:
            errors.append(f"{prefix}: {side} invalid result data")
        if isinstance(accepted, dict) and row.get("portrait_asset_ref") != accepted.get(team):
            errors.append(f"{prefix}: {side} portrait is not from accepted matchup wave")
        sides.append(row)
    if len(sides) == 2 and all(_number(s.get("score")) for s in sides):
        margin = abs(sides[0]["score"] - sides[1]["score"])
        if not _number(result.get("margin")) or abs(margin - result["margin"]) > 0.001:
            errors.append(prefix + ": margin does not match score difference")
    if not _filled(data.get("fact_lock_ref")):
        errors.append(prefix + ": missing final result Fact Lock")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, help="Optional candidate issue JSON to validate; no implied release approval")
    args = parser.parse_args()
    registry = json.loads((HERE / "COMMISSIONER_CREATIVE_DNA_V1.json").read_text(encoding="utf-8"))
    errors = validate_registry(registry)
    if args.packet:
        errors += validate_packet(json.loads(args.packet.read_text(encoding="utf-8")), registry)
    if errors:
        for issue in errors:
            print("FAIL:", issue)
        return 1
    print("PASS: creative DNA registry" + (" and candidate structural packet" if args.packet else "") + " (NOT final visual/release QA)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
