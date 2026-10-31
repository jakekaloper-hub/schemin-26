"""Chapter XLVII source-exact assembly, historical firewall and independent-gate regression."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_BELL_THAT_HAD_NO_OWNER_CHAPTER_47_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_47_NONCANON.md"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_01_46_NONCANON.md"
CHAPTER_SHA = "c1bb3b86aa6f789d59fe2688600c10563496d5a5"
READER_SHA = "ff2a5892b39bbd94e6dfb67572600002cc53fcf0"
PREVIOUS_SHA = "5fcde1cc30adfe9f05aa6a331256626d2856e8f3"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def git_blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

def manifest_rows(text):
    return [
        (int(n), name, sha, int(words))
        for n, name, sha, words in re.findall(
            r"^\| ([0-9]+) \| \`([^\`]+)\` \| \`([0-9a-f]{40})\` \| ([0-9]+) \|$",
            text, re.M
        )
    ]

def source_section(text, name, sha):
    start = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    end = f"<!-- END 2016_CAUSAL {name} -->"
    assert text.count(start) == text.count(end) == 1, (name, text.count(start), text.count(end))
    return text.split(start, 1)[1].split(end, 1)[0].strip()

class FortySevenChapterReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.prev = (BASE / PREVIOUS).read_text()
        cls.rows = manifest_rows(cls.reader)
        cls.prevrows = manifest_rows(cls.prev)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_manifest_sequence(self):
        self.assertEqual([r[0] for r in self.rows], list(range(1, 48)))
        self.assertEqual(self.rows[-1], (47, CHAPTER, CHAPTER_SHA, 5696))

    def test_02_all_markers(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 47)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 47)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

    def test_03_each_source_exact(self):
        for number, name, sha, words in self.rows:
            with self.subTest(ch=number):
                self.assertEqual(source_section(self.reader, name, sha), (BASE / name).read_text().strip())
                self.assertEqual(len((BASE / name).read_text().split()), words)

    def test_04_source_blob_integrity(self):
        for number, name, sha, _ in self.rows:
            with self.subTest(ch=number):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_05_previous_reader_preserved(self):
        self.assertEqual(git_blob(BASE / PREVIOUS), PREVIOUS_SHA)
        self.assertEqual(self.rows[:46], self.prevrows)
        for number, name, sha, _ in self.prevrows:
            with self.subTest(ch=number):
                self.assertEqual(source_section(self.reader, name, sha), source_section(self.prev, name, sha))

    def test_06_exact_current_blobs(self):
        self.assertEqual(git_blob(BASE / CHAPTER), CHAPTER_SHA)
        self.assertEqual(git_blob(BASE / READER), READER_SHA)

    def test_07_six_movements_and_actual_words(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+[.]", self.chapter, re.M)), 6)
        self.assertEqual(len(self.chapter.split()), 5696)
        self.assertGreater(len(self.prose.split()), 5000)
        self.assertEqual(len(self.reader.split()), 275422)

    def test_08_reader_not_promoted(self):
        self.assertTrue(self.reader.startswith(
            "# 2016 Commonwealth — Causal Novel Reading Copy, Chapters I–XLVII (NONCANON)"
        ))
        self.assertIn("Forty-seven fully assembled", self.reader)
        self.assertIn("independent Authors Council/Umpire review", self.reader)

    def test_09_causal_turn_documented(self):
        self.assertIn("**Chapter XLVII turn:**", self.reader)
        self.assertIn("Fara removes the clapper", self.reader)

    def test_10_not_a_valid_public_vote(self):
        self.assertIn("No common decision was entered", self.prose)
        self.assertIn("without agreement", self.reader)
        self.assertIn("No legal policing body", self.chapter)

    def test_11_fara_material_consequence(self):
        self.assertIn("The clapper dropped into her palm.", self.prose)
        self.assertIn("one customer had taken his account book away", self.prose.lower())
        self.assertIn("spoon", self.prose)

    def test_12_other_character_agency(self):
        for name in ("Pell", "Hessa", "Ina", "Eren", "Lysa", "Corin", "Fara", "Sela", "Nella"):
            with self.subTest(name=name):
                self.assertIn(name, self.prose)
        self.assertIn("I won't be the man who closes a road", self.prose)
        self.assertIn('"No," Eren said.', self.prose)

    def test_13_verified_history_firewall(self):
        self.assertIn("NOT provider-authenticated", self.chapter)
        self.assertIn("proposed secondary-world fiction", self.chapter)
        self.assertNotIn("ESPN", self.prose)
        self.assertNotIn("Flaim", self.prose)

    def test_14_single_authorized_interior(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertNotRegex(self.prose, r"(?<![A-Za-z])(?:Edrin|Edin)(?![A-Za-z])")

    def test_15_continuity_wages_and_lodging(self):
        for phrase in ("four false-witness coins remain", "Pell still lacks", "twenty-one-night", "Orrel"):
            self.assertIn(phrase, self.chapter)
        self.assertIn("Sela's family still slept outside", self.prose)

    def test_16_sela_identity_not_auto_merged(self):
        self.assertIn("the two Sela name references remain distinct and unresolved", self.chapter)
        self.assertNotIn("Sela the net-mender was", self.chapter)

    def test_17_protected_main_unchanged(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), sha)

    def test_18_archive_unchanged(self):
        self.assertEqual(
            git_blob(ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"),
            ARCHIVE_SHA
        )

    def test_19_opposing_watch_claim_unresolved(self):
        self.assertIn("Garran's proposed search party departs without agreement", self.reader)
        self.assertIn("He did not write that the settlement was safe", self.prose)
        self.assertIn("The bell was not destroyed", self.prose)

    def test_20_no_release_or_independent_acceptance(self):
        qa = (BASE / "CHAPTER_47_SOURCE_EDITORIAL_QA_RECEIPT.md").read_text()
        for phrase in ("NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION", "NOT INDEPENDENT REVIEW"):
            self.assertIn(phrase, qa)
        self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD", self.chapter)

if __name__ == "__main__":
    unittest.main()
