"""Read actual manuscript sections and apply existing POV gate plus source joins.

This checks concrete artifact contracts, not literary quality or canon release.
"""
import hashlib
import importlib.util
import json
import re
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'SCHEMIN_26_PROJECT_MISSION.md').is_file())
MISSION = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('existing_gate', ROOT / 'living-novel/os/qa/twelve_owner_rewrite_gate.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def check():
    evidence = json.loads((MISSION / 'evidence/2026_FIXTURE_COVERAGE.json').read_text())
    events = {e['event_id']: e for e in evidence['events']}
    locations = {l['id'] for l in json.loads((ROOT / 'world/data/locations.json').read_text())['locations']}
    routes = {r['id'] for r in json.loads((ROOT / 'world/data/routes.json').read_text())['routes']}
    results, hashes, missing = [], {}, []
    seen_scene_ids = set()
    for directory in sorted(p for p in (MISSION / 'manuscript').iterdir() if p.is_dir() and p.name.startswith('2026')):
        register_path = directory / 'SCENE_REGISTER.json'
        if not register_path.is_file():
            missing.append(str(register_path.relative_to(ROOT)))
            continue
        hashes[str(register_path.relative_to(ROOT))] = hashlib.sha256(register_path.read_bytes()).hexdigest()
        register = json.loads(register_path.read_text())
        for scene in register['scenes']:
            path = ROOT / scene['manuscript_path']
            text = path.read_text()
            hashes[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
            marker = '## ' + scene['heading'].removeprefix('## ')
            parts = text.split(marker + '\n')
            errors = []
            if scene['scene_id'] in seen_scene_ids:
                errors.append('DUPLICATE_SCENE_ID')
            seen_scene_ids.add(scene['scene_id'])
            registered_headings = {'## ' + s['heading'].removeprefix('## ') for s in register['scenes'] if s['manuscript_path'] == scene['manuscript_path']}
            actual_headings = set(re.findall(r'^## .+$', text, flags=re.M))
            if registered_headings != actual_headings:
                errors.append('REGISTER_DOES_NOT_COVER_EXACT_MANUSCRIPT_SCENES')
            if len(parts) != 2:
                errors.append('SCENE_HEADING_NOT_UNIQUE')
                prose = ''
            else:
                prose = parts[1].split('\n## ', 1)[0].strip()
            if scene.get('body_sha256') and hashlib.sha256(prose.encode()).hexdigest() != scene['body_sha256']:
                errors.append('REGISTER_BODY_HASH_MISMATCH')
            hydrated = dict(scene, manuscript_text=prose)
            errors.extend(gate.validate_rewrite_scene(hydrated))
            if scene['pov_character_id'] == 'CHAR-MANNING-WELTY':
                errors.append('EL_NINO_INTERIOR_POV_FORBIDDEN_BY_CURRENT_HYDRATION')
            for location in scene.get('location_ids', []):
                if location not in locations:
                    errors.append('UNKNOWN_SCENE_LOCATION:' + location)
            for route in scene.get('route_ids', []):
                if route not in routes:
                    errors.append('UNKNOWN_SCENE_ROUTE:' + route)
            if scene['world_context_id'] not in locations:
                errors.append('UNKNOWN_WORLD_LOCATION')
            for event_id in scene['source_event_ids']:
                if event_id not in events:
                    errors.append('EVENT_ID_NOT_JOINED:' + event_id)
                elif events[event_id]['finality'] != 'REPOSITORY_DECIDED_RECEIPT':
                    errors.append('SOURCE_EVENT_NOT_FINAL:' + event_id)
            if re.search(r'\b(?:Edrin|Edin|Master Oren)\b', prose, flags=re.I):
                errors.append('RETIRED_CHARACTER_IN_PROSE')
            results.append({'scene_id': scene['scene_id'], 'manuscript_path': str(path.relative_to(ROOT)), 'actual_prose_sha256': hashlib.sha256(prose.encode()).hexdigest(), 'diagnostic_word_count': len(prose.split()), 'errors': errors})
    controls = ['living-novel/world/AUTHOR_ROOM_UNIVERSE_HYDRATION_STANDARD_V1.md', 'living-novel/whole-book/WHOLE_BOOK_SOURCE_AUTHORITY_MATRIX_V1.md', 'living-novel/os/qa/twelve_owner_rewrite_gate.py', 'canon/characters/CHARACTER_REGISTRY.yaml', 'world/data/locations.json', 'world/data/routes.json', 'living-novel/production/historical-saga/approved-mission-2015-2026/evidence/2026_FIXTURE_COVERAGE.json']
    control_hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in controls}
    return {'reviewed_control_sha256': control_hashes, 'scope': 'ACTUAL_SCENE_TEXT_CONTRACT_AND_SOURCE_JOINS_ONLY', 'missing_registers': missing, 'scenes': results, 'reviewed_artifact_sha256': hashes, 'not_proven': ['semantic literary quality', 'historical owner binding', 'canon approval', 'full season coverage', 'human or authenticated Director acceptance']}


if __name__ == '__main__':
    result = check()
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(result['missing_registers'] or not result['scenes'] or any(r['errors'] for r in result['scenes'])))
