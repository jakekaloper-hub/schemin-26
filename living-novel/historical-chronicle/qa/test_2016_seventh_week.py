"""Source-exact 2016 Week 7 score, POV, prior text and release holds."""
from pathlib import Path
import hashlib
import json
import re
import unittest

ROOT=Path(__file__).resolve().parents[3]
SRC=ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
STORY=ROOT/"living-novel/historical-chronicle/seasons/2016/weeks/W07.md"
PREVIOUS=ROOT/"living-novel/historical-chronicle/seasons/2016/weeks/W06.md"
PIN_SRC="6dbec1fe2537139f3a97c6a78250e2bae082a518"
PIN_PREVIOUS="6d16b7aca6b337c54d5e96f2f6849b0e6c48bd83"
PROTECTED={
 "PROLOGUE_DRAFT_V1.md":"5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
 "CHAPTER_01_THE_FIRST_ANSWER.md":"26a17f05eb0565e7648c29add03ee9580ec933c3",
 "CHAPTER_02_WHAT_COMES_BACK.md":"30fcf23a3eb8872fa0fb4dff029fe30044141121",
 "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md":"49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
def blob(p):
 raw=p.read_bytes()
 return hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\0"+raw).hexdigest()
class WeekSeven2016(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.s=STORY.read_text(encoding="utf-8")
  cls.db=json.loads(SRC.read_text(encoding="utf-8"))
  cls.rows=next(x["matchups"] for x in cls.db["weeks"] if x["week"]==7)
 def test_source_pinned(self):
  self.assertEqual(blob(SRC),PIN_SRC)
  self.assertEqual(self.db["year"],2016)
  self.assertIn("1417621",self.db["source"])
 def test_six_pairings_twelve_team_ids(self):
  self.assertEqual(len(self.rows),6)
  self.assertEqual(sorted(z for r in self.rows for z in (r["home_id"],r["away_id"])),list(range(1,13)))
  self.assertEqual({r["period"] for r in self.rows},{7})
 def test_winners_and_scores_math(self):
  for r in self.rows:
   self.assertEqual(r["winner"],"HOME" if r["hp"]>r["ap"] else "AWAY")
 def test_six_exact_result_headers(self):
  for i,r in enumerate(self.rows):
   win=(r["home"] if r["winner"]=="HOME" else r["away"]).strip()
   line=(f"Fixture {chr(65+i)} — verified result: {r['home'].strip()} {r['hp']:.2f} — "
         f"{r['away'].strip()} {r['ap']:.2f}. Verified winner: {win}. Margin: {abs(r['hp']-r['ap']):.2f}.")
   with self.subTest(i=i): self.assertIn(line,self.s)
 def test_six_drama_moves(self):
  self.assertEqual(re.findall(r"^## (I|II|III|IV|V|VI) —",self.s,re.M),["I","II","III","IV","V","VI"])
 def test_fiction_substance(self):
  self.assertGreaterEqual(len(self.s.split()),4800)
  self.assertIn("The underside of a borrowed sky",self.s)
  self.assertIn("A roof that could be folded away",self.s)
 def test_single_permitted_pov(self):
  for t in ("CHAR-JAKE-KALOPER","PRINCIPAL_CHARACTER","sole interior viewpoint"):
   self.assertIn(t,self.s)
  self.assertNotRegex(self.s,r"(?im)^## (Edrin|Edin|Oren)\\b")
 def test_identity_unknown_and_distinct_hyenas(self):
  for t in ("NOT PROVIDER-AUTHENTICATED","ID 12","ID 8","real owner's motives"):
   self.assertIn(t.lower(),self.s.lower())
 def test_prior_continuity_open(self):
  for t in ("missing claimant","old unverified labor credit","roof remains closed",
            "invoice remains unpaid","No future scores, trades"):
   self.assertIn(t.lower(),self.s.lower())
 def test_prev_manuscript_byte_immutable(self):
  self.assertEqual(blob(PREVIOUS),PIN_PREVIOUS)
 def test_protected_2026_canon_immutable(self):
  for name,sha in PROTECTED.items():
   with self.subTest(name=name):self.assertEqual(blob(ROOT/"living-novel/manuscript"/name),sha)
 def test_no_promotion(self):
  for t in ("PROPOSED FICTION","historical Commonwealth canon","NOT RECEIVED","No canon promotion or publication"):
   self.assertIn(t.lower(),self.s.lower())
if __name__=="__main__":
 unittest.main()
