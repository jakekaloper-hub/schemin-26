"""Source-exact noncanonical 2016 sixteen-part candidate, Chapter XIX V2."""
from __future__ import annotations
import hashlib
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
DIR=ROOT/"living-novel/historical-chronicle/seasons/2016/causal-novel"
OLD=DIR/"READING_COPY_2016_CAUSAL_CH01_18_FIFTEEN_PARTS_MARKED_BALE_V2_NONCANON.md"
NEW=DIR/"READING_COPY_2016_CAUSAL_CH01_19_SIXTEEN_PARTS_FIGURE_BENEATH_THUMB_V2_NONCANON.md"
ORIG=DIR/"THE_BED_UNDER_THE_OTHER_WINDOW_CHAPTER_19_NONCANON.md"
CH=DIR/"THE_BED_UNDER_THE_OTHER_WINDOW_FIGURE_BENEATH_THUMB_CH19_V2_NONCANON.md"
ARCHIVE=ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
def blob(b):
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\x00"+b).hexdigest()
def rows(s):
    return [(int(n),p,h,int(w)) for n,p,h,w in re.findall(r"^\\| (\\d+) \\| \`([^\`]+)\` \\| \`([0-9a-f]{40})\` \\| (\\d+) \\|$",s,re.M)]
def embedded(s,n,h):
    st=f"<!-- BEGIN 2016_CAUSAL {n} | git_blob {h} -->\n\n"
    en=f"\n\n<!-- END 2016_CAUSAL {n} -->"
    return s.split(st,1)[1].split(en,1)[0]
class TestSixteenPartBedV2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old=OLD.read_text(); cls.new=NEW.read_text(); cls.chapter=CH.read_text(); cls.orig=ORIG.read_text()
        cls.a=rows(cls.new); cls.b=rows(cls.old)
    def test_sixteen_manifest_rows(self):
        self.assertEqual([n for n,_,_,_ in self.a],list(range(1,17)))
    def test_prior_fifteen_manifest_preserved(self):
        self.assertEqual(self.a[:15],self.b)
    def test_exact_embedded_sources(self):
        for n,p,h,w in self.a:
            with self.subTest(part=n):
                src=(DIR/p).read_bytes()
                self.assertEqual(blob(src),h)
                self.assertEqual(embedded(self.new,p,h).rstrip("\n"),src.decode().rstrip("\n"))
    def test_prior_fifteen_bodies_identical(self):
        for n,p,h,w in self.b:
            with self.subTest(part=n): self.assertEqual(embedded(self.new,p,h),embedded(self.old,p,h))
    def test_source_word_counts(self):
        for n,p,h,w in self.a:
            with self.subTest(part=n): self.assertEqual(len((DIR/p).read_text().split()),w)
        self.assertEqual(sum(w for n,p,h,w in self.a),105603)
    def test_six_new_developmental_movements(self):
        for ix in ("I","II","III","IV","V","VI"):
            self.assertIn("### "+ix+". ",self.chapter)
        self.assertIn("### IV. The figure beneath the thumb",self.chapter)
    def test_substantial_prose(self):
        self.assertGreater(len(self.chapter.split()),len(self.orig.split())+1100)
    def test_fictional_receipt_not_payment(self):
        self.assertIn("RECEIPT NOT SHOWN",self.chapter)
        self.assertIn("does not approve a bill",self.chapter)
    def test_unresolved_east_quarter_and_work(self):
        self.assertIn("east quarter remains closed",self.new)
        self.assertIn("no restored personal pallet",self.new)
    def test_one_owner_noncanon(self):
        self.assertIn("fictional Jake",self.new)
        self.assertIn("NONCANON",self.chapter)
        self.assertIn("NO MERGE",self.new)
    def test_archive_hash(self):
        self.assertEqual(blob(ARCHIVE.read_bytes()),"6dbec1fe2537139f3a97c6a78250e2bae082a518")
    def test_protected_hard_canon_hashes(self):
        expected={"PROLOGUE_DRAFT_V1.md":"5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0","CHAPTER_01_THE_FIRST_ANSWER.md":"26a17f05eb0565e7648c29add03ee9580ec933c3","CHAPTER_02_WHAT_COMES_BACK.md":"30fcf23a3eb8872fa0fb4dff029fe30044141121","CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md":"49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc"}
        for n,h in expected.items():
            with self.subTest(file=n):
                self.assertEqual(blob((ROOT/"living-novel/manuscript"/n).read_bytes()),h)
if __name__=="__main__":unittest.main()
