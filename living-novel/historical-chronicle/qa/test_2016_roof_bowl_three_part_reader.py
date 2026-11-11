"""2016 developmental I–IV three-part compression integrity. Mechanical checks only; no canon approval."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = BASE / "THE_ROOF_AND_THE_UNCLAIMED_BOWL_2016_CH01_02_CONSOLIDATED_NONCANON.md"
READER = BASE / "READING_COPY_2016_CAUSAL_CH01_04_THREE_PARTS_ROOF_AND_BOWL_CONSOLIDATION_NONCANON.md"
PRIOR = BASE / "READING_COPY_CAUSAL_CHAPTERS_01_04_NONCANON.md"
CHAPTER_SHA = "011a098cdd760cd820e9fc818ae24097375d3c8e"
READER_SHA = "f1b85135caa3c06a8d26424a8bc7705578a5157d"
PRIOR_SHA = "ea0793584fa21cadee27200373dc881582d2bee6"
SOURCES = [
    (CHAPTER.name, CHAPTER_SHA, 3564),
    ("THE_WORK_OF_UNTURNED_THINGS_CHAPTER_03_NONCANON.md", "f9bf0721c989d30bfd09189388b93293ba3a8ce0", 4495),
    ("WHAT_THE_WALL_KEPT_CHAPTER_04_NONCANON.md", "8994f9e443a6313dee217dfd5f92aedeff7bd88c", 3977),
]
WRAP = re.compile(
    r"<!-- BEGIN 2016_CAUSAL ([^\n]+?) \| git_blob ([0-9a-f]{40}) -->\n\n"
    r"([\s\S]*?)\n\n<!-- END 2016_CAUSAL ([^\n]+?) -->"
)
ROW = re.compile(r"^\| (\d+) \| `([^`]+)` \| `([0-9a-f]{40})` \| (\d+) \|$", re.M)
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

class RoofAndBowlPilot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = CHAPTER.read_text(encoding="utf-8")
        cls.reader = READER.read_text(encoding="utf-8")
        cls.wraps = WRAP.findall(cls.reader)
        cls.rows = ROW.findall(cls.reader.split("## Part 1 —", 1)[0])

    def test_01_new_source_blob(self):
        self.assertEqual(blob(CHAPTER), CHAPTER_SHA)

    def test_02_new_reader_blob(self):
        self.assertEqual(blob(READER), READER_SHA)

    def test_03_original_full_four_source_reader_unchanged(self):
        self.assertEqual(blob(PRIOR), PRIOR_SHA)

    def test_04_manifest_has_three_parts_and_unique_sources(self):
        self.assertEqual(len(self.rows), 3)
        self.assertEqual(len(self.wraps), 3)
        self.assertEqual([int(x[0]) for x in self.rows], [1, 2, 3])
        self.assertEqual(len(set(x[1] for x in self.rows)), 3)

    def test_05_all_three_sources_byte_exact_with_git_pins(self):
        for row, wrap, (_, expected_sha, expected_words) in zip(self.rows, self.wraps, SOURCES):
            part, name, sha, count = row
            source = BASE / name
            with self.subTest(source=name):
                self.assertEqual(wrap[0], name)
                self.assertEqual(wrap[3], name)
                self.assertEqual(wrap[1], sha)
                self.assertEqual(sha, expected_sha)
                self.assertEqual(blob(source), sha)
                self.assertEqual(wrap[2], source.read_text(encoding="utf-8").rstrip("\n"))
                self.assertEqual(int(count), expected_words)
                self.assertEqual(len(source.read_text(encoding="utf-8").split()), expected_words)

    def test_06_compression_arithmetic(self):
        self.assertEqual(sum(x[2] for x in SOURCES), 12036)
        self.assertEqual(4166 + 4108 + 4495 + 3977, 16746)
        self.assertEqual(16746-12036, 4710)
        self.assertIn("source words including metadata: 12036", self.reader)

    def test_07_four_movements_one_principal_pov(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\. ", self.chapter, re.M)), 4)
        self.assertIn("CHAR-JAKE-KALOPER exclusively", self.chapter)
        self.assertNotIn("### I. The latch", self.chapter)

    def test_08_canvas_and_outstanding_debt_state(self):
        for token in ["three nights", "twelve borrowers", "two choose other exits",
                      "missing claimant remains UNKNOWN", "east room remains closed",
                      "rejected fittings", "private file"]:
            self.assertIn(token.lower(), self.chapter.lower())

    def test_09_source_identity_and_pov_gates(self):
        for token in ["NONCANON", "HUMAN OWNER-ID UNKNOWN",
                      "No new scoring line", "not independently authenticated"]:
            self.assertIn(token.lower(), (self.reader + self.chapter).lower())
        self.assertNotRegex(self.chapter, r"\b(?:Edrin|Edin|Master Oren)\b")

    def test_10_no_false_full_2016_compliance(self):
        self.assertIn("NOT a reconstruction of the separate 72-chapter full historical reader", self.reader)
        self.assertIn("does not establish 12 historical 2016 owner POVs", self.reader)
        self.assertIn("NO CANON/PUBLICATION/MERGE", self.reader)

    def test_11_new_chapter_leads_to_return_due(self):
        self.assertIn("the loan ends on the third morning", self.chapter.lower())
        self.assertIn("the third morning", self.reader.lower())
        self.assertIn("The Work of Unturned Things", self.reader)

    def test_12_2016_original_sources_referenced_not_overwritten(self):
        self.assertIn("d93505009d7dda7acc010ce1a6e5ec2bacf65ec2", self.chapter)
        self.assertIn("756126cb4e151a0bd78ece39ab59a4c54ef2aa43", self.chapter)

    def test_13_protected_2026_main_blobs(self):
        for rel, expected in PROTECTED.items():
            with self.subTest(rel=rel):
                self.assertEqual(blob(ROOT / rel), expected)

    def test_14_independent_release_hold(self):
        for token in ["INDEPENDENT AUTHORS COUNCIL", "UMPIRE HOLD",
                      "FOUNDER-ONLY CANON", "NONCANON"]:
            self.assertIn(token, self.chapter)

if __name__ == "__main__":
    unittest.main()
