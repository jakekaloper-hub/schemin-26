"""Survey Line development: evidence, two POVs, geography, and no deed from a score."""
import json
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"living-novel/production/full-rewrite-2026"
REG=json.loads((BASE/"R15_SURVEY_LINE_SOURCE_AND_RELEASE_REGISTER_V1.json").read_text())
TEXT=(ROOT/REG["manuscript_path"]).read_text()
LOC={x["id"]:x for x in json.loads((ROOT/"world/data/locations.json").read_text())["locations"]}
DOM={x["character_id"]:x for x in json.loads((ROOT/"world/data/owner_domains.json").read_text())["domains"]}
class SurveyLineDevelopment(unittest.TestCase):
    def test_four_scenes_two_owner_povs(self):
        self.assertEqual(re.findall(r"(?m)^\*\*POV: (CHAR-[A-Z-]+)",TEXT),[x["owner"] for x in REG["scenes"]])
        self.assertEqual(len(REG["scenes"]),4)
        self.assertEqual({x["owner"] for x in REG["scenes"]},{"CHAR-BOBBY-MITCHELL","CHAR-DAVID-BABB"})
        self.assertGreater(len(TEXT.split()),2500)
    def test_source_joined_domains_and_locations(self):
        for x in REG["scenes"]:
            self.assertEqual(LOC[x["location"]]["physical_zone_id"],x["region"])
            self.assertEqual(DOM[x["owner"]]["primary_location_id"],x["location"])
    def test_w5_certified_match_and_w4_no_misuse(self):
        fixture=REG["fixed_game"]
        self.assertEqual((fixture["week"],fixture["winner"],fixture["winner_points"],fixture["loser"],fixture["loser_points"]),(5,"The LLC",193.73,"Mud Dogs",127.09))
        self.assertIn("193.73",TEXT)
        self.assertIn("127.09",TEXT)
        self.assertNotIn("157.33",TEXT)
        self.assertNotIn("184.91",TEXT)
    def test_no_automatic_title_construction_or_new_chapter(self):
        self.assertEqual(REG["status"],"NONCANON_DEVELOPMENT_NOT_PUBLICATION_ELIGIBLE")
        self.assertEqual(REG["promotion"],"HOLD")
        self.assertIn("No land transferred",TEXT)
        self.assertIn("No construction order",TEXT)
        self.assertIn("not a right",TEXT.lower())
        self.assertNotRegex(TEXT,re.compile(r"\bEdrin(?: Vale)?\b|\bEdin\b",re.I))
    def test_negative_site_swap(self):
        mud=REG["scenes"][0]
        self.assertNotEqual(LOC["LOC-LLC-BOARDROOM"]["physical_zone_id"],mud["region"])
        self.assertNotEqual(DOM["CHAR-DAVID-BABB"]["primary_location_id"],mud["location"])
if __name__=="__main__":
    unittest.main()
