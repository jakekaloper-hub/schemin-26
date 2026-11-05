"""2016 17-part source-pinned NONCANON reading edition, preserved Chapter XX."""
from __future__ import annotations
import hashlib
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
D=ROOT/"living-novel/historical-chronicle/seasons/2016/causal-novel"
OLD=D/"READING_COPY_2016_CAUSAL_CH01_19_SIXTEEN_PARTS_FIGURE_BENEATH_THUMB_V2_NONCANON.md"
NEW=D/"READING_COPY_2016_CAUSAL_CH01_20_SEVENTEEN_PARTS_MARA_DEPARTURE_NONCANON.md"
CH=D/"THE_CLOTH_THAT_WOULD_NOT_STAY_FOLDED_CHAPTER_20_NONCANON.md"
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\x00"+b).hexdigest()
def rows(s):
    return [(int(n),p,h,int(w)) for n,p,h,w in re.findall(r"^\| (\d+) \| `([^`]+)` \| `([a-f0-9]{40})` \| (\d+) \|$",s,re.M)]
def embedded(s,p,h):
    return s.split(f"<!-- BEGIN 2016_CAUSAL {p} | git_blob {h} -->\n\n",1)[1].split(f"\n\n<!-- END 2016_CAUSAL {p} -->",1)[0]
class Test17Part(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.o=OLD.read_text();cls.n=NEW.read_text();cls.rows=rows(cls.n);cls.old=rows(cls.o);cls.ch=CH.read_text()
    def test_rows(self):self.assertEqual([x[0] for x in self.rows],list(range(1,18)))
    def test_prior_rows_preserved(self):self.assertEqual(self.rows[:16],self.old)
    def test_source_hashes_and_word_counts(self):
        for n,p,h,w in self.rows:
            with self.subTest(part=n):
                b=(D/p).read_bytes();self.assertEqual(blob(b),h);self.assertEqual(len(b.decode().split()),w)
    def test_source_exact_embedded(self):
        for n,p,h,w in self.rows:
            with self.subTest(part=n):
                self.assertEqual(embedded(self.n,p,h).rstrip("\n"),(D/p).read_text().rstrip("\n"))
    def test_first_sixteen_unchanged(self):
        for n,p,h,w in self.old:
            with self.subTest(part=n):self.assertEqual(embedded(self.n,p,h),embedded(self.o,p,h))
    def test_total(self):
        self.assertEqual(sum(x[3] for x in self.rows),111884)
        self.assertIn("Source words including chapter metadata: 111884",self.n)
    def test_mara_departure_not_resolved(self):
        self.assertIn("Mara's departure is an actual on-page event",self.ch)
        self.assertIn("Her return is neither guaranteed nor ruled out",self.ch)
    def test_no_silent_approval(self):
        self.assertIn("NONCANON",self.n);self.assertIn("NO MERGE",self.n);self.assertIn("Founder",self.n)
    def test_historical_firewall(self):
        self.assertIn("Historical manager-slot authentication is incomplete",self.n)
    def test_archive_and_hard_canon(self):
        e={"PROLOGUE_DRAFT_V1.md":"5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0","CHAPTER_01_THE_FIRST_ANSWER.md":"26a17f05eb0565e7648c29add03ee9580ec933c3","CHAPTER_02_WHAT_COMES_BACK.md":"30fcf23a3eb8872fa0fb4dff029fe30044141121","CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md":"49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc"}
        for n,h in e.items():
            with self.subTest(n=n):self.assertEqual(blob((ROOT/"living-novel/manuscript"/n).read_bytes()),h)
        self.assertEqual(blob((ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json").read_bytes()),"6dbec1fe2537139f3a97c6a78250e2bae082a518")
if __name__=="__main__":unittest.main()
