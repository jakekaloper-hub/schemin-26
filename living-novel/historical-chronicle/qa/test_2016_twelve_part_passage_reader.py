"""Noncanonical 2016 fire-recovery and passage editions: exact-source and canon safety."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
TEN = "READING_COPY_2016_CAUSAL_CH01_13_TEN_PARTS_FIRE_AND_UNSETTLED_WORK_NONCANON.md"
ELEVEN = "READING_COPY_2016_CAUSAL_CH01_14_ELEVEN_PARTS_THE_DAY_NOT_ENTERED_NONCANON.md"
TWELVE = "READING_COPY_2016_CAUSAL_CH01_15_TWELVE_PARTS_PASSAGE_WITHOUT_TITLE_NONCANON.md"
CH14 = "WHAT_WAS_LEFT_IN_THE_YARD_THE_DAY_NOT_ENTERED_CH14_V2_NONCANON.md"
OLD14 = "WHAT_WAS_LEFT_IN_THE_YARD_CHAPTER_14_NONCANON.md"
CH15 = "THE_PASSAGE_NO_ONE_COULD_SELL_CHAPTER_15_NONCANON.md"
SHA = {
    TEN: "1c965faaaf143d8a29ce83d3608922c469ab5cb0",
    ELEVEN: "d3efc3531330eb959570a3828ca909ba4f75a28f",
    TWELVE: "50463f970f76a6908e286f6cf4f9db09b03eac44",
    CH14: "6ab6b5cd3faeb5b926f4fba35d5e870772b2d7a9",
    OLD14: "f76ec3ae5245bccf57a8df2a3f3d76001319c68e",
    CH15: "5bac0a5028acf452790c61ec41391660e86abb9e",
}
WRAP = re.compile(
    r"<!-- BEGIN 2016_CAUSAL ([^\n]+) \| git_blob ([0-9a-f]{40}) -->\n\n"
    r"([\s\S]*?)\n\n<!-- END 2016_CAUSAL ([^\n]+) -->"
)
ROW = re.compile(r"^\| (\d+) \| `([^`]+)` \| `([0-9a-f]{40})` \| (\d+) \|$", re.M)


def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def split_reader(name):
    content = (BASE / name).read_text(encoding="utf-8")
    wrappers = WRAP.findall(content)
    rows = ROW.findall(content.split("## Part 1", 1)[0])
    return content, wrappers, rows


class TwelvePartRecoveryReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ten, cls.ten_wraps, _ = split_reader(TEN)
        cls.eleven, cls.eleven_wraps, cls.eleven_rows = split_reader(ELEVEN)
        cls.twelve, cls.twelve_wraps, cls.twelve_rows = split_reader(TWELVE)
        cls.revised = (BASE / CH14).read_text(encoding="utf-8")
        cls.original = (BASE / OLD14).read_text(encoding="utf-8")

    def test_01_source_files_sha_pinned(self):
        for name, expected in SHA.items():
            with self.subTest(name=name):
                self.assertEqual(git_blob(BASE / name), expected)

    def test_02_exact_counts(self):
        self.assertEqual((len(self.ten_wraps), len(self.eleven_wraps), len(self.twelve_wraps)), (10, 11, 12))
        self.assertEqual((len(self.eleven_rows), len(self.twelve_rows)), (11, 12))

    def test_03_unchanged_first_ten(self):
        self.assertEqual(self.eleven_wraps[:10], self.ten_wraps)
        self.assertEqual(self.twelve_wraps[:10], self.ten_wraps)

    def test_04_manifest_names_and_hashes(self):
        for wrappers, rows in ((self.eleven_wraps, self.eleven_rows), (self.twelve_wraps, self.twelve_rows)):
            for i, ((name, sha, body, end), (index, row_name, row_sha, words)) in enumerate(zip(wrappers, rows), 1):
                with self.subTest(part=i):
                    self.assertEqual((str(i), name, sha, name), (index, row_name, row_sha, end))
                    self.assertEqual(git_blob(BASE / name), sha)
                    self.assertEqual(body, (BASE / name).read_text(encoding="utf-8").rstrip("\n"))
                    self.assertEqual(len((BASE / name).read_text(encoding="utf-8").split()), int(words))

    def test_05_source_word_total(self):
        self.assertEqual(sum(int(row[3]) for row in self.eleven_rows), 69102)
        self.assertEqual(sum(int(row[3]) for row in self.twelve_rows), 75224)

    def test_06_new_v2_adds_chapter_sixth_movement(self):
        self.assertIn("### VI. The day not entered", self.revised)
        self.assertNotIn("### VI. The day not entered", self.original)
        self.assertIn("### V. A sound that was not the wheel", self.revised)

    def test_07_earned_not_paid_distinction(self):
        for line in [
            "I have no coin for them today.",
            "Put down that I heard it",
            "Not that I accepted it.",
            "Work to be measured",
        ]:
            with self.subTest(phrase=line):
                self.assertIn(line, self.revised)

    def test_08_no_magic_settlement(self):
        for line in [
            "This was not a payment.",
            "He had missed the morning freight queue",
            "the old debts disappeared",
        ]:
            with self.subTest(phrase=line):
                self.assertIn(line, self.revised)

    def test_09_chapter_15_is_source_exact_and_independent(self):
        self.assertEqual(self.twelve_wraps[10], self.eleven_wraps[10])
        self.assertEqual(self.twelve_wraps[11][0], CH15)
        self.assertIn("do not constitute general road access", self.twelve)
        self.assertIn("historical owner's thoughts", self.twelve)

    def test_10_no_non_owner_principal(self):
        for doc in (self.revised, self.eleven, self.twelve):
            self.assertIn("CHAR-JAKE-KALOPER", doc)
            self.assertNotRegex(doc, r"(?m)^### (?:Edrin|Edin|Oren)\b")
            self.assertIn("NONCANON", doc)

    def test_11_four_protected_2026_blobs(self):
        expected = {
            "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
            "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
            "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
            "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
        }
        for name, sha in expected.items():
            with self.subTest(name=name):
                self.assertEqual(git_blob(ROOT / "living-novel/manuscript" / name), sha)

    def test_12_release_gates(self):
        for doc in (self.eleven, self.twelve):
            for phrase in ("DRAFT", "NONCANON", "UMPIRE HOLD", "FOUNDER-ONLY", "NO MERGE",
                           "NO PUBLICATION", "NO CANON PROMOTION"):
                self.assertIn(phrase, doc)


if __name__ == "__main__":
    unittest.main()
