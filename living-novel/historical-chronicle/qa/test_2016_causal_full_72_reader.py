"""2016 causal 72-chapter source-exact NONCANON manuscript integrity; not editorial acceptance."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
READER = BASE / "READING_COPY_CAUSAL_CHAPTERS_01_72_NONCANON.md"
PREVIOUS = BASE / "READING_COPY_CAUSAL_CHAPTERS_01_71_NONCANON.md"
CHAPTER = BASE / "THE_PIT_WITHOUT_A_FLOOR_CHAPTER_72_NONCANON.md"
READER_SHA = "8f1dda21ac4962143ba3291cef4d60769197d62f"
PREVIOUS_SHA = "d27c708fbd7b44730ae8d424a709c2eb15f3bed7"
CHAPTER_SHA = "4cd6a0785a57cdae14f21a1a1a0c7011c324c716"
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
ROW = re.compile(r"^\| (\d+) \| \x60([^\n]+)\x60 \| \x60([0-9a-f]{40})\x60 \| (\d+) \|$", re.M)

def git_blob(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

class Unified2016SeventyTwoSourceReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reader = READER.read_text(encoding="utf-8")
        cls.previous = PREVIOUS.read_text(encoding="utf-8")
        cls.chapter = CHAPTER.read_text(encoding="utf-8")
        cls.matches = list(PATTERN.finditer(cls.reader))
        cls.previous_matches = list(PATTERN.finditer(cls.previous))
        cls.manifest = list(ROW.finditer(cls.reader))

    def test_01_reader_blob(self):
        self.assertEqual(git_blob(READER), READER_SHA)

    def test_02_new_chapter_blob(self):
        self.assertEqual(git_blob(CHAPTER), CHAPTER_SHA)

    def test_03_previous_reader_preserved(self):
        self.assertEqual(git_blob(PREVIOUS), PREVIOUS_SHA)

    def test_04_seventy_two_wrappers(self):
        self.assertEqual(len(self.matches), 72)

    def test_05_seventy_two_manifest_rows(self):
        self.assertEqual(len(self.manifest), 72)

    def test_06_chapter_sequence_unique(self):
        names = [m.group(1) for m in self.matches]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual([int(re.search(r"_CHAPTER_(\d+)_NONCANON\.md$", n).group(1)) for n in names], list(range(1, 73)))

    def test_07_first_seventy_one_wrappers_source_exact(self):
        self.assertEqual(len(self.previous_matches), 71)
        for index in range(71):
            with self.subTest(chapter=index + 1):
                self.assertEqual(self.previous_matches[index].group(0), self.matches[index].group(0))

    def test_08_all_wrapper_source_shas(self):
        for m in self.matches:
            filename, sha, body, closing = m.groups()
            with self.subTest(name=filename):
                src = BASE / filename
                self.assertTrue(src.is_file())
                self.assertEqual(closing, filename)
                self.assertEqual(sha, git_blob(src))
                self.assertEqual(body.strip("\n"), src.read_text(encoding="utf-8").rstrip("\n"))

    def test_09_new_last_chapter_source(self):
        self.assertEqual(self.matches[-1].group(1), CHAPTER.name)
        self.assertEqual(self.matches[-1].group(2), CHAPTER_SHA)

    def test_10_actual_substantial_new_words(self):
        self.assertEqual(len(self.chapter.split()), 5616)

    def test_11_six_story_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\. ", self.chapter, re.M)), 6)

    def test_12_draft_and_approval_holds(self):
        for term in ("DRAFT / NONCANON", "INDEPENDENT EDITORIAL HOLD", "FOUNDER ACCEPTANCE HOLD"):
            self.assertIn(term, self.chapter)

    def test_13_one_canonical_principal_interior(self):
        self.assertIn("Sole limited fictional principal interior: Jake / CHAR-JAKE-KALOPER", self.chapter)
        self.assertIn("no supporting person receives narrated interior access", self.chapter)

    def test_14_historical_identity_not_counterfeited(self):
        self.assertIn("not provider-authenticated", self.chapter)

    def test_15_missing_traveler_status_conditional(self):
        for term in ("unapproved return", "six remain unlocated, none declared dead", "No historical score"):
            self.assertIn(term, self.chapter)

    def test_16_sawpit_not_promoted_to_atlas(self):
        self.assertIn("The local sawpit is closed pending repair", self.chapter)
        self.assertIn("not an Atlas assertion", self.chapter)

    def test_17_protected_prologue_and_opening_sha(self):
        for source, expected in PROTECTED.items():
            with self.subTest(source=source):
                self.assertEqual(git_blob(ROOT / source), expected)

    def test_18_reader_closed_and_noncanon(self):
        self.assertTrue(self.reader.rstrip().endswith("<!-- END_CAUSAL_READING_COPY_01_72 -->"))
        self.assertIn("NOT A CANON RELEASE", self.reader)
        self.assertIn("structural defect", self.reader)

    def test_19_manifest_matches_wrappers_and_source_wordcounts(self):
        self.assertEqual([int(m.group(1)) for m in self.manifest], list(range(1, 73)))
        for row, wrapper in zip(self.manifest, self.matches):
            with self.subTest(chapter=row.group(1)):
                self.assertEqual(row.group(2), wrapper.group(1))
                self.assertEqual(row.group(3), wrapper.group(2))
                self.assertEqual(int(row.group(4)), len((BASE / row.group(2)).read_text(encoding="utf-8").split()))

    def test_20_no_forbidden_institutional_character_names(self):
        self.assertIsNone(re.search(r"\b(?:Edrin|Edin|Master Oren)\b", self.chapter, re.I))

    def test_21_earned_new_physical_dramatic_turn(self):
        for term in ("The ground failed", "The worker came up one step", "The sawpit was no longer a workplace"):
            self.assertIn(term, self.chapter)

    def test_22_previous_manifest_stable(self):
        rows_before = list(ROW.finditer(self.previous))
        self.assertEqual(len(rows_before), 71)
        self.assertEqual([m.group(0) for m in rows_before], [m.group(0) for m in self.manifest[:71]])

if __name__ == "__main__":
    unittest.main()
