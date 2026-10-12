#!/usr/bin/env python3
"""Week 5 preliminary packet preflight; additive to V5.5, NOT renderer QA."""
import json
import sys
from pathlib import Path

CANONICAL_BINDINGS = Path(__file__).resolve().parents[2] / "canon" / "characters" / "NATIVE_RENDER_REFERENCE_BINDING_V1.json"

def validate_canonical_reference(characters, receipt, binding_doc):
    """Cross-check metadata against existing native binding authority; not proof of actual renderer use."""
    if not isinstance(characters, list) or not isinstance(receipt, dict):
        return False
    by_id = {x.get("character_id"): x for x in binding_doc.get("characters", [])}
    refs = receipt.get("bindings")
    if not isinstance(refs, list) or len(refs) != len(characters):
        return False
    seen = set()
    for ref in refs:
        if not isinstance(ref, dict):
            return False
        cid = ref.get("character_id")
        entry = by_id.get(cid)
        if cid not in characters or cid in seen or not entry:
            return False
        if entry.get("binding_state") != "DIRECT_CANONICAL_HANDLE_READY":
            return False
        if ref.get("renderer_reference_id") != entry.get("renderer_reference_id"):
            return False
        seen.add(cid)
    return seen == set(characters)

REQUIRED_FAMILIES = {"cover", "opening", "scoreboard", "overture", "matchup", "data", "closing"}
FORBIDDEN = {"outlaw & sheriff", "animal control vs rabid dog"}

def check_issue(doc, binding_doc=None):
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
    if any(p.get("characters") for p in pages) and binding_doc is None:
        try:
            binding_doc = json.loads(CANONICAL_BINDINGS.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            errors.append("canonical_native_binding_manifest_unavailable")
            binding_doc = {}
    for page in pages:
        pid = page.get("id", "<missing>")
        if page.get("family") not in REQUIRED_FAMILIES:
            errors.append(f"{pid}:unknown_page_family")
        for field in ("copy_budget", "world_anchor", "narrative_job", "text_safe_zone", "source_refs"):
            if field not in page:
                errors.append(f"{pid}:missing_{field}")
        if page.get("family") == "matchup" and page.get("art_ratio", 0) < 0.65:
            errors.append(f"{pid}:art_ratio_review")
        if page.get("characters"):
            receipt = page.get("reference_mount_receipt")
            if not receipt:
                errors.append(f"{pid}:missing_character_mount_receipt")
            elif not validate_canonical_reference(page["characters"], receipt, binding_doc):
                errors.append(f"{pid}:canonical_reference_binding_mismatch")
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
