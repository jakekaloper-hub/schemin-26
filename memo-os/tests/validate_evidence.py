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
    # Prospective issues must present the signed Founder release transaction.
    # Historical published weeks are not retroactively rewritten.
    if manifest.get("season") == 2026 and isinstance(manifest.get("week"), int) and manifest["week"] >= 6:
        state_path = manifest.get("founder_release_state_path")
        if not isinstance(state_path, str) or not state_path:
            errors.append("Founder release transaction missing")
        else:
            state_file = (Path(base).resolve() / state_path).resolve()
            if not state_file.is_relative_to(Path(base).resolve()) or not state_file.is_file():
                errors.append("Founder release transaction inaccessible")
            else:
                try:
                    import sys
                    root = Path(__file__).resolve().parents[2]
                    if str(root) not in sys.path:
                        sys.path.insert(0, str(root))
                    from governance.publication.founder_approval_runtime import inspect, verify_receipt
                    issue = inspect(state_file)
                    if issue.get("state") != "RELEASED":
                        errors.append("Founder transaction not released")
                    if str(issue.get("issue_id")) != str(manifest.get("issue_id")):
                        errors.append("Founder transaction issue mismatch")
                    if issue.get("final_pdf_sha256") != manifest.get("published_artifact_sha256"):
                        errors.append("Founder transaction PDF mismatch")
                    # The signed persisted state proves integrity, not actual upstream
                    # identity-provider authentication or reviewer independence.
                    approvals = issue.get("approvals", {})
                    for slot, gate, expected_hash in (
                        ("creative", "CREATIVE_DIRECTION", issue.get("approved_plan_sha256")),
                        ("publication", "FINAL_PUBLICATION", issue.get("final_pdf_sha256")),
                    ):
                        approval = approvals.get(slot, {})
                        if approval.get("gate") != gate or approval.get("artifact_sha256") != expected_hash or approval.get("decision") != "APPROVED":
                            errors.append("Founder approval absent or stale: " + slot)
                except Exception as exc:
                    errors.append("Founder transaction integrity or verification failure: " + type(exc).__name__)
    base = Path(base).resolve()
    # Prospective releases cannot turn a staged ECS assignment into an ACK.
    # This verifies receipt consistency, not external authentication.
    forward = manifest.get('season') == 2026 and type(manifest.get('week')) is int and manifest['week'] >= 9
    if forward:
        steward_path = manifest.get('data_steward_receipt_path')
        if not isinstance(steward_path, str) or not steward_path:
            errors.append('Data Steward authenticated acceptance receipt required')
        else:
            source = (base / steward_path).resolve()
            if not source.is_relative_to(base) or not source.is_file():
                errors.append('Data Steward receipt inaccessible')
            elif digest(source) != manifest.get('data_steward_receipt_sha256'):
                errors.append('Data Steward receipt hash mismatch')
            else:
                try:
                    from steward_receipt import verify as verify_steward_receipt
                    record = verify_steward_receipt(json.loads(source.read_text()))
                    if record.get('state') != 'VALIDATED' or record.get('decision') != 'ACCEPTED':
                        errors.append('Data Steward acceptance not validated')
                    if not record.get('receiver_id') or not record.get('acknowledged_at') or not record.get('verification_method'):
                        errors.append('Data Steward receiver authentication evidence missing')
                    if record.get('source_receipt_sha256') != manifest.get('provider_receipt_sha256'):
                        errors.append('Data Steward acceptance not bound to provider receipt')
                    if record.get('league_id') != manifest.get('league_id') or record.get('week') != manifest.get('week'):
                        errors.append('Data Steward league/week mismatch')
                    if record.get('freshness') != 'PASS' or record.get('semantics') != 'PASS' or record.get('lineage') != 'PASS':
                        errors.append('Data Steward semantic/freshness/lineage gate unresolved')
                except (ValueError, TypeError, KeyError) as exc:
                    errors.append('Data Steward receipt malformed or untrusted: ' + str(exc))
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
        # Week 9+ character scenes require an independent image-bound
        # action/pose review, not merely a visually attractive hero image.
        forward = manifest.get('season') == 2026 and type(manifest.get('week')) is int and manifest['week'] >= 9
        if forward and page.get('characters'):
            required.add('physicality')
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
            if scope in {"character", "atlas", "visual", "mobile", "physicality"} and isinstance(path, str):
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
            if scope == 'physicality':
                if not rec.get('described_action') or not rec.get('observed_pose') or not rec.get('spatial_interaction'):
                    errors.append(f"page {n}: physicality requires action/pose/interaction assessment")
                if rec.get('reviewer_id') == page.get('generation_operator_id'):
                    errors.append(f"page {n}: physicality reviewer not independent")
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
