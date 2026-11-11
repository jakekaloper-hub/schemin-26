"""Noncanonical 2016 causal Chapter XXI: manifest, source bytes, POV and boundaries.
Checks textual integrity and pinned material only. Not owner authentication,
historical/Atlas acceptance, real-life facts, or independent editorial review.
Command: python3 -m unittest discover -s living-novel/historical-chronicle/qa
with pattern test_2016_causal_chapter*reader.py
"""
import hashlib
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
NEW = "THE_BOOK_THAT_WALKED_OUT_CHAPTER_21_NONCANON.md"
OLD_READER = "READING_COPY_CAUSAL_CHAPTERS_01_20_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_21_NONCANON.md"
OLD_READER_BLOB = "b150c37f0d8adda70359bb8a53d05079b9212631"
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

class CausalTwentyOne(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / NEW).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.old = (BASE / OLD_READER).read_text()
        cls.manifest = rows(cls.reader)
        cls.previous = rows(cls.old)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_manifest_21_ordered_rows(self):
        self.assertEqual([r[0] for r in self.manifest], list(range(1, 22)))
        self.assertEqual(self.manifest[-1][1], NEW)
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 21)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 21)

    def test_all_embedded_sources_exact(self):
        for i, name, sha, words in self.manifest:
            with self.subTest(chapter=i):
                self.assertEqual(extract(self.reader, name, sha), (BASE / name).read_text().strip())
                self.assertEqual(len((BASE / name).read_text().split()), words)

    def test_all_embedded_blob_fingerprints_exact(self):
        for i, name, sha, _ in self.manifest:
            with self.subTest(chapter=i):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_first_twenty_components_unchanged(self):
        self.assertEqual(git_blob(BASE / OLD_READER), OLD_READER_BLOB)
        self.assertEqual(self.manifest[:20], self.previous)
        for i, name, sha, _ in self.previous:
            with self.subTest(chapter=i):
                self.assertEqual(extract(self.old, name, sha), extract(self.reader, name, sha))

    def test_five_full_movements_and_substantive_length(self):
        self.assertGreaterEqual(len(self.chapter.split()), 6000)
        self.assertEqual(len(re.findall(r"^### [IVX]+\.", self.chapter, re.M)), 5)
        self.assertIn("A page that could be carried twice", self.chapter)

    def test_owner_only_viewpoint(self):
        self.assertIn("CHAR-JAKE-KALOPER / PRINCIPAL_CHARACTER", self.chapter)
        self.assertIn("Sole limited interior viewpoint", self.chapter)
        for banned in ("Edrin", "Edin", "Oren"):
            self.assertNotIn(banned, self.prose)

    def test_mara_has_departed_and_not_magically_returned(self):
        self.assertIn("Mara's wagon had been gone for three hours", self.prose)
        self.assertIn("Mara's return", self.chapter)
        self.assertNotIn("Mara returned", self.prose)

    def test_esi_controls_shelter_and_makes_external_decisions(self):
        self.assertIn("The keys stayed under her coat", self.prose)
        self.assertIn("a visit to the market", self.prose)
        self.assertIn("Esi keeps the physical keys", self.chapter)

    def test_claim_mark_does_not_authenticate_claimant(self):
        self.assertIn("no two were alike", self.prose)
        self.assertIn("The private file with the missing claimant's original mark was elsewhere", self.prose)
        self.assertIn("Missing claimant still unidentified", self.chapter)

    def test_distinct_chest_not_claimant_property(self):
        self.assertIn("The woman with its key was not the missing claimant", self.prose)
        self.assertIn("Behind the unsafe eastern boundary", self.prose)
        self.assertIn("chest unretrieved behind a closed unsafe east boundary", self.chapter)

    def test_book_loss_is_observed_not_only_threatened(self):
        self.assertIn("The larger bound book was gone", self.prose)
        self.assertIn("The missing account book had a brown cover", self.prose)
        self.assertIn("Its loss is real within this NONCANON fiction", self.chapter)

    def test_no_certified_thief_or_holl_collusion(self):
        self.assertIn("Thief, organizer, motive, destination and involvement of Holl remain unknown", self.chapter)
        self.assertIn("It did not prove they were partners", self.prose)
        self.assertIn("I didn't say you did", self.prose)

    def test_len_observes_without_unproved_identity(self):
        self.assertIn("I saw a coat", self.prose)
        self.assertIn("The person held the book flat under one arm", self.prose)
        self.assertIn("his injured eye", self.chapter)

    def test_unpaid_debts_and_unknown_message_preserved(self):
        self.assertIn("one partial payment, no release", self.prose)
        self.assertIn("the separate sealed message remains unopened", self.chapter)
        self.assertIn("mill damage", self.chapter)
        self.assertIn("singer refunds", self.chapter)
        self.assertIn("courier note", self.chapter)

    def test_original_historical_archive_and_hard_manuscript_pinned(self):
        self.assertEqual(git_blob(ARCHIVE), ARCHIVE_BLOB)
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), sha)

    def test_no_future_scoring_results_or_unverified_attribution(self):
        for token in ("postseason", "ESPN", "Week 14", "championship belt"):
            self.assertNotIn(token, self.prose)
        self.assertIsNone(re.search(r"\b\d{2,3}\.\d{2}\b", self.prose))
        self.assertIn("not provider-authenticated", self.chapter)

    def test_reader_integrity_and_no_promotion(self):
        self.assertGreater(len(self.reader.split()), 109000)
        self.assertGreater(len(self.reader), len(self.old))
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)
        self.assertIn("independently unaccepted", self.chapter)
        self.assertIn("Founder approval", self.chapter)
        self.assertEqual(self.manifest[-1][2], git_blob(BASE / NEW))

if __name__ == "__main__":
    unittest.main()
