"""Evidence-only per-owner crop x six host environment bridge; not model reference attachment."""
import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HOMES={
'LOC-RED-RUINS':'CHAR-KEVIN-ZEEK',
'LOC-COUNTRY-CLUB-JACKSON':'CHAR-ZACH-WILSON',
'LOC-SLOB-FOOTHILL-CAMP':'CHAR-JORDAN-HOLLINGSHEAD',
'LOC-CHILI-STABLE':'CHAR-BRANDON-PRYOR',
'LOC-MUD-DOGS-SWAMP':'CHAR-BOBBY-MITCHELL',
'LOC-TDS-WATERFALL-TEMPLE':'CHAR-PHILLIP-PITTS'}
class MergedAuthorityIntegration(unittest.TestCase):
 def test_exact_six_home_owner_reference_crops(self):
  lineup=json.loads((ROOT/'canon/characters/APPROVED_LINEUP_2026_10_18.json').read_text())
  self.assertEqual(len(lineup['individuals']),12)
  refs={i['character_id']:i for i in lineup['individuals']}
  assets=json.loads((ROOT/'memo-os/week-6/WEEK_6_EXACT_PNG_INGESTION_MANIFEST.json').read_text())
  locs={a['location_id']:a for a in assets['assets']}
  self.assertEqual(set(HOMES),set(locs))
  for loc,owner in HOMES.items():
   with self.subTest(location=loc):
    a=locs[loc];c=refs[owner]
    self.assertEqual(hashlib.sha256((ROOT/a['candidate_uri']).read_bytes()).hexdigest(),a['sha256'])
    self.assertEqual(hashlib.sha256((ROOT/c['crop']).read_bytes()).hexdigest(),c['crop_sha256'])
    self.assertNotEqual(a['sha256'],c['crop_sha256'])
 def test_lineup_is_not_native_render_acceptance(self):
  lineup=json.loads((ROOT/'canon/characters/APPROVED_LINEUP_2026_10_18.json').read_text())
  self.assertIn('HOLD',lineup['status'])
  self.assertIn('AI provider attachment or generated-character QA',lineup['does_not_approve'])
if __name__=='__main__':unittest.main()
