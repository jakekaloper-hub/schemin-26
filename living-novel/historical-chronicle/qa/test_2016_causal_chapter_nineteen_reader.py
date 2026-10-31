"""Noncanonical 2016 causal Chapter XIX and nineteen-part reading-copy regressions.
Tests prove local file/text integrity only; not ESPN truth or independent literary acceptance.
Run: python3 -m unittest discover -s living-novel/historical-chronicle/qa -p 'test_2016_causal_chapter_nineteen_reader.py' -v
"""
import hashlib
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
NEW = "THE_BED_UNDER_THE_OTHER_WINDOW_CHAPTER_19_NONCANON.md"
OLD_READER = "READING_COPY_CAUSAL_CHAPTERS_01_18_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_19_NONCANON.md"
ARCHIVE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
OLD_READER_SHA = "78560d0a2775a66340570d8382bbb90ae5992a22"
HARD = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def git_blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()

def rows(text):
    found = re.findall(r"^\| (\d+) \| `([^`]+)` \| `([0-9a-f]{40})` \| (\d+) \|$", text, flags=re.M)
    return [(int(n), name, sha, int(words)) for n, name, sha, words in found]

def get_component(reader, filename, sha):
    begin = "<!-- BEGIN 2016_CAUSAL " + filename + " | git_blob " + sha + " -->"
    end = "<!-- END 2016_CAUSAL " + filename + " -->"
    assert reader.count(begin) == reader.count(end) == 1
    return reader.split(begin, 1)[1].split(end, 1)[0].strip()

class CausalNineteen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / NEW).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.old = (BASE / OLD_READER).read_text()
        cls.manifest = rows(cls.reader)
        cls.old_manifest = rows(cls.old)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_ordered_manifest_and_markers(self):
        self.assertEqual([n for n, _, _, _ in self.manifest], list(range(1, 20)))
        self.assertEqual(self.manifest[-1][1], NEW)
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 19)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 19)

    def test_nineteen_sources_exact_and_word_counts(self):
        for n, name, sha, count in self.manifest:
            with self.subTest(chapter=n):
                original = (BASE / name).read_text()
                self.assertEqual(original.strip(), get_component(self.reader, name, sha))
                self.assertEqual(len(original.split()), count)

    def test_manifest_blobs_match_actual_local_git_blobs(self):
        for n, name, sha, _ in self.manifest:
            with self.subTest(chapter=n):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_all_eighteen_preceding_components_are_unchanged(self):
        self.assertEqual(git_blob(BASE / OLD_READER), OLD_READER_SHA)
        self.assertEqual(self.manifest[:18], self.old_manifest)
        for n, name, sha, _ in self.old_manifest:
            with self.subTest(chapter=n):
                self.assertEqual(get_component(self.reader, name, sha), get_component(self.old, name, sha))

    def test_substantial_five_movement_noncanon_prose(self):
        self.assertGreaterEqual(len(self.chapter.split()), 5000)
        self.assertEqual(len(re.findall(r"^### [IVX]+\. ", self.chapter, re.M)), 5)
        self.assertIn('I wanted you to have missed me', self.prose)
        self.assertIn('The shelter did not become silent. It went on living.', self.prose)

    def test_only_eligible_owner_inside_pov(self):
        preamble = self.chapter.split("### I.", 1)[0]
        self.assertIn("CHAR-JAKE-KALOPER", preamble)
        self.assertIn("Sole limited interior viewpoint", preamble)
        for retired in ("Edrin", "Edin", "Oren"):
            self.assertNotIn(retired, self.prose)
        self.assertIn("Mara", self.prose)

    def test_return_really_occurs_but_no_reconciliation(self):
        self.assertIn("You're back.", self.prose)
        self.assertIn("Len was warm beneath the gray blanket", self.prose)
        self.assertIn("Esi had the book.", self.prose)
        self.assertIn("No vow to remain, secured employment, repayment or reconciliation occurs", self.chapter)

    def test_message_remains_factually_unresolved(self):
        self.assertIn("I haven't seen it.", self.prose)
        self.assertIn("courier's actual disposition remains UNKNOWN", self.chapter)

    def test_wage_bounded_and_debt_not_falsely_resolved(self):
        self.assertIn("two days", self.prose)
        self.assertIn("old pledge remain unpaid", self.chapter)
        self.assertIn("great wheel remains unturned", self.chapter)

    def test_no_future_competition_knowledge_in_prose(self):
        self.assertNotIn("ESPN", self.prose)
        self.assertNotIn("Week 14", self.prose)
        self.assertNotIn("postseason", self.prose.lower())
        self.assertIsNone(re.search(r"\b\d{2,3}\.\d{2}\b", self.prose))

    def test_protected_2026_manuscript_github_blobs_pinned(self):
        for name, sha in HARD.items():
            with self.subTest(path=name):
                self.assertEqual(git_blob(ROOT / name), sha)

    def test_retained_2016_archive_unchanged(self):
        self.assertEqual(git_blob(ARCHIVE), ARCHIVE_SHA)
        self.assertIn("not provider-authenticated", self.chapter)

    def test_continuation_and_release_gates_not_waived(self):
        self.assertIn("Chapters I–XIX (NONCANON)", self.reader)
        self.assertIn("Founder-only canon/publication gates remain", self.reader)
        self.assertIn("NONCANON / independently unaccepted", self.chapter)
        self.assertIn("No merge, canon promotion, publication", self.chapter)

    def test_reader_exceeds_ninety_seven_thousand_words(self):
        self.assertGreater(len(self.reader.split()), 97000)
        self.assertGreater(len(self.reader), len(self.old))
        self.assertEqual(self.manifest[-1][2], git_blob(BASE / NEW))

if __name__ == "__main__":
    unittest.main()
