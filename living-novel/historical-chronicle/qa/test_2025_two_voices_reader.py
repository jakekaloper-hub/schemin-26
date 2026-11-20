"""2025 source-exact two-voice historical reader QA. Technical integrity, NOT independent editorial acceptance."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2025/causal-novel"
AUSTIN = BASE / "THE_NARROWEST_DOOR_AUSTIN_2025_NONCANON.md"
JAKE = ROOT / "living-novel/production/historical-saga/R53/HISTORICAL_2025_OBIWAN_NONCANON_PILOT.md"
READER = BASE / "READING_COPY_2025_TWO_VOICES_NONCANON.md"
READER_SHA = "3d82eb3a17c23154bee5c6fd4bde601c19fd372b"
AUSTIN_SHA = "ae5d50aca6c1ac4da20fb8ead28554baa5e70613"
JAKE_SHA = "9737fa9b9832de847ee504ed9b87d5e2c404e481"
PREVIOUS_2016_READER = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel/READING_COPY_CAUSAL_CHAPTERS_01_72_NONCANON.md"
PREVIOUS_2016_READER_SHA = "8f1dda21ac4962143ba3291cef4d60769197d62f"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
WRAPPER = re.compile(
    r"<!-- BEGIN 2025_VOICE ([^\n]+) \| git_blob ([0-9a-f]{40}) -->\n\n"
    r"([\s\S]*?)\n\n<!-- END 2025_VOICE ([^\n]+) -->"
)
MANIFEST = re.compile(
    r"^\| ([12]) \| ([^|]+) \| \x60([^\n]+?)\x60 \| \x60([0-9a-f]{40})\x60 \| (\d+) \|$", re.M
)

def git_blob(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

class TwoVoices2025SourceReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.austin = AUSTIN.read_text(encoding="utf-8")
        cls.jake = JAKE.read_text(encoding="utf-8")
        cls.reader = READER.read_text(encoding="utf-8")
        cls.wrappers = list(WRAPPER.finditer(cls.reader))
        cls.rows = list(MANIFEST.finditer(cls.reader))

    def test_01_austin_exact_source_blob(self):
        self.assertEqual(git_blob(AUSTIN), AUSTIN_SHA)

    def test_02_prior_jake_source_blob_preserved(self):
        self.assertEqual(git_blob(JAKE), JAKE_SHA)

    def test_03_assembled_reader_blob(self):
        self.assertEqual(git_blob(READER), READER_SHA)

    def test_04_two_wrappers(self):
        self.assertEqual(len(self.wrappers), 2)

    def test_05_two_manifest_rows(self):
        self.assertEqual(len(self.rows), 2)

    def test_06_distinct_canonical_owner_povs(self):
        self.assertIn("Austin / CHAR-AUSTIN-BYARS", self.reader)
        self.assertIn("Jake / CHAR-JAKE-KALOPER", self.reader)
        self.assertNotIn("Edrin as narrator", self.reader)

    def test_07_source_exactness_each_wrapper(self):
        for index, src in enumerate((AUSTIN, JAKE)):
            with self.subTest(source=src.name):
                name, sha, body, end = self.wrappers[index].groups()
                self.assertEqual(name, src.name)
                self.assertEqual(end, src.name)
                self.assertEqual(sha, git_blob(src))
                self.assertEqual(body.strip("\n"), src.read_text(encoding="utf-8").rstrip("\n"))

    def test_08_manifest_order_and_sha_and_wordcount(self):
        for index, src in enumerate((AUSTIN, JAKE)):
            with self.subTest(source=src.name):
                row = self.rows[index]
                self.assertEqual(int(row.group(1)), index + 1)
                self.assertEqual(row.group(4), git_blob(src))
                self.assertEqual(int(row.group(5)), len(src.read_text(encoding="utf-8").split()))
                self.assertTrue(row.group(3).endswith(src.name))

    def test_09_austin_substantive_words(self):
        self.assertEqual(len(self.austin.split()), 5001)

    def test_10_six_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\. ", self.austin, re.M)), 6)

    def test_11_championship_score_factual_anchor(self):
        self.assertIn("161.07–109.56", self.austin)
        self.assertIn("161.07–109.56", self.reader)
        self.assertIn("152.20–151.80", self.austin)
        self.assertIn("152.20–151.80", self.reader)

    def test_12_no_false_historical_ownership_claim(self):
        for phrase in ("ownerName=null", "not independently authenticated"):
            self.assertIn(phrase, self.austin)

    def test_13_no_canon_promotion(self):
        for phrase in ("DRAFT / NONCANON", "INDEPENDENT EDITORIAL HOLD", "FOUNDER ACCEPTANCE HOLD"):
            self.assertIn(phrase, self.austin)
            self.assertIn(phrase, self.reader)

    def test_14_no_territorial_claim_by_belt(self):
        self.assertIn("not a crown, kingdom, land title", self.austin)
        self.assertIn("no universal sovereignty", self.reader)

    def test_15_no_institutional_or_supporting_pov(self):
        narrative = self.austin.split("\n---\n\n### Source and narrative handoff")[0]
        self.assertIsNone(re.search(r"\b(?:Edrin|Edin|Master Oren)\b", narrative, re.I))
        self.assertIn("sole canonical-owner interior", self.austin)

    def test_16_protected_2026_hard_manuscript_unchanged(self):
        for rel, expected in PROTECTED.items():
            with self.subTest(rel=rel):
                self.assertEqual(git_blob(ROOT / rel), expected)

    def test_17_2016_seventy_two_reader_unchanged(self):
        self.assertEqual(git_blob(PREVIOUS_2016_READER), PREVIOUS_2016_READER_SHA)

    def test_18_previous_2025_jake_pilot_not_rewritten(self):
        self.assertTrue(self.jake.startswith("# THE YEAR THAT RETURNED THE QUESTION"))
        self.assertTrue(self.jake.rstrip().endswith("This time he did not turn it over."))

    def test_19_closed_reader_marker(self):
        self.assertTrue(self.reader.rstrip().endswith("<!-- END_2025_TWO_VOICES_NONCANON -->"))

    def test_20_review_obligations_explicit(self):
        for phrase in ("independent Umpire", "2025 Atlas geography", "independent reconciliation"):
            self.assertIn(phrase, self.reader)

if __name__ == "__main__":
    unittest.main()
