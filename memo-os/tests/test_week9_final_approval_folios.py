"""Final-results approval drafts, not publication or image acceptance."""
from pathlib import Path
from decimal import Decimal
import json
import unittest

ROOT = Path(__file__).resolve().parents[2]
WEEK = ROOT / 'memo-os/week-9'
APPROVAL = WEEK / 'WEEK_9_FINAL_APPROVAL_FOLIOS_2026-11-10.json'

class FinalApprovalTests(unittest.TestCase):
    def load(self):
        self.assertTrue(APPROVAL.is_file(), 'Final-result folios have not been hydrated')
        return json.loads(APPROVAL.read_text())

    def test_six_results_are_provider_decided_and_source_reconciled(self):
        a = self.load()
        self.assertEqual(len(a['matchups']), 6)
        expected = {'W09-M01':12, 'W09-M02':9, 'W09-M03':2, 'W09-M04':7, 'W09-M05':5, 'W09-M06':3}
        self.assertEqual({m['matchup_id']:m['winner_team_id'] for m in a['matchups']}, expected)
        self.assertTrue(a['verification']['twelve_starter_sums_match'])
        self.assertEqual(a['verification']['fresh_starter_values_matched'], 120)
        self.assertEqual(a['verification']['standings_records_reconciled'], 12)

    def test_all_35_active_packets_have_approval_copies_without_scope_change(self):
        a = self.load()
        issue = json.loads((WEEK/'WEEK_9_COMPLETE_ISSUE_PREVIS_2026-11-08.json').read_text())
        self.assertEqual(len(a['folios']), 35)
        self.assertEqual([f['page_id'] for f in a['folios']], issue['reading_order'])
        self.assertEqual(len(issue['pages']), 40)
        by = {p['page_id']:p for p in issue['pages']}
        for f in a['folios']:
            # The original finalization artifact remains immutable; the full-name revision is checked separately.
            self.assertEqual(by[f['page_id']].get('approval_folio_before_full_names', by[f['page_id']]['approval_folio']), f)
            self.assertEqual(f['canvas'], [1080,1920])
            self.assertTrue(f['copy']['body'])
            self.assertFalse(f['render_authorized'])
            self.assertFalse(f['publication_approved'])

    def test_exact_existing_finale_is_selected_once_and_opposite_is_archived(self):
        a = self.load()
        issue = json.loads((WEEK/'WEEK_9_COMPLETE_ISSUE_PREVIS_2026-11-08.json').read_text())
        ps = {p['page_id']:p for p in issue['pages']}
        finale = {'W09-P07':'home_win','W09-P10':'away_win','W09-P13':'home_win','W09-P15':'home_win','W09-P18':'home_win','W09-P21':'home_win'}
        for f in a['folios']:
            if f['page_id'] not in finale:
                continue
            branch = finale[f['page_id']]
            self.assertEqual(f['selected_branch'], branch)
            self.assertEqual(f['copy']['body'], ps[f['page_id']]['editorial_copy']['conditional_narratives'][branch])
            self.assertFalse(f['opposite_ending_in_publication_copy'])
        self.assertEqual(sum(f.get('is_finale',False) for f in a['folios']),6)

    def test_current_standings_and_forecast_are_distinct(self):
        fs={f['page_id']:f for f in self.load()['folios']}
        self.assertEqual(len(fs['W09-P24']['data_rows']),12)
        self.assertEqual(len(fs['W09-P40']['data_rows']),12)
        self.assertEqual(fs['W09-P24']['data_rows'][0]['team_id'],12)
        self.assertEqual(fs['W09-P40']['data_rows'][1]['projected_rank'],7)
        self.assertFalse(fs['W09-P40']['percentages_available'])
        self.assertTrue(all(r.get('clinched') is None for r in fs['W09-P40']['data_rows']))
        self.assertEqual(len(fs['W09-P25']['data_rows']),12)
        self.assertEqual(fs['W09-P25']['ranking_classification'],'EDITORIAL_SCORING_FORM_NOT_ESPN_SEED_OR_ODDS')

    def test_reporting_and_preview_use_final_facts_and_honest_reserve_scope(self):
        fs={f['page_id']:f for f in self.load()['folios']}
        self.assertEqual([c['label'] for c in fs['W09-P22']['report_cards']],['THE GOOD','THE BAD','THE UGLY'])
        self.assertEqual(len(fs['W09-P38']['report_cards']),3)
        self.assertEqual(len(fs['W09-P26']['data_rows']),6)
        self.assertEqual(fs['W09-P26']['gotw_candidate']['home_team_id'],7)
        self.assertEqual(fs['W09-P26']['gotw_candidate']['away_team_id'],5)
        self.assertFalse(fs['W09-P26']['gotw_candidate']['approved'])
        self.assertEqual(fs['W09-P37']['availability_scope'],'WEEK9_FANTASY_IR_SLOTS_NOT_NEW_NFL_IR_NEWS')
        self.assertFalse(fs['W09-P37']['official_injury_news_verified'])
        self.assertEqual(fs['W09-P27']['book_state'],'CLOSED_ONE_WEEK')

    def test_approval_and_png_gates_remain_closed(self):
        a=self.load()
        self.assertFalse(a['approval']['founder_approved'])
        self.assertFalse(a['approval']['independent_source_acceptance'])
        self.assertFalse(a['approval']['render_authorized'])
        self.assertFalse(a['approval']['release_approved'])
        self.assertEqual(a['verification']['new_scene_images'],0)
        self.assertTrue(a['verification']['character_authority_unchanged'])
        self.assertTrue(a['verification']['reading_order_unchanged'])
        self.assertTrue((WEEK/'WEEK_9_FINAL_APPROVAL_FOLIOS_2026-11-10.md').is_file())
        self.assertTrue((WEEK/'WEEK_9_FINAL_APPROVAL_FOLIOS_2026-11-10.html').is_file())

if __name__ == '__main__':
    unittest.main()
