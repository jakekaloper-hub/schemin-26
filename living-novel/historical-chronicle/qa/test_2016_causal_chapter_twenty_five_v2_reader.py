"""Chapter XXV V2: noncanonical 22-part source-exact reading and authority guards.

These are mechanical regressions, not independent literary or Umpire acceptance.
CI discovers test_2016_causal_chapter*reader.py.
"""
import hashlib
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CH = "THE_MILE_BEYOND_THE_WEIGH_STONES_THE_UNSTRUCK_BELL_CH25_V2_NONCANON.md"
OLD = "READING_COPY_2016_CAUSAL_CH01_24_TWENTY_ONE_PARTS_LOWER_WATER_PATH_V2_NONCANON.md"
NEW = "READING_COPY_2016_CAUSAL_CH01_25_TWENTY_TWO_PARTS_UNSTRUCK_BELL_V2_NONCANON.md"
OLD_BLOB = "8af2796f018366bac4cae0e56fc330f4994bf172"
CH_BLOB = "49b1929c26a2feea252f98e88cdf982880f50a6f"
ORIGINAL_CH_BLOB = "90de3e31f6b729ca33636c74551caf9865a84256"
ARCHIVE_BLOB = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
def rows(text):
    return [(int(n), name, sha, int(w)) for n, name, sha, w in re.findall(
        r"^\| (\d+) \| \x60([^\x60]+)\x60 \| \x60([0-9a-f]{40})\x60 \| (\d+) \|$", text, re.M)]
def extract(text, name, sha):
    begin = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    end = f"<!-- END 2016_CAUSAL {name} -->"
    assert text.count(begin) == 1 and text.count(end) == 1, name
    return text.split(begin, 1)[1].split(end, 1)[0].strip()

class ChapterTwentyFiveV2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CH).read_text()
        cls.reader = (BASE / NEW).read_text()
        cls.old = (BASE / OLD).read_text()
        cls.manifest = rows(cls.reader)
        cls.previous = rows(cls.old)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_22_ordered_components(self):
        self.assertEqual([n for n, _, _, _ in self.manifest], list(range(1, 23)))
        self.assertEqual(len(self.previous), 21)
        self.assertEqual(self.manifest[-1][1], CH)

    def test_02_22_reader_components_are_source_exact(self):
        for n, name, sha, words in self.manifest:
            with self.subTest(part=n):
                source = (BASE / name).read_text()
                self.assertEqual(extract(self.reader, name, sha), source.strip())
                self.assertEqual(len(source.split()), words)

    def test_03_all_manifest_blobs_match_git(self):
        for n, name, sha, _ in self.manifest:
            with self.subTest(part=n):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_04_prior_reader_hash_unchanged(self):
        self.assertEqual(git_blob(BASE / OLD), OLD_BLOB)
        self.assertEqual(self.manifest[:21], self.previous)

    def test_05_all_prior_21_bodies_unchanged(self):
        for n, name, sha, _ in self.previous:
            with self.subTest(part=n):
                self.assertEqual(extract(self.reader, name, sha), extract(self.old, name, sha))

    def test_06_substantive_six_movement_chapter(self):
        self.assertGreaterEqual(len(self.chapter.split()), 7600)
        self.assertEqual(len(re.findall(r"^### [IVX]+\.", self.chapter, re.M)), 6)
        self.assertIn("### VI. The unstruck bell", self.chapter)

    def test_07_workplace_consequence_without_earned_wages(self):
        self.assertIn("My mother doesn't eat decisions", self.prose)
        self.assertIn("My children don't eat smoke", self.prose)
        self.assertIn("He had crossed the entire distance and acquired no wage", self.prose)
        self.assertIn("zero paid stoneworks hours", self.reader.lower())

    def test_08_noll_vessa_agency_and_forward_continuity(self):
        self.assertIn("I'm Noll", self.prose)
        self.assertIn("She keeps them for a reason", self.prose)
        self.assertIn("Vessa had not yet finished with the air", self.prose)
        self.assertIn("The kiln remains closed at Chapter XXVI opening", self.chapter)

    def test_09_exclusive_twelve_owner_interior(self):
        self.assertIn("Sole limited interior viewpoint", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER / PRINCIPAL_CHARACTER", self.chapter)
        for forbidden in ("Edrin", "Edin", "Oren"):
            self.assertNotIn(forbidden, self.prose)

    def test_10_shelter_unresolved_loops_survive_departure(self):
        for phrase in (
            "Mara was still with Senn",
            "Sola had taken her earnings",
            "The unknown clog remained at the shelter",
            "the old supplier invoice",
            "Jake's partial pledge",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.prose)

    def test_11_original_chapter_is_immutable(self):
        self.assertEqual(git_blob(BASE / "THE_MILE_BEYOND_THE_WEIGH_STONES_CHAPTER_25_NONCANON.md"), ORIGINAL_CH_BLOB)

    def test_12_competitive_archive_unchanged(self):
        self.assertEqual(git_blob(ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"), ARCHIVE_BLOB)

    def test_13_protected_2026_main_canon_unchanged(self):
        for name, sha in PROTECTED.items():
            with self.subTest(file=name):
                self.assertEqual(git_blob(ROOT / name), sha)

    def test_14_manifest_word_total_and_noncanonical_gates(self):
        self.assertEqual(sum(w for _, _, _, w in self.manifest), 152316)
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 22)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 22)
        self.assertIn("INDEPENDENT EDITORIAL HOLD", self.reader)
        self.assertIn("NO CANON PROMOTION", self.reader)
        self.assertEqual(git_blob(BASE / CH), CH_BLOB)

if __name__ == "__main__":
    unittest.main()
