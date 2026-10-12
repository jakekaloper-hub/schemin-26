#!/usr/bin/env python3
"""Week 5 preliminary packet preflight; additive to V5.5, NOT renderer QA."""
import json
import sys

REQUIRED_FAMILIES = {"cover", "opening", "scoreboard", "overture", "matchup", "data", "closing"}
FORBIDDEN = {"outlaw & sheriff", "animal control vs rabid dog"}

def check_issue(doc):
    errors = []
    pages = doc.get("pages", [])
    ids = [p.get("id") for p in pages]
    if not pages or len(ids) != len(set(ids)) or any(not x for x in ids):
        errors.append("page_manifest_missing_or_duplicate_ids")
    if doc.get("week") != 5:
        errors.append("wrong_week")
    if doc.get("result_state") != "FACT_LOCK" and any(p.get("winner_pov") for p in pages):
        errors.append("premature_winner_pov")
    overtures = [p for p in pages if p.get("family") == "overture"]
    if len(overtures) != 6 or len({p.get("matchup_id") for p in overtures}) != 6:
        errors.append("six_distinct_overtures_required")
    for page in pages:
        pid = page.get("id", "<missing>")
        if page.get("family") not in REQUIRED_FAMILIES:
            errors.append(f"{pid}:unknown_page_family")
        for field in ("copy_budget", "world_anchor", "narrative_job", "text_safe_zone", "source_refs"):
            if field not in page:
                errors.append(f"{pid}:missing_{field}")
        if page.get("family") == "matchup" and page.get("art_ratio", 0) < 0.65:
            errors.append(f"{pid}:art_ratio_review")
        if page.get("characters") and not page.get("reference_mount_receipt"):
            errors.append(f"{pid}:missing_character_mount_receipt")
        if page.get("has_exact_data") and page.get("data_source") != "deterministic":
            errors.append(f"{pid}:untrusted_generated_data")
        story = str(page.get("story", "")).lower()
        if any(s in story for s in FORBIDDEN):
            errors.append(f"{pid}:superseded_story_premise")
        if page.get("status") == "APPROVED" and not page.get("qa_receipt"):
            errors.append(f"{pid}:approved_without_qa")
    return errors

def main():
    if len(sys.argv) != 2:
        print("usage: python week5_preflight.py manifest.json", file=sys.stderr)
        return 2
    with open(sys.argv[1], encoding="utf-8") as source:
        doc = json.load(source)
    errors = check_issue(doc)
    print(json.dumps({"status": "FAIL" if errors else "PASS", "errors": errors}, indent=2))
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
