"""Focused synthetic CLI checks; no provider data or production writes."""
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_playoff_context_readiness import fixture, PAGE


CLI = Path(__file__).resolve().parents[1]/'playoff_context_preflight.py'


class AnalyticsPreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.packet, self.previs, self.requests = fixture()
        self.packet['evaluation_mode'] = 'CURRENT_CAPTURE'
        self.set_source_time(datetime.now(timezone.utc)-timedelta(seconds=30))
        self.packet_path = self.root/'packet.json'
        self.previs_path = self.root/'previs.json'
        self.render_inputs = self.root/'render-inputs'
        self.write_inputs()

    def set_source_time(self, value):
        timestamp = value.isoformat()
        self.packet['source_as_of'] = timestamp
        self.previs['sports_snapshot_utc'] = timestamp
        self.previs['sports_source']['source_as_of'] = timestamp

    def write_inputs(self):
        self.packet_path.write_text(json.dumps(self.packet))
        self.previs_path.write_text(json.dumps(self.previs))
        for page_id, request in self.requests.items():
            path = self.render_inputs/page_id/'request.json'
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(request))

    def run_cli(self, *extra):
        return subprocess.run([sys.executable, str(CLI), '--packet', str(self.packet_path),
            '--previs', str(self.previs_path), '--render-inputs', str(self.render_inputs), *extra],
            capture_output=True, text=True, timeout=10)

    def snapshot(self):
        return {str(path.relative_to(self.root)): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in self.root.rglob('*') if path.is_file()}

    def test_fresh_actual_consumption_passes_without_mutating_inputs_or_granting_authority(self):
        before = self.snapshot()
        earliest = datetime.now(timezone.utc)
        run = self.run_cli()
        self.assertEqual(run.returncode, 0, run.stderr)
        result = json.loads(run.stdout)
        self.assertEqual(result['status'], 'PASS')
        self.assertEqual(result['scope'], 'ADDITIONAL_ANALYTICS_CONSUMPTION_ONLY')
        self.assertEqual(result['native_memo_production'], 'NOT_EVALUATED_OR_OVERRIDDEN')
        self.assertFalse(result['publication_authorized'])
        self.assertFalse(result['artwork_reviewed'])
        self.assertGreaterEqual(datetime.fromisoformat(result['checked_at']), earliest)
        self.assertEqual(before, self.snapshot())

    def test_hold_uses_actual_inputs_instead_of_cached_pass_metadata(self):
        self.packet['production_readiness'] = {'status': 'SOURCE_AND_RENDER_INPUTS_VERIFIED',
                                              'consumption_witnessed': True}
        self.previs['final_fact_lock'] = False
        self.write_inputs()
        before = self.snapshot()
        run = self.run_cli(); result = json.loads(run.stdout)
        self.assertEqual(run.returncode, 1)
        self.assertEqual(result['status'], 'HOLD')
        self.assertIn('PREVIS_NOT_FACT_LOCKED', result['issue_codes'])
        self.assertEqual(before, self.snapshot())

    def test_stale_source_cannot_reuse_previous_freshness_check(self):
        self.set_source_time(datetime.now(timezone.utc)-timedelta(days=3))
        self.packet['production_readiness'] = {'status': 'PASS', 'checked_at': datetime.now(timezone.utc).isoformat()}
        self.write_inputs()
        run = self.run_cli()
        self.assertEqual(run.returncode, 1)
        self.assertIn('STALE_OR_FUTURE_ANALYTICS_SOURCE', json.loads(run.stdout)['issue_codes'])

    def test_missing_input_and_empty_render_directory_fail_closed(self):
        self.packet_path.unlink()
        run = self.run_cli()
        self.assertEqual(run.returncode, 2)
        self.assertEqual(json.loads(run.stderr)['status'], 'INVALID_INPUT')
        self.write_inputs()
        (self.render_inputs/PAGE/'request.json').unlink()
        run = self.run_cli()
        self.assertEqual(run.returncode, 2)
        self.assertIn('no per-page request.json', json.loads(run.stderr)['error'])

    def test_malformed_json_or_shape_fails_closed(self):
        for bad in ('{not json', '[]', '{"bad": NaN}'):
            with self.subTest(input=bad):
                self.packet_path.write_text(bad)
                run = self.run_cli()
                self.assertEqual(run.returncode, 2)
                self.assertEqual(json.loads(run.stderr)['status'], 'INVALID_INPUT')

    def test_render_request_identity_must_match_its_directory(self):
        self.requests[PAGE]['page_id'] = 'W04-P27'
        self.write_inputs()
        run = self.run_cli()
        self.assertEqual(run.returncode, 2)
        self.assertIn('identity', json.loads(run.stderr)['error'])

    def test_historical_packet_cannot_clear_current_intake(self):
        self.packet['evaluation_mode'] = 'HISTORICAL_REPLAY'
        self.write_inputs()
        run = self.run_cli()
        self.assertEqual(run.returncode, 1)
        self.assertIn('NONCURRENT_ANALYTICS_PACKET', json.loads(run.stdout)['issue_codes'])

    def test_no_historical_clock_override_is_exposed(self):
        run = self.run_cli('--as-of', '2030-10-20T12:30:00Z')
        self.assertEqual(run.returncode, 2)
        self.assertIn('unrecognized arguments', run.stderr)


if __name__ == '__main__':
    unittest.main()
