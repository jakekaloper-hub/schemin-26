import unittest, tempfile, json
from pathlib import Path
from ScheminBridge.export_location import export_location, SNAPSHOT
class ExportTests(unittest.TestCase):
 def test_real_canonical_location(self):
  data=export_location("LOC-TRADE-JEDI-MOUNTAIN-BASE")
  self.assertEqual(data["source_location"]["name"],"Trade Jedi Mountain Base")
  self.assertEqual(data["source_location"]["coordinate_space"],"schemin-local-v1 (abstract, non-metric)")
  self.assertEqual(data["characters"],[])
  self.assertEqual(data["status"],"PREVIEW")
 def test_unknown_location_rejected(self):
  with self.assertRaises(ValueError):export_location("LOC-NOT-REAL")
 def test_provisional_location_rejected(self):
  with self.assertRaises(ValueError):export_location("LOC-STORM-BOWL")
 def test_bad_coordinate_space_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   d=json.loads(SNAPSHOT.read_text());d["coordinate_space"]="meters"
   p=Path(td)/"bad.json";p.write_text(json.dumps(d))
   with self.assertRaises(ValueError):export_location("LOC-TRADE-JEDI-MOUNTAIN-BASE",p)
if __name__=="__main__":unittest.main()
