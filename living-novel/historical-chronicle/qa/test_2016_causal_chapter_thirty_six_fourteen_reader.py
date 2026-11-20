"""2016 Chapter XXXVI V2 33-part source-exact reader. Mechanical checks only, not editorial approval."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
ORIG = "THE_ASH_AT_FARAS_DOOR_CHAPTER_36_NONCANON.md"
INTERLUDE = "THE_WHOLE_OF_FOURTEEN_CH36_INTERLUDE_V2_NONCANON.md"
NEW = "THE_ASH_AT_FARAS_DOOR_THE_WHOLE_OF_FOURTEEN_CH36_V2_NONCANON.md"
PREV = "READING_COPY_2016_CAUSAL_CH01_35_THIRTY_TWO_PARTS_ROOF_DUE_NONCANON.md"
READER = "READING_COPY_2016_CAUSAL_CH01_36_THIRTY_THREE_PARTS_WHOLE_OF_FOURTEEN_NONCANON.md"
ORIG_SHA = "7a893b228e9c0bf21504c837b216763080ec6e09"
CHAPTER_SHA = "d4bb254766ba03e49c45d0f42e66c9d2208a4595"
PREV_SHA = "e0206b6d92f4f65d87b332a79c8e66165668e0e1"
READER_SHA = "d3aaf9f6577934a4d360ededcc2426509fb2c6e3"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
CHAPTER_WORDS = 8992
TOTAL_WORDS = 242231
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
def blob(p):
    data = p.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
def rows(s):
    return [(int(n), f, sha, int(w)) for n, f, sha, w in re.findall(r"^\| (\d+) \| `([^`]+)` \| `([a-f0-9]{40})` \| (\d+) \|$", s, re.M)]
def component(s, name, sha):
    a = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->\n\n"
    b = f"\n\n<!-- END 2016_CAUSAL {name} -->"
    assert s.count(a) == s.count(b) == 1, name
    return s.split(a, 1)[1].split(b, 1)[0]

class ChapterThirtySixFourteen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = (BASE / ORIG).read_text()
        cls.standalone = (BASE / INTERLUDE).read_text()
        cls.chapter = (BASE / NEW).read_text()
        cls.previous = (BASE / PREV).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.oldrows = rows(cls.previous)
        cls.newrows = rows(cls.reader)
        cls.scene = "### Interlude — The whole of fourteen" + cls.standalone.split("### Interlude — The whole of fourteen", 1)[1].split("\n---\n\n**Provenance", 1)[0].rstrip()

    def test_01_archival_chapter_unchanged(self): self.assertEqual(blob(BASE / ORIG), ORIG_SHA)
    def test_02_chapter_blob_exact(self): self.assertEqual(blob(BASE / NEW), CHAPTER_SHA)
    def test_03_previous_reader_preserved(self): self.assertEqual(blob(BASE / PREV), PREV_SHA)
    def test_04_new_reader_blob_exact(self): self.assertEqual(blob(BASE / READER), READER_SHA)
    def test_05_original_six_movements_retained(self):
        self.assertEqual(re.findall(r"^### ([IVX]+)\. ", self.chapter, re.M), ["I", "II", "III", "IV", "V", "VI"])
        a = self.original.split("### I. ", 1)[1].split("### VI. What the morning could not say", 1)[0]
        b = self.original.split("### VI. What the morning could not say", 1)[1].split("\n---\n\n### Editorial handoff", 1)[0]
        self.assertIn(a.rstrip(), self.chapter)
        self.assertIn(b.rstrip(), self.chapter)
    def test_06_new_scene_exact_from_standalone(self): self.assertIn(self.scene, self.chapter)
    def test_07_substantial_scene(self):
        self.assertGreaterEqual(len(self.scene.split()), 2000)
        self.assertIn("Nine places in Fara's room, four across the lane, one beneath the sheltered eave", self.scene)
        self.assertIn("the will of fourteen", self.scene)
    def test_08_exclusive_jake_pov(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        for forbidden in ("Edrin thought", "Edin knew", "Hessa thought", "Fara wondered"):
            self.assertNotIn(forbidden, self.scene)
    def test_09_reader_manifest_33_parts(self):
        self.assertEqual([n for n, *_ in self.newrows], list(range(1, 34)))
        self.assertEqual(self.oldrows, self.newrows[:32])
        self.assertEqual(self.newrows[-1], (33, NEW, CHAPTER_SHA, CHAPTER_WORDS))
    def test_10_balanced_embedded_markers(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 33)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 33)
    def test_11_each_embedded_part_matches_source_file(self):
        for n, f, sha, w in self.newrows:
            with self.subTest(part=n):
                self.assertEqual(blob(BASE / f), sha)
                src = (BASE / f).read_text()
                self.assertEqual(len(src.split()), w)
                self.assertEqual(component(self.reader, f, sha), src.rstrip("\n"))
    def test_12_32_old_embedded_parts_source_exact(self):
        for n, f, sha, w in self.oldrows:
            with self.subTest(part=n):
                self.assertEqual(component(self.previous, f, sha), component(self.reader, f, sha))
    def test_13_component_word_totals(self):
        self.assertEqual(len(self.chapter.split()), CHAPTER_WORDS)
        self.assertEqual(sum(w for _, _, _, w in self.newrows), TOTAL_WORDS)
        self.assertIn(f"Source component words including metadata: {TOTAL_WORDS}", self.reader)
    def test_14_archive_blob_unchanged(self):
        self.assertEqual(blob(ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"), ARCHIVE_SHA)
    def test_15_four_protected_main_2026_manuscript_blobs(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path): self.assertEqual(blob(ROOT / path), sha)
    def test_16_noncanon_release_boundary(self):
        for word in ("NONCANON", "NO MERGE", "NO PUBLICATION", "NO CANON PROMOTION"):
            self.assertIn(word, self.reader)
    def test_17_characters_and_story_continuity(self):
        for name in ("Hessa", "Fara", "Orin", "Ina"):
            self.assertIn(name, self.scene)
        nxt = (BASE / "THE_COMPANY_THAT_CAME_APART_CHAPTER_37_NONCANON.md").read_text()
        self.assertIn("Fourteen fictional travelers", nxt)
        self.assertIn("eight of the fourteen", nxt.lower())
    def test_18_ledger_unknowns_and_no_false_facts(self):
        for word in ("Mael", "ash", "bird"):
            self.assertIn(word.lower(), self.chapter.lower())
        for phrase in ("no confirmed group split until Chapter XXXVII", "no new wages"):
            self.assertIn(phrase.lower(), self.chapter.lower())
    def test_19_new_material_sequencing(self):
        self.assertLess(self.chapter.index("### V. The road that was not theirs"), self.chapter.index(self.scene))
        self.assertLess(self.chapter.index(self.scene), self.chapter.index("### VI. What the morning could not say"))

if __name__ == "__main__":
    unittest.main()
