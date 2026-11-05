"""20-part developmental reader tests. No editorial or release acceptance is implied."""
from __future__ import annotations
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
D = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
OLD = D / "READING_COPY_2016_CAUSAL_CH01_22_NINETEEN_PARTS_DRY_END_OF_THE_HOUSE_NONCANON.md"
NEW = D / "READING_COPY_2016_CAUSAL_CH01_23_TWENTY_PARTS_BLANKET_AT_THRESHOLD_V2_NONCANON.md"
CH = D / "THE_ROOM_BEYOND_THE_THRESHOLD_WIDTH_OF_A_BLANKET_CH23_V2_NONCANON.md"
ORIGINAL = D / "THE_ROOM_BEYOND_THE_THRESHOLD_CHAPTER_23_NONCANON.md"
CH22 = D / "THE_COVER_AND_THE_CARGO_DRY_END_OF_THE_HOUSE_CH22_V2_NONCANON.md"

def blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def rows(text: str):
    return [(int(n), f, sha, int(w)) for n, f, sha, w in re.findall(
        r"^\| (\d+) \| \x60([^\x60]+)\x60 \| \x60([a-f0-9]{40})\x60 \| (\d+) \|$",
        text, re.M)]

def body(text: str, filename: str, sha: str) -> str:
    start = f"<!-- BEGIN 2016_CAUSAL {filename} | git_blob {sha} -->\n\n"
    end = f"\n\n<!-- END 2016_CAUSAL {filename} -->"
    return text.split(start, 1)[1].split(end, 1)[0]

class ChapterXXIIITwentyPartReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = OLD.read_text(encoding="utf-8")
        cls.new = NEW.read_text(encoding="utf-8")
        cls.chapter = CH.read_text(encoding="utf-8")
        cls.old_rows = rows(cls.old)
        cls.new_rows = rows(cls.new)

    def test_01_prior_reader_blob(self):
        self.assertEqual(blob(OLD.read_bytes()), "3826d48edce0339dfb8008dc27a2a4fa00ea9dc4")

    def test_02_original_chapter_preserved(self):
        self.assertEqual(blob(ORIGINAL.read_bytes()), "d30c325ab05acf462693067e427bce9b069e0325")

    def test_03_ch22_v2_preserved(self):
        self.assertEqual(blob(CH22.read_bytes()), "d800ef4f301bda4a90e262821efae98ab2f3c915")

    def test_04_manifest_twenty_parts_ordered(self):
        self.assertEqual([r[0] for r in self.new_rows], list(range(1, 21)))

    def test_05_previous_manifest_unchanged(self):
        self.assertEqual(self.new_rows[:19], self.old_rows)

    def test_06_all_source_blobs_and_counts(self):
        for i, filename, sha, words in self.new_rows:
            with self.subTest(part=i):
                src = (D / filename).read_bytes()
                self.assertEqual(blob(src), sha)
                self.assertEqual(len(src.decode("utf-8").split()), words)

    def test_07_all_twenty_embedded_bodies_exact(self):
        for i, filename, sha, words in self.new_rows:
            with self.subTest(part=i):
                self.assertEqual(body(self.new, filename, sha),
                                 (D / filename).read_text(encoding="utf-8").rstrip("\n"))

    def test_08_first_nineteen_bodies_previous_reader_exact(self):
        for i, filename, sha, words in self.old_rows:
            with self.subTest(part=i):
                self.assertEqual(body(self.old, filename, sha), body(self.new, filename, sha))

    def test_09_total_chapter_words(self):
        self.assertEqual(sum(x[3] for x in self.new_rows), 136631)
        self.assertIn("Source words including chapter metadata: 136631", self.new)

    def test_10_new_chapter_length(self):
        self.assertEqual(len(self.chapter.split()), 7781)
        self.assertIn("### IV. The width of a blanket", self.chapter)

    def test_11_original_movements_in_order(self):
        markers = ["### III. What a wall would cost", "### IV. The width of a blanket",
                   "### V. The room no ledger held", "### VI. The road that had no witness"]
        positions = [self.chapter.index(s) for s in markers]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("The supper bell brought no resolution.", self.chapter)

    def test_12_screen_remains_unbuilt(self):
        self.assertIn("The mother pulled the blanket down.", self.chapter)
        self.assertIn("The shelter had acquired neither a wall nor a screen", self.chapter)

    def test_13_nell_keeps_second_bedding(self):
        self.assertIn("It was the second length of bedding, still hers to withhold.", self.chapter)
        self.assertIn("She did not lay down the second bedding length", self.chapter)
        self.assertIn("remaining soap", self.chapter)

    def test_14_flour_not_falsely_reconciled(self):
        self.assertIn("Not all of what had fallen could be saved.", self.chapter)
        self.assertIn("future yield remains unquantified", self.chapter)

    def test_15_next_chapter_sola_reentry_possible(self):
        self.assertIn("Chapter XXIV's return for paid craft work remains possible", self.chapter)
        self.assertIn("Esi holds keys and ledger stewardship", self.chapter)

    def test_16_protected_2026_hard_canon(self):
        expected = {
            "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
            "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
            "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
            "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc"
        }
        for fn, sha in expected.items():
            with self.subTest(file=fn):
                self.assertEqual(blob((ROOT / "living-novel/manuscript" / fn).read_bytes()), sha)

    def test_17_historical_source_archive_frozen(self):
        p = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(blob(p.read_bytes()), "6dbec1fe2537139f3a97c6a78250e2bae082a518")

    def test_18_release_barriers_present(self):
        for term in ("NONCANON", "NO MERGE", "NO PUBLICATION", "NO CANON PROMOTION", "FOUNDER-ONLY"):
            with self.subTest(term=term):
                self.assertIn(term, self.new)

    def test_19_latest_manifest_pins_actual_chapter(self):
        self.assertEqual(self.new_rows[-1][1], CH.name)
        self.assertEqual(self.new_rows[-1][2], blob(CH.read_bytes()))

    def test_20_one_wrapper_per_part(self):
        self.assertEqual(self.new.count("<!-- BEGIN 2016_CAUSAL "), 20)
        self.assertEqual(self.new.count("<!-- END 2016_CAUSAL "), 20)

if __name__ == "__main__":
    unittest.main()
