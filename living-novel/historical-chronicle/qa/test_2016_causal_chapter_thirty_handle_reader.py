"""Noncanonical Chapter XXX V2 and 27-part reader source-exact checks.

Mechanical/provenance guardrails ONLY. Does not imply editorial acceptance,
historical 2016 owner authentication, an Umpire review, or canon promotion.
"""
import hashlib
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
NEW = "THE_FOURTH_NOTE_AT_THE_RIVER_THE_HANDLE_ACROSS_THE_TABLE_CH30_V2_NONCANON.md"
ORIGINAL = "THE_FOURTH_NOTE_AT_THE_RIVER_CHAPTER_30_NONCANON.md"
READER = "READING_COPY_2016_CAUSAL_CH01_30_TWENTY_SEVEN_PARTS_HANDLE_ACROSS_TABLE_NONCANON.md"
PRIOR = "READING_COPY_2016_CAUSAL_CH01_29_TWENTY_SIX_PARTS_FISH_TO_SHADOW_V2_NONCANON.md"
NEW_SHA = "343eaf03f3921475439c721251e5b32744db0e30"
ORIG_SHA = "1b65f32ca5b41b52e8d362b8cfea95b4e2a03b8d"
PRIOR_SHA = "2e363c740322461252fdc58a25041754266a04cf"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
 "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
 "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
 "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
 "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def git_blob(path):
    raw=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def manifest(content):
    return [(int(n), name, sha, int(words)) for n,name,sha,words in
            re.findall(r"^\| (\d+) \| \x60([^\x60]+)\x60 \| \x60([a-f0-9]{40})\x60 \| (\d+) \|$", content, re.M)]

def extract_body(content,name,sha):
    begin=f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    end=f"<!-- END 2016_CAUSAL {name} -->"
    assert content.count(begin)==content.count(end)==1, name
    return content.split(begin+"\n\n",1)[1].split("\n\n"+end,1)[0]

class ChapterThirtyHandleReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter=(BASE/NEW).read_text()
        cls.original=(BASE/ORIGINAL).read_text()
        cls.reader=(BASE/READER).read_text()
        cls.prior=(BASE/PRIOR).read_text()
        cls.rows=manifest(cls.reader)
        cls.prev_rows=manifest(cls.prior)
        cls.new_scene=cls.chapter.split("### V. The handle across the table",1)[1].split("### VI. Not the same song",1)[0]

    def test_01_new_chapter_pinned(self):
        self.assertEqual(git_blob(BASE/NEW),NEW_SHA)

    def test_02_original_chapter_preserved(self):
        self.assertEqual(git_blob(BASE/ORIGINAL),ORIG_SHA)

    def test_03_previous_reader_preserved(self):
        self.assertEqual(git_blob(BASE/PRIOR),PRIOR_SHA)

    def test_04_six_movements_in_order(self):
        self.assertEqual(re.findall(r"^### ([IVX]+)\. ",self.chapter,re.M),
                         ["I","II","III","IV","V","VI"])

    def test_05_substantial_new_movement(self):
        self.assertEqual(len(("### V. The handle across the table"+self.new_scene).split()),2005)
        self.assertIn("You could put a splinter in your hand",self.new_scene)
        self.assertIn("Tell me more things",self.new_scene)
        self.assertIn("They set the pan into the basket",self.new_scene)

    def test_06_original_earlier_scenes_verbatim(self):
        first=self.original.split("### I. A reed in the wrong place",1)[1].split("### V. Not the same song",1)[0]
        revised=self.chapter.split("### I. A reed in the wrong place",1)[1].split("### V. The handle across the table",1)[0]
        self.assertEqual(revised,first)

    def test_07_original_final_movement_and_handoff_verbatim(self):
        original=self.original.split("### V. Not the same song",1)[1]
        revised=self.chapter.split("### VI. Not the same song",1)[1]
        self.assertEqual(original,revised)

    def test_08_reader_order_and_final_row(self):
        self.assertEqual([row[0] for row in self.rows],list(range(1,28)))
        self.assertEqual(self.rows[-1],(27,NEW,NEW_SHA,7657))

    def test_09_27_balanced_markers(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "),27)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "),27)

    def test_10_all_27_sources_pinned_and_embedded(self):
        for part,name,sha,words in self.rows:
            with self.subTest(part=part):
                source=(BASE/name).read_text()
                self.assertEqual(git_blob(BASE/name),sha)
                self.assertEqual(len(source.split()),words)
                self.assertEqual(extract_body(self.reader,name,sha),source.rstrip("\n"))

    def test_11_prior_26_bodies_unchanged(self):
        self.assertEqual(self.rows[:26],self.prev_rows)
        for part,name,sha,_ in self.prev_rows:
            with self.subTest(part=part):
                self.assertEqual(extract_body(self.reader,name,sha),
                                 extract_body(self.prior,name,sha))

    def test_12_source_words_and_wrapper(self):
        self.assertEqual(sum(x[3] for x in self.rows),189313)
        self.assertIn("Source component words including metadata: 189313",self.reader)
        self.assertEqual(len(self.chapter.split()),7657)

    def test_13_pov_and_historical_firewall(self):
        self.assertIn("sole proposed principal interior viewpoint is fictional Jake",self.chapter)
        self.assertIn("owner-slot binding remains UNAUTHENTICATED",self.chapter)
        for forbidden in ("Edrin","Edin"):
            self.assertNotIn(forbidden,self.new_scene)

    def test_14_child_safe_and_important_loops_unchanged(self):
        for anchor in ("four paid stoneworks hours","Mev","Pell","Vessa","kiln",
                       "Eren","Esi"):
            self.assertIn(anchor,self.chapter)
        self.assertIn("The fourth note",self.chapter)
        self.assertIn("NO MERGE / NO PUBLICATION / NO CANON PROMOTION",self.reader)

    def test_15_historical_competition_archive(self):
        archive=ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(git_blob(archive),ARCHIVE_SHA)

    def test_16_protected_main_prologue_and_three_chapters(self):
        for path,sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT/path),sha)

    def test_17_status_and_approvals_still_held(self):
        self.assertIn("FOUNDER-ONLY CANON & PUBLICATION APPROVAL",self.reader)
        self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD",self.chapter)
        self.assertIn("27-Part Developmental Reading",self.reader)

if __name__=="__main__":
    unittest.main()
