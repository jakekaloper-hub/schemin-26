"""Chapter XXIV NONCANON source-exact reader integrity and narrative-boundary regressions.

Run via the existing Novel OS CI historical reader discovery step:
python -m unittest discover -s living-novel/historical-chronicle/qa -p 'test_2016_causal_chapter*reader.py' -v
These are mechanical gates, NOT independent editorial/Atlas/Umpire acceptance.
"""
import hashlib
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
NEW = "THE_THINGS_SHE_CAME_BACK_FOR_CHAPTER_24_NONCANON.md"
OLD_READER = "READING_COPY_CAUSAL_CHAPTERS_01_23_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_24_NONCANON.md"
OLD_READER_BLOB = "cef21bdf82699e31b1fed5d3e439957d7d5ec939"
NEW_CHAPTER_BLOB = "f767d79d9cd2ae6fdd58129ea96fbe0a73713461"
ARCHIVE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
ARCHIVE_BLOB = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def blob(path):
    b = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()

def rows(doc):
    return [
        (int(i), name, sha, int(words))
        for i, name, sha, words in re.findall(
            r"^\| (\d+) \| \x60([^\x60]+)\x60 \| \x60([0-9a-f]{40})\x60 \| (\d+) \|$",
            doc, re.M
        )
    ]

def extract(doc, name, sha):
    start = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    end = f"<!-- END 2016_CAUSAL {name} -->"
    assert doc.count(start) == 1, name
    assert doc.count(end) == 1, name
    return doc.split(start, 1)[1].split(end, 1)[0].strip()

class ChapterTwentyFourReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / NEW).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.old = (BASE / OLD_READER).read_text()
        cls.manifest = rows(cls.reader)
        cls.previous = rows(cls.old)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_manifest_has_24_ordered_chapters(self):
        self.assertEqual([row[0] for row in self.manifest], list(range(1, 25)))
        self.assertEqual(len(self.previous), 23)
        self.assertEqual(self.manifest[-1][1], NEW)

    def test_02_all_24_reader_components_source_exact(self):
        for i, name, sha, words in self.manifest:
            with self.subTest(chapter=i):
                self.assertEqual(extract(self.reader, name, sha), (BASE / name).read_text().strip())
                self.assertEqual(len((BASE / name).read_text().split()), words)

    def test_03_all_manifest_git_blobs_match_real_source(self):
        for i, name, sha, _ in self.manifest:
            with self.subTest(chapter=i):
                self.assertEqual(blob(BASE / name), sha)

    def test_04_previous_reader_immutable_and_23_sources_preserved(self):
        self.assertEqual(blob(BASE / OLD_READER), OLD_READER_BLOB)
        self.assertEqual(self.previous, self.manifest[:23])
        for i, name, sha, _ in self.previous:
            with self.subTest(chapter=i):
                self.assertEqual(extract(self.reader, name, sha), extract(self.old, name, sha))

    def test_05_substantial_five_movement_prose(self):
        self.assertGreaterEqual(len(self.chapter.split()), 6000)
        self.assertEqual(len(re.findall(r"^### [IVX]+\.", self.chapter, re.M)), 5)
        self.assertIn("### Editorial handoff", self.chapter)

    def test_06_twelve_owner_exclusive_interior_constraint(self):
        self.assertIn("Sole limited interior viewpoint", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER / PRINCIPAL_CHARACTER", self.chapter)
        for forbidden in ("Edrin", "Edin", "Oren"):
            self.assertNotIn(forbidden, self.prose)

    def test_07_sola_self_directed_not_rescued(self):
        self.assertIn("She had not come back to be found", self.prose)
        self.assertIn("She did not ask for a bed", self.prose)
        self.assertIn("Now, is there money for a screen?", self.prose)
        self.assertIn("paid reed-panel work", self.chapter)

    def test_08_unrelated_clog_does_not_prove_attack_or_thief(self):
        self.assertIn("Both were worn at the inner heel", self.prose)
        self.assertIn("The stranger's clog was longer and narrower", self.prose)
        self.assertIn("The stranger's clog remained unidentified", self.prose)
        self.assertIn("The removed leaves and their carrier were unknown", self.prose)

    def test_09_screen_is_partial_priced_real_work(self):
        self.assertIn("A screen did not recover anyone's privacy", self.prose)
        self.assertIn("It had only two leaves", self.prose)
        self.assertIn("She counted every piece", self.prose)
        self.assertIn("remaining unpaid third leaf", self.chapter)

    def test_10_seasonal_offer_is_selected_not_falsely_fulfilled(self):
        self.assertIn("I'll take the work", self.prose)
        self.assertIn("If the cart comes in three mornings", self.prose)
        self.assertIn("There was no wage in that small assistance", self.prose)
        self.assertIn("does not claim to have arrived", self.chapter)

    def test_11_esi_and_residents_make_independent_choices(self):
        self.assertIn("the next arrangement required willing people", self.prose)
        self.assertIn("the watch and serving shifts are actually reassigned", self.chapter.lower())
        self.assertIn("the cook could not release its reserve", self.prose)

    def test_12_named_consequential_open_loops_are_preserved(self):
        for s in (
            "Mara had not returned with Senn",
            "Len's eye had not healed",
            "The singer was still owed refunds",
            "the daughter's commission was unsigned",
            "the other woman's chest",
            "separate unopened message"
        ):
            self.assertIn(s.lower(), self.chapter.lower())

    def test_13_historical_archive_and_privacy_boundary_unchanged(self):
        self.assertEqual(blob(ARCHIVE), ARCHIVE_BLOB)
        self.assertIn("not verified 2016 ESPN results", self.chapter)
        self.assertIn("No provider-authenticated 2016 owner-slot association", self.chapter)
        self.assertIn("real owner's private motives", self.chapter)

    def test_14_protected_2026_canon_files_unchanged(self):
        for path, expected in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(blob(ROOT / path), expected)

    def test_15_reader_noncanon_gate_and_exact_markers(self):
        self.assertIn("Twenty-four fully assembled", self.reader)
        self.assertGreaterEqual(len(self.reader.split()), 128000)
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 24)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 24)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)
        self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD", self.chapter)
        self.assertEqual(blob(BASE / NEW), NEW_CHAPTER_BLOB)

if __name__ == "__main__":
    unittest.main()
