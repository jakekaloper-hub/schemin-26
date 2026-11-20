"""2016 Chapter XLIII V2: 40-part reading source, historical and POV firewalls."""
import unittest
import re
import hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
ORIGINAL="THE_NAME_HE_SOLD_CHAPTER_43_NONCANON.md"
SCENE="THE_NAME_HE_SOLD_THREAD_WITH_NO_DIRECTION_CH43_V2_SCENE_NONCANON.md"
CHAPTER="THE_NAME_HE_SOLD_THREAD_WITH_NO_DIRECTION_CH43_V2_NONCANON.md"
PRIOR="READING_COPY_2016_CAUSAL_CH01_42_THIRTY_NINE_PARTS_SILENT_ENDING_NONCANON.md"
READER="READING_COPY_2016_CAUSAL_CH01_43_FORTY_PARTS_THREAD_NO_DIRECTION_NONCANON.md"
SHAS={
  "THE_NAME_HE_SOLD_CHAPTER_43_NONCANON.md": "c4e3705531e1c4589ac95845df15ccc108da6fd3",
  "THE_NAME_HE_SOLD_THREAD_WITH_NO_DIRECTION_CH43_V2_SCENE_NONCANON.md": "678c9a73f270135811fa4d6ac7c8cea3749ec5f2",
  "THE_NAME_HE_SOLD_THREAD_WITH_NO_DIRECTION_CH43_V2_NONCANON.md": "21b5acd9cef84784dfa66a74fe8c1b752c3fc537",
  "READING_COPY_2016_CAUSAL_CH01_42_THIRTY_NINE_PARTS_SILENT_ENDING_NONCANON.md": "6b4fb8e8fc939d55553953480879380b9ba6d3a8",
  "READING_COPY_2016_CAUSAL_CH01_43_FORTY_PARTS_THREAD_NO_DIRECTION_NONCANON.md": "0519fc6ef7f81787acb2a239fc9072c5dfb62beb"
}
PROTECTED={
  "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
  "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
  "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
  "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc"
}

def gitblob(p):
    data=p.read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def rows(s):
    pat=r"^\| (\d+) \| \x60([^\x60]+)\x60 \| \x60([a-f0-9]{40})\x60 \| (\d+) \|$"
    return [(int(i),name,sha,int(words)) for i,name,sha,words in re.findall(pat,s,re.M)]

def block(doc,name,sha):
    a="<!-- BEGIN 2016_CAUSAL "+name+" | git_blob "+sha+" -->"
    b="<!-- END 2016_CAUSAL "+name+" -->"
    assert doc.count(a)==1 and doc.count(b)==1
    return doc.split(a+"\n\n",1)[1].split("\n\n"+b,1)[0]

class TestFortyThreeThreadV2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src=(BASE/ORIGINAL).read_text()
        cls.scene=(BASE/SCENE).read_text()
        cls.chapter=(BASE/CHAPTER).read_text()
        cls.prior=(BASE/PRIOR).read_text()
        cls.reader=(BASE/READER).read_text()
        cls.prev=rows(cls.prior)
        cls.current=rows(cls.reader)
    def test_01_pinned_blob_shas(self):
        for name,sha in SHAS.items():
            with self.subTest(name=name):
                self.assertEqual(gitblob(BASE/name),sha)
    def test_02_substantial_scene(self):
        self.assertEqual(len(self.scene.split()),2260)
    def test_03_exact_movement_order(self):
        self.assertEqual(re.findall(r"^### ([IVX]+)\.",self.chapter,re.M),
                         ["I","II","III","IV","V","VI","VII"])
    def test_04_old_six_movement_text_unchanged(self):
        def narrative(s):
            return s.split("### I.",1)[1].split("\n---\n\n### Editorial handoff",1)[0]
        restored=narrative(self.chapter).replace(self.scene.rstrip()+"\n\n","")
        restored=restored.replace("### V. The eight coins","### IV. The eight coins")
        restored=restored.replace("### VI. The weight of a true answer","### V. The weight of a true answer")
        restored=restored.replace("### VII. A correction that could not travel faster","### VI. A correction that could not travel faster")
        self.assertEqual(restored,narrative(self.src))
    def test_05_scene_once(self):
        self.assertEqual(self.chapter.count(self.scene.rstrip()),1)
    def test_06_40_part_manifest(self):
        self.assertEqual(len(self.prev),39)
        self.assertEqual(len(self.current),40)
        self.assertEqual(self.current[:39],self.prev)
        self.assertEqual(self.current[39],(40,CHAPTER,SHAS[CHAPTER],9424))
    def test_07_prior_39_embeds_preserved(self):
        for n,name,sha,w in self.prev:
            with self.subTest(part=n):
                self.assertEqual(block(self.reader,name,sha),block(self.prior,name,sha))
    def test_08_all_40_sources_exact(self):
        for n,name,sha,w in self.current:
            with self.subTest(part=n):
                data=(BASE/name).read_text().rstrip("\n")
                self.assertEqual(gitblob(BASE/name),sha)
                self.assertEqual(block(self.reader,name,sha),data)
                self.assertEqual(len(data.split()),w)
    def test_09_source_words(self):
        self.assertEqual(len(self.chapter.split()),9424)
        self.assertEqual(sum(x[3] for x in self.current),307670)
    def test_10_reader_counts(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "),40)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "),40)
    def test_11_reader_has_new_total(self):
        self.assertIn("Source component words including metadata: 307670",self.reader)
    def test_12_owner_pov_explicit(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake",self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER",self.chapter)
    def test_13_no_supporting_character_interior(self):
        for phrase in ("Hessa thought","Orin knew","Ina wondered","Sela remembered","Edin recalled","Edrin felt"):
            self.assertNotIn(phrase,self.scene)
    def test_14_hessa_agency_and_unknown_sister(self):
        for phrase in ("Hessa","Orin","sister","twine","Ina","twenty-one"):
            self.assertIn(phrase,self.scene.lower() if phrase=="twenty-one" else self.scene)
    def test_15_no_unsupported_sports_records(self):
        for phrase in ("ESPN","Flaim","playoff","championship","standings"):
            self.assertNotIn(phrase,self.scene)
    def test_16_protected_hard_canon_blobs(self):
        for name,sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(gitblob(ROOT/name),sha)
    def test_17_2016_evidence_blob_unchanged(self):
        f=ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(gitblob(f),"6dbec1fe2537139f3a97c6a78250e2bae082a518")
    def test_18_explicit_holds(self):
        for flag in ("NONCANON","UNAUTHENTICATED","NO MERGE","NO CANON PROMOTION","NO PUBLICATION"):
            self.assertIn(flag,self.chapter)
            self.assertIn(flag,self.reader)
    def test_19_false_witness_not_erased(self):
        for phrase in ("eight coins","false","correction","second horse"):
            self.assertIn(phrase,self.chapter)
    def test_20_independent_gate_not_self_certified(self):
        for phrase in ("Authors Council","Umpire","Founder"):
            self.assertIn(phrase,self.reader)
if __name__ == "__main__":
    unittest.main()
