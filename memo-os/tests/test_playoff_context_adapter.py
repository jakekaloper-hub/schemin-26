import importlib.util
from pathlib import Path
import sys
import unittest
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'data-gateway'/'playoff-context'/'src'))
sys.path.insert(0, str(ROOT/'data-gateway'/'playoff-context'/'tests'))
from test_pipeline import fixture, NOW


class MemoAdapterTests(unittest.TestCase):
    def adapter(self):
        path = ROOT/'memo-os'/'playoff_context_adapter.py'
        self.assertTrue(path.exists(), 'Memo OS has no analytics consumer')
        spec = importlib.util.spec_from_file_location('tested_memo_adapter', path)
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        return module

    def test_no_false_exactness_or_publication_authority(self):
        module = self.adapter()
        from playoff_context.pipeline import build_report
        capture, config = fixture()
        report = build_report(capture, config, now=NOW, simulations=10)
        packet = module.build_memo_packet(report, now=NOW)
        self.assertFalse(packet['publication_authorized'])
        self.assertEqual(packet['forecast']['status'], 'HOLD')
        self.assertTrue(all('playoff_probability' not in t for t in packet['teams'].values()))
        self.assertIn('No simulated 0%/100% clinch or elimination claim.', packet['prohibited_inferences'])

    def test_hydration_preserves_copy_and_final_fact_lock(self):
        module = self.adapter()
        from playoff_context.pipeline import build_report
        capture, config = fixture()
        report = build_report(capture, config, now=NOW, simulations=10)
        previs = {'final_fact_lock': False, 'pages': [{'page_id': 'W02-P30', 'title': 'Keep this title', 'body': 'Keep approved copy.'}]}
        packet = module.build_memo_packet(report, previs=previs, now=NOW,
            bindings={'W02-P30': 'playoff_picture'})
        hydrated = packet['hydrated_previs']
        self.assertFalse(hydrated['final_fact_lock'])
        self.assertEqual(hydrated['pages'][0]['body'], 'Keep approved copy.')
        self.assertIn('analytics_context', hydrated['pages'][0])
        self.assertNotIn('analytics_context', previs['pages'][0])
        self.assertTrue(packet['copy_change_required'])
        self.assertEqual(packet['production_readiness']['status'], 'HOLD')
        self.assertFalse(packet['production_readiness']['consumption_witnessed'])
        self.assertEqual(hydrated['derived_analytics']['production_readiness'], 'HOLD')

    def test_stale_or_wrong_week_attachment_is_rejected(self):
        module = self.adapter()
        from playoff_context.pipeline import build_report
        capture, config = fixture()
        report = build_report(capture, config, now=NOW, simulations=10)
        with self.assertRaisesRegex(ValueError, 'STALE'):
            module.build_memo_packet(report, now=datetime(2026, 11, 20, tzinfo=timezone.utc))
        with self.assertRaisesRegex(ValueError, 'week|page'):
            module.build_memo_packet(report, previs={'pages':[{'page_id':'W03-P30'}]},
                bindings={'W03-P30':'playoff_picture'}, now=NOW)

    def test_unvalidated_forecasts_are_removed_from_memo_copy_candidates(self):
        module = self.adapter()
        from playoff_context.pipeline import build_report
        capture, config = fixture()
        report = build_report(capture, config, now=NOW, simulations=10)
        report['forecast'].update(status='CONDITIONAL_MODEL_ESTIMATE', editorial_probability_eligible=False)
        report['teams']['1'].update(playoff_probability=0.99, seed_probability={'1': .5},
            division_title_probability=.4, expected_final_wins=2.1, next_game_leverage={'leverage_delta_pp':45})
        report['editorial_candidates'] = [{'class':'PROBABILISTIC','kind':'HIGH_LEVERAGE','team_id':'1'}]
        packet = module.build_memo_packet(report, now=NOW)
        self.assertNotIn('playoff_probability', packet['teams']['1'])
        self.assertNotIn('next_game_leverage', packet['teams']['1'])
        self.assertNotIn('expected_final_wins', packet['teams']['1'])
        self.assertEqual(packet['interpretations'], [])
        self.assertEqual(packet['forecast']['status'], 'WITHHELD_FROM_MEMO')


if __name__ == '__main__':
    unittest.main()
