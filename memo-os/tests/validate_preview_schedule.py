"""Fail-closed fixture reconciliation for released Memo previews.

A manifest row is an editorial assertion, not proof that raster text is correct.
The independent final-page reviewer must still compare the actual preview image.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def check(manifest):
    week = manifest.get('week')
    if manifest.get('publication_state') not in ('RELEASED', 'PUBLISHED') or type(week) is not int or week < 8:
        return []
    errors = []
    source = manifest.get('preview_schedule_source')
    expected_hash = manifest.get('preview_schedule_source_sha256')
    rows = manifest.get('preview_fixture_rows')
    preview_week = manifest.get('preview_week')
    if type(preview_week) is not int or preview_week != week + 1:
        errors.append('preview: next-week identifier required')
    if not isinstance(rows, list) or len(rows) != 6:
        errors.append('preview: exactly six published fixture rows required')
    if not isinstance(source, str) or not source.startswith('memo-os/') or '..' in Path(source).parts:
        return errors + ['preview: repository source path required']
    path = (ROOT / source).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        return errors + ['preview: source file unavailable']
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected_hash:
        return errors + ['preview: source SHA256 mismatch']
    try:
        data = json.loads(raw)
        if str(data['league_id']) != '1417621' or data['season'] != manifest.get('season', 2026):
            raise ValueError('league or season mismatch')
        block = data[f'week{preview_week}_matchups']
        if block.get('matchupPeriod') != preview_week:
            raise ValueError('source week mismatch')
        games = block['matchups']
        actual = [(str(g['home']['teamName']).strip(), str(g['away']['teamName']).strip()) for g in games]
        printed = [(str(g['home']).strip(), str(g['away']).strip()) for g in rows]
    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        return errors + [f'preview: malformed source or rows: {exc}']
    if len(actual) != 6 or len(set(actual)) != 6 or len(set(printed)) != 6 or set(printed) != set(actual):
        errors.append('preview: published fixture rows do not match authenticated provider schedule')
    # An unbound PASS string is insufficient: tie the independent visual review
    # to the exact final PDF and the exact schedule row set. Image-only PDFs
    # cannot be checked for rendered text by this validator.
    review = manifest.get('preview_final_raster_review')
    pdf_hash = manifest.get('published_artifact_sha256')
    if not isinstance(review, dict) or review.get('decision') != 'PASS' or not review.get('reviewer_id') or not review.get('reviewed_at'):
        errors.append('preview: independent final raster review missing')
    else:
        if review.get('pdf_sha256') != pdf_hash or not isinstance(pdf_hash, str) or len(pdf_hash) != 64:
            errors.append('preview: visual review not bound to final PDF')
        rows_hash = hashlib.sha256(json.dumps(rows, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
        if review.get('fixture_rows_sha256') != rows_hash:
            errors.append('preview: visual review not bound to fixture rows')
        if review.get('reviewer_id') == manifest.get('generation_operator_id'):
            errors.append('preview: visual reviewer not independent of generator')
    return errors
