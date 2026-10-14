"""Release evidence gate for new Memo candidates.

Receipts are independent input records with precise artifact bindings; they do
not replace authenticated reviewer verification or actual visual judgment.
"""
import hashlib
import json
from pathlib import Path

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def validate_evidence(manifest, base):
    errors = []
    if manifest.get("publication_state") not in ("RELEASED", "PUBLISHED"):
        return errors
    base = Path(base).resolve()
    receipt_path = manifest.get("provider_receipt_path")
    if not receipt_path:
        errors.append("provider receipt required")
    else:
        source = (base / receipt_path).resolve()
        if not source.is_relative_to(base) or not source.is_file():
            errors.append("provider receipt inaccessible")
        elif digest(source) != manifest.get("provider_receipt_sha256"):
            errors.append("provider receipt hash mismatch")
        else:
            try:
                receipt = json.loads(source.read_text())
                if receipt.get("league_id") != manifest.get("league_id") or receipt.get("week") != manifest.get("week"):
                    errors.append("provider league/week mismatch")
                games = receipt.get("matchups", [])
                if len(games) != 6 or len({t for g in games for t in (g.get("home"), g.get("away"))}) != 12:
                    errors.append("provider receipt must contain six games and twelve unique teams")
                frozen = {g.get("matchup_key"): g.get("final_scores") for g in games}
                if frozen != manifest.get("results"):
                    errors.append("independent provider result mismatch")
                if receipt.get("source") != "FLAIM_ESPN" or receipt.get("status") != "FINAL":
                    errors.append("provider provenance/finality unresolved")
            except (ValueError, TypeError, KeyError):
                errors.append("provider receipt malformed")
    pdf_sha = manifest.get("published_artifact_sha256")
    for page in manifest.get("pages", []):
        n = page.get("slot")
        required = {"character", "atlas", "visual", "mobile"}
        if not page.get("characters"):
            required.remove("character")
        receipts = page.get("review_receipts")
        if not isinstance(receipts, list):
            errors.append(f"page {n}: reviewer receipts missing")
            continue
        seen = set()
        for rec in receipts:
            if not isinstance(rec, dict):
                errors.append(f"page {n}: invalid review receipt")
                continue
            scope = rec.get("scope")
            if scope in seen:
                errors.append(f"page {n}: duplicated {scope} review")
            seen.add(scope)
            if rec.get("decision") != "PASS" or not rec.get("reviewer_id") or not rec.get("reviewed_at") or not rec.get("evidence_path"):
                errors.append(f"page {n}: incomplete {scope} approval evidence")
            if rec.get("page_sha256") != page.get("asset_sha256") or rec.get("pdf_sha256") != pdf_sha:
                errors.append(f"page {n}: {scope} approval not artifact-bound")
            path = rec.get("evidence_path")
            if isinstance(path, str):
                evidence = (base / path).resolve()
                if not evidence.is_relative_to(base) or not evidence.is_file() or digest(evidence) != rec.get("evidence_sha256"):
                    errors.append(f"page {n}: {scope} evidence bytes missing/mismatched")
            if scope in {"character", "atlas", "visual", "mobile"} and isinstance(path, str):
                try:
                    from PIL import Image
                    with Image.open(evidence) as img:
                        img.verify()
                except (OSError, ValueError, NameError):
                    errors.append(f"page {n}: {scope} evidence is not a readable image")
            if scope == "character" and not rec.get("canonical_character_ids"):
                errors.append(f"page {n}: character source identifiers absent")
            if scope == "character" and not rec.get("reference_sha256"):
                errors.append(f"page {n}: canonical character source hash absent")
            if scope == "atlas" and not rec.get("venue_id"):
                errors.append(f"page {n}: Atlas venue absent")
        if not required.issubset(seen):
            errors.append(f"page {n}: missing independent review scopes {sorted(required-seen)}")
    ump = manifest.get("umpire_receipt")
    if not isinstance(ump, dict) or ump.get("decision") != "PASS" or not ump.get("reviewer_id") or not ump.get("reviewed_at") or ump.get("pdf_sha256") != pdf_sha:
        errors.append("independent Umpire evidence not bound to released PDF")
    else:
        identity = ump["reviewer_id"]
        if any(identity == r.get("reviewer_id") for p in manifest.get("pages", []) for r in p.get("review_receipts", []) if isinstance(r, dict)):
            errors.append("Umpire is not independent of page approvals")
    return errors
