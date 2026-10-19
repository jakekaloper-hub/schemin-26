"""Protect known unresolved visual and world-state gates, not a substitute for real approval."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SL0B_KNOWN_DEFECT_SHA='94d8b7cbf6bd001b0a41c56e7f58bea8e40ecc75571300a3965330a24f7a91da'
class ReleaseGates(unittest.TestCase):
 def test_defective_slob_candidate_must_remain_unapproved(self):
  m=json.loads((ROOT/'memo-os/week-6/WEEK_6_EXACT_PNG_INGESTION_MANIFEST.json').read_text())
  item=next(x for x in m['assets'] if x['location_id']=='LOC-SLOB-FOOTHILL-CAMP')
  reg=json.loads((ROOT/'world/location-control-plane/registries/LOCATION_REFERENCE_REGISTRY.json').read_text())
  entry=next(x for x in reg['locations'] if x['location_id']=='LOC-SLOB-FOOTHILL-CAMP')
  if item['sha256']==SL0B_KNOWN_DEFECT_SHA:
   self.assertFalse(entry['approved_cinematic_reference_uris'],'KNOWN_VEHICLE_DEFECT_CANNOT_BE_PROMOTED')
 def test_week3_world_state_must_not_be_labeled_week6_verified(self):
  j=json.loads((ROOT/'world/data/current_world_state.json').read_text())
  if j.get('as_of')=='end_of_week_3_2026':
   self.assertFalse(j.get('week_6_entry_verified',False),'UNRECONCILED_WORLD_STATE')
 def test_commissioner_creative_lock_not_final_image_approval(self):
  j=json.loads((ROOT/'memo-os/week-6/WEEK_6_EXACT_PNG_INGESTION_MANIFEST.json').read_text())
  self.assertEqual(j['commissioner_decision'],'CREATIVE_LOCK_NOT_CANONICAL_APPROVAL')
  self.assertNotEqual(j.get('canonical_approval'),'GRANTED')
if __name__=='__main__':unittest.main()
