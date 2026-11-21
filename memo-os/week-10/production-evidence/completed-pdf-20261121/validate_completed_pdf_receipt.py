#!/usr/bin/env python3
"""Strict, non-promoting Week 10 completed-artifact / historic-folio validator.

The PDF is private and intentionally absent from the repository. Without --pdf,
this validates the SOURCE-to-RECEIPT mapping, not original image/render bytes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / "preproduction/render-inputs/manifest.json"
RECEIPT = HERE / "WEEK10_COMPLETED_PDF_RECEIPT_V1.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for buf in iter(lambda: stream.read(1 << 20), b""):
            h.update(buf)
    return h.hexdigest()


def check_receipt(receipt: dict, manifest: dict, source_sha256: str) -> list[str]:
    errors: list[str] = []

    def need(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    artifact = receipt.get("artifact", {})
    origin = receipt.get("source_preproduction", {})
    statuses = receipt.get("status", {})
    delta = receipt.get("edition_delta", {})
    crosswalk = receipt.get("page_crosswalk", [])

    need(receipt.get("schema") == "schemin.memo.completed_pdf_reconciliation.v1", "schema")
    need(receipt.get("scope") == "FACTUAL_SOURCE_TO_COMPLETED_ARTIFACT_RECONCILIATION_ONLY", "scope")
    need(artifact.get("filename") == "Schemin-26-Week-10-Memo.pdf", "pdf_filename")
    need(artifact.get("sha256") == "520fa19c5881623c74c5052d36ba09fefbc793592917e523ec9f4114cf84f2b2", "pdf_sha")
    need(artifact.get("byte_length") == 106403159, "pdf_bytes")
    need(artifact.get("physical_page_count") == 35, "pdf_pages")
    need(artifact.get("bytes_embedded_in_public_repo") is False, "public_pdf_bytes")

    need(origin.get("repository") == "jakekaloper-hub/schemin-26", "source_repo")
    need(origin.get("pull_request") == 315, "source_pr")
    need(origin.get("manifest_path") == "memo-os/week-10/preproduction/render-inputs/manifest.json", "source_path")
    need(origin.get("manifest_sha256") == source_sha256, "source_manifest_changed")
    need(origin.get("manifest_folio_count") == 34, "source_page_count_claim")
    need(origin.get("manifest_art_generated_at_preproduction") is False, "preproduction_art_history")
    need(origin.get("manifest_publication_approved_at_preproduction") is False, "preproduction_publication_history")
    need(origin.get("do_not_rewrite_historical_manifest") is True, "historical_manifest_preservation")
    need(manifest.get("page_count") == 34 and len(manifest.get("pages", [])) == 34, "manifest_page_count")

    expected_source_positions = list(range(1, 35))
    need([entry.get("reading_position") for entry in manifest.get("pages", [])] == expected_source_positions, "source_position_sequence")
    need(isinstance(crosswalk, list) and len(crosswalk) == 35, "crosswalk_count")
    if not isinstance(crosswalk, list):
        return errors
    page_numbers = [entry.get("pdf_physical_page") for entry in crosswalk]
    need(page_numbers == list(range(1, 36)), "crosswalk_physical_order")
    need(len(set(page_numbers)) == 35, "duplicate_or_missing_physical_pages")

    for source in manifest.get("pages", []):
        position = source.get("reading_position")
        pdf_position = position + (1 if position >= 34 else 0)
        rows = [row for row in crosswalk if row.get("pdf_physical_page") == pdf_position]
        if len(rows) != 1:
            errors.append(f"missing_pdf_position_{pdf_position}")
            continue
        row = rows[0]
        need(row.get("source_page_id") == source.get("page_id"), f"page_id_at_{pdf_position}")
        need(row.get("source_reading_position") == position, f"source_position_at_{pdf_position}")
        need(row.get("source_title") == source.get("title"), f"source_title_at_{pdf_position}")
        need(row.get("exact_pixel_and_copy_match") == "NOT_CERTIFIED", f"unsupported_pixel_cert_at_{pdf_position}")

    added = [row for row in crosswalk if row.get("pdf_physical_page") == 34]
    need(len(added) == 1 and added[0].get("source_page_id") is None and
         added[0].get("source_title") == "PITTSY'S BOOK" and
         added[0].get("relationship") == "COMMISSIONER_EDITION_ADDED_PAGE_NOT_IN_PREPRODUCTION_MANIFEST",
         "pittsys_book_insertion")
    need(delta.get("added_page", {}).get("pdf_physical_page") == 34, "extra_page_position")
    need(delta.get("last_original_source_folio", {}).get("pdf_physical_page") == 35, "final_word_position")
    need(delta.get("last_original_source_folio", {}).get("source_page_id") == "W10-P33", "final_word_source_id")

    need(statuses.get("finished_assembled_artifact") == "VERIFIED", "complete_artifact")
    need(statuses.get("source_page_order_crosswalk") == "VERIFIED_VISUAL_STRUCTURE", "page_order_scope")
    need(statuses.get("all_35_pages_full_copy_character_pixel_qa") == "NOT_CERTIFIED", "unauthorized_qa_claim")
    need(statuses.get("source_image_bytes_to_pdf_image_bytes") == "NOT_ESTABLISHED", "unauthorized_render_provenance")
    need(statuses.get("league_distribution_date_and_channel") == "NOT_VERIFIED", "unauthorized_distribution")
    need(statuses.get("publication_manifest_release") == "NOT_PROMOTED", "unauthorized_release")
    need(statuses.get("current_benchmark") == "UNCHANGED", "unauthorized_benchmark")
    need(statuses.get("fresh_authenticated_steward_and_canon_release_signoff") == "NOT_ESTABLISHED", "unauthorized_steward_signoff")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=Path, help="Optional authorized local original PDF: verify bytes and hash only")
    args = parser.parse_args()
    receipt = json.loads(RECEIPT.read_text())
    manifest = json.loads(SOURCE.read_text())
    errors = check_receipt(receipt, manifest, sha256(SOURCE))

    if args.pdf:
        if not args.pdf.is_file():
            errors.append("pdf_unavailable")
        else:
            if sha256(args.pdf) != receipt["artifact"]["sha256"]:
                errors.append("actual_pdf_sha_mismatch")
            if args.pdf.stat().st_size != receipt["artifact"]["byte_length"]:
                errors.append("actual_pdf_size_mismatch")
            with args.pdf.open("rb") as f:
                if not f.read(5) == b"%PDF-":
                    errors.append("actual_pdf_header")

    print(json.dumps({"verdict": "PASS" if not errors else "HOLD", "errors": errors,
                      "source_folios": len(manifest["pages"]),
                      "pdf_physical_pages": receipt["artifact"]["physical_page_count"],
                      "attached_pdf_hash_checked": bool(args.pdf)}, indent=2))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
