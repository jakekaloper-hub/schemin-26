"""Noncanonical Chapter XLVI source-exact assembly, continuity and protected-canon checks."""
import hashlib
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/"living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER="THE_DISTANCE_BETWEEN_TWO_GATES_CHAPTER_46_NONCANON.md"
READER="READING_COPY_CAUSAL_CHAPTERS_01_46_NONCANON.md"
PREVIOUS="READING_COPY_CAUSAL_CHAPTERS_01_45_NONCANON.md"
CHAPTER_SHA="9c866df37a5bebe0b244b55921e1bf28aa75e06d"
READER_SHA="5fcde1cc30adfe9f05aa6a331256626d2856e8f3"
PREVIOUS_SHA="de28a89a8624479a9f5af202968edadc7c7fecdd"
ARCHIVE_SHA="6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED={
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md":"5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md":"26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md":"30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md":"49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc"
}
def git_blob(p):
    b=p.read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def rows(text):
    matches=re.findall(r"^\| ([0-9]+) \| `([^`]+)` \| `([0-9a-f]{40})` \| ([0-9]+) \|$",text,re.M)
    return [(int(n),name,sha,int(words)) for n,name,sha,words in matches]
def section(reader,name,sha):
    start=f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    end=f"<!-- END 2016_CAUSAL {name} -->"
    assert reader.count(start)==reader.count(end)==1,(name,reader.count(start),reader.count(end))
    return reader.split(start,1)[1].split(end,1)[0].strip()
class FortySixChapterReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter=(BASE/CHAPTER).read_text()
        cls.reader=(BASE/READER).read_text()
        cls.prev=(BASE/PREVIOUS).read_text()
        cls.rows=rows(cls.reader)
        cls.prevrows=rows(cls.prev)
        cls.prose=cls.chapter.split("### I.",1)[1].split("\n---\n",1)[0]
    def test_01_manifest_seq(self):
        self.assertEqual([x[0] for x in self.rows],list(range(1,47)))
        self.assertEqual(self.rows[-1],(46,CHAPTER,CHAPTER_SHA,5586))
    def test_02_markers(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "),46)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "),46)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"),1)
    def test_03_source_exact_all_chapters(self):
        for n,name,sha,words in self.rows:
            with self.subTest(ch=n):
                self.assertEqual(section(self.reader,name,sha),(BASE/name).read_text().strip())
                self.assertEqual(len((BASE/name).read_text().split()),words)
    def test_04_all_git_blob_hashes(self):
        for n,name,sha,words in self.rows:
            with self.subTest(ch=n):
                self.assertEqual(git_blob(BASE/name),sha)
    def test_05_previous_reader_immutable(self):
        self.assertEqual(git_blob(BASE/PREVIOUS),PREVIOUS_SHA)
        self.assertEqual(self.rows[:45],self.prevrows)
        for n,name,sha,words in self.prevrows:
            with self.subTest(ch=n):
                self.assertEqual(section(self.reader,name,sha),section(self.prev,name,sha))
    def test_06_current_sha(self):
        self.assertEqual(git_blob(BASE/CHAPTER),CHAPTER_SHA)
        self.assertEqual(git_blob(BASE/READER),READER_SHA)
    def test_07_length_six_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+[.]",self.chapter,re.M)),6)
        self.assertEqual(len(self.chapter.split()),5586)
        self.assertGreater(len(self.prose.split()),5000)
        self.assertEqual(len(self.reader.split()),269566)
    def test_08_reader_hold(self):
        self.assertTrue(self.reader.startswith("# 2016 Commonwealth — Causal Novel Reading Copy, Chapters I–XLVI (NONCANON)"))
        self.assertIn("Forty-six fully assembled",self.reader)
        self.assertIn("independent Authors Council/Umpire review",self.reader)
    def test_09_causal_turn(self):
        self.assertIn("**Chapter XLVI turn:**",self.reader)
        self.assertIn("Nella sees the river",self.reader)
    def test_10_no_unauthorized_map(self):
        self.assertIn("draws a memory rather than a certified map",self.reader)
        self.assertIn("No route certified",self.prose)
        self.assertIn("No approved Commonwealth route",self.chapter)
    def test_11_child_agency(self):
        for phrase in ("Nella","Tam","Sela","the rise","the river","the gate","Lysa","Corin"):
            self.assertIn(phrase,self.prose)
    def test_12_bounded_return(self):
        self.assertIn("come back before dark",self.prose)
        self.assertIn("we came back",self.prose.lower())
        self.assertIn("not a new family home",self.reader)
    def test_13_fictions_not_historical_claims(self):
        self.assertIn("NOT provider-authenticated",self.chapter)
        self.assertIn("proposed secondary-world fiction",self.chapter)
        self.assertNotIn("ESPN",self.prose)
        self.assertNotIn("Flaim",self.prose)
    def test_14_limited_interior(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake",self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER",self.chapter)
        self.assertNotRegex(self.prose,r"(?<![A-Za-z])(?:Edrin|Edin)(?![A-Za-z])")
    def test_15_material_debt(self):
        for phrase in ("four remain","Pell","Orrel","twenty-one-night","Fara","shortened"):
            self.assertIn(phrase,self.chapter)
    def test_16_unresolved_sela_identity(self):
        self.assertIn("Sela name references remain distinct and unresolved",self.chapter)
        self.assertNotIn("Sela the net-mender was",self.chapter)
    def test_17_2026_protected(self):
        for p,sha in PROTECTED.items():
            with self.subTest(path=p):
                self.assertEqual(git_blob(ROOT/p),sha)
    def test_18_2016_archive_protected(self):
        self.assertEqual(git_blob(ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"),ARCHIVE_SHA)
    def test_19_visiting_troupe_departed(self):
        self.assertIn("Veyra's company remained somewhere outside Jake's sight",self.prose)
        self.assertNotIn("the performers returned",self.prose)
    def test_20_no_promotion(self):
        qa=(BASE/"CHAPTER_46_SOURCE_EDITORIAL_QA_RECEIPT.md").read_text()
        for gate in ("NO MERGE","NO CANON PROMOTION","NO PUBLICATION"):
            self.assertIn(gate,qa)
        self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD",self.chapter)
if __name__=="__main__":
    unittest.main()
