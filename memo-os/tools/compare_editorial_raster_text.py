#!/usr/bin/env python3
"""Observed raster text diagnostics, not editorial or independent approval.

Compare OCR of immutable PNG pixels with the compositor's rendered line commands.
Only the OCR command's terminal line separator is removed. No whitespace, case,
Unicode or punctuation normalization is authorized by this diagnostic.
"""
import argparse
import difflib
import hashlib
from io import BytesIO
import json
from pathlib import Path
import subprocess
import tempfile
from PIL import Image


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def observe(png_path, receipt_path):
    raw = Path(png_path).read_bytes()
    receipt_raw = Path(receipt_path).read_bytes()
    receipt = json.loads(receipt_raw)
    if not isinstance(receipt, dict) or receipt.get('output_sha256') != digest(raw):
        raise ValueError('render receipt is not bound to PNG bytes')
    regions = receipt.get('source_text_regions')
    if not isinstance(regions, list) or not regions:
        raise ValueError('rendered text regions required')
    with Image.open(BytesIO(raw)) as source:
        source.load()
        if source.format != 'PNG' or list(source.size) != receipt.get('dimensions'):
            raise ValueError('PNG dimensions do not match render receipt')
        raster = source.convert('RGB')
    version = subprocess.run(['tesseract', '--version'], capture_output=True,
                             text=True, check=True, timeout=30).stdout.splitlines()[0]
    observations = []
    with tempfile.TemporaryDirectory(prefix='schemin-ocr-') as tmp:
        for index, region in enumerate(regions):
            if not isinstance(region, dict):
                raise ValueError('invalid region')
            box = region.get('box')
            lines = region.get('rendered_lines')
            if (not isinstance(box, list) or len(box) != 4
                    or any(type(v) is not int for v in box)
                    or not isinstance(lines, list) or not lines
                    or any(not isinstance(v, str) for v in lines)):
                raise ValueError('invalid rendered region contract')
            x, y, w, h = box
            if x < 0 or y < 0 or w <= 0 or h <= 0 or x+w > raster.width or y+h > raster.height:
                raise ValueError('region outside PNG')
            crop = raster.crop((x, y, x+w, y+h))
            target = Path(tmp) / f'{index}.png'
            crop.save(target)
            result = subprocess.run(['tesseract', str(target), 'stdout', '-l', 'eng', '--psm', '6'],
                                    capture_output=True, check=True, timeout=60)
            observed = result.stdout.decode('utf-8').removesuffix('\n')
            expected = '\n'.join(lines)
            observations.append({'region_index': index, 'role': region.get('role'),
                                 'crop_sha256': digest(target.read_bytes()),
                                 'expected_rendered_text': expected, 'observed_text': observed,
                                 'exact_match': observed == expected,
                                 'diff': list(difflib.unified_diff(expected.splitlines(), observed.splitlines(),
                                             fromfile='render_commands', tofile='observed_pixels', lineterm=''))})
    return {'status': 'DIAGNOSTIC_ONLY_NOT_APPROVED', 'png_sha256': digest(raw),
            'render_receipt_sha256': digest(receipt_raw), 'ocr_engine': version,
            'ocr_language': 'eng', 'ocr_page_segmentation_mode': 6,
            'comparison': 'exact rendered lines; remove one OCR terminal LF only',
            'all_regions_exact_match': all(r['exact_match'] for r in observations),
            'regions': observations, 'source_copy_approval_verified': False,
            'independent_visual_acceptance': False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('png')
    p.add_argument('render_receipt')
    p.add_argument('output')
    args = p.parse_args()
    if Path(args.output).resolve() in (Path(args.png).resolve(), Path(args.render_receipt).resolve()):
        p.error('output must not overwrite inputs')
    result = observe(args.png, args.render_receipt)
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['all_regions_exact_match'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
