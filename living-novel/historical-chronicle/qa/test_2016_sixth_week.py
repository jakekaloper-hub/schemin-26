"""2016 W06 archive/result, bounded fiction, protected canon and continuity tests."""
from pathlib import Path
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
W06 = ROOT / "living-novel/historical-chronicle/seasons/2016/weeks/W06.md"
W05 = ROOT / "living-novel/historical-chronicle/seasons/2016/weeks/W05.md"
PINNED_SRC = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PINNED_W05 = "bab0fe58cd46e77950d59fe0359a92efb78bd1ae"
PROTECTED = {
    "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def blob(p):
    raw = p.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

class WeekSix2016(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prose = W06.read_text(encoding="utf-8")
        cls.data = json.loads(SRC.read_text(encoding="utf-8"))
        cls.rows = next(x["matchups"] for x in cls.data["weeks"] if x["week"] == 6)

    def test_source_blob_and_year(self):
        self.assertEqual(blob(SRC), PINNED_SRC)
        self.assertEqual(self.data["year"], 2016)
        self.assertIn("1417621", self.data["source"])

    def test_all_twelve_team_ids_once(self):
        self.assertEqual(len(self.rows), 6)
        self.assertEqual([x["period"] for x in self.rows], [6]*6)
        self.assertEqual(sorted(z for x in self.rows for z in (x["home_id"],x["away_id"])), list(range(1,13)))

    def test_winner_consistency(self):
        for row in self.rows:
            with self.subTest(row=row["home"]):
                self.assertEqual(row["winner"], "HOME" if row["hp"] > row["ap"] else "AWAY")

    def test_six_source_exact_fixture_lines(self):
        for i,r in enumerate(self.rows):
            winner = (r["home"] if r["winner"]=="HOME" else r["away"]).strip()
            s = (f"Fixture {chr(65+i)} — verified result: {r['home'].strip()} {r['hp']:.2f} — "
                 f"{r['away'].strip()} {r['ap']:.2f}. Verified winner: {winner}. "
                 f"Margin: {abs(r['hp']-r['ap']):.2f}.")
            with self.subTest(scene=i):
                self.assertIn(s, self.prose)

    def test_six_drama_sections(self):
        self.assertEqual(re.findall(r"^## (I|II|III|IV|V|VI) —",self.prose,re.M),
                         ["I","II","III","IV","V","VI"])

    def test_substantial_fiction(self):
        self.assertGreaterEqual(len(self.prose.split()), 4400)
        self.assertIn("The length of a doorway", self.prose)
        self.assertIn("The entry the building could not keep", self.prose)

    def test_singular_eligible_pov(self):
        self.assertIn("CHAR-JAKE-KALOPER", self.prose)
        self.assertIn("PRINCIPAL_CHARACTER", self.prose)
        self.assertIn("sole interior viewpoint", self.prose)
        self.assertNotRegex(self.prose, r"(?im)^## (Edrin|Edin|Oren)\\b")

    def test_owner_and_atlas_not_authenticated(self):
        for token in ("NOT PROVIDER-AUTHENTICATED", "PROPOSED FICTION",
                      "not a fresh authenticated upstream snapshot", "historical Commonwealth canon"):
            self.assertIn(token.lower(), self.prose.lower())

    def test_hyena_team_ids_not_conflated(self):
        self.assertIn("scoring slot **12**", self.prose)
        self.assertIn("scoring slot **8**", self.prose)

    def test_continuity_no_free_resolution(self):
        for token in ("missing claimant remains UNKNOWN", "invoice remains unpaid",
                      "paper seal", "reinspection", "labor credit remains unverified",
                      "No subsequent scores, trades, playoff outcomes"):
            self.assertIn(token.lower(),self.prose.lower())

    def test_week_five_unchanged(self):
        self.assertEqual(blob(W05),PINNED_W05)

    def test_protected_hard_canon_unchanged(self):
        for name,sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(blob(ROOT/"living-novel/manuscript"/name),sha)

    def test_approval_holds(self):
        self.assertIn("No canon promotion or publication",self.prose)
        self.assertIn("NOT RECEIVED",self.prose)
        self.assertIn("HOLD",self.prose)

if __name__=="__main__":
    unittest.main()
