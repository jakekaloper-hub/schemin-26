#!/usr/bin/env python3
"""Create offline, unreviewed OCR packets from hash-verified memo originals.

No candidate text is loaded by the public catalog. Review against source pixels
is required before a separate accepted companion can be published.
"""
import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess

SITE = Path(__file__).resolve().parent
ROOT = SITE.parents[1]
INTAKE = 'governance/publication-manifest/WEEKS_04_06_COMMISSIONER_SOURCE_INTAKE_2026_10_22.json'
STATUS = 'UNREVIEWED_OCR_CANDIDATE'


def digest(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def build_candidates(root, manifest, revision, week, pages, output, runner=subprocess.run):
    root, output = Path(root).resolve(), Path(output).resolve()
    site = root / 'productions/audience-site'
    if any(output.is_relative_to(site / name) for name in ('src', 'dist')):
        raise ValueError('Unreviewed OCR must remain outside public src/dist')
    if not re.fullmatch(r'[0-9a-f]{40}', revision):
        raise ValueError('Full source revision required')
    entries = [entry for entry in manifest.get('files', []) if entry.get('week') == week]
    if len(entries) != 1:
        raise ValueError('Week must resolve to exactly one source edition')
    entry = entries[0]
    source = (root / entry['archive_path']).resolve()
    if not source.is_relative_to(root) or not source.is_file():
        raise ValueError('Source must be an existing repository file')
    if digest(source) != entry['sha256'] or source.stat().st_size != entry['size_bytes']:
        raise ValueError('Original PDF hash or size mismatch; materialize exact LFS bytes')
    with source.open('rb') as stream:
        if not stream.read(5).startswith(b'%PDF-'):
            raise ValueError('Original is not PDF bytes')
    info = runner(['pdfinfo', str(source)], check=True, capture_output=True, text=True, timeout=30).stdout
    match = re.search(r'^Pages:\s+(\d+)\s*$', info, re.MULTILINE)
    if not match or int(match.group(1)) != entry['pages']:
        raise ValueError('Physical PDF page count differs from source manifest')
    if not pages or any(type(p) is not int or not 1 <= p <= entry['pages'] for p in pages) or len(set(pages)) != len(pages):
        raise ValueError('Choose distinct physical page numbers within the source edition')
    if output.exists() and any(output.iterdir()):
        raise ValueError('Output must be empty; do not overwrite an earlier review packet')
    output.mkdir(parents=True, exist_ok=True)
    receipts, sections = [], []
    for page in sorted(pages):
        stem = output / f'page-{page:03d}'
        runner(['pdftoppm', '-f', str(page), '-l', str(page), '-singlefile', '-scale-to', '1800',
                '-png', str(source), str(stem)], check=True, capture_output=True, timeout=120)
        runner(['tesseract', str(stem.with_suffix('.png')), str(stem), '--psm', '3'],
               check=True, capture_output=True, timeout=180)
        image, text = stem.with_suffix('.png'), stem.with_suffix('.txt')
        receipt = {'physical_page': page, 'image': image.name, 'image_sha256': digest(image),
                   'candidate_text': text.name, 'candidate_text_sha256': digest(text),
                   'status': STATUS, 'reviewed': False}
        receipts.append(receipt)
        sections.append(f'<section aria-labelledby="page-{page}"><h2 id="page-{page}">Physical page {page}</h2>'
                        '<p>Unreviewed OCR: words, names, numbers and reading order may be wrong. '
                        'Compare with the original page; this is not accepted publication text.</p>'
                        f'<div class="comparison"><a href="{image.name}"><img src="{image.name}" '
                        f'alt="Original source edition, physical page {page}; open full image for visual review"></a>'
                        f'<pre tabindex="0" aria-label="Unreviewed OCR candidate for physical page {page}">'
                        f'{html.escape(text.read_text())}</pre></div></section>')
    if digest(source) != entry['sha256']:
        raise ValueError('Source changed during OCR; discard this partial packet')
    packet = {'schema_version': 1, 'status': STATUS, 'publication_eligible': False,
              'source_revision': revision, 'source_manifest': INTAKE,
              'source_manifest_sha256': hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest(),
              'manifest_hash_encoding': 'JSON sorted keys, default separators, UTF-8',
              'source_path': entry['archive_path'], 'source_sha256': entry['sha256'],
              'source_size_bytes': entry['size_bytes'], 'source_page_count': entry['pages'],
              'processing': {'renderer': 'pdftoppm -singlefile -scale-to 1800 -png',
                             'ocr': 'tesseract --psm 3'},
              'week': week, 'pages': receipts}
    (output / 'candidate.json').write_text(json.dumps(packet, indent=2) + '\n')
    document = ('<!doctype html><html lang="en"><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1">'
                '<title>Unreviewed memo OCR review packet</title><style>'
                'body{font:18px/1.6 system-ui;max-width:1400px;margin:2rem auto;padding:0 1rem}'
                '.comparison{display:grid;grid-template-columns:1fr 1fr;gap:2rem}'
                'code{overflow-wrap:anywhere}img{max-width:100%}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}'
                ':focus-visible{outline:3px solid #245c8b} @media(max-width:700px){.comparison{grid-template-columns:1fr}}'
                '</style><main><h1>Unreviewed memo OCR review packet</h1>'
                f'<p>Week {week} · source SHA-256 <code>{entry["sha256"]}</code></p>'
                '<p>Candidate only. No factual, editorial, accessibility or publication acceptance is implied.</p>'
                '<nav aria-label="Physical pages">' + ' '.join(f'<a href="#page-{p}">Page {p}</a>' for p in sorted(pages)) +
                '</nav>' + ''.join(sections) + '</main></html>')
    (output / 'review.html').write_text(document)
    return packet


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--week', type=int, required=True)
    parser.add_argument('--page', type=int, action='append', required=True, help='Physical page, repeat for several pages')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    raw = subprocess.check_output(['git', 'show', f'{revision}:{INTAKE}'], cwd=ROOT)
    packet = build_candidates(ROOT, json.loads(raw), revision, args.week, args.page, args.output)
    print(json.dumps({'status': packet['status'], 'pages': len(packet['pages']), 'output': str(args.output)}))


if __name__ == '__main__':
    main()
