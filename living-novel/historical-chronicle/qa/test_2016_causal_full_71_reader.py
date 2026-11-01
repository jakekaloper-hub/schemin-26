"""2016 causal 71-chapter assembled draft integrity gate; technical, not editorial acceptance."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
READER = BASE / "READING_COPY_CAUSAL_CHAPTERS_01_71_NONCANON.md"
PREVIOUS = BASE / "READING_COPY_CAUSAL_CHAPTERS_01_70_NONCANON.md"
CHAPTER = BASE / "THE_MEASURE_OF_THE_ROAD_CHAPTER_71_NONCANON.md"
READER_SHA = "d27c708fbd7b44730ae8d424a709c2eb15f3bed7"
PREVIOUS_SHA = "6616634a516b4a3e99b015d01c19a5f72be186de"
CHAPTER_SHA = "acef39f31b9a58b8da64d4bba8c151323849f8b2"
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
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

class Unified2016SeventyOneSourceReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reader = READER.read_text(encoding="utf-8")
        cls.previous = PREVIOUS.read_text(encoding="utf-8")
        cls.chapter = CHAPTER.read_text(encoding="utf-8")
        cls.matches = list(PATTERN.finditer(cls.reader))
        cls.previous_matches = list(PATTERN.finditer(cls.previous))

    def test_01_exact_reader_blob(self):
        self.assertEqual(git_blob(READER), READER_SHA)

    def test_02_exact_chapter_blob(self):
        self.assertEqual(git_blob(CHAPTER), CHAPTER_SHA)

    def test_03_predecessor_reader_unchanged(self):
        self.assertEqual(git_blob(PREVIOUS), PREVIOUS_SHA)

    def test_04_wrapper_count(self):
        self.assertEqual(len(self.matches), 71)

    def test_05_manifest_count(self):
        self.assertEqual(len(re.findall(r"^\| \d+ \| `[^\n]+` \| `[0-9a-f]{40}` \| \d+ \|$", self.reader, re.M)), 71)

    def test_06_sequence_and_unique_sources(self):
        names = [m.group(1) for m in self.matches]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual([int(re.search(r"_CHAPTER_(\d+)_NONCANON\.md$", n).group(1)) for n in names], list(range(1, 72)))

    def test_07_previous_seventy_exact_wrappers(self):
        self.assertEqual(len(self.previous_matches), 70)
        for i in range(70):
            with self.subTest(chapter=i + 1):
                self.assertEqual(self.previous_matches[i].groups(), self.matches[i].groups())

    def test_08_each_wrapper_source_sha(self):
        for match in self.matches:
            name, claimed, body, ending = match.groups()
            with self.subTest(name=name):
                source = BASE / name
                self.assertTrue(source.exists())
                self.assertEqual(name, ending)
                self.assertEqual(claimed, git_blob(source))
                self.assertEqual(body.strip("\n"), source.read_text(encoding="utf-8").rstrip("\n"))

    def test_09_final_source(self):
        self.assertEqual(self.matches[-1].group(1), CHAPTER.name)
        self.assertEqual(self.matches[-1].group(2), CHAPTER_SHA)

    def test_10_substantive_chapter_words(self):
        self.assertEqual(len(self.chapter.split()), 4715)

    def test_11_six_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\. ", self.chapter, re.M)), 6)

    def test_12_noncanon_gates(self):
        for word in ["DRAFT / NONCANON", "INDEPENDENT EDITORIAL HOLD", "FOUNDER ACCEPTANCE HOLD"]:
            self.assertIn(word, self.chapter)

    def test_13_exclusive_principal(self):
        self.assertIn("Sole limited fictional principal interior: Jake / CHAR-JAKE-KALOPER", self.chapter)
        self.assertIn("no supporting person receives narrated interior access", self.chapter)

    def test_14_unverified_manager_identity(self):
        self.assertIn("not provider-authenticated", self.chapter)

    def test_15_conditional_missing_travelers(self):
        for term in ["six remain unlocated, none declared dead", "unapproved survivor-return", "No historical score"]:
            self.assertIn(term, self.chapter)

    def test_16_road_authority_remains_unverified(self):
        self.assertIn("claim of authority remains unresolved", self.chapter)
        self.assertIn("no Atlas route, law, kingdom, border or toll institution is promoted", self.chapter)

    def test_17_protected_2026_sources(self):
        for name, expected in PROTECTED.items():
            with self.subTest(source=name):
                self.assertEqual(git_blob(ROOT / name), expected)

    def test_18_unified_reader_closed_and_gated(self):
        self.assertTrue(self.reader.rstrip().endswith("<!-- END_CAUSAL_READING_COPY_01_71 -->"))
        self.assertIn("NOT A CANON RELEASE", self.reader)
        self.assertIn("structural defect", self.reader)

if __name__ == "__main__":
    unittest.main()
