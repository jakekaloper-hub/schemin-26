"""Source-exact and continuity guards for the noncanonical 2016 five-part consolidated reader.

Mechanical producer tests only. Passing does not grant independent literary,
Atlas, Character Canon, Umpire or Founder acceptance.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
READER_NAME = "READING_COPY_2016_CAUSAL_CH01_08_FIVE_PARTS_WHEEL_THAT_COULD_NOT_SIGN_NONCANON.md"
PRIOR_NAME = "READING_COPY_2016_CAUSAL_CH01_06_FOUR_PARTS_ROOF_CLOTH_GRAIN_PRINT_NONCANON.md"
NEW_NAME = "THE_WHEEL_THAT_COULD_NOT_SIGN_2016_CH07_08_INTEGRATED_NONCANON.md"
READER_SHA = "24a99b967b944bd12ecd1e452d3f4f026426af77"
PRIOR_SHA = "2448e7e1f6a03e1459bc53b0b4be0d418e1e0af7"
SOURCES = [
    ("THE_ROOF_AND_THE_UNCLAIMED_BOWL_2016_CH01_02_CONSOLIDATED_NONCANON.md", "011a098cdd760cd820e9fc818ae24097375d3c8e", 3564),
    ("THE_CLOTH_AND_THE_LOCK_2016_CH03_04_CONSOLIDATED_NONCANON.md", "ccf74ae267e3ffd9ae679c2744c11198e07b7293", 7742),
    ("THE_WEIGHT_OF_DRY_GRAIN_CHAPTER_05_NONCANON.md", "40d12860e93d9393b18d7771c427061c82e46c8c", 4733),
    ("THE_SILENCE_IN_THE_SECOND_PRINTING_CHAPTER_06_NONCANON.md", "4e3d655895847e9910b7e8c69349fb2b09c94b4b", 4303),
    ("THE_WHEEL_THAT_COULD_NOT_SIGN_2016_CH07_08_INTEGRATED_NONCANON.md", "0a1bdc02d3c0122f6deaec8b8b4422c0090ac2e1", 11131),
]
ORIGINALS = {
    "THE_YARD_WHERE_THE_WHEEL_STOOD_STILL_CHAPTER_07_NONCANON.md": "419e7f6775d0205cf1b49dba5629500245ac59a8",
    "THE_MEASURE_OF_WHAT_REMAINS_CHAPTER_08_NONCANON.md": "5266de4f74ee1b9154672acfc7c5f50dc881347c",
}
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
WRAP = re.compile(r"<!-- BEGIN 2016_CAUSAL ([^\n]+) \| git_blob ([0-9a-f]{40}) -->\n\n([\s\S]*?)\n\n<!-- END 2016_CAUSAL ([^\n]+) -->")
ROW = re.compile(r"^\| (\d+) \| `([^`]+)` \| `([0-9a-f]{40})` \| (\d+) \|$", re.M)


def blob(path):
    content = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()


class TestWheelReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reader = (BASE / READER_NAME).read_text(encoding="utf-8")
        cls.chapter = (BASE / NEW_NAME).read_text(encoding="utf-8")
        cls.wraps = WRAP.findall(cls.reader)
        cls.rows = ROW.findall(cls.reader.split("## Part 1 —", 1)[0])

    def test_01_reader_pinned_blob(self):
        self.assertEqual(blob(BASE / READER_NAME), READER_SHA)

    def test_02_earlier_reader_pinned_blob(self):
        self.assertEqual(blob(BASE / PRIOR_NAME), PRIOR_SHA)

    def test_03_five_body_wrappers_source_exact(self):
        self.assertEqual(len(self.wraps), 5)
        self.assertEqual(len(self.rows), 5)
        for index, ((name, sha, words), wrap, row) in enumerate(zip(SOURCES, self.wraps, self.rows), start=1):
            with self.subTest(index=index, name=name):
                self.assertEqual([wrap[0], wrap[1], wrap[3]], [name, sha, name])
                self.assertEqual([int(row[0]), row[1], row[2], int(row[3])], [index, name, sha, words])
                source = BASE / name
                self.assertEqual(blob(source), sha)
                self.assertEqual(wrap[2], source.read_text(encoding="utf-8").rstrip("\n"))
                self.assertEqual(len(source.read_text(encoding="utf-8").split()), words)

    def test_04_original_sources_preserved(self):
        for name, sha in ORIGINALS.items():
            with self.subTest(name=name):
                self.assertEqual(blob(BASE / name), sha)

    def test_05_word_math_and_reader_status(self):
        self.assertEqual(sum(s[2] for s in SOURCES), 31473)
        self.assertIn("Source words, including metadata: 31473", self.reader)
        self.assertIn("72-chapter manuscript remains untouched", self.reader)

    def test_06_chapter_has_eleven_numbered_movements(self):
        headings = re.findall(r"(?m)^### ([IVX]+)\. ", self.chapter)
        self.assertEqual(headings, ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI"])

    def test_07_new_evening_scene_has_material_choice(self):
        self.assertIn("### VI. A paper that must not become permission", self.chapter)
        for phrase in ["Doubtful bags isolated for examination", "Not cleared for food", "No custodian or further storage agreed", "The boards were due at dawn"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), self.chapter.lower())

    def test_08_old_printing_consequence_precedes_road(self):
        self.assertLess(self.reader.index("By noon a stranger had written"), self.reader.index("### VI. A paper that must not become permission"))
        self.assertIn("The printer's second sheet", self.chapter)

    def test_09_wheel_and_crossing_not_falsely_resolved(self):
        for phrase in ["unfinished and unturned", "lower crossing", "cart", "sacks"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), self.chapter.lower())
        self.assertNotIn("the great wheel finally turned", self.chapter.lower())

    def test_10_overnight_board_loan_repaid_next_day(self):
        self.assertLess(self.chapter.index("The boards were due at dawn"), self.chapter.index("The boards had been promised back at dawn"))
        self.assertIn("She pointed toward a rack", self.chapter)

    def test_11_new_scene_preserves_nonowner_agency(self):
        for phrase in ["The daughter checked the count", "The visitor read the amended board", "She closed the lid", "The worker nodded toward the boards"]:
            self.assertIn(phrase, self.chapter)
        self.assertNotRegex(self.chapter, r"(?m)^### (?:Edrin|Edin|Oren)\b")

    def test_12_historical_firewall(self):
        for phrase in ["historical human-owner binding unknown", "No new scores", "postseason", "secondary-world inventions"]:
            self.assertIn(phrase.lower(), self.chapter.lower())

    def test_13_release_holds(self):
        for phrase in ["NONCANON", "UMPIRE HOLD", "FOUNDER-ONLY", "NO CANON PROMOTION"]:
            self.assertIn(phrase, self.reader + "\n" + self.chapter)

    def test_14_protected_main_blobs(self):
        for name, sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(blob(ROOT / name), sha)


if __name__ == "__main__":
    unittest.main()
