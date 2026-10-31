"""2016 Week 12 noncanon Chronicle — archived outcomes, continuity and protected hard canon."""
from pathlib import Path
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
STORY = ROOT / "living-novel/historical-chronicle/seasons/2016/weeks/W12.md"
PREVIOUS = ROOT / "living-novel/historical-chronicle/seasons/2016/weeks/W11.md"
SOURCE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PREVIOUS_SHA = "7b7c53091e1dec4c253b271677468b8256bb8f75"
PROTECTED = {
 "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
 "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
 "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
 "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

class WeekTwelve2016(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.story = STORY.read_text(encoding="utf-8")
        cls.archive = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.rows = next(w["matchups"] for w in cls.archive["weeks"] if w["week"] == 12)

    def test_source_sha_and_origin(self):
        self.assertEqual(blob(SOURCE), SOURCE_SHA)
        self.assertEqual(self.archive["year"], 2016)
        self.assertIn("1417621", self.archive["source"])

    def test_exactly_six_distinct_fixtures(self):
        self.assertEqual(len(self.rows), 6)
        self.assertEqual(sorted(n for row in self.rows for n in (row["home_id"], row["away_id"])), list(range(1,13)))
        self.assertEqual({row["period"] for row in self.rows}, {12})

    def test_winner_math(self):
        for row in self.rows:
            with self.subTest(home=row["home"]):
                self.assertEqual(row["winner"], "HOME" if row["hp"] > row["ap"] else "AWAY")

    def test_source_exact_six_annotated_fixtures(self):
        annotations = re.findall(r"^\*Fixture ([A-F]) — archived result: (.+)\*$",self.story,re.M)
        self.assertEqual([n for n,_ in annotations], list("ABCDEF"))
        for i,row in enumerate(self.rows):
            winner = row["home"] if row["winner"] == "HOME" else row["away"]
            phrase = (f"{row['home'].strip()} (ID {row['home_id']}) {row['hp']:.2f} — "
                      f"{row['away'].strip()} (ID {row['away_id']}) {row['ap']:.2f}. "
                      f"Winner: {winner.strip()} (ID {row['home_id'] if row['winner']=='HOME' else row['away_id']}). "
                      f"Margin: {abs(row['hp']-row['ap']):.2f}.")
            with self.subTest(fixture=i+1):
                self.assertEqual(annotations[i][1],phrase)

    def test_six_scenes_not_six_chapters(self):
        self.assertEqual(re.findall(r"^## (I|II|III|IV|V|VI) —",self.story,re.M),["I","II","III","IV","V","VI"])
        self.assertNotRegex(self.story,r"(?m)^# Chapter [IVX]")

    def test_substantive_original_fiction(self):
        self.assertGreaterEqual(len(self.story.split()),5000)
        for line in ("An inventory of departures","The girl's","A victory that purchased nothing","The record that stayed open"):
            self.assertIn(line.lower(),self.story.lower())

    def test_exclusive_owner_principal_pov(self):
        for text in ("CHAR-JAKE-KALOPER","PRINCIPAL_CHARACTER","only interior","twelve"):
            self.assertIn(text.lower(),self.story.lower())
        self.assertNotRegex(self.story,r"(?im)^## (Edrin|Edin|Oren)\b")

    def test_historical_identity_firewall(self):
        for text in ("NOT PROVIDER-AUTHENTICATED","ID 12","ID 8","not a newly authenticated"):
            self.assertIn(text.lower(),self.story.lower())

    def test_continuity_holds_not_fabricated_resolution(self):
        for text in ("unopened and undelivered","remained unpaid","cordon","unturned wheel",
                     "found key", "old timber claim", "not been built"):
            self.assertIn(text.lower(),self.story.lower())

    def test_no_atlas_or_canon_promotion(self):
        for text in ("FICTION ONLY","NONCANON","Atlas","HOLD","canon promotion"):
            self.assertIn(text.lower(),self.story.lower())

    def test_previous_story_byte_unchanged(self):
        self.assertEqual(blob(PREVIOUS), PREVIOUS_SHA)

    def test_four_protected_main_sources_unchanged(self):
        for name, sha in PROTECTED.items():
            with self.subTest(path=name):
                self.assertEqual(blob(ROOT / "living-novel/manuscript" / name),sha)

if __name__ == "__main__":
    unittest.main()
