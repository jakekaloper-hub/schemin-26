"""2016 Chapter XVI river-roof V2: source-exact 13-part developmental edition and negative canon guards."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
OLD = "THE_WORK_THAT_CROSSED_BACK_CHAPTER_16_NONCANON.md"
NEW = "THE_WORK_THAT_CROSSED_BACK_THE_ROOF_THAT_TRAVELED_CH16_V2_NONCANON.md"
PREV = "READING_COPY_2016_CAUSAL_CH01_15_TWELVE_PARTS_PASSAGE_WITHOUT_TITLE_NONCANON.md"
READER = "READING_COPY_2016_CAUSAL_CH01_16_THIRTEEN_PARTS_ROOF_THAT_TRAVELED_V2_NONCANON.md"
CH17 = "THE_HOURS_BETWEEN_HAMMERS_CHAPTER_17_NONCANON.md"
PIN = {
    OLD: "134372fe502087a049f22871e0c9ac187d690059",
    NEW: "cb0e438cd6c38dff913023e90c8c18eb94833741",
    PREV: "50463f970f76a6908e286f6cf4f9db09b03eac44",
}
WRAP = re.compile(
    r"<!-- BEGIN 2016_CAUSAL ([^\n]+) \| git_blob ([0-9a-f]{40}) -->\n\n"
    r"([\s\S]*?)\n\n<!-- END 2016_CAUSAL ([^\n]+) -->"
)
ROW = re.compile(r"^\| (\d+) \| \x60([^\x60]+)\x60 \| \x60([0-9a-f]{40})\x60 \| (\d+) \|$", re.M)


def blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def words(s):
    return len(s.split())


class RoofThatTraveled(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = (BASE / OLD).read_text(encoding="utf8")
        cls.new = (BASE / NEW).read_text(encoding="utf8")
        cls.previous = (BASE / PREV).read_text(encoding="utf8")
        cls.reader = (BASE / READER).read_text(encoding="utf8")
        cls.before = WRAP.findall(cls.previous)
        cls.after = WRAP.findall(cls.reader)
        cls.rows = ROW.findall(cls.reader.split("## Part 1", 1)[0])

    def test_01_pinned_prior_and_revised_sources(self):
        for name, expected in PIN.items():
            with self.subTest(path=name):
                self.assertEqual(blob(BASE / name), expected)

    def test_02_13_exact_source_components(self):
        self.assertEqual((len(self.before), len(self.after), len(self.rows)), (12, 13, 13))
        self.assertEqual(self.after[:12], self.before)

    def test_03_all_manifest_source_sha_word_counts(self):
        for n, ((name, sha, body, end), (index, row_name, row_sha, word_count)) in enumerate(zip(self.after, self.rows), 1):
            with self.subTest(part=n):
                self.assertEqual((name, sha, name), (row_name, row_sha, end))
                self.assertEqual(int(index), n)
                self.assertEqual(blob(BASE / name), sha)
                original = (BASE / name).read_text(encoding="utf8")
                self.assertEqual(body, original.rstrip("\n"))
                self.assertEqual(words(original), int(word_count))

    def test_04_source_words_total(self):
        self.assertEqual(words(self.new), 8063)
        self.assertEqual(sum(int(row[-1]) for row in self.rows), 83287)
        self.assertIn("**Source words including chapter metadata: 83287**", self.reader)

    def test_05_chapter_v2_contains_new_material(self):
        self.assertEqual(len(re.findall(r"(?m)^### [IVX]+\.", self.new)), 6)
        self.assertIn("### VI. The roof that traveled", self.new)
        self.assertNotIn("### VI. The roof that traveled", self.old)
        self.assertGreater(words(self.new) - words(self.old), 1900)

    def test_06_prior_narrative_preserved_before_v2_insertion(self):
        key = "The boat went upriver. Behind it,"
        old_start = self.old.index("### I. What the river gave back")
        new_start = self.new.index("### I. What the river gave back")
        self.assertEqual(self.old[old_start:self.old.index(key)], self.new[new_start:self.new.index("### VI. The roof that traveled")])
        self.assertTrue(self.new.index("### VI. The roof that traveled") < self.new.index(key))

    def test_07_cost_is_real_but_no_resolution_claimed(self):
        for phrase in ("Pell", "the cloth lay dry", "wet outer cord", "marked the bale",
                       "won't make the landing before the next meal",
                       "No delivery acceptance", "UNACCEPTED"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.new)
        self.assertIn("one wet outer binding marked for later inspection", self.reader)

    def test_08_neighboring_chapters_remain_source_exact(self):
        self.assertEqual(self.after[11][0], "THE_PASSAGE_NO_ONE_COULD_SELL_CHAPTER_15_NONCANON.md")
        self.assertEqual(self.after[12][0], NEW)
        self.assertIn("Pell, the oldest of the hired carriers", (BASE / CH17).read_text(encoding="utf8"))

    def test_09_pov_and_temporal_negative_guards(self):
        for doc in (self.new, self.reader):
            self.assertIn("CHAR-JAKE-KALOPER", doc)
            self.assertIn("NONCANON", doc)
            self.assertNotRegex(doc, r"(?m)^### (?:Edrin|Edin|Oren)\b")
            self.assertNotIn("2016 postseason champion", doc)
        self.assertIn("IN TRANSIT_UNCONFIRMED", self.new)
        self.assertIn("NOT ACCEPTED", self.new)
        
    def test_10_founder_and_independent_review_gates(self):
        for phrase in ("DRAFT", "NONCANON", "UMPIRE HOLD", "FOUNDER-ONLY",
                       "NO MERGE", "NO PUBLICATION", "NO CANON PROMOTION"):
            self.assertIn(phrase, self.reader)

    def test_11_protected_main_2026_blobs(self):
        protected = {
            "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
            "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
            "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
            "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
        }
        for name, sha in protected.items():
            with self.subTest(path=name):
                self.assertEqual(blob(ROOT / "living-novel/manuscript" / name), sha)


if __name__ == "__main__":
    unittest.main()
