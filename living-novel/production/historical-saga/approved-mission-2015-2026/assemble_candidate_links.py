"""Join actual draft scene anchors to audited events; never accept literary coverage."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'SCHEMIN_26_PROJECT_MISSION.md').exists())


def build():
    events = {}
    for ledger in sorted((HERE / 'evidence').glob('*_FIXTURE_COVERAGE.json')):
        data = json.loads(ledger.read_text())
        for event in data.get('events', []):
            events[event['event_id']] = dict(event, source_path=event.get('source_path', data.get('source_path')))
    links = {}
    for register in sorted((HERE / 'manuscript').glob('*/SCENE_REGISTER.json')):
        data = json.loads(register.read_text())
        for scene in data['scenes']:
            path = ROOT / scene['manuscript_path']
            content = path.read_text()
            heading = scene['heading']
            if not heading.startswith('## '):
                heading = '## ' + heading
            if content.splitlines().count(heading) != 1:
                raise ValueError(f'Anchor missing or ambiguous: {path}: {heading}')
            for event_id in scene['source_event_ids']:
                if event_id not in events:
                    raise ValueError(f'Unresolved event: {event_id}')
                links.setdefault(event_id, []).append({
                    'scene_id': scene['scene_id'],
                    'manuscript_path': scene['manuscript_path'],
                    'heading': heading,
                    'line': content.splitlines().index(heading) + 1,
                    'manuscript_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                    'pov_character_id': scene['pov_character_id'],
                    'story_time_cutoff': scene['story_time_cutoff'],
                    'register_path': str(register.relative_to(ROOT)),
                    'coverage_status': 'DRAFT_CONTEXT_OR_AFTERMATH_LINK_NOT_ACCEPTED_COVERAGE',
                })
    result = {
        'status': 'PROPOSED_NONCANON_LINKS_ONLY',
        'scope': 'Actual new scene-to-source links; distinct linked events do not equal accepted or fully dramatized contests.',
        'baseline_passage_audit': 'evidence/CURRENT_SEASON_PASSAGE_AUDIT.json',
        'distinct_linked_event_count': len(links),
        'distinct_scene_count': len({scene['scene_id'] for rows in links.values() for scene in rows}),
        'scene_link_count': sum(len(v) for v in links.values()),
        'accepted_event_count_claimed': None,
        'events': [{'event_id': key, 'source_path': events[key]['source_path'], 'candidate_scenes': links[key]} for key in sorted(links)],
    }
    (HERE / 'CANDIDATE_EVENT_LINKS.json').write_text(json.dumps(result, indent=2) + '\n')
    seasons = []
    for year in range(2015, 2027):
        ledger = json.loads((HERE / 'evidence' / f'{year}_FIXTURE_COVERAGE.json').read_text())
        year_events = {key: rows for key, rows in links.items() if events[key]['season'] == year}
        seasons.append({
            'season': year,
            'observed_contest_denominator': ledger['observed_paired_contests'],
            'denominator_scope': ledger['denominator_scope'],
            'new_candidate_event_links': len(year_events),
            'new_candidate_scene_ids': sorted({row['scene_id'] for rows in year_events.values() for row in rows}),
            'complete_season_claim': False,
            'accepted_coverage_count_claimed': None,
            'remaining_work': 'Resolve event-specific historical identity authority and period staging; recover/revise existing prose and produce all missing season movements and contest consequences.' if year < 2026 else 'Complete remaining verified W1-W6 causal coverage and legacy POV repairs; no W7 results or season ending licensed.',
            'binding_matrix': 'evidence/HISTORICAL_BINDING_MATRIX_2015_2025.json' if year < 2026 else None,
        })
    (HERE / 'ALL_SEASON_PROGRESS.json').write_text(json.dumps({
        'status': 'PARTIAL_PRODUCTION_NOT_ACCEPTANCE',
        'rule': 'New candidate links do not erase existing prose or establish full literary coverage. See inventories, passage audits and independent reviews.',
        'seasons': seasons,
    }, indent=2) + '\n')
    print(f'Linked {len(links)} events to {result["distinct_scene_count"]} distinct scenes ({result["scene_link_count"]} references); no literary acceptance asserted.')


if __name__ == '__main__':
    build()
