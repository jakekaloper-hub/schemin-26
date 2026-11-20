#!/usr/bin/env python3
"""Build a read-only, provenance-bound website projection. Never promotes canon."""
import argparse
import hashlib
import json
import pathlib
import shutil
import subprocess
import urllib.parse
import importlib.util
import re
from concurrent.futures import ThreadPoolExecutor

BASE = pathlib.Path(__file__).resolve().parent
ROOT = BASE.parents[1]
REVISION = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout.strip()
REPO = f'https://github.com/jakekaloper-hub/schemin-26/blob/{REVISION}/'
MEDIA = f'https://media.githubusercontent.com/media/jakekaloper-hub/schemin-26/{REVISION}/'
# Fresh source-byte ingestion receipts from canonical Library materialization.
# Hashes were first measured in this ingestion, not asserted by the old repo receipts.
RECOVERED_RELEASES = {
    2: {'filename': 'Week 2 memo.pdf', 'size': 68380271, 'pages': 14,
        'sha256': 'b03f9090a1d203789ab49e7fb8046ad6e721eec3a2adade66331796df30fb6c4',
        'libraryFileId': 'libfile_5adf869426408191af3fee17cb6b3088',
        'authority': 'docs/publications/WEEK_2_OFFICIAL_PUBLICATION_RECOVERY_RECEIPT_V1.md'},
    3: {'filename': 'Pro_Schemin_Week_3_Memo_Final.pdf', 'size': 103917769, 'pages': 21,
        'sha256': '9f3978dcb5e8c11b658a8d5a29e011b614d4170e57cd14461f440ac360700fcb',
        'libraryFileId': 'libfile_a674d1dc77508191acf66303f6369b0e',
        'authority': 'world/qa/WEEK3_RELEASE_ARTIFACT_RECONCILIATION.md'},
}


def sha256(path):
    digest = hashlib.sha256()
    with pathlib.Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def verify_file(path, expected):
    actual = sha256(path)
    if actual != expected:
        raise ValueError(f'Source hash mismatch: {path}')
    return actual


def build_catalog(output=None, render=True, released_source_dir=None):
    output = pathlib.Path(output or BASE / 'dist')
    output.mkdir(parents=True, exist_ok=True)
    (output / 'assets').mkdir(exist_ok=True)
    sources = []

    def read(path):
        local = ROOT / path
        sources.append({'path': path, 'sha256': sha256(local), 'url': REPO + urllib.parse.quote(path)})
        return json.loads(local.read_text())

    def copy(source, name, expected=None):
        source = pathlib.Path(source)
        if expected:
            verify_file(source, expected)
        destination = output / 'assets' / name
        shutil.copyfile(source, destination)
        return 'assets/' + name

    def page(pdf, number, name, scale=1600, quality=86):
        destination = output / 'assets' / name
        if render:
            subprocess.run(['pdftoppm', '-f', str(number), '-l', str(number), '-scale-to', str(scale),
                            '-jpeg', '-jpegopt', f'quality={quality}', '-singlefile', str(pdf),
                            str(destination.with_suffix(''))], check=True, capture_output=True)
        return 'assets/' + name if render else None

    lineup_path = 'canon/characters/APPROVED_LINEUP_2026_10_18.json'
    lineup = read(lineup_path)
    characters = []
    for person in lineup['individuals']:
        appearance = read(person['appearance_delta'])
        assertions = appearance['approved_visual_assertions']
        characters.append({
            'id': person['character_id'], 'owner': person['owner'], 'name': person['display_title'],
            'team': person['team'], 'locationId': person['home_location_id'],
            'description': assertions['subject_morphology'],
            'details': assertions.get('recognizable_props', []),
            'image': copy(ROOT / person['crop'], person['character_id'] + '.png', person['crop_sha256']),
            'sha256': person['crop_sha256'], 'source': person['appearance_delta'],
            'sourceUrl': REPO + person['appearance_delta'],
        })
    locations = read('world/data/locations.json')['locations']
    for location in locations:
        location['x'], location['y'] = location['abstract_position']
        location['zone'] = location['physical_zone_id']
        location['description'] = ', '.join(location.get('persistent_landmarks', []))
        location['source'] = 'world/data/locations.json'
        location['sourceUrl'] = REPO + 'world/data/locations.json'
    routes = read('world/data/routes.json')['routes']
    zones = read('world/data/physical_zones.json')['regions']
    intake_path = 'governance/publication-manifest/WEEKS_04_06_COMMISSIONER_SOURCE_INTAKE_2026_10_22.json'
    intake = read(intake_path)
    memos = []
    for item in intake['files']:
        pdf = ROOT / item['archive_path']
        verify_file(pdf, item['sha256'])
        week = item['week']
        status = 'Artwork review edition' if week == 5 else 'Commissioner source edition'
        def render_memo_page(number):
            return page(pdf, number, f'week-{week}-page-{number:02d}.jpg', scale=1200, quality=75)
        # Each task writes a distinct page; no shared source or output mutations.
        with ThreadPoolExecutor(max_workers=3) as executor:
            memo_pages = list(executor.map(render_memo_page, range(1, item['pages'] + 1)))
        # Large originals remain available from their authoritative LFS download URL.
        # This keeps the static site small and avoids altering source PDF bytes.
        memos.append({
            'id': f'week-{week}', 'week': week, 'title': item['title'], 'pages': item['pages'],
            'status': status, 'releaseState': 'SOURCE_VERIFIED_NOT_RELEASE_PROMOTED',
            'currentBenchmark': False, 'pdf': MEDIA + urllib.parse.quote(item['archive_path']),
            'cover': memo_pages[0], 'pageImages': memo_pages, 'pageCount': item['pages'],
            'source': item['archive_path'],
            'sourceUrl': REPO + item['archive_path'], 'sha256': item['sha256'],
            'note': 'Original supplied edition. Source verification does not establish publication release acceptance.',
        })
        sources.append({'path': item['archive_path'], 'sha256': item['sha256'],
                        'authority': intake_path, 'url': REPO + item['archive_path']})
    chapter_sources = [
        ('prologue', 'Prologue', 'living-novel/manuscript/PROLOGUE_DRAFT_V1.md'),
        ('chapter-1', 'The First Answer', 'living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md'),
        ('chapter-2', 'What Comes Back', 'living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md'),
        ('chapter-3', 'The Hill Is Not the Kingdom', 'living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md'),
    ]
    manifest = read('governance/publication-manifest/PUBLICATION_MANIFEST_V1.json')
    current_released_memo_id = None
    if released_source_dir is not None:
        resolver_path = ROOT / 'governance/publication-manifest/memo_reference_resolver.py'
        resolver_spec = importlib.util.spec_from_file_location('memo_reference_resolver', resolver_path)
        resolver = importlib.util.module_from_spec(resolver_spec)
        resolver_spec.loader.exec_module(resolver)
        current = resolver.resolve_memo_reference('latest', manifest)
        for week, recovered in RECOVERED_RELEASES.items():
            publication = resolver.resolve_memo_reference(f'week {week}', manifest)
            if publication['canonical_artifact'] != recovered['filename']:
                raise ValueError(f'Recovered release identity conflict: week {week}')
            pdf = pathlib.Path(released_source_dir) / recovered['filename']
            if pdf.stat().st_size != recovered['size']:
                raise ValueError(f'Recovered release byte-size mismatch: week {week}')
            verify_file(pdf, recovered['sha256'])
            pdf_info = subprocess.run(['pdfinfo', str(pdf)], check=True, capture_output=True, text=True).stdout
            page_match = re.search(r'^Pages:\s+(\d+)$', pdf_info, flags=re.MULTILINE)
            if not page_match or int(page_match.group(1)) != recovered['pages']:
                raise ValueError(f'Recovered release page-count mismatch: week {week}')
            def render_released_page(number):
                return page(pdf, number, f'week-{week}-page-{number:02d}.jpg', scale=1200, quality=75)
            with ThreadPoolExecutor(max_workers=3) as executor:
                images = list(executor.map(render_released_page, range(1, recovered['pages'] + 1)))
            is_current = publication['publication_id'] == current['publication_id']
            if is_current:
                current_released_memo_id = f'week-{week}'
            memos.append({'id': f'week-{week}', 'week': week, 'title': publication['title'],
                          'pages': recovered['pages'], 'pageCount': recovered['pages'],
                          'cover': images[0], 'pageImages': images, 'status': 'Released edition',
                          'releaseState': publication['release_state'], 'currentBenchmark': is_current,
                          'source': recovered['filename'], 'sourceUrl': REPO + recovered['authority'],
                          'sha256': recovered['sha256'], 'libraryFileId': recovered['libraryFileId'],
                          'note': 'Exact historical released edition. Original source preserved; pages rendered for web reading.'})
            sources.append({'path': recovered['filename'], 'sha256': recovered['sha256'],
                            'sizeBytes': recovered['size'], 'pages': recovered['pages'],
                            'libraryFileId': recovered['libraryFileId'], 'authority': recovered['authority'],
                            'url': REPO + recovered['authority'],
                            'hashReceiptKind': 'FRESH_SOURCE_BYTE_INGESTION'})
    approved = {p['canonical_artifact'] for p in manifest['publications']
                if p['family'] == 'living_novel' and p['release_state'] == 'CANON_CLOSED'}
    rewrite_path = 'living-novel/production/full-rewrite-2026/REWRITE_CONTROL_AND_MANUSCRIPT_BRIEF.md'
    sources.append({'path': rewrite_path, 'sha256': sha256(ROOT / rewrite_path), 'url': REPO + rewrite_path})
    chapters = []
    for chapter_id, title, path in chapter_sources:
        if path not in approved:
            raise ValueError(f'No historical manuscript acceptance: {path}')
        text = (ROOT / path).read_text()
        chapters.append({'id': chapter_id, 'title': title, 'text': text, 'source': path,
                         'sourceUrl': REPO + path, 'sha256': sha256(ROOT / path),
                         'status': 'Archive edition · rewrite commissioned',
                         'note': 'Historical accepted text preserved verbatim. A twelve-owner rewrite is commissioned; candidates are not published here.'})
        sources.append({'path': path, 'sha256': sha256(ROOT / path), 'url': REPO + path})
    week6 = ROOT / intake['files'][2]['archive_path']
    hero = page(week6, 5, 'commonwealth-atlas.jpg')
    art = [
        {'image': page(week6, number, f'week-6-scene-{number}.jpg'), 'page': number,
         'source': intake['files'][2]['archive_path'], 'label': label}
        for number, label in [(6, 'Red Ruins'), (9, 'Jackson Invitational'), (13, 'Chili Stable'), (17, 'Waterfall Temple')]
    ]
    data = {'characters': characters, 'locations': locations, 'routes': routes, 'zones': zones,
            'memos': sorted(memos, key=lambda x: x['week'], reverse=True), 'chapters': chapters,
            'meta': {'title': 'Schemin · The Commonwealth', 'schemaVersion': 1, 'sourceRevision': REVISION,
                     'currentReleasedMemoId': current_released_memo_id,
                     'coordinateSpace': 'Abstract, non-metric canonical topology; not a geographic survey.',
                     'hero': hero, 'heroSource': 'Week 6 supplied memo, page 5', 'art': art,
                     'sources': sources,
                     'warnings': [
                         'Source editions are not promoted release or benchmark claims.',
                         'Novel archive editions are historical text; the twelve-owner rewrite remains separate and unpromoted.',
                         'Existing approved character crops are reused without generating or redesigning characters.',
                         'Original PDFs open from their public GitHub LFS source; availability depends on that host.',
                     ]}}
    (output / 'data.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    source_dir = BASE / 'src'
    if source_dir.exists():
        shutil.copytree(source_dir, output, dirs_exist_ok=True)
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=pathlib.Path, default=BASE / 'dist')
    parser.add_argument('--no-render', action='store_true', help='Skip PDF rasterization for data tests only')
    parser.add_argument('--released-source-dir', type=pathlib.Path,
                        help='Directory containing the exact recovered Week 2 and Week 3 released PDFs')
    args = parser.parse_args()
    data = build_catalog(args.output, render=not args.no_render, released_source_dir=args.released_source_dir)
    print(json.dumps({'output': str(args.output), 'characters': len(data['characters']),
                      'locations': len(data['locations']), 'memos': len(data['memos']),
                      'chapters': len(data['chapters'])}))
