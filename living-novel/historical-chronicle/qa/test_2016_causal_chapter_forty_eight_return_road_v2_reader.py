"""Chapter XLVIII V2 original fiction and 45-part reader source-exact regression."""
import hashlib
import importlib.util
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/"living-novel/historical-chronicle/seasons/2016/causal-novel"
QA=Path(__file__).parent
ORIGINAL="THE_MORNING_OF_SMALL_LOAVES_CHAPTER_48_NONCANON.md"
SCENE="THE_MORNING_OF_SMALL_LOAVES_THE_RETURN_ROAD_CH48_V2_SCENE_NONCANON.md"
CHAPTER="THE_MORNING_OF_SMALL_LOAVES_THE_RETURN_ROAD_CH48_V2_NONCANON.md"
ORIGINAL_SHA="7641b297fa5ff72f79f67edaf3b5a8428c21bed7"
SCENE_SHA="3cd28ff1af7b513ee9580a3a3a223198c66f67a1"
CHAPTER_SHA="c41f2faee9f3889ee0f7b88e9aa29ec56e31ad34"
PRIOR_WORDS=339262
TOTAL_WORDS=347780

def blob(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def movements(text):
    return [m.group(1).strip() for m in re.finditer(r"(?ms)^### [IVX]+\. [^\n]+\n(.*?)(?=^### [IVX]+\.|^---\n|\Z)",text)]
def mod():
    spec=importlib.util.spec_from_file_location("reader_45",QA/"build_2016_causal_45_part_return_road_reader.py")
    out=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(out)
    return out

class ChapterXLVIIIReturnRoad(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old=(BASE/ORIGINAL).read_text(encoding="utf-8")
        cls.scene=(BASE/SCENE).read_text(encoding="utf-8")
        cls.new=(BASE/CHAPTER).read_text(encoding="utf-8")
        cls.builder=mod()
        cls.prior=cls.builder.prior_reader()
        cls.reader=cls.builder.build_from_repo()

    def test_01_old_source_pinned(self):
        self.assertEqual(blob((BASE/ORIGINAL).read_bytes()),ORIGINAL_SHA)
    def test_02_scene_source_pinned(self):
        self.assertEqual(blob((BASE/SCENE).read_bytes()),SCENE_SHA)
    def test_03_revision_source_pinned(self):
        self.assertEqual(blob((BASE/CHAPTER).read_bytes()),CHAPTER_SHA)
    def test_04_new_original_substantive(self):
        self.assertEqual(len(self.scene.split()),2679)
        self.assertGreaterEqual(len(self.scene.split()),2000)
    def test_05_revised_chapter_word_count(self):
        self.assertEqual(len(self.old.split()),5642)
        self.assertEqual(len(self.new.split()),8518)
    def test_06_seven_ordered_movements(self):
        self.assertEqual(re.findall(r"(?m)^### ([IVX]+)\.",self.new),
                         ["I","II","III","IV","V","VI","VII"])
    def test_07_all_six_old_movement_bodies_byte_exact(self):
        old=movements(self.old)
        new=movements(self.new)
        self.assertEqual(len(old),6)
        self.assertEqual(len(new),7)
        self.assertEqual(old,new[:5]+[new[6]])
    def test_08_new_scene_embedded_once(self):
        self.assertEqual(self.new.count(self.scene.strip()),1)
    def test_09_prev_manifest_preserved(self):
        rows=self.builder.rows(self.prior)
        self.assertEqual([r[0] for r in rows],list(range(1,45)))
        self.assertEqual(sum(r[3] for r in rows),PRIOR_WORDS)
    def test_10_45_manifest_source_exhaustive(self):
        rows=self.builder.rows(self.reader)
        self.assertEqual([r[0] for r in rows],list(range(1,46)))
        self.assertEqual(rows[-1],(45,CHAPTER,CHAPTER_SHA,8518))
        self.assertEqual(sum(r[3] for r in rows),TOTAL_WORDS)
    def test_11_45_marker_pairs(self):
        self.assertEqual(self.reader.count(self.builder.BEGIN),45)
        self.assertEqual(self.reader.count(self.builder.END),45)
        self.assertEqual(self.reader.count(self.builder.TERMINAL),1)
    def test_12_previous_44_sections_unchanged(self):
        prior_body=self.prior[self.prior.index(self.builder.BEGIN):self.prior.index(self.builder.TERMINAL)].rstrip()
        start=f"{self.builder.BEGIN}{CHAPTER} | git_blob {CHAPTER_SHA} -->"
        revised_body=self.reader[self.reader.index(self.builder.BEGIN):self.reader.index(start)].rstrip()
        self.assertEqual(prior_body,revised_body)
    def test_13_embedded_new_chapter_exact(self):
        start=f"{self.builder.BEGIN}{CHAPTER} | git_blob {CHAPTER_SHA} -->"
        end=f"{self.builder.END}{CHAPTER} -->"
        self.assertEqual(self.reader.split(start+"\n\n",1)[1].split("\n\n"+end,1)[0],
                         self.new.rstrip("\n"))
    def test_14_corrupt_new_source_fails_closed(self):
        with self.assertRaises(ValueError):
            self.builder.build(self.prior,self.new+"x")
    def test_15_corrupt_prior_manifest_fails_closed(self):
        with self.assertRaises(ValueError):
            self.builder.build(self.prior.replace("339262","999999",1),self.new)
    def test_16_missing_prior_marker_fails_closed(self):
        with self.assertRaises(ValueError):
            self.builder.build(self.prior.replace(self.builder.BEGIN,"",1),self.new)
    def test_17_only_proposed_jake_interior(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake",self.new)
        for name in ("Edrin","Edin","Garran thought","Fara knew secretly","the driver remembered"):
            self.assertNotIn(name,self.scene)
    def test_18_historical_league_fact_firewall(self):
        for term in ("ESPN","Flaim","standings","playoff","Week 12","final score"):
            self.assertNotIn(term,self.scene)
        self.assertIn("NOT provider-authenticated",self.new)
    def test_19_2016_archive_pinned(self):
        archive=ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(blob(archive.read_bytes()),"6dbec1fe2537139f3a97c6a78250e2bae082a518")
    def test_20_protected_2026_main_pinned(self):
        protected={
         "PROLOGUE_DRAFT_V1.md":"5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
         "CHAPTER_01_THE_FIRST_ANSWER.md":"26a17f05eb0565e7648c29add03ee9580ec933c3",
         "CHAPTER_02_WHAT_COMES_BACK.md":"30fcf23a3eb8872fa0fb4dff029fe30044141121",
         "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md":"49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc"
        }
        for name,sha in protected.items():
            with self.subTest(name=name):
                self.assertEqual(blob((ROOT/"living-novel/manuscript"/name).read_bytes()),sha)
    def test_21_driver_keeps_agency_and_damage_outstanding(self):
        for phrase in ("The driver did not leave with Garran's coins.","Half to begin","inspection","damaged sack","no knowing"):
            self.assertIn(phrase,self.scene)
        self.assertIn("partial voluntary restitution",self.old)
    def test_22_release_and_editorial_holds_explicit(self):
        for phrase in ("NONCANON","INDEPENDENT EDITORIAL HOLD","NO MERGE","NO CANON PROMOTION","NO PUBLICATION"):
            self.assertIn(phrase,self.new)
        self.assertNotIn("CANON RELEASE APPROVED",self.new)

if __name__=="__main__":unittest.main()
