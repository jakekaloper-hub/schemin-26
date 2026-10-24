"""Post-render Week 5 PNG candidate checker (never a publication or Umpire pass).

This validates actual PNG bytes, page packet/manuscript, registered original/mount
bytes, shot metadata, and verified payoff transcriptions. Neither manually
supplied annotations nor code checks attest that a native renderer conditioned
on those images or that its pixels look correct. Live pixel QA remains mandatory.
"""
import argparse
import importlib.util
import hashlib
import json
import struct
import zlib
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
GOTW_ROLES = {
    "P004": "QUIET_MARKET_APPROACH_PROSE_FORWARD",
    "P005": "OVERHEAD_MONUMENTAL_BOARD_AND_SHELTERED_STALLS",
    "P006": "DIAGONAL_TACTICAL_STONE_COLLISION",
    "P007": "CHECKMATE_AFTERMATH_WITH_RESULTS_LOWER_THIRD",
}
PAYOFFS = {"P007", "P011", "P015", "P019", "P023", "P027"}


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _safe_path(root, relative):
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError("ASSET_PATH_UNSAFE")
    root = Path(root).resolve()
    path = (root / relative).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError("ASSET_PATH_UNSAFE")
    return path


def _png_header(path):
    """Transport-level structural PNG validation; not pixel-semantic QA."""
    blob = Path(path).read_bytes()
    if not blob.startswith(PNG_SIGNATURE):
        raise ValueError("NOT_PNG")
    pos, ihdr, idat, iend, size_xy = 8, False, False, False, None
    while pos + 12 <= len(blob):
        size = struct.unpack_from(">I", blob, pos)[0]
        kind = blob[pos + 4:pos + 8]
        end = pos + 12 + size
        if end > len(blob):
            raise ValueError("PNG_TRUNCATED")
        data = blob[pos + 8:pos + 8 + size]
        crc = struct.unpack_from(">I", blob, pos + 8 + size)[0]
        if (zlib.crc32(kind + data) & 0xffffffff) != crc:
            raise ValueError("PNG_CRC_MISMATCH")
        if kind == b"IHDR":
            if ihdr or pos != 8 or size != 13:
                raise ValueError("PNG_IHDR_INVALID")
            ihdr, size_xy = True, struct.unpack_from(">II", data)
        elif kind == b"IDAT":
            idat = True
        elif kind == b"IEND":
            iend = True
            if end != len(blob):
                raise ValueError("PNG_TRAILING_BYTES")
            break
        pos = end
    if not (ihdr and idat and iend) or size_xy != (1024, 1536):
        raise ValueError("INVALID_1024_X_1536_PNG")


def _locked_copy(packet):
    anchor = "**Narrative copy:**\n\n"
    return packet.split(anchor, 1)[1].split("\n\n**Visual coordination", 1)[0].strip() if anchor in packet else None


def inspect_candidate(page_id, png_path, receipt, repo_root, previous_page_digests=None):
    def stop(reason):
        return {"state": "CANDIDATE_BLOCKED", "page_id": page_id, "reason": reason}

    root = Path(repo_root).resolve()
    week = root / "memo-os" / "week-5"
    if not isinstance(receipt, dict):
        return stop("CANDIDATE_RECEIPT_REQUIRED")
    try:
        manifest = json.loads((week / "PUBLICATION_PAGE_MANIFEST.json").read_text())
        titles = json.loads((week / "production-evidence" / "WEEK_5_CHARACTER_AND_TITLE_RENDER_GATES_2026-10-13.json").read_text())
        page = next(p for p in manifest["pages"] if p["page_id"] == page_id)
        title = next(p for p in titles["pages"] if p["page_id"] == page_id)
    except (OSError, KeyError, StopIteration, ValueError, TypeError):
        return stop("AUTHORITY_UNAVAILABLE")
    png_path = Path(png_path)
    if not png_path.is_file() or png_path.name != page.get("expected_flattened_png"):
        return stop("WRONG_OR_MISSING_PAGE_IMAGE")
    try:
        _png_header(png_path)
    except (OSError, ValueError, struct.error):
        return stop("INVALID_1024_X_1536_PNG")
    digest = _sha(png_path)
    if receipt.get("page_id") != page_id or receipt.get("png_sha256") != digest:
        return stop("PNG_RECEIPT_MISMATCH")
    if previous_page_digests and any(pid != page_id and d == digest for pid, d in previous_page_digests.items()):
        return stop("REUSED_PAGE_IMAGE")
    if receipt.get("visible_primary_header_transcription") != title.get("display_header"):
        return stop("MAIN_HEADER_NOT_VERIFIED")
    if receipt.get("league_masthead_dominates") is not False:
        return stop("MASTHEAD_HIERARCHY_UNVERIFIED")
    try:
        packet = _safe_path(root, page["packet_path"])
        packet_sha = _sha(packet)
    except (OSError, KeyError, ValueError, TypeError):
        return stop("SOURCE_PACKET_UNAVAILABLE")
    if receipt.get("source_packet_sha256") != packet_sha:
        return stop("SOURCE_PACKET_DRIFT")
    text = _locked_copy(packet.read_text(encoding="utf-8"))
    if not text or receipt.get("transcribed_editorial_copy") != text:
        return stop("MANUSCRIPT_NOT_VERBATIM")
    if page_id in GOTW_ROLES and receipt.get("shot_role") != GOTW_ROLES[page_id]:
        return stop("GOTW_SCENE_ROLE_MISMATCH")
    if page_id == "P004" and receipt.get("editorial_text_area_percent") not in range(65, 76):
        return stop("OVERTURE_EDITORIAL_RATIO_UNVERIFIED")
    if page_id == "P005" and receipt.get("camera") != "OVERHEAD_WIDE":
        return stop("CHESSBOARD_OVERHEAD_CAMERA_REQUIRED")
    if page_id in PAYOFFS:
        if not receipt.get("illustrated_lower_third_result_banner_inspected"):
            return stop("PAYOFF_ILLUSTRATED_RESULTS_BANNER_MISSING")
        try:
            contract = json.loads((week / "production-evidence" / "WEEK_5_PAYOFF_RESULT_BANNER_CONTRACT_2026-10-13.json").read_text())
            result = next(p for p in contract["result_pages"] if p["page_id"] == page_id)
            if result["result_status"] != "DECIDED":
                return stop("RESULT_NOT_VERIFIED_FINAL")
            expected_panel = {
                "away_team": result["away"]["team"],
                "away_points": f'{result["away"]["points"]:.2f}',
                "away_record": result["away"]["post_week_5_record"],
                "home_team": result["home"]["team"],
                "home_points": f'{result["home"]["points"]:.2f}',
                "home_record": result["home"]["post_week_5_record"],
                "winner_team": result["winner_team"],
            }
        except (OSError, KeyError, StopIteration, ValueError, TypeError):
            return stop("VERIFIED_RESULT_CONTRACT_MISSING")
        if receipt.get("result_panel_transcription") != expected_panel:
            return stop("RESULT_PANEL_FACT_OR_TYPO_MISMATCH")
    try:
        expected_refs = {r["character_id"]: r["raw_sha256"] for r in title["owner_reference_requirements"]}
    except (KeyError, TypeError, ValueError):
        return stop("OWNER_REFERENCE_CONTRACT_INVALID")
    gate_spec = importlib.util.spec_from_file_location("week5_preflight_authority", Path(__file__).with_name("production_gate.py"))
    gate = importlib.util.module_from_spec(gate_spec)
    gate_spec.loader.exec_module(gate)
    authority = gate.current_reference_authority(root, expected_refs)
    if authority.get("state") != "REFERENCE_AUTHORITY_RESOLVED":
        return stop("ACTIVE_SOURCE_CONTRACT_MISMATCH")
    refs = receipt.get("reference_mounts")
    if not isinstance(refs, list) or len(refs) != len(expected_refs):
        return stop("ORIGINAL_REFERENCES_UNVERIFIED")
    seen, subjects, ids = set(), set(), set()
    for ref in refs:
        if not isinstance(ref, dict) or ref.get("character_id") not in expected_refs:
            return stop("CHARACTER_SUBSTITUTION")
        cid = ref["character_id"]
        if cid in seen:
            return stop("DUPLICATE_CHARACTER_REFERENCE")
        seen.add(cid)
        subject, generation = ref.get("subject_binding_id"), ref.get("generation_reference_id")
        if not isinstance(subject, str) or not subject or not isinstance(generation, str) or not generation:
            return stop("SUBJECT_BINDING_UNVERIFIED")
        subjects.add(subject)
        ids.add(generation)
        try:
            original = _safe_path(root, ref.get("original_repo_path"))
            mounted = _safe_path(root, ref.get("mounted_repo_path"))
            if _sha(original) != expected_refs[cid] or _sha(mounted) != expected_refs[cid]:
                return stop("SOURCE_OR_MOUNT_BYTES_WRONG")
        except (OSError, ValueError, TypeError):
            return stop("REFERENCE_BYTES_UNAVAILABLE")
    if seen != set(expected_refs) or len(subjects) != len(expected_refs) or len(ids) != len(expected_refs):
        return stop("SUBJECT_TO_REFERENCE_SWAP_OR_COLLISION")
    if not receipt.get("full_res_manual_pixel_review") or not receipt.get("mobile_390px_manual_review"):
        return stop("PIXEL_AND_MOBILE_REVIEW_UNVERIFIED")
    return {
        "state": "TECHNICAL_CANDIDATE_CHECK_PASSED_PUBLICATION_HOLD",
        "page_id": page_id,
        "png_sha256": digest,
        "packet_sha256": packet_sha,
        "provider_conditioning": "NOT_ATTESTED_BY_THIS_CHECK",
        "independent_umpire": "NOT_ATTESTED_BY_THIS_CHECK",
        "may_publish": False,
    }


def main():
    p = argparse.ArgumentParser(description="Check an actual Week 5 PNG without granting publication")
    p.add_argument("page_id")
    p.add_argument("png")
    p.add_argument("--repo-root", default=".")
    p.add_argument("--receipt", required=True)
    p.add_argument("--previous-digests")
    args = p.parse_args()
    try:
        receipt = json.loads(Path(args.receipt).read_text(encoding="utf-8"))
        ledger = json.loads(Path(args.previous_digests).read_text(encoding="utf-8")) if args.previous_digests else None
        result = inspect_candidate(args.page_id, args.png, receipt, args.repo_root, ledger)
    except (OSError, ValueError, TypeError):
        result = {"state": "CANDIDATE_BLOCKED", "reason": "INVALID_RECEIPT_OR_LEDGER"}
    print(json.dumps(result, sort_keys=True))
    return 0 if result["state"] == "TECHNICAL_CANDIDATE_CHECK_PASSED_PUBLICATION_HOLD" else 2


if __name__ == "__main__":
    raise SystemExit(main())
