import unittest,copy,json,tempfile
from pathlib import Path
from ScheminBridge.build_world_manifest import build,SNAPSHOT
class WorldManifestTests(unittest.TestCase):
 def test_full_atlas(self):
  x=build();self.assertEqual(len(x["locations"]),23);self.assertEqual(len(x["regions"]),7)
 def test_no_character_instantiation(self):
  self.assertTrue(all(x["characters_allowed"] is False for x in build()["locations"]))
 def test_statuses_remain_distinct(self):
  x=build()["locations"];self.assertEqual(sum(i["render_classification"]=="CANON_SOURCE_PREVIEW" for i in x),8)
 def test_mutated_snapshot_blocked(self):
  with tempfile.TemporaryDirectory() as t:
   d=json.loads(SNAPSHOT.read_text());d["locations"][0]["name"]="False"
   p=Path(t)/"modified.json";p.write_text(json.dumps(d))
   with self.assertRaises(ValueError):build(p)
