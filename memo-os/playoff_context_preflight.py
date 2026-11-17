"""Read-only preflight for opt-in additional analytics consumption.

A HOLD applies to use of the supplied analytics packet. This command does not
supersede the native Memo source/proof pipeline, authorize art or publication,
refresh a source, or change any input. Current time is always used.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import sys


def _invalid_constant(value):
    raise ValueError('non-finite JSON number: '+value)


def _read_object(path):
    raw = path.read_bytes()
    value = json.loads(raw, parse_constant=_invalid_constant)
    if not isinstance(value, dict):
        raise ValueError(f'{path.name} must contain a JSON object')
    return value, hashlib.sha256(raw).hexdigest()


def _read_render_requests(directory):
    if not directory.is_dir():
        raise ValueError('render-inputs must be an existing directory')
    requests, hashes = {}, {}
    for path in sorted(directory.glob('*/request.json')):
        request, file_hash = _read_object(path)
        page_id = request.get('page_id')
        if not isinstance(page_id, str) or page_id != path.parent.name or page_id in requests:
            raise ValueError('render request page identity is missing, duplicated or mismatched')
        requests[page_id] = request
        hashes[page_id] = file_hash
    if not requests:
        raise ValueError('render-inputs contains no per-page request.json files')
    return requests, hashes


def check_inputs(packet_path, previs_path, render_inputs_path):
    """Read actual inputs and return a compact, dated result without writes."""
    packet, packet_hash = _read_object(Path(packet_path))
    previs, previs_hash = _read_object(Path(previs_path))
    requests, request_hashes = _read_render_requests(Path(render_inputs_path))
    spec = importlib.util.spec_from_file_location(
        'memo_analytics_readiness', Path(__file__).with_name('playoff_context_readiness.py'))
    readiness = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(readiness)
    result = readiness.audit_memo_readiness(
        packet, previs=previs, render_requests=requests, now=datetime.now(timezone.utc))
    if packet.get('evaluation_mode') != 'CURRENT_CAPTURE':
        result['issues'].append({'code': 'NONCURRENT_ANALYTICS_PACKET',
            'detail': 'Historical replay or unspecified packet mode cannot clear current additional-analytics intake.'})
        result['status'] = 'HOLD'
        result['consumption_witnessed'] = False
        result['copy_change_required'] = True
    passed = result['status'] == 'SOURCE_AND_RENDER_INPUTS_VERIFIED' and result['consumption_witnessed'] is True
    return {
        'scope': 'ADDITIONAL_ANALYTICS_CONSUMPTION_ONLY',
        'status': 'PASS' if passed else 'HOLD',
        'native_memo_production': 'NOT_EVALUATED_OR_OVERRIDDEN',
        'checked_at': result['checked_at'],
        'source_as_of': packet.get('source_as_of'),
        'packet_sha256': packet_hash, 'previs_sha256': previs_hash,
        'render_inputs_sha256': readiness.digest(request_hashes),
        'report_sha256': packet.get('report_sha256'),
        'render_request_count': len(requests),
        'analytics_copy_reconciliation_required': result['copy_change_required'],
        'analytics_consumption_witnessed': result['consumption_witnessed'],
        'issue_count': len(result['issues']),
        'issue_codes': sorted({issue['code'] for issue in result['issues']}),
        'affected_page_ids': sorted({issue['page_id'] for issue in result['issues']
                                     if isinstance(issue.get('page_id'), str)}),
        'advisory_note_count': len(result.get('review_notes', [])),
        'publication_authorized': False, 'artwork_reviewed': False,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', type=Path, required=True,
                        help='Explicit local analytics packet to consider consuming')
    parser.add_argument('--previs', type=Path, required=True,
                        help='Actual current Memo issue previs')
    parser.add_argument('--render-inputs', type=Path, required=True,
                        help='Actual per-page render-inputs directory')
    args = parser.parse_args(argv)
    try:
        result = check_inputs(args.packet, args.previs, args.render_inputs)
    except (OSError, UnicodeError, ValueError, TypeError, KeyError, AttributeError) as exc:
        print(json.dumps({'scope': 'ADDITIONAL_ANALYTICS_CONSUMPTION_ONLY',
                          'status': 'INVALID_INPUT', 'error': str(exc),
                          'native_memo_production': 'NOT_EVALUATED_OR_OVERRIDDEN',
                          'publication_authorized': False}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
