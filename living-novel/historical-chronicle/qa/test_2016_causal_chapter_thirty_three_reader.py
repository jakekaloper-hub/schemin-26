"""Source-exact Chapter XXXIII 2016 causal reading-copy regression; no editorial approval."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_FEAST_WITH_NO_VOWS_CHAPTER_33_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_33_NONCANON.md"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_01_32_NONCANON.md"
CHAPTER_SHA = "3d7f1375a9f848e363ee35198daf824dd4bf2813"
READER_SHA = "72f7b9ae92627cc5bc8f63562a710b9a26d959d0"
PREVIOUS_SHA = "a30d1abcb91eafd80c73771aa33a34c245444751"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def rows(text):
    return [(int(n), name, sha, int(words)) for n, name, sha, words in re.findall(
        r"^\| (\d+) \| \x60([^\x60]+)\x60 \| \x60([a-f0-9]{40})\x60 \| (\d+) \|$", text, re.M
    )]

def passage(text, name, sha):
    start = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    end = f"<!-- END 2016_CAUSAL {name} -->"
    assert text.count(start) == 1 and text.count(end) == 1
    return text.split(start, 1)[1].split(end, 1)[0].strip()

class ThirtyThreeChapterReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.old = (BASE / PREVIOUS).read_text()
        cls.manifest = rows(cls.reader)
        cls.old_manifest = rows(cls.old)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_manifest_complete_and_ordered(self):
        self.assertEqual([n for n, _, _, _ in self.manifest], list(range(1, 34)))
        self.assertEqual(self.manifest[-1], (33, CHAPTER, CHAPTER_SHA, len(self.chapter.split())))

    def test_02_balanced_source_markers(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 33)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 33)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

    def test_03_source_exact_33_components(self):
        for n, name, sha, words in self.manifest:
            with self.subTest(chapter=n):
                source = (BASE / name).read_text()
                self.assertEqual(passage(self.reader, name, sha), source.strip())
                self.assertEqual(len(source.split()), words)

    def test_04_git_blob_manifest_matches_sources(self):
        for n, name, sha, _ in self.manifest:
            with self.subTest(chapter=n):
                self.assertEqual(blob(BASE / name), sha)

    def test_05_old_reader_not_overwritten(self):
        self.assertEqual(blob(BASE / PREVIOUS), PREVIOUS_SHA)
        self.assertEqual(self.manifest[:-1], self.old_manifest)

    def test_06_substantial_narrative_and_five_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\.", self.chapter, re.M)), 5)
        self.assertGreaterEqual(len(self.chapter.split()), 6500)
        self.assertGreaterEqual(len(self.reader.split()), 182000)

    def test_07_twelve_owner_firewall(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertIn("2016 league scoring slot remains UNAUTHENTICATED", self.chapter)
        for retired in ("Edrin", "Edin", "Oren"):
            self.assertNotIn(retired, self.prose)

    def test_08_vow_is_declined_explicitly(self):
        for phrase in ("I haven't said I will marry you", "Not with me", "I can't say vows today"):
            self.assertIn(phrase, self.prose)

    def test_09_gate_remains_open_and_unchanged_marital_status(self):
        for phrase in ("bar lifted", "Leave it", "no one got married"):
            self.assertIn(phrase, self.prose)

    def test_10_feast_is_independent_of_vows(self):
        self.assertIn("The houses had paid Fara her agreed price", self.prose)
        self.assertIn("The old woman with the sticks", self.prose)
        self.assertIn("The beans are cooked", self.prose)

    def test_11_independent_supporting_character_decisions(self):
        for phrase in ("Lysa stepped back", "Corin did not reach for the ring", "Serra stayed until the end"):
            self.assertIn(phrase, self.prose)

    def test_12_preexisting_loops_remain_open(self):
        for phrase in ("kiln passage remained sealed", "letter to Esi had not been confirmed delivered",
                       "No carrier had brought a confirmed report"):
            self.assertIn(phrase, self.prose)

    def test_13_history_not_promoted_as_truth(self):
        self.assertIn("No new 2016 competition facts are introduced", self.chapter)
        self.assertIn("secondary-world invention", self.chapter)
        self.assertNotIn("ESPN", self.prose)
        self.assertNotIn("Flaim", self.prose)

    def test_14_protected_canon_and_archival_facts_preserved(self):
        self.assertEqual(blob(ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"), ARCHIVE_SHA)
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(blob(ROOT / path), sha)

    def test_15_exact_readback_and_release_hold(self):
        self.assertEqual(blob(BASE / CHAPTER), CHAPTER_SHA)
        self.assertEqual(blob(BASE / READER), READER_SHA)
        self.assertIn("Thirty-three fully assembled", self.reader)
        self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD", self.chapter)
        self.assertIn("No independently authenticated Authors Council", self.chapter)
        self.assertIn("NO MERGE, NO CANON PROMOTION, NO PUBLICATION", self.chapter)

if __name__ == "__main__":
    unittest.main()
