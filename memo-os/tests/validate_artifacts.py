"""Validate actual Memo release artifacts, not self-reported manifest fields.

Candidate file layout: manifest JSON at any location, paths resolved relative to
manifest parent. Release QA remains independent: this gate never self-certifies
character likeness or editorial merit.
"""
import argparse
import hashlib
import json
from pathlib import Path

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def inspect(manifest, manifest_path):
    errors = []
    try:
        import fitz
        from PIL import Image
    except ImportError as exc:
        return [f"required PDF/image inspection dependency missing: {exc}"]
    base = Path(manifest_path).resolve().parent
    def checked_path(value, label):
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{label}: source path missing")
            return None
        path = (base / value).resolve()
        if not path.is_relative_to(base):
            errors.append(f"{label}: path escapes release directory")
            return None
        if not path.is_file():
            errors.append(f"{label}: file missing: {value}")
            return None
        return path
    pdf = checked_path(manifest.get("pdf_path"), "PDF")
    pages = manifest.get("pages", [])
    expected = manifest.get("expected_pages")
    if pdf:
        if sha256(pdf) != manifest.get("published_artifact_sha256"):
            errors.append("PDF: actual SHA256 differs from manifest")
        try:
            document = fitz.open(pdf)
            if document.needs_pass or not document.is_pdf:
                errors.append("PDF: encrypted or not PDF")
            elif document.page_count != expected:
                errors.append(f"PDF: actual page count {document.page_count} != {expected}")
            else:
                for i in range(document.page_count):
                    sheet = document.load_page(i)
                    if sheet.rect.width <= 0 or sheet.rect.height <= 0:
                        errors.append(f"PDF page {i+1}: invalid dimensions")
                    # Render at phone-like width to check ability to process
                    # the actual final PDF (not a self-declared QA flag).
                    scale = 390 / sheet.rect.width
                    bitmap = sheet.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
                    if bitmap.width < 380 or bitmap.height < 100:
                        errors.append(f"PDF page {i+1}: mobile preview unreadable/invalid")
        except Exception as exc:
            errors.append(f"PDF: failed actual rendering: {exc}")
        finally:
            try:
                document.close()
            except Exception:
                pass
    # Forward issue masters: historical released candidates retain their original geometry.
    # Explicitly opted-in candidates (including in-progress Week 7) and Week 8+
    # must pass the native format gate; never infer a historical publication rewrite.
    issue_week = manifest.get("week")
    forward_native = (type(issue_week) is int and issue_week >= 8) or manifest.get("native_page_format") == "1080x1920"
    if forward_native:
        import importlib.util
        spec = importlib.util.spec_from_file_location("memo_native_png", Path(__file__).resolve().parents[1] / "native_png_contract.py")
        native = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(native)
    for page in pages:
        slot = page.get("slot")
        path = checked_path(page.get("asset_path"), f"page {slot}")
        if not path:
            continue
        if sha256(path) != page.get("asset_sha256"):
            errors.append(f"page {slot}: actual asset hash mismatch")
        try:
            with Image.open(path) as im:
                im.verify()
            if forward_native:
                try:
                    native.validate_png(path)
                except native.NativePNGError as exc:
                    errors.append(f"page {slot}: native 1080x1920 PNG rejected: {exc}")
            with Image.open(path) as im:
                if im.width < 390 or im.height < 700:
                    errors.append(f"page {slot}: insufficient master dimensions")
        except Exception as exc:
            errors.append(f"page {slot}: corrupt or unsupported image: {exc}")
    return errors


def inspect_creative_dna(manifest, manifest_path):
    """Bind Week 6+ staged Memo publication to a hashed Creative DNA page packet.

    This supplements existing release gates and does not attest to visual QA.
    """
    import re
    import sys

    if not isinstance(manifest, dict):
        return ["creative DNA: manifest must be an object"]

    base = Path(manifest_path).resolve().parent
    found = re.fullmatch(r"2026-week-(\d+)", base.name)
    folder_week = int(found.group(1)) if found else None
    raw_week = manifest.get("week")
    declared_season = manifest.get("season", 2026 if found else None)
    if found and declared_season not in (2026, "2026"):
        return ["creative DNA: folder season conflicts with declared season"]
    if found and raw_week is not None and raw_week != folder_week:
        return ["creative DNA: folder week conflicts with declared week"]
    week = folder_week if found else (raw_week if type(raw_week) is int else None)
    if declared_season not in (2026, "2026") or week is None or week < 6:
        return []

    errors = []
    relative = manifest.get("creative_dna_packet_path")
    if not isinstance(relative, str) or not relative.strip():
        return ["creative DNA: Week 6+ candidate missing creative_dna_packet_path"]
    source = (base / relative).resolve()
    if not source.is_relative_to(base):
        return ["creative DNA: packet path escapes release candidate directory"]
    if not source.is_file():
        return [f"creative DNA: source file missing: {relative}"]
    if sha256(source) != manifest.get("creative_dna_packet_sha256"):
        return ["creative DNA: packet SHA256 mismatch"]
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        return [f"creative DNA: invalid packet JSON: {exc}"]

    current_root = Path(__file__).resolve().parents[1]
    dna_root = current_root / "creative-dna"
    sys.path.insert(0, str(dna_root))
    from validate_creative_dna import validate_packet
    registry = json.loads((dna_root / "COMMISSIONER_CREATIVE_DNA_V1.json").read_text(encoding="utf-8"))
    errors.extend("creative DNA: " + issue for issue in validate_packet(data, registry))
    if not isinstance(data, dict) or not isinstance(data.get("pages"), list):
        return errors
    expected = manifest.get("expected_pages")
    rows = data["pages"]
    slots = [row.get("slot") for row in rows if isinstance(row, dict)]
    if type(expected) is not int or len(rows) != expected or any(type(n) is not int for n in slots) or sorted(n for n in slots if type(n) is int) != list(range(1, expected + 1)):
        errors.append("creative DNA: candidate page slots must cover every physical page")
    return errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest")
    args = parser.parse_args()
    with open(args.manifest, encoding="utf-8") as f:
        manifest = json.load(f)
    from validate_issue import validate
    from validate_evidence import validate_evidence
    from validate_character_provenance import validate_character_provenance
    errors = validate(manifest) + inspect(manifest, args.manifest) + validate_evidence(manifest, Path(args.manifest).resolve().parent) + inspect_creative_dna(manifest, args.manifest) + validate_character_provenance(manifest, Path(args.manifest).resolve().parent)
    print(json.dumps({"status": "FAIL" if errors else "PASS", "errors": errors}, indent=2))
    return bool(errors)

if __name__ == "__main__":
    raise SystemExit(main())
