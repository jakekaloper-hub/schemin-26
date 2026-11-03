"""2016 developmental first-five causal chapter consolidation: mechanistic source/POV/release checks only.
Not an independent literary, Character Canon, Atlas, ESPN ownership or Umpire approval.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = BASE / "THE_CLOTH_AND_THE_LOCK_2016_CH03_04_CONSOLIDATED_NONCANON.md"
READER = BASE / "READING_COPY_2016_CAUSAL_CH01_05_THREE_PARTS_ROOF_CLOTH_GRAIN_NONCANON.md"
PRIOR = BASE / "READING_COPY_2016_CAUSAL_CH01_04_THREE_PARTS_ROOF_AND_BOWL_CONSOLIDATION_NONCANON.md"
ORIGINALS = [
    ("THE_WORK_OF_UNTURNED_THINGS_CHAPTER_03_NONCANON.md", "f9bf0721c989d30bfd09189388b93293ba3a8ce0"),
    ("WHAT_THE_WALL_KEPT_CHAPTER_04_NONCANON.md", "8994f9e443a6313dee217dfd5f92aedeff7bd88c"),
]
SOURCES = [
    ("THE_ROOF_AND_THE_UNCLAIMED_BOWL_2016_CH01_02_CONSOLIDATED_NONCANON.md", "011a098cdd760cd820e9fc818ae24097375d3c8e", 3564),
    (CHAPTER.name, "ccf74ae267e3ffd9ae679c2744c11198e07b7293", 7742),
    ("THE_WEIGHT_OF_DRY_GRAIN_CHAPTER_05_NONCANON.md", "40d12860e93d9393b18d7771c427061c82e46c8c", 4733),
]
READER_BLOB = "09d5ddd8980cdb12c5641d96914771a10e890477"
PRIOR_BLOB = "f1b85135caa3c06a8d26424a8bc7705578a5157d"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
WRAP = re.compile(
    r"<!-- BEGIN 2016_CAUSAL ([^\n]+?) \| git_blob ([0-9a-f]{40}) -->\n\n"
    r"([\s\S]*?)\n\n<!-- END 2016_CAUSAL ([^\n]+?) -->"
)
ROW = re.compile(r"^\| (\d+) \| `([^`]+)` \| `([0-9a-f]{40})` \| (\d+) \|$", re.M)

def blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

class ClothLockFiveChapterPilot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = CHAPTER.read_text(encoding="utf-8")
        cls.reader = READER.read_text(encoding="utf-8")
        cls.wraps = WRAP.findall(cls.reader)
        cls.rows = ROW.findall(cls.reader.split("## Part 1 —", 1)[0])

    def test_01_new_chapter_blob(self):
        self.assertEqual(blob(CHAPTER), SOURCES[1][1])

    def test_02_new_compiled_reader_blob(self):
        self.assertEqual(blob(READER), READER_BLOB)

    def test_03_prior_three_part_reader_untouched(self):
        self.assertEqual(blob(PRIOR), PRIOR_BLOB)

    def test_04_original_chapters_three_four_untouched(self):
        for name, sha in ORIGINALS:
            with self.subTest(name=name):
                self.assertEqual(blob(BASE / name), sha)

    def test_05_exactly_three_unique_manifest_parts(self):
        self.assertEqual([int(row[0]) for row in self.rows], [1, 2, 3])
        self.assertEqual(len(self.wraps), 3)
        self.assertEqual(len(set(row[1] for row in self.rows)), 3)

    def test_06_all_wrapped_bodies_are_exact_source_files(self):
        for row, wrap, (name, sha, words) in zip(self.rows, self.wraps, SOURCES):
            with self.subTest(name=name):
                self.assertEqual(row[1], name)
                self.assertEqual(row[2], sha)
                self.assertEqual(int(row[3]), words)
                self.assertEqual(wrap[0], name)
                self.assertEqual(wrap[1], sha)
                self.assertEqual(wrap[3], name)
                self.assertEqual(blob(BASE / name), sha)
                self.assertEqual(wrap[2], (BASE / name).read_text(encoding="utf-8").rstrip("\n"))
                self.assertEqual(len((BASE / name).read_text(encoding="utf-8").split()), words)

    def test_07_source_word_arithmetic_and_editorial_reduction(self):
        self.assertEqual(sum(s[2] for s in SOURCES), 16039)
        self.assertEqual(4166 + 4108 + 4495 + 3977 + 4733, 21479)
        self.assertEqual(21479 - 16039, 5440)
        self.assertIn("16039 source words", self.reader)
        self.assertIn("editorial reduction: 5440", self.reader)

    def test_08_nine_causes_one_jake_principal_pov(self):
        labels = re.findall(r"^### ([IVX]+)\. ", self.chapter, re.M)
        self.assertEqual(labels, ["I","II","III","IV","V","VI","VII","VIII","IX"])
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertNotRegex(self.chapter, r"\b(?:Edrin|Edin|Master Oren)\b")

    def test_09_new_bridge_has_irreducible_material_action(self):
        for phrase in ["The work at the empty place", "long bench",
                       "patched heel", "The debt doesn't vanish", "three nights"]:
            self.assertIn(phrase.lower(), self.chapter.lower())

    def test_10_canvas_return_and_market_awning_separate(self):
        for phrase in ["The canvas owner had brought the cart himself",
                       "small market awning", "canvas had been returned"]:
            self.assertIn(phrase.lower(), self.chapter.lower())

    def test_11_chest_owner_not_missing_claimant_and_no_unbuilt_frame_fantasy(self):
        for phrase in ["the chest", "reaching frame", "unfinished plan",
                       "missing claimant"]:
            self.assertIn(phrase.lower(), self.chapter.lower())
        self.assertIn("frame UNBUILT", self.chapter)

    def test_12_wheel_stop_and_old_wages_unsettled(self):
        self.assertIn("The wheel remained still", self.chapter)
        self.assertIn("old wage claim", self.chapter)
        self.assertIn("two mornings", self.chapter)

    def test_13_chapter_five_story_state_supported(self):
        for phrase in ["Grain is not certified safe", "a different small market awning",
                       "suspect grain", "The Weight of Dry Grain"]:
            self.assertIn(phrase.lower(), self.chapter.lower() + self.reader.lower())

    def test_14_no_false_historical_owner_joins(self):
        for phrase in ["HISTORICAL HUMAN-MANAGER OWNERSHIP UNKNOWN",
                       "not biographical history", "2016 ESPN/Flaim"]:
            self.assertIn(phrase.lower(), self.chapter.lower())
        self.assertIn("two different Austin-named", self.reader)

    def test_15_protected_2026_hardcanon_identical_blob(self):
        for rel, expected in PROTECTED.items():
            with self.subTest(rel=rel):
                self.assertEqual(blob(ROOT / rel), expected)

    def test_16_noncanon_review_and_publication_holds(self):
        for phrase in ["NONCANON", "INDEPENDENT AUTHORS COUNCIL",
                       "UMPIRE HOLD", "FOUNDER-ONLY CANON"]:
            self.assertIn(phrase, self.chapter)
        self.assertIn("NO CANON PROMOTION", self.reader)
        self.assertIn("not an accepted 2016 season novel", self.reader)

if __name__ == "__main__":
    unittest.main()
