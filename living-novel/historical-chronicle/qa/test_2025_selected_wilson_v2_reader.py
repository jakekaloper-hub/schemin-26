"""2025 selected Wilson V2 reader: executable source, POV and continuity guards.
These checks are technical only; they do not establish period ownership, an Atlas
route, independent literary review, Umpire acceptance or canon promotion.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2025/causal-novel"
CHAPTER = BASE / "THE_ROAD_THAT_SPOKE_IN_TWO_VOICES_WILSON_2025_SELECTED_REVISION_V2_NONCANON.md"
READER = BASE / "READING_COPY_2025_TWELVE_VOICES_ELEVEN_PARTS_SELECTED_WILSON_V2_NONCANON.md"
A = BASE / "THE_ROAD_THAT_SPOKE_IN_TWO_VOICES_WILSON_2025_INTEGRATED_NONCANON.md"
A_READER = BASE / "READING_COPY_2025_TWELVE_VOICES_ELEVEN_PARTS_INTEGRATED_WILSON_NONCANON.md"
B = BASE / "THE_ROAD_NO_BANNER_COULD_OWN_TWO_TRUE_DISPATCHES_WILSON_2025_INTEGRATED_NONCANON.md"
READER_2016 = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel/READING_COPY_CAUSAL_CHAPTERS_01_72_NONCANON.md"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
PINNED = {
    CHAPTER: "5c953eb78e8f383d1038712501335418ce8af4ab",
    READER: "9a0181bf15bfff9ea8516fce06cda5ea1e8ba2c1",
    A: "bdaac1446d87c9ce0e738f6f9bbd632397152251",
    A_READER: "22f438a91aba72f391ae4ec7be5cae3c375230ce",
    B: "57b767cf2d417895db070c24fa7da07892629f62",
    READER_2016: "8f1dda21ac4962143ba3291cef4d60769197d62f",
}
WRAP = re.compile(
    r"<!-- BEGIN 2025_VOICE ([^\n]+) \| git_blob ([0-9a-f]{40}) -->\n\n"
    r"([\s\S]*?)\n\n<!-- END 2025_VOICE ([^\n]+) -->"
)
ROW = re.compile(
    r"^\| (\d+) \| ([^|]+) \| `([^`]+)` \| `([0-9a-f]{40})` \| (\d+) \|$",
    re.M,
)
OWNERS = {
    "CHAR-AUSTIN-BYARS", "CHAR-JAKE-KALOPER", "CHAR-ZACH-WILSON",
    "CHAR-PHILLIP-PITTS", "CHAR-BEN-WHIPPLE", "CHAR-DAVID-BABB",
    "CHAR-BRANDON-PRYOR", "CHAR-BOBBY-MITCHELL", "CHAR-KEVIN-ZEEK",
    "CHAR-JORDAN-HOLLINGSHEAD", "CHAR-WILSON-LOOK", "CHAR-MANNING-WELTY",
}

def blob(p):
    data = p.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()

class SelectedWilsonRevisionV2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.story = CHAPTER.read_text(encoding="utf-8")
        cls.reader = READER.read_text(encoding="utf-8")
        cls.prior = A_READER.read_text(encoding="utf-8")
        cls.wrap = list(WRAP.finditer(cls.reader))
        cls.previous_wrap = list(WRAP.finditer(cls.prior))
        cls.rows = ROW.findall(cls.reader.split("## Part 1 —", 1)[0])

    def test_01_source_blobs_and_archived_options_unchanged(self):
        for file, sha in PINNED.items():
            with self.subTest(file=file.name):
                self.assertEqual(blob(file), sha)

    def test_02_protected_2026_blobs(self):
        for file, sha in PROTECTED.items():
            with self.subTest(file=file):
                self.assertEqual(blob(ROOT / file), sha)

    def test_03_eleven_parts_and_rows(self):
        self.assertEqual(len(self.wrap), 11)
        self.assertEqual(len(self.rows), 11)
        self.assertEqual(len(self.previous_wrap), 11)

    def test_04_each_wrapper_is_source_exact(self):
        for index, (match, row) in enumerate(zip(self.wrap, self.rows), 1):
            part, owner, path, sha, word_count = row
            file = BASE / match.group(1)
            with self.subTest(part=index):
                self.assertEqual(int(part), index)
                self.assertEqual(match.group(1), match.group(4))
                self.assertEqual(match.group(1), Path(path).name)
                self.assertEqual(match.group(2), sha)
                self.assertEqual(blob(file), sha)
                self.assertEqual(match.group(3), file.read_text(encoding="utf-8").rstrip("\n"))
                self.assertEqual(len(file.read_text(encoding="utf-8").split()), int(word_count))

    def test_05_ten_other_chapters_are_identical(self):
        a = [m.group(0) for i,m in enumerate(self.previous_wrap) if i != 6]
        b = [m.group(0) for i,m in enumerate(self.wrap) if i != 6]
        self.assertEqual(a, b)

    def test_06_selected_source_in_part_seven_only(self):
        self.assertEqual(self.wrap[6].group(1), CHAPTER.name)
        self.assertEqual(self.wrap[6].group(2), PINNED[CHAPTER])
        self.assertEqual(sum(m.group(1)==CHAPTER.name for m in self.wrap), 1)

    def test_07_counts(self):
        self.assertEqual(len(self.story.split()), 11603)
        self.assertEqual(sum(int(row[4]) for row in self.rows), 65009)
        self.assertIn("65009 source words", self.reader)

    def test_08_all_twelve_registered_pov_ids(self):
        present=set(re.findall(r"CHAR-[A-Z0-9-]+", " ".join(r[1] for r in self.rows)))
        self.assertEqual(present, OWNERS)

    def test_09_correctly_qualified_previous_cart(self):
        self.assertIn("An empty cart was examined yesterday", self.story)
        self.assertIn("It proved nothing about a loaded crossing", self.story)
        self.assertNotIn("One wagon was examined yesterday and allowed through", self.story)

    def test_10_loaded_trial_and_second_hold(self):
        self.assertIn("ONE INSPECTED LOADED WAGON PASSED BY TEMPORARY WORKS", self.story)
        self.assertIn("SECOND LOADED WAGON HELD", self.story)
        self.assertIn("NO CLEARANCE FOR FURTHER LOADED CROSSING", self.story)
        self.assertIn("The second wagon stayed where it was.", self.story)

    def test_11_one_departure_and_eleven_movements(self):
        self.assertEqual(self.story.count("The procession moved."),1)
        self.assertEqual(
            re.findall(r"^### ([IVX]+)\. ", self.story.split("## Source and editorial receipt",1)[0], re.M),
            ["I","II","III","IV","V","VI","VII","VIII","IX","X","XI"]
        )

    def test_12_driver_does_not_receive_false_compensation(self):
        self.assertIn("I want a record of what the delay costs", self.story)
        self.assertIn("He had been offered no compensation", self.story)
        self.assertIn("not yet known", self.story)
        self.assertIn("A witnessed wage", self.story)

    def test_13_separate_watcher_payment_not_a_toll(self):
        self.assertIn("four agreed wages", self.story)
        self.assertIn("Nothing signed here appoints you.", self.story)
        self.assertIn("four separate hands", self.story)

    def test_14_unverified_silhouettes_remain_unassigned(self):
        self.assertIn("three indistinct figures", self.story)
        self.assertIn("declined a search", self.story)

    def test_15_two_messages_without_asserted_delivery_to_jake(self):
        self.assertIn("ONE WAGON PASSED", self.story)
        self.assertIn("FURTHER LOADED PASSAGE HELD", self.story)
        self.assertIn("no historical owner-account mapping", self.story)

    def test_16_explicit_release_and_period_holds(self):
        self.assertIn("DRAFT / NONCANON", self.story)
        self.assertIn("period Character Canon approval", self.reader)
        self.assertIn("not canon promoted", self.reader)
        self.assertIn("independent Umpire", self.story)

if __name__ == "__main__":
    unittest.main()
