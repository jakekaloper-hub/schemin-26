"""Noncanonical 2016 causal Chapter XX source/assembly/continuity regressions.
Tests local textual integrity; not historical attribution, Atlas or independent acceptance.
Run: python3 -m unittest discover -s living-novel/historical-chronicle/qa -p 'test_2016_causal_chapter*reader.py' -q
"""
import hashlib
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
NEW = "THE_CLOTH_THAT_WOULD_NOT_STAY_FOLDED_CHAPTER_20_NONCANON.md"
OLD_READER = "READING_COPY_CAUSAL_CHAPTERS_01_19_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_20_NONCANON.md"
OLD_READER_SHA = "98ab302848f4f3ed97d36cb3f1d4396a6529e004"
ARCHIVE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
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
    return [(int(a),b,c,int(d)) for a,b,c,d in re.findall(
        r"^\| (\d+) \| `([^`]+)` \| `([0-9a-f]{40})` \| (\d+) \|$", text, flags=re.M)]
def component(reader, filename, sha):
    start = f"<!-- BEGIN 2016_CAUSAL {filename} | git_blob {sha} -->"
    end = f"<!-- END 2016_CAUSAL {filename} -->"
    assert reader.count(start) == reader.count(end) == 1
    return reader.split(start, 1)[1].split(end, 1)[0].strip()

class CausalTwenty(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / NEW).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.old = (BASE / OLD_READER).read_text()
        cls.manifest = rows(cls.reader)
        cls.old_manifest = rows(cls.old)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]
    def test_twenty_manifest_rows_ordered(self):
        self.assertEqual([x[0] for x in self.manifest], list(range(1,21)))
        self.assertEqual(self.manifest[-1][1], NEW)
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "),20)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "),20)
    def test_every_chapter_source_exact(self):
        for n,name,sha,words in self.manifest:
            with self.subTest(chapter=n):
                original = (BASE / name).read_text()
                self.assertEqual(original.strip(), component(self.reader,name,sha))
                self.assertEqual(len(original.split()),words)
    def test_all_github_blob_fingerprints_exact(self):
        for n,name,sha,_ in self.manifest:
            with self.subTest(chapter=n):
                self.assertEqual(git_blob(BASE / name),sha)
    def test_previous_reader_and_nineteen_components_unchanged(self):
        self.assertEqual(git_blob(BASE / OLD_READER), OLD_READER_SHA)
        self.assertEqual(self.manifest[:19],self.old_manifest)
        for n,name,sha,_ in self.old_manifest:
            with self.subTest(chapter=n):
                self.assertEqual(component(self.reader,name,sha),component(self.old,name,sha))
    def test_new_chapter_is_substantive_five_movement_scene(self):
        self.assertGreaterEqual(len(self.chapter.split()), 6000)
        self.assertEqual(len(re.findall(r"^### [IVX]+\. ", self.chapter, re.M)),5)
        self.assertIn("Good morning to you, sister",self.prose)
        self.assertIn("The cost of an empty chair", self.chapter)
    def test_prose_sole_permitted_owner_viewpoint(self):
        preamble = self.chapter.split("### I.",1)[0]
        self.assertIn("CHAR-JAKE-KALOPER",preamble)
        self.assertIn("Sole limited interior viewpoint",preamble)
        for banned in ("Edrin","Edin","Oren"):
            self.assertNotIn(banned,self.prose)
    def test_senn_is_independent_visitor_not_new_owner_identity(self):
        self.assertIn("sister",self.prose.lower())
        self.assertIn("There's work in the lower valley",self.prose)
        self.assertIn("newly invented Senn",self.chapter)
        self.assertIn("not provider-authenticated",self.chapter)
    def test_mara_physically_leaves_without_final_certainty(self):
        self.assertIn("She climbed into the wagon",self.prose)
        self.assertIn("They did not look back together",self.prose)
        self.assertIn("Her return is neither guaranteed nor ruled out",self.chapter)
    def test_esi_continues_independent_shelter_management(self):
        self.assertIn("She began calling the morning amounts",self.prose)
        self.assertIn("keys",self.prose)
        self.assertIn("Esi retains the shelter keys and books",self.chapter)
    def test_len_and_daughter_retain_independent_pursuits(self):
        self.assertIn("He held his wooden bird",self.prose)
        self.assertIn("These must go to their buyer",self.prose)
        self.assertIn("Travel is paid whether I can save the beam or not",self.prose)
    def test_no_invented_final_debt_repayment(self):
        self.assertIn("The remainder was still there",self.prose)
        self.assertIn("bounded partial coin payment",self.chapter)
        self.assertIn("does not discharge his pledge",self.chapter)
    def test_archive_and_protected_hard_canon_untouched(self):
        self.assertEqual(git_blob(ARCHIVE), ARCHIVE_SHA)
        for path,sha in HARD.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path),sha)
    def test_no_future_espn_outcomes(self):
        self.assertNotIn("Week 14",self.prose)
        self.assertNotIn("postseason",self.prose.lower())
        self.assertNotIn("ESPN",self.prose)
        self.assertIsNone(re.search(r"\b\d{2,3}\.\d{2}\b",self.prose))
    def test_unresolved_continuity_and_editorial_gates(self):
        self.assertIn("East wing closed",self.chapter)
        self.assertIn("great wheel unturned",self.chapter)
        self.assertIn("courier message disposition unknown",self.chapter)
        self.assertIn("NONCANON / independently unaccepted",self.chapter)
        self.assertIn("Founder sign-off claimed",self.chapter)
    def test_new_reader_is_longer_and_has_no_duplicate_final_marker(self):
        self.assertGreater(len(self.reader.split()), 103000)
        self.assertGreater(len(self.reader),len(self.old))
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"),1)
        self.assertEqual(self.manifest[-1][2],git_blob(BASE / NEW))

if __name__ == "__main__":
    unittest.main()
