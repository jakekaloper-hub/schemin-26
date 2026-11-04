"""Chapter XXXVII V2: source exact 34-part reader and Orin/Rovan continuity tests; NONCANON."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
OLD = "THE_COMPANY_THAT_CAME_APART_CHAPTER_37_NONCANON.md"
SCENE = "THE_EMPTY_PLACE_AT_THE_SECOND_TABLE_CH37_INTERLUDE_V2_NONCANON.md"
CHAPTER = "THE_COMPANY_THAT_CAME_APART_THE_EMPTY_PLACE_AT_SECOND_TABLE_CH37_V2_NONCANON.md"
PREVIOUS = "READING_COPY_2016_CAUSAL_CH01_36_THIRTY_THREE_PARTS_WHOLE_OF_FOURTEEN_NONCANON.md"
READER = "READING_COPY_2016_CAUSAL_CH01_37_THIRTY_FOUR_PARTS_EMPTY_SECOND_TABLE_NONCANON.md"
OLD_SHA = "92aba7618d9d7a5ba88758be48084ded30eca4ba"
SCENE_SHA = "f64925f00534f9e736ac65c6d5ebb9b95334eb8a"
CHAPTER_SHA = "655d437756306ee5386b7d8fa4b825ebb5f33ab5"
PREVIOUS_SHA = "d3aaf9f6577934a4d360ededcc2426509fb2c6e3"
READER_SHA = "63d9fcbc3f5fb76438882ca26b5da8b8f821a575"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
TOTAL_WORDS = 250940
CHAPTER_WORDS = 8709
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
def gitblob(p):
    data = p.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\\0" + data).hexdigest()
def rows(s):
    return [(int(n), f, sha, int(w)) for n,f,sha,w in re.findall(
        r"^\\| (\\d+) \\| \\x60([^\\x60]+)\\x60 \\| \\x60([a-f0-9]{40})\\x60 \\| (\\d+) \\|$",s,re.M)]
def component(s, name, sha):
    a = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->\\n\\n"
    b = f"\\n\\n<!-- END 2016_CAUSAL {name} -->"
    assert s.count(a)==s.count(b)==1, name
    return s.split(a,1)[1].split(b,1)[0]
class ChapterThirtySevenV2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old=(BASE/OLD).read_text()
        cls.scene=(BASE/SCENE).read_text()
        cls.chapter=(BASE/CHAPTER).read_text()
        cls.previous=(BASE/PREVIOUS).read_text()
        cls.reader=(BASE/READER).read_text()
        cls.oldrows=rows(cls.previous)
        cls.newrows=rows(cls.reader)
        cls.prose=cls.chapter.split("### I.",1)[1].split("\\n---\\n",1)[0]
    def test_01_old_chapter_preserved(self): self.assertEqual(gitblob(BASE/OLD),OLD_SHA)
    def test_02_scene_preserved(self): self.assertEqual(gitblob(BASE/SCENE),SCENE_SHA)
    def test_03_new_chapter_blob(self): self.assertEqual(gitblob(BASE/CHAPTER),CHAPTER_SHA)
    def test_04_prior_reader_preserved(self): self.assertEqual(gitblob(BASE/PREVIOUS),PREVIOUS_SHA)
    def test_05_reader_blob(self): self.assertEqual(gitblob(BASE/READER),READER_SHA)
    def test_06_six_original_movements(self):
        self.assertEqual(re.findall(r"^### ([IVX]+)\\. ",self.chapter,re.M),["I","II","III","IV","V","VI"])
        for line in ("The ash did not leave the tiles", "The travelers stayed in the back room", "The first cut made a sound", "The narrow cart would depart at first light", "Fara's gate stood open"):
            self.assertIn(line,self.chapter)
    def test_07_substantive_scene_and_exact_body(self):
        heading="### Interlude — The empty place at the second table"
        scene=heading+self.scene.split(heading,1)[1].split("\\n---\\n\\n**Provenance",1)[0].rstrip()
        self.assertGreaterEqual(len(scene.split()),2000)
        self.assertIn(scene,self.chapter)
        self.assertLess(self.chapter.index("### IV. "),self.chapter.index(heading))
        self.assertLess(self.chapter.index(heading),self.chapter.index("### V. "))
    def test_08_child_and_adult_are_distinct(self):
        self.assertIn("Rovan held the reins",self.chapter)
        self.assertNotIn("Orin held the reins",self.chapter)
        self.assertIn("Orin carried his bird cage",self.chapter)
        self.assertIn("Rovan checked the narrow cart",self.chapter)
        prev=(BASE/"THE_ASH_AT_FARAS_DOOR_THE_WHOLE_OF_FOURTEEN_CH36_V2_NONCANON.md").read_text()
        nxt=(BASE/"THE_HAND_THAT_CUT_THE_LEATHER_CHAPTER_38_NONCANON.md").read_text()
        self.assertIn("a boy of perhaps twelve",prev)
        self.assertIn("Orin watched her needle",nxt)
    def test_09_only_permitted_jake_interior(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake",self.chapter)
        for x in ("Edrin thought","Edin knew","Hessa thought","Fara wondered","Rovan believed"):
            self.assertNotIn(x,self.prose)
    def test_10_split_eight_six(self):
        self.assertIn("Eight want to go while the road is passable",self.chapter)
        self.assertIn("Six will stay another night",self.chapter)
        self.assertIn("The baby stayed with the six",self.chapter)
    def test_11_awning_loss_unchanged(self):
        for x in ("the old awning will no longer reach the outer post", "She drew the line herself", "The faded flower was upside down"):
            self.assertIn(x,self.chapter)
    def test_12_source_manifest_34(self):
        self.assertEqual([n for n,*_ in self.newrows],list(range(1,35)))
        self.assertEqual(self.newrows[:33],self.oldrows)
        self.assertEqual(self.newrows[-1],(34,CHAPTER,CHAPTER_SHA,CHAPTER_WORDS))
    def test_13_markers_balanced(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "),34)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "),34)
    def test_14_every_part_exact(self):
        for n,f,sha,w in self.newrows:
            with self.subTest(part=n):
                self.assertEqual(gitblob(BASE/f),sha)
                src=(BASE/f).read_text()
                self.assertEqual(len(src.split()),w)
                self.assertEqual(component(self.reader,f,sha),src.rstrip("\\n"))
    def test_15_old_bodies_exact(self):
        for _,f,sha,_ in self.oldrows:
            with self.subTest(file=f):
                self.assertEqual(component(self.previous,f,sha),component(self.reader,f,sha))
    def test_16_component_words(self):
        self.assertEqual(len(self.chapter.split()),CHAPTER_WORDS)
        self.assertEqual(sum(w for _,_,_,w in self.newrows),TOTAL_WORDS)
        self.assertIn(f"Source component words including metadata: {TOTAL_WORDS}",self.reader)
    def test_17_historical_evidence_unchanged(self):
        self.assertEqual(gitblob(ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"),ARCHIVE_SHA)
    def test_18_protected_2026_files(self):
        for f,sha in PROTECTED.items():
            with self.subTest(file=f): self.assertEqual(gitblob(ROOT/f),sha)
    def test_19_release_gates(self):
        for marker in ("NONCANON","NO MERGE","NO PUBLICATION","NO CANON PROMOTION"):
            self.assertIn(marker,self.reader)
    def test_20_no_invented_historical_disposition(self):
        self.assertIn("not a historical 2016 fire",self.chapter.lower())
        self.assertIn("The cause of the ash was still unknown",self.chapter)
        self.assertIn("older shelter",self.reader.lower())
if __name__=="__main__": unittest.main()
