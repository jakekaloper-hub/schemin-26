"""Bounded evidence verifier, not a literary-quality or canon-acceptance gate."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent


def reading_errors(receipt, assembly, sources):
    errors = []
    if receipt.get("scope") not in {"EXCERPT_ONLY", "FULL_ASSEMBLED_MANUSCRIPT"}:
        errors.append("unknown reading scope")
    if not assembly or not all(assembly.values()):
        errors.append("assembly must contain pinned hashes")
    if receipt.get("scope") == "FULL_ASSEMBLED_MANUSCRIPT":
        if receipt.get("read_files") != assembly or receipt.get("gaps"):
            errors.append("incomplete assembled-manuscript coverage")
    if receipt.get("accepted"):
        errors.append("reading receipt cannot grant acceptance")
    for ref in receipt.get("reference_revisits", []):
        source = sources.get(ref.get("source_id"))
        if not source:
            errors.append("unknown reference")
        elif ref.get("claim_depth") == "FULL_BOOK" and not source.get("full_book_read"):
            errors.append("reference depth inflated")
        elif source.get("read_depth") == "CATALOG_ONLY" and ref.get("method_applied"):
            errors.append("catalog is not a learned method")
    if not receipt.get("findings"):
        errors.append("missing passage-backed findings")
    for finding in receipt.get("findings", []):
        if not finding.get("passage") or len(finding.get("alternatives", [])) < 2:
            errors.append("finding needs passage and alternatives")
    return errors


def handoff_errors(packet):
    errors = []
    if packet.get("historical_claim") and packet.get("owner_binding") != "VERIFIED":
        errors.append("historical owner unverified")
    if packet.get("coverage_claim") == "FULL_MANUSCRIPT" and packet.get("coverage") != "FULL_MANUSCRIPT":
        errors.append("fixture is not manuscript coverage")
    if packet.get("review_mode") == "SIMULATED" and packet.get("accepted"):
        errors.append("simulation cannot accept")
    return errors


def verify_artifacts():
    prov = json.loads((HERE / "provenance.json").read_text())
    source = ROOT / prov["source_path"]
    assert hashlib.sha256(source.read_bytes()).hexdigest() == prov["source_sha256"], "source drift"
    assert hashlib.sha256((HERE / "before.md").read_bytes()).hexdigest() == prov["before_sha256"], "before drift"
    lo, hi = prov["source_lines"]
    expected = "\n".join(source.read_text().splitlines()[lo-1:hi]).strip() + "\n"
    assert (HERE / "before.md").read_text() == expected, "excerpt provenance mismatch"
    sources = json.loads((HERE / "sources.json").read_text())
    assert len({s["id"] for s in sources}) == len(sources)
    for s in sources:
        assert all(s.get(k) for k in ["url", "author", "title", "section_read", "attributable_claim", "application_inference"])
        assert s["full_book_read"] is False
    location = json.loads((ROOT / prov["source_location"]).read_text())
    assert not location["owner_character_ids"], "re-review changed location owner evidence"
    assert location["reference_status"]["visual_reference_status"] == "MISSING_APPROVED_VISUAL_REFERENCE"
    receipt = json.loads((HERE / "reading-receipt.json").read_text())
    assembly = {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
                for name in ["before.md", "first-revision.md", "after.md"]}
    assert receipt["assembly"] == assembly, "reading assembly drift"
    assert receipt["read_files"] == assembly, "exercise receipt drift"
    assert not reading_errors(receipt, assembly, {s["id"]: s for s in sources})
    handoff = json.loads((HERE / "handoff-exercise.json").read_text())
    assert len(handoff_errors(handoff["before"])) == 3, "negative handoff escaped"
    assert not handoff_errors(handoff["after"]), "bounded handoff rejected"
    return {"applied_receipt": "PASS_EXCERPT_ONLY", "handoff_negative_controls": 3, "provenance": "PASS", "sources": len(sources), "owner_binding": "UNVERIFIED", "visual_production": "HUMAN_REVIEW_REQUIRED", "literary_quality": "NOT_PROVEN_BY_SCRIPT", "full_manuscript_passes": 0}


if __name__ == "__main__":
    print(json.dumps(verify_artifacts(), indent=2))
