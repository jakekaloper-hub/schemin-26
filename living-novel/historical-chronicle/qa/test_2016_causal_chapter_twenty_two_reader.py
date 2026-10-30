"""Noncanonical Chapter XXII: source-exact assembly and fail-closed continuity checks.

These deterministic assertions do not authenticate historical owners, approve geography,
simulate independent review, or authorize manuscript/canon promotion.
Run: python -m unittest discover -s living-novel/historical-chronicle/qa -p 'test_2016_causal_chapter*reader.py' -v
"""
import hashlib
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
NEW = "THE_COVER_AND_THE_CARGO_CHAPTER_22_NONCANON.md"
OLD_READER = "READING_COPY_CAUSAL_CHAPTERS_01_21_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_22_NONCANON.md"
OLD_READER_BLOB = "322138c36de8bf80cf01b41b7870203bc70fd205"
ARCHIVE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
ARCHIVE_BLOB = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def git_blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

def rows(document):
    return [
        (int(i), name, sha, int(words))
        for i, name, sha, words in re.findall(
            r"^\| (\d+) \| \x60([^\x60]+)\x60 \| \x60([0-9a-f]{40})\x60 \| (\d+) \|$",
            document, re.M
        )
    ]

def extract(reader, filename, sha):
    start = f"<!-- BEGIN 2016_CAUSAL {filename} | git_blob {sha} -->"
    end = f"<!-- END 2016_CAUSAL {filename} -->"
    assert reader.count(start) == reader.count(end) == 1
    return reader.split(start, 1)[1].split(end, 1)[0].strip()

class ChapterTwentyTwoReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / NEW).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.old = (BASE / OLD_READER).read_text()
        cls.manifest = rows(cls.reader)
        cls.previous = rows(cls.old)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_manifest_order_and_sources(self):
        self.assertEqual([i for i, *_ in self.manifest], list(range(1, 23)))
        self.assertEqual(self.manifest[-1][1], NEW)
        self.assertEqual(len(self.previous), 21)

    def test_each_component_source_exact(self):
        for i, name, sha, words in self.manifest:
            with self.subTest(chapter=i):
                source = (BASE / name).read_text()
                self.assertEqual(extract(self.reader, name, sha), source.strip())
                self.assertEqual(len(source.split()), words)

    def test_each_source_blob_exact(self):
        for i, name, sha, _ in self.manifest:
            with self.subTest(chapter=i):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_old_reader_and_first_21_components_unchanged(self):
        self.assertEqual(git_blob(BASE / OLD_READER), OLD_READER_BLOB)
        self.assertEqual(self.manifest[:21], self.previous)
        for i, name, sha, _ in self.previous:
            with self.subTest(chapter=i):
                self.assertEqual(extract(self.old, name, sha), extract(self.reader, name, sha))

    def test_length_five_movements_and_source_handoff(self):
        self.assertGreaterEqual(len(self.chapter.split()), 6000)
        self.assertEqual(len(re.findall(r"^### [IVX]+\.", self.chapter, re.M)), 5)
        self.assertIn("### Editorial handoff", self.chapter)
        self.assertIn("The cover remained locked", self.prose)

    def test_exclusive_owner_pov(self):
        self.assertIn("sole limited principal pov", self.chapter.lower())
        self.assertIn("CHAR-JAKE-KALOPER / PRINCIPAL_CHARACTER", self.chapter)
        for forbidden in ("Edrin", "Edin", "Oren"):
            self.assertNotIn(forbidden, self.prose)

    def test_concrete_material_progress_without_certified_culprit(self):
        self.assertIn("The threads have been cut", self.prose)
        self.assertIn("the pages didn't fall from the cover", self.prose.lower())
        self.assertIn("The west store did not release grain against the cover", self.chapter)
        self.assertIn("not authenticated as the thief", self.chapter)
        self.assertIn("For another day", self.prose)

    def test_esi_has_decision_and_custody(self):
        self.assertIn("Measure the sacks", self.prose)
        self.assertIn("disputed pending source reconciliation", self.prose)
        self.assertIn("Esi retains keys", self.chapter)
        self.assertIn("one-day evidence hold", self.chapter)

    def test_missing_notice_remains_unposted(self):
        self.assertIn("I never posted it", self.prose)
        self.assertIn("Jake has *not* posted the notice", self.chapter)
        self.assertIn("Tomorrow, before you take a cart", self.prose)

    def test_no_invented_recovery_or_debt_discharge(self):
        self.assertIn("Most of the leaves gone", self.prose)
        self.assertIn("older supplier invoice", self.chapter.lower())
        self.assertIn("partial-pledge remainder", self.chapter)
        self.assertIn("no forgiveness of his unpaid pledge", self.prose)

    def test_mara_len_claimant_chest_continuity(self):
        self.assertIn("Mara remains away with Senn", self.chapter)
        self.assertIn("Len's injured eye is not healed", self.chapter)
        self.assertIn("private claimant file and separate unopened message", self.chapter)
        self.assertIn("other woman's locked chest", self.chapter)
        self.assertNotIn("Mara returned", self.prose)

    def test_no_league_facts_or_owner_binding_claims(self):
        self.assertIn("does not authenticate Jake as a 2016 ESPN scoring-slot owner", self.chapter)
        for forbidden in ("ESPN", "Week 14", "postseason", "championship belt"):
            self.assertNotIn(forbidden, self.prose)
        self.assertIsNone(re.search(r"\b\d{2,3}\.\d{2}\b", self.prose))

    def test_historical_archive_and_protected_2026_unchanged(self):
        self.assertEqual(git_blob(ARCHIVE), ARCHIVE_BLOB)
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), sha)

    def test_new_reader_integrity_and_hold(self):
        self.assertGreater(len(self.reader.split()), 116000)
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 22)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 22)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)
        self.assertEqual(self.manifest[-1][2], git_blob(BASE / NEW))
        self.assertIn("Twenty-two fully assembled", self.reader)
        self.assertIn("independently unaccepted", self.chapter)
        self.assertIn("Founder approval", self.chapter)

if __name__ == "__main__":
    unittest.main()
