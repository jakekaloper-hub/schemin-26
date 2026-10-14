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
            with Image.open(path) as im:
                if im.width < 390 or im.height < 700:
                    errors.append(f"page {slot}: insufficient master dimensions")
        except Exception as exc:
            errors.append(f"page {slot}: corrupt or unsupported image: {exc}")
    return errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest")
    args = parser.parse_args()
    with open(args.manifest, encoding="utf-8") as f:
        manifest = json.load(f)
    from validate_issue import validate
    from validate_evidence import validate_evidence
    errors = validate(manifest) + inspect(manifest, args.manifest) + validate_evidence(manifest, Path(args.manifest).resolve().parent)
    print(json.dumps({"status": "FAIL" if errors else "PASS", "errors": errors}, indent=2))
    return bool(errors)

if __name__ == "__main__":
    raise SystemExit(main())
