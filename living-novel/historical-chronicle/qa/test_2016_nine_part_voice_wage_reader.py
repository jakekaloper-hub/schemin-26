"""Source-pinned regression tests for 2016 Chapter XII V2 nine-part noncanonical reader."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
NINE = BASE / "READING_COPY_2016_CAUSAL_CH01_12_NINE_PARTS_VOICE_WAGE_AND_UNPAID_DEBTS_NONCANON.md"
EIGHT = BASE / "READING_COPY_2016_CAUSAL_CH01_11_EIGHT_PARTS_HOUSE_BEYOND_MARKER_NONCANON.md"
CH12 = BASE / "THE_PRICE_OF_A_VOICE_WAGE_THAT_DID_NOT_SETTLE_CH12_V2_NONCANON.md"
OLD12 = BASE / "THE_PRICE_OF_A_VOICE_CHAPTER_12_NONCANON.md"
NINE_SHA = "964ec5e886b51d2671d4cc4080e6588604b32a92"
EIGHT_SHA = "737789cff129d4bf5409c8ba5d1fc1ab85cfdb26"
CH12_SHA = "1d606748bfd719aecf7234136f71c4f48c222d0b"
OLD12_SHA = "722cc9318e744d7ab8fdae5fdd4fb0af775d1745"
WRAP = re.compile(r"<!-- BEGIN 2016_CAUSAL ([^\n]+) \| git_blob ([0-9a-f]{40}) -->\n\n([\s\S]*?)\n\n<!-- END 2016_CAUSAL ([^\n]+) -->")
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


class NinePartVoiceWageReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.book = NINE.read_text(encoding="utf-8")
        cls.previous = EIGHT.read_text(encoding="utf-8")
        cls.chapter = CH12.read_text(encoding="utf-8")
        cls.wraps = WRAP.findall(cls.book)
        cls.oldwraps = WRAP.findall(cls.previous)
        cls.rows = ROW.findall(cls.book.split("## Part 1 —", 1)[0])

    def test_01_new_edition_blob_pinned(self):
        self.assertEqual(blob(NINE), NINE_SHA)

    def test_02_prior_eight_part_blob_pinned(self):
        self.assertEqual(blob(EIGHT), EIGHT_SHA)

    def test_03_revised_twelve_blob_pinned(self):
        self.assertEqual(blob(CH12), CH12_SHA)

    def test_04_original_twelve_retained(self):
        self.assertEqual(blob(OLD12), OLD12_SHA)

    def test_05_nine_source_exact_bodies_and_manifest(self):
        self.assertEqual(len(self.wraps), 9)
        self.assertEqual(len(self.rows), 9)
        for i, (wrap, row) in enumerate(zip(self.wraps, self.rows), 1):
            with self.subTest(part=i):
                name, sha, body, end = wrap
                self.assertEqual(end, name)
                self.assertEqual((int(row[0]), row[1], row[2]), (i, name, sha))
                data = (BASE / name).read_text(encoding="utf-8")
                self.assertEqual(blob(BASE / name), sha)
                self.assertEqual(body, data.rstrip("\n"))
                self.assertEqual(int(row[3]), len(data.split()))

    def test_06_first_eight_source_exact(self):
        self.assertEqual(self.wraps[:8], self.oldwraps)

    def test_07_revised_chapter_only_ninth(self):
        self.assertEqual(self.wraps[8][0], CH12.name)
        self.assertEqual(self.wraps[8][1], CH12_SHA)
        self.assertEqual(self.wraps[8][2], self.chapter.rstrip("\n"))

    def test_08_source_word_arithmetic(self):
        self.assertEqual(sum(int(row[3]) for row in self.rows), 56623)
        self.assertEqual(int(self.rows[8][3]), 7810)
        self.assertEqual(int(self.rows[7][3]), 5490)
        self.assertIn("56623", self.book)

    def test_09_2016_story_time_before_postseason_knowledge(self):
        self.assertIn("before Jake learns any postseason outcome", self.book)
        self.assertIn("after the retained 2016 Week 13 notice", self.book)

    def test_10_six_scene_movements_and_jake_pov(self):
        for heading in [
            "### I. The sound beneath the door",
            "### IV. The work of giving back",
            "### V. The wage that did not settle anything",
            "### VI. A tune the road kept",
        ]:
            self.assertIn(heading, self.chapter)
        self.assertEqual(len(re.findall(r"(?m)^### [IVX]+\. ", self.chapter)), 6)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertNotRegex(self.chapter, r"(?m)^### (?:Edrin|Edin|Oren)\b")

    def test_11_distinct_freight_income_not_ticket_proceeds(self):
        for phrase in [
            "From my freight pay, not from any ticket.",
            "Mara was serving a thin stew.",
            "partial household contribution",
            "not proceeds of the unauthorized performance",
        ]:
            self.assertIn(phrase, self.chapter)

    def test_12_unsettled_debts_and_ownership_hold(self):
        for phrase in [
            "old timber wages and supplier invoice unpaid",
            "human-Jake association is not provider-authenticated",
            "singer's next destination unknown",
        ]:
            self.assertIn(phrase.lower(), self.chapter.lower())

    def test_13_release_holds(self):
        for phrase in ["NONCANON", "NO MERGE", "NO PUBLICATION", "NO CANON PROMOTION", "UMPIRE HOLD", "FOUNDER-ONLY"]:
            self.assertIn(phrase, self.book)

    def test_14_preserved_2026_hard_manuscript(self):
        for name, sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(blob(ROOT / name), sha)


if __name__ == "__main__":
    unittest.main()
