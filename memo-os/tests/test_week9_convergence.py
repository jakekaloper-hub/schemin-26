"""Validate coverage and input completeness, never final image or fact acceptance."""
from pathlib import Path
import json
import unittest
ROOT=Path(__file__).resolve().parents[2]
WEEK=ROOT/'memo-os/week-9'
class ConvergenceTests(unittest.TestCase):
 def setUp(self):
  self.issue=json.loads((WEEK/'WEEK_9_COMPLETE_ISSUE_PREVIS_2026-11-08.json').read_text())
  self.assertIn('convergence_review',self.issue,'Page-by-page review not implemented')
  self.review=self.issue['convergence_review'];self.pages={p['page_id']:p for p in self.issue['pages']}
 def test_all_40_sources_have_answers_and_destinations(self):
  rows=self.review['coverage'];self.assertEqual(len(rows),40)
  self.assertEqual({r['source_id'] for r in rows},{f'W09-P{i:02}' for i in range(1,41)})
  for r in rows:
   self.assertEqual(set(r['answers']),{f'Q{i}' for i in range(1,11)});self.assertTrue(r['destinations']);self.assertTrue(r['preserved_content'])
   for d in r['destinations']:self.assertIn(d,self.issue['reading_order'])
 def test_active_packets_and_both_orders_are_complete(self):
  active=[p for p in self.pages.values() if p['publication_included']]
  self.assertEqual(len(active),35);self.assertEqual(len(self.issue['reading_order']),35)
  self.assertEqual(set(self.issue['reading_order']),{p['page_id'] for p in active})
  self.assertEqual(len(self.issue['production_queue']),35)
  self.assertEqual({q['page_id'] for q in self.issue['production_queue']},set(self.issue['reading_order']))
  for p in active:
   for f in ['narrative_job','reference_assets','encounter','editorial_copy','layout_spec','page_character_contract','fact_dependencies','adjacent_pages','production_inputs']:self.assertIn(f,p)
   self.assertFalse(p['render_authorized']);self.assertIsNone(p['actual_winner_team_id']);self.assertEqual(p['layout_spec']['canvas'],[1080,1920])
 def test_overtures_have_two_different_viewpoints(self):
  ps=[p for p in self.pages.values() if p['page_role']=='two_character_pov_overture'];self.assertEqual(len(ps),6)
  for p in ps:
   self.assertEqual(len(p['characters_present']),2);self.assertEqual(set(p['editorial_copy']['pov']),{'home','away'})
   self.assertNotEqual(p['editorial_copy']['pov']['home'],p['editorial_copy']['pov']['away'])
   self.assertIsNone(p['editorial_copy']['selected_branch']);self.assertFalse(p['page_character_contract']['reference_bound_execution_proven'])
 def test_only_duplicate_carriers_are_absorbed(self):
  merged={r['source_id']:r for r in self.review['coverage'] if r['disposition']=='ABSORB_AND_RESTAGE'}
  self.assertEqual(set(merged),{'W09-P04','W09-P08','W09-P11','W09-P16','W09-P19'})
  for r in merged.values():self.assertTrue(r['causal_transfer'])
  for pid in ['W09-P14','W09-P29','W09-P38']:self.assertTrue(self.pages[pid]['publication_included'])
 def test_sources_not_falsely_promoted(self):
  self.assertIn('2026-11-09',self.issue['active_sports_source']['as_of']);self.assertFalse(self.issue['active_sports_source']['final_results_accepted'])
  self.assertEqual(self.pages['W09-P27']['book_operating_state'],'CLOSED_WEEK9_FOUNDER_CONFIRMED')
  self.assertFalse(self.pages['W09-P40']['forecast_contract']['percentages_available'])
  self.assertFalse(self.review['comparison']['crisper_visions']['visual_samples_inspected']);self.assertFalse(self.review['publication_approved'])
 def test_generation_queue_not_enabled_by_clock(self):
  self.assertEqual(self.issue['production_queue'][0]['page_id'],'W09-P05')
  for q in self.issue['production_queue']:
   self.assertEqual(q['state'],'BLOCKED_PENDING_DECLARED_INPUTS_AND_PROOF');self.assertIn('EXACT_SUBJECT_ATTACHMENTS',q['required_gates'])
  self.assertIn('WEEK9_EXPLICIT_SELECTOR',self.review['final_data_handoff']['requirements']);self.assertFalse(self.review['final_data_handoff']['scheduled'])
if __name__=='__main__':unittest.main()
