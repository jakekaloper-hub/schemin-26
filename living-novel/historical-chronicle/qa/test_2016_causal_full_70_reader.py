"""Source-exact 2016 causal 70-chapter manuscript tests (technical only).

A PASS does not supply historical owner authentication, Authors Council editorial
acceptance, Atlas clearance, Umpire independence, or Founder canon approval.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
READER = BASE / "READING_COPY_CAUSAL_CHAPTERS_01_70_NONCANON.md"
PREVIOUS = BASE / "READING_COPY_CAUSAL_CHAPTERS_01_69_NONCANON.md"
CHAPTER = BASE / "THE_NAMES_ON_THE_WORKBOARD_CHAPTER_70_NONCANON.md"
READER_SHA = "6616634a516b4a3e99b015d01c19a5f72be186de"
PREVIOUS_SHA = "af620c3b8a4cb38fe0027bf1c741898a37461c3e"
CHAPTER_SHA = "07f5967461d19378dd80ac27fc3a74d8c0e1854e"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
PATTERN = re.compile(
    r"<!-- BEGIN 2016_CAUSAL ([^\n]+?) \| git_blob ([0-9a-f]{40}) -->\n\n"
    r"([\s\S]*?)\n\n<!-- END 2016_CAUSAL ([^\n]+?) -->"
)


def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


class Unified2016SeventySourceReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reader = READER.read_text(encoding="utf-8")
        cls.previous = PREVIOUS.read_text(encoding="utf-8")
        cls.chapter = CHAPTER.read_text(encoding="utf-8")
        cls.matches = list(PATTERN.finditer(cls.reader))
        cls.previous_matches = list(PATTERN.finditer(cls.previous))

    def test_01_reader_blob_is_exact(self):
        self.assertEqual(git_blob(READER), READER_SHA)

    def test_02_69_chapter_reader_untouched(self):
        self.assertEqual(git_blob(PREVIOUS), PREVIOUS_SHA)

    def test_03_new_chapter_blob_is_exact(self):
        self.assertEqual(git_blob(CHAPTER), CHAPTER_SHA)

    def test_04_exactly_seventy_wrappers(self):
        self.assertEqual(len(self.matches), 70)
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 70)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 70)

    def test_05_sequential_source_filenames(self):
        names = [m.group(1) for m in self.matches]
        self.assertEqual(len(set(names)), 70)
        self.assertEqual(
            [int(re.search(r"_CHAPTER_(\d+)_NONCANON\.md$", x).group(1)) for x in names],
            list(range(1, 71)),
        )

    def test_06_every_wrapper_matches_source_byte_exactly(self):
        for m in self.matches:
            name, claimed, content, closing = m.groups()
            with self.subTest(source=name):
                path = BASE / name
                self.assertTrue(path.is_file())
                self.assertEqual(name, closing)
                self.assertEqual(git_blob(path), claimed)
                self.assertEqual(content.strip("\n"), path.read_text(encoding="utf-8").rstrip("\n"))

    def test_07_seventy_manifest_rows(self):
        rows = re.findall(r"^\| \d+ \| `[^\n]+` \| `[0-9a-f]{40}` \| \d+ \|$", self.reader, re.M)
        self.assertEqual(len(rows), 70)

    def test_08_every_manifest_row_pinned_to_wrapped_source(self):
        for i, m in enumerate(self.matches, 1):
            name, sha = m.group(1), m.group(2)
            with self.subTest(chapter=i):
                self.assertRegex(self.reader, re.escape(f"| {i} | `{name}` | `{sha}` | ") + r"\d+ \|")

    def test_09_sixty_nine_predecessor_bodies_preserved(self):
        self.assertEqual(len(self.previous_matches), 69)
        for i in range(69):
            with self.subTest(chapter=i + 1):
                self.assertEqual(self.matches[i].groups(), self.previous_matches[i].groups())

    def test_10_last_source_is_lxx(self):
        self.assertEqual(self.matches[-1].group(1), CHAPTER.name)
        self.assertEqual(self.matches[-1].group(2), CHAPTER_SHA)

    def test_11_chapter_substantial(self):
        self.assertGreaterEqual(len(self.chapter.split()), 3500)
        self.assertEqual(len(self.chapter.split()), 5633)

    def test_12_six_causal_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\. ", self.chapter, re.M)), 6)

    def test_13_noncanon_and_editorial_holds(self):
        for term in ("DRAFT / NONCANON", "INDEPENDENT EDITORIAL HOLD", "FOUNDER ACCEPTANCE HOLD"):
            with self.subTest(term=term):
                self.assertIn(term, self.chapter)

    def test_14_sole_principal_owner_identity(self):
        self.assertIn("Sole limited fictional principal interior: Jake / CHAR-JAKE-KALOPER", self.chapter)
        self.assertIn("no supporting person receives narrated interior access", self.chapter)

    def test_15_owner_authentication_not_claimed(self):
        self.assertIn("not provider-authenticated", self.chapter)

    def test_16_conditional_missing_travelers_not_turned_into_history(self):
        for term in ("conditionally follows the unapproved survivor-return story", "six remain unlocated, none declared dead", "No historical score"):
            with self.subTest(term=term):
                self.assertIn(term, self.chapter)

    def test_17_carried_obligations_remain_visible(self):
        for name in ("Esi", "Meric", "Hessa", "Ilyen", "Fara", "Dovan", "roof", "cart", "wages"):
            with self.subTest(name=name):
                self.assertIn(name, self.chapter)

    def test_18_protected_2026_canon_blobs(self):
        for name, expected in PROTECTED.items():
            with self.subTest(path=name):
                self.assertEqual(git_blob(ROOT / name), expected)

    def test_19_reader_reasserts_release_and_structural_holds(self):
        for term in ("NOT A CANON RELEASE", "structural defect", "No score, league result, death, identified route or owner history"):
            with self.subTest(term=term):
                self.assertIn(term, self.reader)

    def test_20_reader_header_footer_and_length(self):
        self.assertTrue(self.reader.startswith("# 2016 Commonwealth — Unified Causal Novel Reading Copy, Chapters I–LXX"))
        self.assertTrue(self.reader.endswith("<!-- END_CAUSAL_READING_COPY_01_70 -->\n"))
        self.assertIn("391,588 whitespace-delimited source words", self.reader)


if __name__ == "__main__":
    unittest.main()
