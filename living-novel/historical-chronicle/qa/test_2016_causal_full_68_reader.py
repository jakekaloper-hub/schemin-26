"""Source-exact 2016 causal novel I-LXVIII assembly: all 68 original Git blobs.

This is technical provenance QA, not a literary acceptance or canon-approval test.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
READER = BASE / "READING_COPY_CAUSAL_CHAPTERS_01_68_NONCANON.md"
BASE_55 = BASE / "READING_COPY_CAUSAL_CHAPTERS_01_55_NONCANON.md"
TAIL_13 = BASE / "READING_COPY_CAUSAL_CHAPTERS_56_68_NONCANON.md"
SHA_68 = "8a53badc92492dc9f76b3b210a6f34cca626f553"
SHA_55 = "a21bbcbc7268e6523378097aa60d62e1c85bed35"
SHA_13 = "e3e4edca68f02a81c7fc982f7a9b36f1b264aaf6"
PATTERN = re.compile(
    r"<!-- BEGIN 2016_CAUSAL ([^\n]+?) \| git_blob ([0-9a-f]{40}) -->\n\n"
    r"([\s\S]*?)\n\n<!-- END 2016_CAUSAL ([^\n]+?) -->"
)
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def blob_sha(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

class FullSixtyEightChapterReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reader = READER.read_text(encoding="utf-8")
        cls.matches = list(PATTERN.finditer(cls.reader))

    def test_01_new_assembled_reader_blob(self):
        self.assertEqual(blob_sha(READER), SHA_68)

    def test_02_legacy_55_reader_unchanged(self):
        self.assertEqual(blob_sha(BASE_55), SHA_55)

    def test_03_legacy_13_reader_unchanged(self):
        self.assertEqual(blob_sha(TAIL_13), SHA_13)

    def test_04_exactly_sixty_eight_wrappers(self):
        self.assertEqual(len(self.matches), 68)
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 68)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 68)

    def test_05_all_68_unique_sequential_chapters(self):
        names = [m.group(1) for m in self.matches]
        self.assertEqual(len(set(names)), 68)
        self.assertEqual(
            [int(re.search(r"_CHAPTER_(\d+)_NONCANON\.md$", x).group(1)) for x in names],
            list(range(1, 69)),
        )

    def test_06_every_wrapper_matches_source_blob_and_text(self):
        for m in self.matches:
            name, claimed_sha, rendered, end_name = m.groups()
            with self.subTest(chapter=name):
                original = BASE / name
                self.assertTrue(original.is_file())
                self.assertEqual(name, end_name)
                self.assertEqual(blob_sha(original), claimed_sha)
                # Wrappers contribute blank-line separators, not narrative changes.
                self.assertEqual(rendered.strip("\n"), original.read_text(encoding="utf-8").rstrip("\n"))

    def test_07_every_chapter_in_provenance_manifest(self):
        for i, m in enumerate(self.matches, 1):
            filename, claimed_sha = m.group(1), m.group(2)
            with self.subTest(chapter=i):
                self.assertIn(f"| {i} | `{filename}` | `{claimed_sha}` | ", self.reader)

    def test_08_manifest_rows_are_exactly_sixty_eight(self):
        self.assertEqual(
            len(re.findall(r"^\| (?:[1-9]|[1-5][0-9]|6[0-8]) \| `[^\n]+` \| `[0-9a-f]{40}` \| \d+ \|$", self.reader, re.M)),
            68,
        )

    def test_09_protected_2026_canon_preserved(self):
        for relative, expected_sha in PROTECTED.items():
            with self.subTest(path=relative):
                self.assertEqual(blob_sha(ROOT / relative), expected_sha)

    def test_10_editorial_hold_explicit(self):
        for phrase in ("DRAFT / INDEPENDENT EDITORIAL HOLD", "NOT A CANON RELEASE", "structural defect", "Founder review"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.reader)

    def test_11_survivor_return_remains_conditional(self):
        self.assertIn("survivor returning in Chapter LXVII", self.reader)
        self.assertIn("six-unlocated follow-up in Chapter LXVIII", self.reader)

    def test_12_real_league_data_not_inferred(self):
        self.assertIn("No score, league result, death, identified route or owner history has been inferred", self.reader)

    def test_13_single_continuous_reader_boundary(self):
        self.assertTrue(self.reader.startswith("# 2016 Commonwealth — Unified Causal Novel Reading Copy"))
        self.assertTrue(self.reader.endswith("<!-- END_CAUSAL_READING_COPY_01_68 -->\n"))

if __name__ == "__main__":
    unittest.main()
