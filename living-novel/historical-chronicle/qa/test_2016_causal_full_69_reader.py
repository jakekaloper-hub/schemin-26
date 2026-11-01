"""2016 unified causal Chapters I-LXIX source/identity firewall.

Technical verifications only. A passing test never supplies historical owner
authentication, Atlas approval, independent literary acceptance, or canon.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
READER_69 = BASE / "READING_COPY_CAUSAL_CHAPTERS_01_69_NONCANON.md"
READER_68 = BASE / "READING_COPY_CAUSAL_CHAPTERS_01_68_NONCANON.md"
CH_69 = BASE / "THE_PLACE_IN_THE_WEATHER_CHAPTER_69_NONCANON.md"
EXPECTED_69 = "af620c3b8a4cb38fe0027bf1c741898a37461c3e"
EXPECTED_68 = "8a53badc92492dc9f76b3b210a6f34cca626f553"
EXPECTED_69_CHAPTER = "0289d1301bbecb2ea03b85e7e63db566901ad295"
EXPECTED_55 = "a21bbcbc7268e6523378097aa60d62e1c85bed35"
EXPECTED_56_68 = "e3e4edca68f02a81c7fc982f7a9b36f1b264aaf6"
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

def blob_sha(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

class Unified2016SixtyNineSourceReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reader = READER_69.read_text(encoding="utf-8")
        cls.previous = READER_68.read_text(encoding="utf-8")
        cls.chapter = CH_69.read_text(encoding="utf-8")
        cls.matches = list(PATTERN.finditer(cls.reader))
        cls.previous_matches = list(PATTERN.finditer(cls.previous))

    def test_01_new_reader_blob_pinned(self):
        self.assertEqual(blob_sha(READER_69), EXPECTED_69)

    def test_02_predecessor_68_reader_untouched(self):
        self.assertEqual(blob_sha(READER_68), EXPECTED_68)

    def test_03_prior_55_core_untouched(self):
        self.assertEqual(blob_sha(BASE / "READING_COPY_CAUSAL_CHAPTERS_01_55_NONCANON.md"), EXPECTED_55)

    def test_04_prior_13_continuation_untouched(self):
        self.assertEqual(blob_sha(BASE / "READING_COPY_CAUSAL_CHAPTERS_56_68_NONCANON.md"), EXPECTED_56_68)

    def test_05_exactly_sixty_nine_chapter_wrappers(self):
        self.assertEqual(len(self.matches), 69)
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 69)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 69)

    def test_06_sequential_nonduplicated_source_filenames(self):
        names = [m.group(1) for m in self.matches]
        self.assertEqual(len(set(names)), 69)
        self.assertEqual(
            [int(re.search(r"_CHAPTER_(\d+)_NONCANON\.md$", p).group(1)) for p in names],
            list(range(1, 70)),
        )

    def test_07_exact_git_blob_sha_and_text_for_all_sources(self):
        for m in self.matches:
            name, claimed, content, ending = m.groups()
            with self.subTest(chapter=name):
                p = BASE / name
                self.assertTrue(p.is_file())
                self.assertEqual(name, ending)
                self.assertEqual(blob_sha(p), claimed)
                self.assertEqual(content.strip("\n"), p.read_text(encoding="utf-8").rstrip("\n"))

    def test_08_all_sixty_nine_manifest_rows_match(self):
        for i, m in enumerate(self.matches, 1):
            name, sha = m.group(1), m.group(2)
            with self.subTest(number=i):
                self.assertRegex(self.reader, re.escape(f"| {i} | `{name}` | `{sha}` | ") + r"\d+ \|")

    def test_09_manifest_has_exactly_sixty_nine_rows(self):
        rows = re.findall(r"^\| \d+ \| `[^\n]+` \| `[0-9a-f]{40}` \| \d+ \|$", self.reader, re.M)
        self.assertEqual(len(rows), 69)

    def test_10_original_68_manuscript_bodies_preserved(self):
        self.assertEqual(len(self.previous_matches), 68)
        for i in range(68):
            with self.subTest(chapter=i+1):
                self.assertEqual(self.matches[i].groups(), self.previous_matches[i].groups())

    def test_11_new_chapter_source_sha_pinned(self):
        self.assertEqual(blob_sha(CH_69), EXPECTED_69_CHAPTER)
        self.assertEqual(self.matches[-1].group(1), CH_69.name)

    def test_12_chapter_is_substantive(self):
        self.assertGreaterEqual(len(self.chapter.split()), 3000)
        self.assertEqual(len(self.chapter.split()), 4360)

    def test_13_six_causal_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\. ", self.chapter, re.M)), 6)

    def test_14_explicit_draft_editorial_hold(self):
        for phrase in ("DRAFT / NONCANON", "INDEPENDENT EDITORIAL HOLD", "Founder", "not provider-authenticated"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.chapter)

    def test_15_twelve_owner_sole_jake_pov_firewall_declaration(self):
        self.assertIn("Sole limited fictional principal interior: Jake / CHAR-JAKE-KALOPER", self.chapter)
        self.assertIn("no supporting person receives narrated interior access", self.chapter)

    def test_16_no_fictional_survivor_promoted_as_history(self):
        self.assertIn("conditionally follows the unapproved survivor-return story", self.chapter)
        self.assertIn("six remain unlocated, none declared dead", self.chapter)

    def test_17_continuity_obligations_are_not_dropped(self):
        for term in ("Esi", "Meric", "Ilyen", "Hessa", "six travelers", "roof", "cart"):
            with self.subTest(term=term):
                self.assertIn(term, self.chapter)

    def test_18_protected_canon_blob_integrity(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(blob_sha(ROOT / path), sha)

    def test_19_reader_repeats_editorial_and_history_firewall(self):
        self.assertIn("NOT A CANON RELEASE", self.reader)
        self.assertIn("structural defect", self.reader)
        self.assertIn("No score, league result, death, identified route or owner history has been inferred", self.reader)

    def test_20_reader_has_expected_bounds(self):
        self.assertTrue(self.reader.startswith("# 2016 Commonwealth — Unified Causal Novel Reading Copy"))
        self.assertTrue(self.reader.endswith("<!-- END_CAUSAL_READING_COPY_01_69 -->\n"))

if __name__ == "__main__":
    unittest.main()
