"""Chapter XXIII NONCANON reader integrity and source-boundary regression gates.

These tests verify file/source integrity and narrowly check continuity assertions;
they cannot independently authenticate 2016 historical identities, assess literature,
approve Atlas geography, or stand in for an Umpire.
Run: python -m unittest discover -s living-novel/historical-chronicle/qa -p 'test_2016_causal_chapter*reader.py' -v
"""
import hashlib
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
NEW = "THE_ROOM_BEYOND_THE_THRESHOLD_CHAPTER_23_NONCANON.md"
OLD_READER = "READING_COPY_CAUSAL_CHAPTERS_01_22_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_23_NONCANON.md"
OLD_READER_BLOB = "58f1dedfee156a0e581956f3b91b5a0d653053a2"
NEW_CHAPTER_BLOB = "d30c325ab05acf462693067e427bce9b069e0325"
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
    stop = f"<!-- END 2016_CAUSAL {name} -->"
    assert doc.count(start) == doc.count(stop) == 1, name
    return doc.split(start, 1)[1].split(stop, 1)[0].strip()

class ChapterTwentyThreeReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / NEW).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.old = (BASE / OLD_READER).read_text()
        cls.manifest = rows(cls.reader)
        cls.previous = rows(cls.old)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_manifest_complete_and_ordered(self):
        self.assertEqual([row[0] for row in self.manifest], list(range(1, 24)))
        self.assertEqual(len(self.previous), 22)
        self.assertEqual(self.manifest[-1][1], NEW)

    def test_02_each_chapter_is_source_exact(self):
        for i, name, sha, words in self.manifest:
            with self.subTest(chapter=i):
                self.assertEqual(extract(self.reader, name, sha), (BASE / name).read_text().strip())
                self.assertEqual(len((BASE / name).read_text().split()), words)

    def test_03_all_component_blob_identifiers_match(self):
        for i, name, sha, _ in self.manifest:
            with self.subTest(chapter=i):
                self.assertEqual(blob(BASE / name), sha)

    def test_04_previous_reader_and_22_sources_preserved(self):
        self.assertEqual(blob(BASE / OLD_READER), OLD_READER_BLOB)
        self.assertEqual(self.previous, self.manifest[:22])
        for i, name, sha, _ in self.previous:
            with self.subTest(chapter=i):
                self.assertEqual(extract(self.reader, name, sha), extract(self.old, name, sha))

    def test_05_substantial_five_movement_literary_chapter(self):
        self.assertGreaterEqual(len(self.chapter.split()), 5000)
        self.assertEqual(len(re.findall(r"^### [IVX]+\.", self.chapter, re.M)), 5)
        self.assertIn("### Editorial handoff", self.chapter)

    def test_06_sole_proposed_canonical_owner_pov(self):
        self.assertIn("Sole limited interior viewpoint", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER / PRINCIPAL_CHARACTER", self.chapter)
        for forbidden in ("Edrin", "Edin", "Oren"):
            self.assertNotIn(forbidden, self.prose)

    def test_07_notice_posted_in_this_chapter_not_retroactively(self):
        self.assertIn("The notice had already been nailed to the board", self.prose)
        self.assertIn("previously unposted theft notice is now actually posted by Esi and Tern", self.chapter)
        self.assertIn("previously unposted theft notice", self.chapter)

    def test_08_sola_decides_her_own_departure(self):
        self.assertIn("I'm leaving before the second meal", self.prose)
        self.assertIn("Sola was not making a journey", self.prose)
        self.assertIn("Sola's shelf was still empty", self.prose)
        self.assertIn("not authenticated as Sola's", self.chapter)

    def test_09_witnessed_uncertainty_does_not_name_thief(self):
        self.assertIn("a fragment that might not be part of the stolen book at all", self.prose)
        self.assertIn("the leaves and their carrier remained unknown", self.prose)
        self.assertIn("not proof of injury", self.chapter)

    def test_10_elected_body_or_hard_law_not_implied(self):
        self.assertIn("They had not voted a new law into being", self.prose)
        self.assertIn("one-night voluntary watch arrangement", self.chapter)
        self.assertIn("not an enduring new government", self.chapter)

    def test_11_esi_and_len_independent_agency(self):
        self.assertIn("Esi retains keys", self.chapter)
        self.assertIn("I asked to sit", self.prose)
        self.assertIn("Len's injured eye remains impaired", self.chapter)

    def test_12_preserve_disputed_and_separate_objects(self):
        self.assertIn("old supplier obligation and Jake's partial-pledge remainder remain unresolved", self.chapter)
        self.assertIn("Mara remains away with Senn", self.chapter)
        self.assertIn("other woman's chest unretrieved", self.chapter)
        self.assertIn("separate unopened message", self.chapter)

    def test_13_historical_2016_archive_untouched(self):
        self.assertEqual(blob(ARCHIVE), ARCHIVE_BLOB)
        self.assertIn("not verified ESPN history", self.chapter)
        self.assertIn("owner-slot attribution remains unverified", self.chapter)

    def test_14_protected_2026_hard_manuscript_untouched(self):
        for path, expected in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(blob(ROOT / path), expected)

    def test_15_reader_envelope_and_noncanonical_holds(self):
        self.assertGreater(len(self.reader.split()), 122000)
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 23)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 23)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)
        self.assertIn("Twenty-three fully assembled", self.reader)
        self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD", self.chapter)
        self.assertEqual(blob(BASE / NEW), NEW_CHAPTER_BLOB)

if __name__ == "__main__":
    unittest.main()
