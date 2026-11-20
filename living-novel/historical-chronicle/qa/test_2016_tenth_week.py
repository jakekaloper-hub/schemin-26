"""Source-pinned 2016 Week 10 Chronicle: six matchups, POV firewall and prior-canon immutability."""
from pathlib import Path
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
STORY = ROOT / "living-novel/historical-chronicle/seasons/2016/weeks/W10.md"
PREVIOUS = ROOT / "living-novel/historical-chronicle/seasons/2016/weeks/W09.md"
PIN_SRC = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PIN_PREVIOUS = "b615615d42980b32d37b8773f861ee9cba5b9505"
PROTECTED = {
 "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
 "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
 "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
 "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def blob(path):
 raw = path.read_bytes()
 return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

class WeekTen2016(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.s = STORY.read_text(encoding="utf-8")
  cls.db = json.loads(SRC.read_text(encoding="utf-8"))
  cls.rows = next(w["matchups"] for w in cls.db["weeks"] if w["week"] == 10)

 def test_source_blob_pinned(self):
  self.assertEqual(blob(SRC), PIN_SRC)
  self.assertEqual(self.db["year"], 2016)
  self.assertIn("1417621", self.db["source"])

 def test_six_distinct_fixtures(self):
  self.assertEqual(len(self.rows), 6)
  self.assertEqual(sorted(z for row in self.rows for z in (row["home_id"], row["away_id"])), list(range(1, 13)))
  self.assertEqual({row["period"] for row in self.rows}, {10})

 def test_winner_math(self):
  for row in self.rows:
   with self.subTest(row=row["home"]):
    self.assertEqual(row["winner"], "HOME" if row["hp"] > row["ap"] else "AWAY")
    self.assertGreater(abs(row["hp"]-row["ap"]),0)

 def test_exact_six_fixture_annotations(self):
  for i, row in enumerate(self.rows):
   winner = (row["home"] if row["winner"] == "HOME" else row["away"]).strip()
   line = (f"Fixture {chr(65+i)} — verified result: {row['home'].strip()} {row['hp']:.2f} — "
           f"{row['away'].strip()} {row['ap']:.2f}. Verified winner: {winner}. Margin: {abs(row['hp']-row['ap']):.2f}.")
   with self.subTest(fixture=chr(65+i)):
    self.assertIn(line, self.s)

 def test_six_distinct_roman_scenes(self):
  self.assertEqual(re.findall(r"^## (I|II|III|IV|V|VI) —", self.s, re.M), ["I","II","III","IV","V","VI"])

 def test_substantive_fiction(self):
  self.assertGreaterEqual(len(self.s.split()), 5600)
  for phrase in ("The sound of a door being carried", "What the threshold kept", "The seal with no name"):
   self.assertIn(phrase, self.s)

 def test_exclusive_pov_firewall(self):
  for phrase in ("CHAR-JAKE-KALOPER", "PRINCIPAL_CHARACTER", "sole interior viewpoint"):
   self.assertIn(phrase.lower(), self.s.lower())
  self.assertNotRegex(self.s, r"(?im)^## (Edrin|Edin|Oren)\b")
  self.assertNotIn("El Niño arrived", self.s)

 def test_owner_and_hyena_separation(self):
  for phrase in ("NOT PROVIDER-AUTHENTICATED", "ID 12", "ID 8", "real owner's motives"):
   self.assertIn(phrase.lower(), self.s.lower())

 def test_open_prior_obligations_remain_open(self):
  for phrase in ("missing claimant remains unknown", "labor credit remains disputed", "the eastern room closed",
                 "invoice remains unpaid", "No future season result"):
   self.assertIn(phrase.lower(), self.s.lower())

 def test_no_world_auto_promotion(self):
  for phrase in ("PROPOSED FICTION", "not historical Commonwealth canon", "HOLD",
                 "No canon promotion or publication"):
   self.assertIn(phrase.lower(), self.s.lower())

 def test_previous_chronicle_immutable(self):
  self.assertEqual(blob(PREVIOUS), PIN_PREVIOUS)

 def test_protected_2026_hard_canon_immutable(self):
  for name, sha in PROTECTED.items():
   with self.subTest(path=name):
    self.assertEqual(blob(ROOT / "living-novel/manuscript" / name), sha)

if __name__ == "__main__":
 unittest.main()
