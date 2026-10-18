"""Deterministic non-metric spatial/visual candidate preflight. No engineering certification."""
import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('preview',Path(__file__).with_name('week6_candidate_image_resolver.py'))
resolver=importlib.util.module_from_spec(spec);spec.loader.exec_module(resolver)
EXPECTED={
 'LOC-RED-RUINS':('CHAR-KEVIN-ZEEK','REG-EASTERN-STORM-COAST','PERMANENT_CANON'),
 'LOC-COUNTRY-CLUB-JACKSON':('CHAR-ZACH-WILSON','REG-SOUTHERN-WETLANDS','PERMANENT_CANON'),
 'LOC-SLOB-FOOTHILL-CAMP':('CHAR-JORDAN-HOLLINGSHEAD','REG-UPPER-VALLEYS','PROVISIONAL_CANON'),
 'LOC-CHILI-STABLE':('CHAR-BRANDON-PRYOR','REG-WESTERN-TABLELANDS','PERMANENT_CANON'),
 'LOC-MUD-DOGS-SWAMP':('CHAR-BOBBY-MITCHELL','REG-SOUTHERN-WETLANDS','PERMANENT_CANON'),
 'LOC-TDS-WATERFALL-TEMPLE':('CHAR-PHILLIP-PITTS','REG-SOUTHERN-WETLANDS','PERMANENT_CANON'),
}
class SpatialImagePreflight(unittest.TestCase):
 def test_six_location_parent_owner_zone_and_visual_binding(self):
  locations={x['id']:x for x in json.loads((ROOT/'world/data/locations.json').read_text())['locations']}
  specs={x['location_id']:x for x in json.loads((ROOT/'memo-os/week-6/WEEK_6_CINEMATIC_CANDIDATE_REVIEW_V1.json').read_text())['locations']}
  self.assertEqual(set(specs),set(EXPECTED))
  for loc,(owner,zone,status) in EXPECTED.items():
   with self.subTest(loc=loc):
    x=locations[loc];self.assertEqual((x['owner_character_id'],x['physical_zone_id'],x['canon_status']),(owner,zone,status))
    self.assertEqual(specs[loc]['zone'],zone)
    self.assertEqual(resolver.resolve(loc)['location_id'],loc)
    self.assertTrue(specs[loc]['rejected_drift'])
 def test_abstract_coordinates_never_claim_metric_feasibility(self):
  x=json.loads((ROOT/'world/data/locations.json').read_text())
  self.assertIn('non-metric',x['coordinate_space'])
  for loc in EXPECTED:self.assertEqual(len(next(v for v in x['locations'] if v['id']==loc)['abstract_position']),2)
 def test_active_reference_registry_still_unapproved(self):
  reg={x['location_id']:x for x in json.loads((ROOT/'world/location-control-plane/registries/LOCATION_REFERENCE_REGISTRY.json').read_text())['locations']}
  for loc in EXPECTED:
   with self.subTest(loc=loc):self.assertEqual(reg[loc]['approved_cinematic_reference_uris'],[])
 def test_temporary_event_structures_not_promoted_into_parent_landmarks(self):
  locs={x['id']:x for x in json.loads((ROOT/'world/data/locations.json').read_text())['locations']}
  self.assertFalse(any('soccer stadium' in x.lower() for x in locs['LOC-RED-RUINS']['persistent_landmarks']))
  self.assertFalse(any('rodeo arena' in x.lower() for x in locs['LOC-CHILI-STABLE']['persistent_landmarks']))
  self.assertFalse(any('secret vault' in x.lower() for x in locs['LOC-TDS-WATERFALL-TEMPLE']['persistent_landmarks']))
if __name__=='__main__':unittest.main()
