"""Page-specific design integration must not rewrite canon or source facts."""
import hashlib,json,unittest
from pathlib import Path
P=Path(__file__).resolve().parent
E=P.parent/'production-evidence/design-personalization-20261117'
def load(p): return json.loads(p.read_text())
def digest(x): return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
class CompositionPersonalization(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.issue=load(P/'issue-previs.json');cls.pages={p['page_id']:p for p in cls.issue['pages']};cls.order=cls.issue['recommended_reading_order']
 def test_all_34_pages_have_distinct_scene_led_directions(self):
  for pid in self.order:
   with self.subTest(page=pid):
    c=self.pages[pid].get('composition_direction');self.assertIsInstance(c,dict,'Page-specific composition not integrated')
    for key in ['family','dominant_action','reading_path','heading_treatment','narration_placement','protected_subjects','data_treatment','personalization_note_ref']: self.assertTrue(c.get(key),key)
  self.assertTrue(all('composition_direction' in self.pages[p] for p in self.order))
  self.assertGreaterEqual(len({self.pages[p]['composition_direction']['family'] for p in self.order}),8)
 def test_directive_is_in_actual_request_prompt_and_all_mirrors(self):
  bs={p['page_id']:p for p in load(P/'illustrated-page-briefs.json')['pages']};fs={p['page_id']:p for p in load(P/'storyboard-folio-plan-pass5.json')['folios']}
  for pid in self.order:
   with self.subTest(page=pid):
    p=self.pages[pid];self.assertTrue('composition_direction' in p,pid)
    c=p['composition_direction'];r=load(P/'render-inputs'/pid/'request.json')
    self.assertEqual(r['scene']['composition_direction'],c);self.assertIn(c['reading_path'],r['prompt'])
    self.assertEqual(bs[pid]['composition_direction'],c);self.assertEqual(fs[pid]['composition_direction'],c)
    self.assertEqual(p['illustrated_page_brief'],bs[pid])
 def test_storycards_directors_and_landscapes_use_the_same_directions(self):
  cards=load(P/'storycards.json');directors=load(P/'director-sequences.json');land=load(P/'landscape-set-bible-pass4.json')
  for m in cards['matchups']:
   group=sorted([p for p in self.pages.values() if p['source_card_id']==m['id']],key=lambda p:p['recommended_reading_position'])
   self.assertEqual(len(group),len(m['beats']))
   for beat,page in zip(m['beats'],group):
    self.assertEqual(beat['composition_direction'],page['composition_direction'])
  for d in cards['departments']:
   matches=[p for p in self.pages.values() if p['source_card_id']==d['unit_id'] and p['page_id'] in self.order]
   if matches:self.assertEqual(d['composition_direction'],matches[0]['composition_direction'])
  for d in directors['pages']+land['department_landscapes']:
   self.assertEqual(d['composition_direction'],self.pages[d['page_id']]['composition_direction'])
 def test_fact_body_cast_and_geography_invariance(self):
  b=load(E/'baseline.json');self.assertEqual(b['reading_order'],self.order)
  self.assertEqual(hashlib.sha256((P/'facts.json').read_bytes()).hexdigest(),b['facts_sha256'])
  # A later, separately reviewed harvest changes copy on exactly these pages.
  # The historical design baseline still controls every cast/geography field
  # and the copy on the other 31 folios.
  selected=load(P/'playoff-harvest-copy.json')['pages']
  self.assertEqual(set(selected),{'W10-P28','W10-P30','W10-P31'})
  for pid in self.order:
   with self.subTest(page=pid):
    p=self.pages[pid]
    if pid in selected:self.assertEqual(p['draft_copy'],selected[pid]['publication_copy'])
    else:self.assertEqual(digest(p['draft_copy']),b['pages'][pid]['publication_copy_sha256'])
    self.assertEqual(p['characters_present'],b['pages'][pid]['characters_present']);self.assertEqual(p['encounter'],b['pages'][pid]['encounter'])
 def test_omitted_pittsys_book_does_not_acquire_design_or_render_target(self):
  self.assertNotIn('W10-P32',self.order)
  self.assertNotIn('composition_direction',self.pages['W10-P32'])
 def test_color_word_does_not_introduce_a_third_team(self):
  copy=self.pages['W10-P22']['draft_copy']['body'];self.assertNotIn('Red Leopards fire',copy);self.assertIn('Red fire crosses',copy)
 def test_personalization_pass_covers_six_arcs_and_sixteen_departments(self):
  path=P/'personalization-pass-20261117.json';self.assertTrue(path.exists(),'Missing live personalization pass')
  d=load(path);self.assertEqual(len(d['matchups']),6);self.assertEqual(len(d['supporting_pages']),16)
  ids=[pid for m in d['matchups'] for pid in m['page_ids']]+[p['page_id'] for p in d['supporting_pages']]
  self.assertEqual(set(ids),set(self.order));self.assertEqual(len(ids),34)
  for r in d['matchups']+d['supporting_pages']:
   self.assertEqual(r['status'],'SOURCE_GROUNDED_EDITORIAL_PASS_COMPLETE');self.assertEqual(r['founder_notes'],[]);self.assertFalse(r['approved_new_copy'])
 def test_current_archive_has_unambiguous_personalization_pointer(self):
  text=(P/'personalization-review.md').read_text();self.assertIn('PERSONALIZATION_PASS_2026-11-17.md',text.splitlines()[0])
 def test_personalization_is_a_completed_editorial_pass_not_blank_intake(self):
  d=load(P/'personalization-pass-20261117.json')
  self.assertEqual(d['status'],'SOURCE_GROUNDED_EDITORIAL_PASS_COMPLETE')
  for r in d['matchups']+d['supporting_pages']:
   with self.subTest(record=r.get('matchup_id',r.get('page_id'))):
    self.assertTrue(r.get('editorial_assessment'))
    for k in ['retain','strengthen','avoid','source_basis']:self.assertTrue(r['editorial_assessment'].get(k),k)
    self.assertEqual(r['founder_note_status'],'OPTIONAL_ADDITIONS_NOT_REQUIRED_TO_COMPLETE_PASS')
 def test_personalized_performance_notes_reach_all_actual_prompts(self):
  for pid in self.order:
   p=self.pages[pid];r=load(P/'render-inputs'/pid/'request.json')
   with self.subTest(page=pid):
    self.assertIsInstance(p.get('personalization_direction'),dict)
    self.assertEqual(r['scene']['personalization_direction'],p['personalization_direction'])
    self.assertIn(p['personalization_direction']['focus'],r['prompt'])
    self.assertTrue(p['personalization_direction']['source_refs'])
    self.assertIn('personalization_direction',p['illustrated_page_brief'])
 def test_personalization_does_not_leak_between_director_and_department_pages(self):
  d=load(P/'director-sequences.json');l=load(P/'landscape-set-bible-pass4.json')
  for entry in d['pages']+l['department_landscapes']:
   with self.subTest(page=entry['page_id']):
    self.assertEqual(entry['personalization_direction'],self.pages[entry['page_id']]['personalization_direction'])
 def test_proposed_narration_is_not_silently_published(self):
  d=load(P/'personalization-pass-20261117.json')
  for m in d['matchups']:
   cand=m.get('candidate_line');self.assertTrue(cand)
   self.assertEqual(cand['status'],'OPTIONAL_EDITORIAL_ALTERNATIVE_NOT_INSERTED')
   self.assertFalse(cand['attributed_real_quote'])
   self.assertTrue(all(cand['text'] not in self.pages[pid]['draft_copy']['body'] for pid in m['page_ids']))
 def test_scene_active_fire_is_not_instructed_as_quiet_ended_battle(self):
  d=self.pages['W10-P24']['composition_direction']
  self.assertEqual(d['family'],'kinetic_action')
  self.assertIn('surviving battery',d['protected_subjects'].lower())

 def test_personalization_reaches_every_consumer_without_candidate_lines(self):
  bs={p['page_id']:p for p in load(P/'illustrated-page-briefs.json')['pages']};fs={p['page_id']:p for p in load(P/'storyboard-folio-plan-pass5.json')['folios']}
  for pid in self.order:
   p=self.pages[pid];self.assertEqual(bs[pid]['personalization_direction'],p['personalization_direction']);self.assertEqual(fs[pid]['personalization_direction'],p['personalization_direction'])
  cards=load(P/'storycards.json')
  for m in cards['matchups']:
   group=sorted([p for p in self.pages.values() if p['source_card_id']==m['id']],key=lambda p:p['recommended_reading_position'])
   for beat,p in zip(m['beats'],group):self.assertEqual(beat['personalization_direction'],p['personalization_direction'])
  for d in load(P/'director-sequences.json')['pages']+load(P/'landscape-set-bible-pass4.json')['department_landscapes']:
   self.assertEqual(d['personalization_direction'],self.pages[d['page_id']]['personalization_direction'])
  candidates=[m['candidate_line']['text'] for m in load(P/'personalization-pass-20261117.json')['matchups']]
  for pid in self.order:
   prompt=load(P/'render-inputs'/pid/'request.json')['prompt']
   for candidate in candidates:self.assertNotIn(candidate,prompt)

if __name__=='__main__':unittest.main(verbosity=2)
