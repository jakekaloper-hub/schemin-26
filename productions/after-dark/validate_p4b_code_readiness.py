#!/usr/bin/env python3
"""Code-only readiness: verify references, unresolved authority and six-page handoff."""
import json,re,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def j(p):return json.loads((R/p).read_text())
class Readiness(unittest.TestCase):
 def test_candidate_unique_in_region(self):
  cs=j('world/data/atlas_location_candidates.json')['candidates']
  x=[c for c in cs if c['id']=='CAND-AFTER-DARK-BROADCAST-HOUSE']
  self.assertEqual(len(x),1)
  self.assertIn('REG-CENTRAL-BASIN',x[0]['likely_physical_zone_ids'])
 def test_candidate_not_active(self):
  locs=j('world/data/locations.json')['locations']
  self.assertFalse(any(x['id']=='CAND-AFTER-DARK-BROADCAST-HOUSE' for x in locs))
 def test_no_unapproved_route(self):
  routes=j('world/data/routes.json')['routes']
  self.assertFalse(any('AFTER-DARK' in json.dumps(x).upper() for x in routes))
 def test_visual_identity_explicitly_candidate(self):
  s=(R/'productions/after-dark/P4A_HOST_STUDIO_CANDIDATE_HARDENING.md').read_text()
  self.assertIn('no identity or location canon mutation',s)
  self.assertIn('front/three-quarter/profile',s)
  self.assertIn('profile',s)
 def test_six_copy_packets(self):
  s=(R/'productions/after-dark/P3G_LLC_FOLIO_COPY_AND_VISUAL_PACKETS.md').read_text()
  self.assertEqual(len(re.findall(r'^## Page \d{2} — ',s,re.M)),6)
  self.assertIn('1080 × 1920',s)
 def test_previews_remain_previews(self):
  for p in range(1,7):
   self.assertTrue((R/f'productions/after-dark/previews/page-{p:02d}.png').exists())
 def test_no_false_released_novel(self):
  manifest=j('governance/publication-manifest/PUBLICATION_MANIFEST_V1.json')
  self.assertFalse(any(x['publication_id']=='memo.2026.week-07' and x['release_state']=='RELEASED' for x in manifest['publications']))
if __name__=='__main__':unittest.main(verbosity=2)
