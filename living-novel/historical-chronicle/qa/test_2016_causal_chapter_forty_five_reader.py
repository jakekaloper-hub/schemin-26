"""Noncanonical 2016 Chapter XLV exact-source reader and continuity regressions.
These tests do not constitute independent editorial, character, Atlas, Umpire or Founder approval.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_ROAD_THAT_WOULD_NOT_WAIT_CHAPTER_45_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_45_NONCANON.md"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_01_44_NONCANON.md"
CHAPTER_SHA = "8c36678412071e935fd6b7bf0c469a04386f6588"
READER_SHA = "de28a89a8624479a9f5af202968edadc7c7fecdd"
PREVIOUS_SHA = "e83303d18e0485a4cc811d7ac9c12b42f28a58be"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
def git_blob(path):
    b=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def rows(text):
    out=[]
    for line in text.splitlines():
        match=re.fullmatch(r"[|] ([0-9]+) [|] `([^`]+)` [|] `([0-9a-f]{40})` [|] ([0-9]+) [|]",line)
        if match:
            n,name,sha,words=match.groups()
            out.append((int(n),name,sha,int(words)))
    return out
def section(reader,name,sha):
    start=f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    end=f"<!-- END 2016_CAUSAL {name} -->"
    assert reader.count(start)==reader.count(end)==1
    return reader.split(start,1)[1].split(end,1)[0].strip()

class FortyFiveChapterReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter=(BASE/CHAPTER).read_text()
        cls.reader=(BASE/READER).read_text()
        cls.previous=(BASE/PREVIOUS).read_text()
        cls.rows=rows(cls.reader)
        cls.prevrows=rows(cls.previous)
        cls.prose=cls.chapter.split("### I.",1)[1].split("\n---\n",1)[0]

    def test_01_manifest_sequence(self):
        self.assertEqual([r[0] for r in self.rows],list(range(1,46)))
        self.assertEqual(self.rows[-1],(45,CHAPTER,CHAPTER_SHA,4664))
    def test_02_complete_source_boundaries(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "),45)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "),45)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"),1)
    def test_03_all_45_source_sections_exact(self):
        for n,name,sha,words in self.rows:
            with self.subTest(chapter=n):
                source=(BASE/name).read_text()
                self.assertEqual(section(self.reader,name,sha),source.strip())
                self.assertEqual(len(source.split()),words)
    def test_04_all_source_git_blob_hashes(self):
        for n,name,sha,words in self.rows:
            with self.subTest(chapter=n):
                self.assertEqual(git_blob(BASE/name),sha)
    def test_05_prior_reader_immutable(self):
        self.assertEqual(git_blob(BASE/PREVIOUS),PREVIOUS_SHA)
        self.assertEqual(self.rows[:44],self.prevrows)
        for n,name,sha,words in self.prevrows:
            with self.subTest(chapter=n):
                self.assertEqual(section(self.reader,name,sha),section(self.previous,name,sha))
    def test_06_exact_new_sha(self):
        self.assertEqual(git_blob(BASE/CHAPTER),CHAPTER_SHA)
        self.assertEqual(git_blob(BASE/READER),READER_SHA)
    def test_07_six_substantial_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+[.]",self.chapter,re.M)),6)
        self.assertEqual(len(self.chapter.split()),4664)
        self.assertGreater(len(self.prose.split()),3800)
        self.assertEqual(len(self.reader.split()),263852)
    def test_08_reader_is_current_noncanon(self):
        self.assertTrue(self.reader.startswith("# 2016 Commonwealth — Causal Novel Reading Copy, Chapters I–XLV (NONCANON)"))
        self.assertIn("Forty-five fully assembled",self.reader)
        self.assertIn("independent Authors Council/Umpire review",self.reader)
    def test_09_noncanonical_causal_turn(self):
        self.assertIn("Chapter XLV turn",self.reader)
        self.assertIn("The company departs",self.reader)
    def test_10_mother_child_conflict_not_travel_contract(self):
        self.assertIn("wanting will not be forbidden",self.prose)
        self.assertIn("Not tonight",self.prose)
        self.assertIn("No child joins a traveling company",self.chapter)
    def test_11_art_not_published_as_disaster_evidence(self):
        self.assertIn("red-sky painting",self.chapter)
        self.assertIn("withdrawn",self.chapter)
        self.assertIn("painted door",self.prose)
    def test_12_family_and_hosts_have_agency(self):
        for name in ("Sela","Nella","Tam","Fara","Veyra","Berrit","Sol","Eren","Meric","Hessa"):
            self.assertIn(name,self.prose)
        self.assertNotIn("Iven",self.chapter)
    def test_13_coin_debt_and_shelter_still_open(self):
        for phrase in ("four coins","Pell","Orrel","twenty-one nights","portable floor"):
            self.assertIn(phrase,self.chapter)
    def test_14_interiority_only_licensed_owner(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake",self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER",self.chapter)
        self.assertNotRegex(self.prose,r"(?<![A-Za-z])(?:Edrin|Edin)(?![A-Za-z])")
    def test_15_no_competitive_facts_asserted(self):
        self.assertNotIn("ESPN",self.prose)
        self.assertNotIn("Flaim",self.prose)
        self.assertNotRegex(self.prose,r"(?<![A-Za-z])Week [0-9]+(?![A-Za-z])")
    def test_16_protected_opening_unchanged(self):
        for path,sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT/path),sha)
    def test_17_historical_archive_unchanged(self):
        path=ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(git_blob(path),ARCHIVE_SHA)
    def test_18_sela_identity_not_falsely_joined(self):
        self.assertIn("earlier Sela net-mender",self.chapter)
        self.assertIn("NOT silently equated",self.chapter)
    def test_19_unknown_roads_not_resolved(self):
        self.assertIn("no route, arrival, salary",self.prose)
        self.assertIn("missing freight",self.chapter)
        self.assertIn("second horse",self.chapter)
    def test_20_no_release_or_independent_signoff_claim(self):
        for label in ("NONCANON / INDEPENDENT EDITORIAL HOLD","UNAUTHENTICATED","NO MERGE","NO CANON PROMOTION","NO PUBLICATION"):
            self.assertIn(label,self.chapter)

if __name__=="__main__":
    unittest.main()
