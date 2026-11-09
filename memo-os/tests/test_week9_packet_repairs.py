"""Regression checks for the actual Week9 consumer conflicts. No art/fact approval."""
from pathlib import Path
import copy, hashlib, importlib.util, json, subprocess, sys, tempfile, unittest
ROOT=Path(__file__).resolve().parents[2]
W=ROOT/'memo-os/week-9'
REG=W/'WEEK_9_COMPLETE_ISSUE_PREVIS_2026-11-08.json'

class PacketRepairTests(unittest.TestCase):
 def setUp(self):
  self.issue=json.loads(REG.read_text());self.pages={p['page_id']:p for p in self.issue['pages']}
  spec=importlib.util.spec_from_file_location('prep_repairs',W/'prepare_production_inputs.py')
  self.mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.mod)
 def test_inline_proofs_resolve_current_layout_copy_and_neighbors(self):
  for pid in ['W09-P05','W09-P20']:
   p=self.pages[pid];proof=p['proof_preparation'];h=proof['execution_handoff']
   self.assertEqual(h['layout_source'],'layout_spec');self.assertEqual(h['exact_copy_source'],'editorial_copy')
   self.assertEqual(proof['sequence_readthrough']['previous_page'],p['adjacent_pages']['previous'])
   self.assertEqual(proof['sequence_readthrough']['next_page'],p['adjacent_pages']['next'])
   self.assertEqual(proof['legacy_layout_disposition'],'HISTORICAL_NON_EXECUTABLE')
 def test_active_beat_placement_is_unique_and_source_is_preserved(self):
  seen=set()
  for pid in self.issue['reading_order']:
   for b in self.pages[pid].get('written_storyboard',{}).get('beats',[]):
    self.assertEqual(b['page_id'],pid);self.assertNotIn(b['beat_id'],seen);seen.add(b['beat_id'])
  for pid,old in [('W09-P31','W09-P04'),('W09-P32','W09-P08'),('W09-P33','W09-P11'),('W09-P35','W09-P16'),('W09-P36','W09-P19')]:
   self.assertTrue(all(b['source_page_id']==old for b in self.pages[pid]['written_storyboard']['beats']))
   self.assertFalse(self.pages[old]['publication_included'])
 def test_chili_overture_is_not_the_cart_setup(self):
  a=self.pages['W09-P34']['written_storyboard']['beats'];b=self.pages['W09-P14']['written_storyboard']['beats']
  self.assertEqual(len(a),2);self.assertFalse({x['beat_id'] for x in a}&{x['beat_id'] for x in b})
  self.assertEqual({x['viewpoint'] for x in a},{'home','away'})
  self.assertEqual([x['beat_id'] for x in b],['W09-M04-B01','W09-M04-B02','W09-M04-B03'])
 def test_paintball_beats_have_real_ordered_regions(self):
  p=self.pages['W09-P20'];layout=p['layout_spec'];seq=layout.get('art_sequence',[])
  self.assertEqual(seq,['breakout','crossing_slide','counter_move'])
  previous_bottom=300
  for name in seq:
   x,y,w,h=layout['zones'][name];self.assertGreaterEqual(y,previous_bottom);self.assertGreaterEqual(w,900);previous_bottom=y+h
  self.assertLessEqual(previous_bottom,layout['zones']['body'][1])
  self.assertEqual([a['zone'] for a in p['proof_preparation']['action_blocks']],seq)
  self.assertTrue(all('paint' in a['action'].lower() or 'marker' in a['action'].lower() for a in p['proof_preparation']['action_blocks']))
 def test_export_includes_transfers_current_beats_and_scene_rules(self):
  p=self.pages['W09-P20']
  with tempfile.TemporaryDirectory() as td:
   out=Path(td)/'kit';m=self.mod.export_page_kit(ROOT,self.issue,'W09-P20',out)
   self.assertIn('ACTIVE_SCENE.json',m['files']);scene=json.loads((out/'ACTIVE_SCENE.json').read_text())
   self.assertEqual(scene['layout_spec'],p['layout_spec']);self.assertEqual(scene['adjacent_pages'],p['adjacent_pages'])
   self.assertEqual(scene['absorbed_source_beats'],p['absorbed_source_beats'])
   text=(out/'COMMISSION.md').read_text();self.assertIn(p['absorbed_source_beats'][0]['required_visible_transfer'],text)
   self.assertFalse(m['renderer_binding_proven']);self.assertFalse(m['artwork_generated'])
 def test_stale_layout_and_missing_transfer_are_rejected_before_export(self):
  for mode in ['layout','transfer','adjacency']:
   issue=copy.deepcopy(self.issue);p=next(p for p in issue['pages'] if p['page_id']=='W09-P20')
   if mode=='layout':p['proof_preparation']['execution_handoff']['layout_source']='proof_preparation.layout'
   elif mode=='transfer':p['absorbed_source_beats']=[]
   else:p['proof_preparation']['sequence_readthrough']['previous_page']='W09-P19'
   with tempfile.TemporaryDirectory() as td:
    out=Path(td)/'kit'
    with self.assertRaises(ValueError,msg=mode):self.mod.export_page_kit(ROOT,issue,'W09-P20',out)
    self.assertFalse(out.exists())
 def test_gate_phases_do_not_require_output_before_attempt(self):
  for q in self.issue['production_queue']:
   phases=q.get('gate_phases',{});self.assertIn('proof_preflight',phases);self.assertIn('post_render',phases)
   pre=phases['proof_preflight']['requirements']
   self.assertNotIn('FINAL_RASTER_QA',pre);self.assertNotIn('ACCEPTED_WEEK9_OUTCOME_FOR_PUBLISHED_VERSION',pre)
   self.assertIn('FINAL_RASTER_QA',phases['post_render']['requirements'])
   self.assertFalse(phases['release']['authorized']);self.assertFalse(phases['proof_preflight']['satisfied'])
  for pid in ['W09-P27','W09-P29','W09-P30']:
   q=next(q for q in self.issue['production_queue'] if q['page_id']==pid)
   self.assertFalse(q['gate_phases']['publication_data']['week9_result_required'])
 def test_review_owners_are_not_fabricated_acceptance(self):
  r=self.issue.get('approval_routing',{})
  self.assertEqual(r.get('design_work'),'DELEGATED_WITHIN_EXISTING_SCOPE')
  self.assertEqual(r['source_acceptance']['state'],'UNRESOLVED_NO_RECEIVER_ACK')
  self.assertIsNone(r['source_acceptance']['acceptance_receipt'])
  self.assertEqual(r['founder_visual_review']['owner'],'Jake');self.assertFalse(r['release_approved'])
 def test_map_sources_and_markers_match_canonical_data(self):
  m=self.pages['W09-P30'].get('map_binding',{});self.assertEqual(len(m.get('home_markers',[])),12);self.assertEqual(len(m.get('event_markers',[])),6)
  locations={x['id']:x for x in json.loads((ROOT/'world/data/locations.json').read_text())['locations']}
  for item in m['source_assets']:
   self.assertEqual(hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest(),item['sha256'])
  for row in m['home_markers']+m['event_markers']:
   self.assertEqual(row['abstract_position'],locations[row['location_id']]['abstract_position'])
  self.assertFalse(m['new_geography']);self.assertFalse(m['final_map_accepted'])
 def test_reader_copy_not_production_policy_and_reports_honest(self):
  self.assertNotIn('not a new geography',self.pages['W09-P30']['editorial_copy']['body'])
  self.assertNotIn('none is invented here',self.pages['W09-P40']['editorial_copy']['body'])
  self.assertEqual(set(self.pages['W09-P22']['reporting_contract']['sections']),{'GOOD','BAD','UGLY'})
  for pid in ['W09-P22','W09-P37','W09-P38','W09-P25','W09-P40']:
   self.assertFalse(self.pages[pid]['reporting_contract']['final_content_accepted'])
 def test_preview_consumes_packet_without_overriding_values(self):
  builder=W/'production-evidence/convergence-2026-11-09/build_layout_rehearsal.py'
  before=REG.read_bytes();subprocess.run([sys.executable,str(builder)],check=True,capture_output=True)
  self.assertEqual(before,REG.read_bytes());text=(W/'WEEK_9_FULL_PAGE_LAYOUT_REHEARSAL_2026-11-09.html').read_text()
  self.assertIn('data-zone="breakout"',text);self.assertIn('data-zone="crossing_slide"',text)
  self.assertIn(self.pages['W09-P40']['editorial_copy']['body'],text)
 def test_report_cards_are_populated_but_not_final_claims(self):
  c=self.pages['W09-P22']['editorial_copy'].get('report_cards',[])
  self.assertEqual([x['heading'] for x in c],['THE GOOD','THE BAD','THE UGLY'])
  for x in c:
   self.assertTrue(x['body']);self.assertTrue(x['source_paths']);self.assertFalse(x['final_accepted'])
   self.assertIn('2026-11-09',x['as_of']);self.assertTrue(all((ROOT/p).is_file() for p in x['source_paths']))
  self.assertEqual(len(self.pages['W09-P23']['editorial_copy'].get('report_cards',[])),3)
  self.assertEqual(len(self.pages['W09-P39']['editorial_copy'].get('report_cards',[])),3)
 def test_existing_canon_and_result_guards_remain(self):
  self.assertEqual(len(self.issue['reading_order']),35);self.assertEqual(len(self.issue['pages']),40)
  self.assertFalse(self.issue['active_sports_source']['final_results_accepted'])
  for p in self.pages.values():self.assertFalse(p['render_authorized']);self.assertIsNone(p['actual_winner_team_id'])
  for r in self.issue['resolved_character_appearances'].values():
   self.assertFalse(r['identity_reapproval_required'])
   self.assertEqual(hashlib.sha256((ROOT/r['appearance_authority_path']).read_bytes()).hexdigest(),r['appearance_authority_sha256'])

if __name__=='__main__':unittest.main()
