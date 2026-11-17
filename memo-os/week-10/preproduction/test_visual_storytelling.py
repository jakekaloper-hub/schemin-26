"""Sequential folio direction is content, not proof of rendered visual quality."""
import hashlib,json,unittest
from pathlib import Path
P=Path(__file__).resolve().parent
E=P.parent/'production-evidence/visual-storytelling-20261117'
def read(p):return json.loads(p.read_text())
class VisualStorytelling(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.issue=read(P/'issue-previs.json');cls.order=cls.issue['recommended_reading_order'];cls.pages={x['page_id']:x for x in cls.issue['pages']}
 def registry(self):
  p=P/'visual-storytelling-pass-20261117.json';self.assertTrue(p.is_file(),'Missing sequential visual-storytelling contract');return read(p)
 def test_all_34_folios_have_shot_direction(self):
  d=self.registry();self.assertEqual([x['page_id'] for x in d['pages']],self.order);self.assertNotIn('W10-P32',[x['page_id'] for x in d['pages']])
  self.assertTrue(d['one_folio_may_contain_multiple_shots']);self.assertFalse(d['images_generated'])
 def test_shots_are_intelligible_and_bound_to_canonical_cast(self):
  for p in self.registry()['pages']:
   with self.subTest(page=p['page_id']):
    self.assertTrue(1<=len(p['shots'])<=3);self.assertEqual(len(p['shots']),len({s['id'] for s in p['shots']}))
    for s in p['shots']:
     for k in ['camera','action','new_information','time_relation','role']:self.assertTrue(s[k],k)
     self.assertTrue(set(s['pov_owner_ids']).issubset(self.pages[p['page_id']]['characters_present']))
 def test_every_matchup_has_a_pov_opening_and_causal_escalation(self):
  d=self.registry();ps={p['page_id']:p for p in d['pages']}
  self.assertEqual(len(d['matchups']),6)
  for arc in d['matchups']:
   with self.subTest(arc=arc['id']):
    self.assertEqual(len(arc['pages']),3);self.assertGreater(len(ps[arc['pages'][0]]['shots']),1)
    self.assertEqual(set(x for s in ps[arc['pages'][0]]['shots'] for x in s['pov_owner_ids']),set(self.pages[arc['pages'][0]]['characters_present']))
    self.assertGreater(len({ps[pid]['structure'] for pid in arc['pages']}),1)
    self.assertTrue(arc['cause_and_effect']);self.assertTrue(arc['page_turn'])
 def test_copy_facts_cast_and_geography_follow_accepted_sources(self):
  b=read(E/'baseline.json');self.assertEqual(b['order'],self.order)
  self.assertEqual(hashlib.sha256((P/'facts.json').read_bytes()).hexdigest(),b['facts_sha256'])
  founder=read(E.parent/'founder-revision-20261117'/'approved-fields.json')
  for pid,old in b['pages'].items():
   with self.subTest(page=pid):
    selected=read(P/'playoff-harvest-copy.json')['pages']
    self.assertEqual(set(selected),{'W10-P28','W10-P30','W10-P31'})
    expected=selected[pid]['publication_copy'] if pid in selected else old['copy']
    changes=founder.get(pid,{})
    self.assertEqual(self.pages[pid]['draft_copy'],expected | changes.get('copy',{}))
    self.assertEqual(self.pages[pid]['characters_present'],old['cast'])
    self.assertEqual(self.pages[pid]['encounter'],old['encounter'] | changes.get('encounter',{}))
 def test_full_body_flows_once_in_unchanged_order(self):
  for p in self.registry()['pages']:
   body=self.pages[p['page_id']]['draft_copy']['body'];zones=p['copy_flow']['body_ranges'];self.assertTrue(zones)
   self.assertEqual(''.join(body[z['start']:z['end']] for z in zones),body,p['page_id'])
   self.assertEqual(zones[0]['start'],0);self.assertEqual(zones[-1]['end'],len(body))
   self.assertTrue(all(zones[n]['end']==zones[n+1]['start'] for n in range(len(zones)-1)))
 def test_actual_prompts_and_principal_mirrors_consume_shots(self):
  bs={p['page_id']:p for p in read(P/'illustrated-page-briefs.json')['pages']};fs={p['page_id']:p for p in read(P/'storyboard-folio-plan-pass5.json')['folios']}
  for p in self.registry()['pages']:
   pid=p['page_id'];r=read(P/'render-inputs'/pid/'request.json')
   with self.subTest(page=pid):
    self.assertEqual(self.pages[pid].get('visual_storytelling'),p);self.assertEqual(r['scene'].get('visual_storytelling'),p)
    self.assertEqual(bs[pid].get('visual_storytelling'),p);self.assertEqual(fs[pid].get('visual_storytelling'),p)
    self.assertTrue(all(s['new_information'] in r['prompt'] for s in p['shots']))
    self.assertEqual(r['canvas'],[1080,1920]);self.assertFalse(r['image_generation_executed'])
 def test_all_remaining_consumers_match(self):
  self.registry();cards=read(P/'storycards.json')
  for m in cards['matchups']:
   group=sorted([p for p in self.pages.values() if p['source_card_id']==m['id']],key=lambda p:p['recommended_reading_position'])
   for beat,page in zip(m['beats'],group):self.assertEqual(beat.get('visual_storytelling'),page.get('visual_storytelling'),page['page_id'])
  for dep in cards['departments']:
   targets=[p for p in self.pages.values() if p['page_id'] in self.order and p['source_card_id']==dep['unit_id']]
   if targets:self.assertEqual(dep.get('visual_storytelling'),targets[0].get('visual_storytelling'))
  for p in read(P/'director-sequences.json')['pages']+read(P/'landscape-set-bible-pass4.json')['department_landscapes']:
   self.assertEqual(p.get('visual_storytelling'),self.pages[p['page_id']].get('visual_storytelling'),p['page_id'])
 def test_hero_rest_pages_and_canon_specific_guardrails(self):
  d=self.registry();p={x['page_id']:x for x in d['pages']}
  for pid in ['W10-P02','W10-P04','W10-P14','W10-P17','W10-P21','W10-P27','W10-P29','W10-P33']:self.assertEqual(len(p[pid]['shots']),1,pid)
  self.assertEqual(p['W10-P09']['time_logic'],'CHRONOLOGICAL_SAME_LOCATION')
  self.assertEqual(p['W10-P35']['time_logic'],'SIMULTANEOUS_SAME_LOCATION')
  self.assertEqual(p['W10-P01']['time_logic'],'EDITORIAL_JUXTAPOSITION_NOT_A_MEETING')
  self.assertIn('surviving battery',json.dumps(p['W10-P24']).lower());self.assertIn('untouched burger',json.dumps(p['W10-P21']).lower())

 def test_founder_scene_choices_reach_the_renderer_in_order(self):
  # Read the actions that the illustrator actually receives for each shot.
  markers = {
   'W10-P05': ['gets a laugh', 'imitation', 'draws his own lasso'],
   'W10-P08': ['storm roll in', 'sandbag'],
   'W10-P09': ['fallen trunk', 'whole tree topples', 'right-wall backboard'],
   'W10-P22': ['both batteries', 'disables the first battery', 'rises'],
   'W10-P23': ['descends', 'illuminated arch', 'blade still lit'],
   'W10-P24': ['face obiwan', 'raises a hand', 'surviving battery', 'lightning', 'silhouette'],
  }
  for pid, phrases in markers.items():
   with self.subTest(page=pid):
    request=read(P/'render-inputs'/pid/'request.json')
    shots=request['scene']['visual_storytelling']['shots']
    actions=' '.join(shot['action'].lower() for shot in shots)
    position=0
    for phrase in phrases:
     index=actions.find(phrase,position)
     self.assertGreaterEqual(index,0,phrase)
     position=index+len(phrase)
    self.assertTrue(all(s['action'] in request['prompt'] for s in shots))

 def test_founder_change_scope(self):
  changes=read(E.parent/'founder-revision-20261117'/'approved-fields.json')
  self.assertEqual(set(changes),set('W10-P'+n for n in ['01','02','05','08','09','22','23','24']))
  for pid, fields in changes.items():
   self.assertLessEqual(set(fields.get('copy',{})),{'body','headline'})
   self.assertLessEqual(set(fields.get('encounter',{})),{'venue_type','persistent_landmarks','temporary_scene_props'})
   self.assertEqual(self.pages[pid]['encounter']['venue_id'],read(E/'baseline.json')['pages'][pid]['encounter']['venue_id'])

if __name__=='__main__':unittest.main(verbosity=2)
