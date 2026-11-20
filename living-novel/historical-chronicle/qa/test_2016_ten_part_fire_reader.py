"""Ten-part 2016 reader—source exact through the mill-fire consequence (noncanon)."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
TEN = BASE / "READING_COPY_2016_CAUSAL_CH01_13_TEN_PARTS_FIRE_AND_UNSETTLED_WORK_NONCANON.md"
NINE = BASE / "READING_COPY_2016_CAUSAL_CH01_12_NINE_PARTS_VOICE_WAGE_AND_UNPAID_DEBTS_NONCANON.md"
THIRTEEN = BASE / "THE_DOOR_THAT_FED_THE_FIRE_CHAPTER_13_NONCANON.md"
TEN_SHA = "1c965faaaf143d8a29ce83d3608922c469ab5cb0"
NINE_SHA = "964ec5e886b51d2671d4cc4080e6588604b32a92"
THIRTEEN_SHA = "f238e02a331467db03060f66ff711b65f5a92d04"
WRAP = re.compile(r"<!-- BEGIN 2016_CAUSAL ([^\n]+) \| git_blob ([0-9a-f]{40}) -->\n\n([\s\S]*?)\n\n<!-- END 2016_CAUSAL ([^\n]+) -->")
ROW = re.compile(r"^\| (\d+) \| `([^`]+)` \| `([0-9a-f]{40})` \| (\d+) \|$", re.M)


def blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


class TenPartFireReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.book = TEN.read_text(encoding="utf-8")
        cls.prior = NINE.read_text(encoding="utf-8")
        cls.chapter = THIRTEEN.read_text(encoding="utf-8")
        cls.wraps = WRAP.findall(cls.book)
        cls.oldwraps = WRAP.findall(cls.prior)
        cls.rows = ROW.findall(cls.book.split("## Part 1 —", 1)[0])

    def test_01_ten_part_file_pinned(self):
        self.assertEqual(blob(TEN), TEN_SHA)

    def test_02_nine_part_file_pinned(self):
        self.assertEqual(blob(NINE), NINE_SHA)

    def test_03_original_chapter_thirteen_preserved(self):
        self.assertEqual(blob(THIRTEEN), THIRTEEN_SHA)

    def test_04_manifest_and_source_bodies_match(self):
        self.assertEqual(len(self.wraps), 10)
        self.assertEqual(len(self.rows), 10)
        for i, (wrap, row) in enumerate(zip(self.wraps, self.rows), 1):
            with self.subTest(i=i):
                name, sha, body, ending = wrap
                self.assertEqual(ending, name)
                self.assertEqual((int(row[0]), row[1], row[2]), (i, name, sha))
                data = (BASE / name).read_text(encoding="utf-8")
                self.assertEqual(blob(BASE / name), sha)
                self.assertEqual(body, data.rstrip("\n"))
                self.assertEqual(int(row[3]), len(data.split()))

    def test_05_first_nine_unchanged(self):
        self.assertEqual(self.wraps[:9], self.oldwraps)

    def test_06_tenth_is_unmodified_thirteen(self):
        self.assertEqual(self.wraps[9][0], THIRTEEN.name)
        self.assertEqual(self.wraps[9][1], THIRTEEN_SHA)
        self.assertEqual(self.wraps[9][2], self.chapter.rstrip("\n"))

    def test_07_ten_part_source_word_math(self):
        self.assertEqual(sum(int(row[3]) for row in self.rows), 61784)
        self.assertEqual(int(self.rows[-1][3]), 5161)
        self.assertIn("61784", self.book)

    def test_08_fire_has_cost_not_clean_rescue(self):
        for phrase in ["I opened it. It drew the fire down.", "The fire had wanted one too.", "the daughter's voice"]:
            self.assertIn(phrase, self.chapter)

    def test_09_no_unauthorized_2016_named_owner_pov(self):
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertNotRegex(self.chapter, r"(?m)^### (?:Edrin|Edin|Oren)\b")
        self.assertIn("No other canonical owner's identity", self.book)

    def test_10_unsettled_historical_world_continuity(self):
        for phrase in ["old wages are unpaid", "grain uncertified", "lower crossing unsafe", "wheel is asserted", "before any 2016 postseason result"]:
            self.assertIn(phrase, self.book)

    def test_11_noncanonical_release_gate(self):
        for phrase in ["NONCANON", "NO MERGE", "NO PUBLICATION", "NO CANON PROMOTION", "UMPIRE HOLD", "FOUNDER-ONLY"]:
            self.assertIn(phrase, self.book)

    def test_12_2026_protected_files_sha_contract(self):
        for filename, sha in {
            "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
            "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
            "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
            "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
        }.items():
            with self.subTest(name=filename):
                self.assertEqual(blob(ROOT / "living-novel/manuscript" / filename), sha)


if __name__ == "__main__":
    unittest.main()
