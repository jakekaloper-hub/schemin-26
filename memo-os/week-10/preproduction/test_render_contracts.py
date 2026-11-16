"""Regression tests for the actual Week 10 page-render inputs, not artwork approval."""
import hashlib,json,unittest
from pathlib import Path
P=Path(__file__).resolve().parent
R=P.parents[2]
def load(name): return json.loads((P/name).read_text())
class Week10RenderContracts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.issue=load('issue-previs.json');cls.briefs=load('illustrated-page-briefs.json');cls.plan=load('storyboard-folio-plan-pass5.json')
  cls.pages={p['page_id']:p for p in cls.issue['pages']};cls.bs={p['page_id']:p for p in cls.briefs['pages']};cls.fs={p['page_id']:p for p in cls.plan['folios']}
 def test_order_and_six_sheet_counts(self):
  order=self.issue['recommended_reading_order'];self.assertEqual(len(order),34);self.assertEqual(len(set(order)),34);self.assertNotIn('W10-P32',order)
  self.assertEqual(order[18],'W10-P34');self.assertEqual(order[32],'W10-P35');self.assertEqual([len(order[i:i+6]) for i in range(0,34,6)],[6,6,6,6,6,4])
 def test_cover_subjects_in_every_consumer(self):
  ids={'CHAR-AUSTIN-BYARS','CHAR-DAVID-BABB'};self.assertEqual(set(self.pages['W10-P01']['characters_present']),ids)
  self.assertEqual({x['character_id'] for x in self.fs['W10-P01']['characters']},ids)
 def test_opening_drive_matches_published_editorial_precedent(self):
  p=self.pages['W10-P02'];self.assertIn('briefing',p['camera_and_composition'].lower());self.assertEqual(p['draft_copy']['department_heading'],'OPENING DRIVE')
  self.assertNotEqual(p['encounter']['venue_id'],'LOC-BRIDGE-MOUNTAIN-LAKE')
 def test_full_prose_and_nested_briefs_are_synchronized(self):
  for id in self.issue['recommended_reading_order']:
   with self.subTest(page=id):
    p=self.pages[id];b=self.bs[id];f=self.fs[id]
    self.assertEqual(p['draft_copy'],b['publication_copy']);self.assertEqual(p['draft_copy'],f['publication_copy'])
    self.assertEqual(p['illustrated_page_brief'],b);self.assertEqual(p['candidate_render_prompt'],b['artist_prompt'])
    self.assertGreater(len(p['draft_copy']['body']),40);self.assertNotIn('annotated storyboard',f['sketch_format'].lower())
 def test_all_page_requests_have_actual_image_bytes(self):
  for id in self.issue['recommended_reading_order']:
   with self.subTest(page=id):
    request=load('render-inputs/'+id+'/request.json');self.assertEqual(request['canvas'],[1080,1920]);self.assertEqual(request['publication_copy'],self.pages[id]['draft_copy'])
    self.assertTrue(request['reference_images']);self.assertFalse(request['image_generation_executed'])
    for im in request['reference_images']:
     path=R/im['repo_path'];self.assertTrue(path.is_file(),str(path));self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),im['sha256'])
    cast={x['character_id'] for x in request['reference_images'] if x.get('character_id')}
    self.assertTrue(set(self.pages[id]['characters_present']).issubset(cast))
 def test_chili_later_reference_is_attached(self):
  for id in ['W10-P05','W10-P06','W10-P07']:
   request=load('render-inputs/'+id+'/request.json');refs=[x for x in request['reference_images'] if x.get('character_id')=='CHAR-BRANDON-PRYOR']
   self.assertTrue(any(x['role']=='current_appearance_override' for x in refs))
 def test_scoreboard_pairs_exact(self):
  expected=[('The Chili Cheesers','D0nkey K0ng'),('Red Leopards','El Niño'),('Three Dreaded Snake','Seven Deadly Chins'),('Mud Dogs','Slob on my Dobb'),('Dr. Duckhook',"His Majesty's Blood"),('ObiWan Jacoby','The LLC')]
  rows=self.pages['W10-P04']['draft_copy']['rows'];self.assertEqual([(r['home_team'].strip(),r['away_team'].strip()) for r in rows],expected)
  self.assertTrue(all(r['status']=='PROVISIONAL' for r in rows))
 def test_grayscale_proofs_do_not_claim_results_or_approval(self):
  for id in self.issue['recommended_reading_order']:
   request=load('render-inputs/'+id+'/request.json');self.assertFalse(request['publication_approved']);self.assertEqual(request['stage'],'GRAYSCALE_FOLIO_PROOF')
   self.assertEqual(request['sports_policy']['unresolved_numerals'],'BLANK_RESERVED_FIELDS');self.assertFalse(request['sports_policy']['official_winner_decided'])
if __name__=='__main__': unittest.main(verbosity=2)
