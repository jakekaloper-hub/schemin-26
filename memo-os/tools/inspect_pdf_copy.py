#!/usr/bin/env python3
"""Final PDF render-back/text diagnostics; never authenticates editorial approval."""
import hashlib
import json
from pathlib import Path
import tempfile
import subprocess
import fitz
from compare_editorial_raster_text import observe


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def inspect_pdf_copy(manifest, manifest_path):
    """Observe declared editorial regions on final PDF pages, preserving gaps.

    Called after the existing artifact gate. The source compositor receipt must
    match the master and source spec. A derivative receipt is only an OCR input,
    never a replacement for original approval/provenance evidence.
    """
    base = Path(manifest_path).resolve().parent
    errors = []
    report = {'status': 'DIAGNOSTIC_ONLY_NOT_APPROVED', 'pages': [],
              'independent_acceptance': False, 'errors': errors}

    def read(relative):
        if not isinstance(relative, str) or not relative:
            raise ValueError('missing source path')
        path = (base / relative).resolve()
        if not path.is_relative_to(base):
            raise ValueError('path escapes release directory')
        return path.read_bytes()

    if not isinstance(manifest, dict):
        errors.append("manifest must be an object")
        return report
    if manifest.get('artifact_stage', 'ISSUE_PACKAGE') != 'ISSUE_PACKAGE':
        report['status'] = 'NOT_APPLICABLE_PAGE_PRODUCTION'
        return report
    try:
        pdf_bytes = read(manifest.get('pdf_path'))
        report['pdf_sha256'] = digest(pdf_bytes)
        if report['pdf_sha256'] != manifest.get('published_artifact_sha256'):
            raise ValueError('PDF hash mismatch')
        with fitz.open(stream=pdf_bytes, filetype='pdf') as doc, tempfile.TemporaryDirectory(prefix='memo-pdf-copy-') as tmp:
            pages = manifest.get('pages')
            if not isinstance(pages, list) or len(pages) != doc.page_count or any(not isinstance(p, dict) for p in pages):
                raise ValueError('PDF/manifest page count mismatch')
            for index, page in enumerate(pages):
                sheet = doc[index]
                entry = {'physical_page': index+1, 'selectable_pdf_text': sheet.get_text(),
                         'region_comparison': 'NOT_RUN_NO_EDITORIAL_RECEIPT'}
                report['pages'].append(entry)
                if not page.get('editorial_receipt_path'):
                    continue
                try:
                    receipt_raw = read(page['editorial_receipt_path'])
                    receipt = json.loads(receipt_raw)
                    master_raw = read(page.get('asset_path'))
                    spec_raw = read(page.get('editorial_spec_path'))
                    if not isinstance(receipt, dict) or receipt.get('output_sha256') != digest(master_raw) or digest(master_raw) != page.get('asset_sha256'):
                        raise ValueError('editorial receipt/master hash mismatch')
                    if receipt.get('spec_sha256') != digest(spec_raw):
                        raise ValueError('editorial source spec hash mismatch')
                    from PIL import Image
                    from io import BytesIO
                    with Image.open(BytesIO(master_raw)) as master:
                        width, height = master.size
                        master_rgb = master.convert('RGB').tobytes()
                    bitmap = sheet.get_pixmap(matrix=fitz.Matrix(width/sheet.rect.width, height/sheet.rect.height),
                                               colorspace=fitz.csRGB, alpha=False, annots=True)
                    if sheet.rotation or bitmap.width != width or bitmap.height != height or bitmap.samples != master_rgb:
                        raise ValueError('final PDF rendered pixels differ from master')
                    raster = Path(tmp) / f'page{index}.png'
                    bitmap.save(raster)
                    derivative = dict(receipt, output_sha256=digest(raster.read_bytes()))
                    derivative_path = Path(tmp) / f'render{index}.json'
                    derivative_path.write_text(json.dumps(derivative))
                    entry.update({'original_render_receipt_sha256': digest(receipt_raw),
                                  'source_spec_sha256': digest(spec_raw),
                                  'master_sha256': digest(master_raw),
                                  'observation': observe(raster, derivative_path),
                                  'region_comparison': 'OBSERVED'})
                    if not entry['observation']['all_regions_exact_match']:
                        errors.append(f'PDF page {index+1}: observed editorial text differs from rendered commands')
                except (OSError, ValueError, TypeError, KeyError, RuntimeError, subprocess.SubprocessError) as exc:
                    entry['region_comparison'] = 'FAILED'
                    errors.append(f'PDF page {index+1}: text observation failed: {exc}')
    except (OSError, ValueError, TypeError, RuntimeError) as exc:
        errors.append(f'PDF text diagnostic failed: {exc}')
    report['all_pages_observed'] = bool(report['pages']) and all(p['region_comparison'] == 'OBSERVED' for p in report['pages'])
    return report
