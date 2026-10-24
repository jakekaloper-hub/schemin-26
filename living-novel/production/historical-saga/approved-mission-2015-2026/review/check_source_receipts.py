"""Independent read-only verification of the mission's historical receipts.

Checks source bytes/pointers, observation accounting and reported winner/score
exceptions. It does not manufacture bracket completeness or owner identity.
"""
import hashlib
import json
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'SCHEMIN_26_PROJECT_MISSION.md').is_file())
EVIDENCE = Path(__file__).resolve().parent.parent / 'evidence'


def check():
    errors, qualifications = [], []
    observation_count = paired = unpaired = duplicates = 0
    ledger_hashes = {}
    for year in range(2015, 2026):
        path = EVIDENCE / f'{year}_FIXTURE_COVERAGE.json'
        ledger_hashes[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
        ledger = json.loads(path.read_text())
        seen_observations = set()
        for event in ledger['events']:
            source_path = ROOT / event['source_path']
            if hashlib.sha256(source_path.read_bytes()).hexdigest() != event['source_sha256']:
                errors.append([event['event_id'], 'SOURCE_HASH_MISMATCH'])
            source = json.loads(source_path.read_text())
            for observation in event['observations']:
                pointer = observation['source_pointer']
                key = (event['source_path'], pointer)
                if key in seen_observations:
                    errors.append([event['event_id'], 'SOURCE_ROW_COUNTED_TWICE'])
                seen_observations.add(key)
                cursor = source
                try:
                    for component in pointer.strip('/').split('/'):
                        cursor = cursor[int(component)] if isinstance(cursor, list) else cursor[component]
                except (KeyError, IndexError, ValueError, TypeError):
                    errors.append([event['event_id'], 'UNRESOLVED_SOURCE_POINTER', pointer])
                    cursor = None
                if isinstance(cursor, dict):
                    aliases = {'period': ('period', 'matchupPeriodId'), 'home_id': ('home_id', 'home_team_id'), 'home': ('home', 'home_name'), 'home_score': ('hp', 'home_points'), 'away_id': ('away_id', 'away_team_id'), 'away': ('away', 'away_name'), 'away_score': ('ap', 'away_points'), 'winner': ('winner',), 'tier': ('tier',)}
                    for field, keys in aliases.items():
                        original = next((cursor[k] for k in keys if k in cursor), None)
                        if event[field] != original:
                            errors.append([event['event_id'], 'FIELD_DIFFERS_FROM_SOURCE', pointer, field])
                observation_count += 1
            if event['kind'] != 'PAIRED_CONTEST':
                unpaired += 1
                continue
            paired += 1
            home, away = event['home_score'], event['away_score']
            if home == away and event['winner'] in ('HOME', 'AWAY'):
                qualifications.append({'event_id': event['event_id'], 'reason': 'EQUAL_DISPLAY_SCORES_WITH_DECLARED_WINNER', 'source_winner': event['winner'], 'rule': 'Preserve provider declaration; tiebreak or precision cause remains unknown.'})
            elif home > away and event['winner'] != 'HOME' or away > home and event['winner'] != 'AWAY':
                errors.append([event['event_id'], 'NON_TIED_SCORE_WINNER_CONFLICT'])
        duplicates += ledger['duplicate_display_rows']
        if len(seen_observations) != ledger['returned_rows']:
            errors.append([year, 'OBSERVATION_ACCOUNTING_MISMATCH'])
    return {'scope': 'HISTORICAL_RECEIPT_INTEGRITY_ONLY', 'resolved_source_observations': observation_count, 'paired_contests': paired, 'unpaired_rows': unpaired, 'duplicate_display_rows': duplicates, 'errors': errors, 'result_qualifications': qualifications, 'reviewed_ledger_sha256': ledger_hashes, 'not_proven': ['historical owner identity', 'complete schedule beyond observed extracts', 'literary acceptance', 'raw provider byte authenticity']}


if __name__ == '__main__':
    report = check()
    print(json.dumps(report, indent=2))
    raise SystemExit(bool(report['errors']))
