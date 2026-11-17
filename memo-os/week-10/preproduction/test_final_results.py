"""Final-result regression coverage, written before finalization implementation."""
import hashlib,json,re,unittest
from pathlib import Path
P=Path(__file__).resolve().parent
EXPECTED={7:93.70,5:156.67,2:147.82,9:189.08,6:82.78,11:146.22,10:113.62,3:179.29,12:127.67,8:208.76,1:166.53,4:203.96}
FINALES=['W10-P07','W10-P10','W10-P14','W10-P17','W10-P21','W10-P24']
def load(n):return json.loads((P/n).read_text())
class FinalResults(unittest.TestCase):
 def setUp(self):
  self.f=load('facts.json');self.i=load('issue-previs.json');self.pages={p['page_id']:p for p in self.i['pages']}
 def test_all_six_official_winners_and_final_scores(self):
  for g in self.f['games']:
   self.assertEqual(g['provider_winner'],'AWAY');self.assertEqual(g['final_winner'],g['away']);self.assertEqual(g['scope'],'W10_FINAL')
  for t,v in EXPECTED.items():self.assertEqual(self.f['teams'][f'T{t:02d}']['current_points'],v)
 def test_official_records_and_seeds_through_ten(self):
  for t in self.f['teams'].values():
   r=t['post_week10_official_record'];self.assertIsNotNone(r);self.assertEqual(r['w']+r['l']+r['t'],10);self.assertIsNotNone(t['post_week10_official_seed'])
  self.assertEqual([r['team'] for r in self.pages['W10-P27']['draft_copy']['rows']][:3],['Slob on my Dobb','El Niño','D0nkey K0ng'])
 def test_scoreboard_and_six_finale_receipts(self):
  self.assertTrue(all(r['status']=='FINAL' for r in self.pages['W10-P04']['draft_copy']['rows']))
  for pid in FINALES:
   self.assertEqual(self.pages[pid]['draft_copy'].get('result',{}).get('status'),'FINAL')
 def test_no_outdated_pending_claims_in_reader_copy(self):
  banned=['Tonight\'s remaining starters','all six results await','the final sports outcome remains unposted','if the current leads hold','Monday can still change','THE The LLC','current leading-score branch','nine posted results']
  for pid in self.i['recommended_reading_order']:
   body=json.dumps(self.pages[pid]['draft_copy'],ensure_ascii=False).lower()
   for s in banned:self.assertNotIn(s.lower(),body,pid+': '+s)
 def test_every_request_declares_final_week10_not_final_week11(self):
  for pid in self.i['recommended_reading_order']:
   q=load('render-inputs/'+pid+'/request.json')
   self.assertTrue(q['sports_policy']['official_winner_decided'],pid)
   self.assertEqual(q['sports_policy']['source_capture_scope'],'W10_PROVIDER_FINAL')
   self.assertFalse(q['publication_approved']);self.assertFalse(q['image_generation_executed'])
 def test_scoring_form_uses_final_pf_once(self):
  from decimal import Decimal,ROUND_HALF_UP
  rows=self.f.get('scoring_form',{}).get('rows',[]);self.assertEqual(len(rows),12)
  for tid,ppg,unrounded,display in rows:
   t=self.f['teams'][tid];v=Decimal('0.7')*Decimal(str(t['post_week10_official_points_for']))/10+Decimal('0.3')*Decimal(str(t['current_points']))
   self.assertEqual(display,float(v.quantize(Decimal('.01'),rounding=ROUND_HALF_UP)))
 def test_distinct_final_and_current_roster_snapshots(self):
  x=load('final-league-snapshot.json');self.assertEqual(x['week10_roster_entry_count'],224);self.assertEqual(x['current_roster_entry_count'],222)
 def test_all_manifest_hashes_match_current_requests(self):
  for x in load('render-inputs/manifest.json')['pages']:
   self.assertEqual(hashlib.sha256((P/x['request']).read_bytes()).hexdigest(),x['request_sha256'])
 def test_user_week11_implications_are_in_the_exact_existing_folio(self):
  p=self.pages['W10-P31'];self.assertEqual(p['recommended_reading_position'],32)
  rows=p['draft_copy']['rows'];self.assertEqual(len(rows),6)
  self.assertTrue(all(r.get('implication') for r in rows))
  self.assertIn('three divisional rounds',p['draft_copy']['body'])
  self.assertIn('not automatic eliminators',p['draft_copy']['body'])
  self.assertEqual(self.f['week11_implications']['only_automatic_loss_elimination_team'],'T10')
 def test_availability_exclusion_ids_are_unique(self):
  data=load('available-slots-pass3.json')
  for pos,rows in data['excluded_returned_entries'].items():
   ids=[x['id'] for x in rows];self.assertEqual(len(ids),len(set(ids)),pos)
 def test_provider_week10_game_totals_balance(self):
  snap=load('final-league-snapshot.json');self.assertEqual(sum(t['wins'] for t in snap['standings']),60)
  self.assertEqual(sum(t['losses'] for t in snap['standings']),60)
  self.assertEqual(sum(1 for x in self.f['official_records']['records'].values() if x['w']==6),6)
 def test_playoff_claims_have_constructive_witnesses(self):
  w=load('playoff-witnesses-final.json');self.assertEqual(w['witnesses_passed'],25)
  for tid,v in w['team_status'].items():
   self.assertIn(int(tid),v['qualification_witness']['qualified_team_ids'])
   self.assertNotIn(int(tid),v['nonqualification_witness']['qualified_team_ids'])
 def test_effective_scoring_roster_matches_every_team_final(self):
  snap=load('final-league-snapshot.json')
  for tid,players in snap['week10_players'].items():
   from decimal import Decimal
   total=sum(Decimal(str(p['points'])) for p in players if p['started'])
   self.assertEqual(float(total),EXPECTED[int(tid)])
 def test_render_prompts_are_page_scoped_not_whole_roster_dumps(self):
  for pid in self.i['recommended_reading_order']:
   request=load('render-inputs/'+pid+'/request.json')
   self.assertLess(len(request['prompt']),45000,pid)
   self.assertTrue(all('snapshot_value' not in x for x in request['sports_policy']['refresh_fields']),pid)
if __name__=='__main__':unittest.main(verbosity=2)
