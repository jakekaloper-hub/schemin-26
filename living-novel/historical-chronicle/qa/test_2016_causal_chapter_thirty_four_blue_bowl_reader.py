"""Chapter XXXIV V2: mechanical checks for 31-part NONCANON reader, NOT independent editorial approval."""
import hashlib
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/"living-novel/historical-chronicle/seasons/2016/causal-novel"
NEW="THE_BEES_IN_THE_WEDDING_ARCH_BLUE_BOWL_AT_STAIR_CH34_V2_NONCANON.md"
OLD="THE_BEES_IN_THE_WEDDING_ARCH_CHAPTER_34_NONCANON.md"
READER="READING_COPY_2016_CAUSAL_CH01_34_THIRTY_ONE_PARTS_BLUE_BOWL_NONCANON.md"
PRIOR="READING_COPY_2016_CAUSAL_CH01_33_THIRTY_PARTS_BRANCHES_ABOVE_GATE_NONCANON.md"
NEW_SHA="13db26031b0f821318eee1e586633691f85a3411"
OLD_SHA="6793680804005b9af165cf26b63d1d52c34c233e"
READER_SHA="5424afc1de335b3dd3c2920013751c95a16090f4"
PRIOR_SHA="1d8a7fb08f7111d222887ec7d97d18db2dd54151"
ARCHIVE_SHA="6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED={
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
def blob(path):
    data=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def rows(s):
    return [(int(n),name,sha,int(words)) for n,name,sha,words in re.findall(
       r"^\| (\d+) \| \x60([^\x60]+)\x60 \| \x60([a-f0-9]{40})\x60 \| (\d+) \|$",s,re.M)]
def body(s,name,sha):
    a=f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->\n\n"
    b=f"\n\n<!-- END 2016_CAUSAL {name} -->"
    assert s.count(a)==1 and s.count(b)==1, name
    return s.split(a,1)[1].split(b,1)[0]
class ChapterThirtyFourBlueBowl(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter=(BASE/NEW).read_text()
        cls.orig=(BASE/OLD).read_text()
        cls.reader=(BASE/READER).read_text()
        cls.prior=(BASE/PRIOR).read_text()
        cls.rows=rows(cls.reader)
        cls.oldrows=rows(cls.prior)
        cls.scene="### VI. The blue bowl at the stair"+cls.chapter.split("### VI. The blue bowl at the stair",1)[1].split("\n\n---\n\n### Editorial handoff",1)[0]
    def test_01_new_chapter_blob(self):
        self.assertEqual(blob(BASE/NEW),NEW_SHA)
    def test_02_original_chapter_untouched(self):
        self.assertEqual(blob(BASE/OLD),OLD_SHA)
    def test_03_prior_reader_untouched(self):
        self.assertEqual(blob(BASE/PRIOR),PRIOR_SHA)
    def test_04_new_reader_blob(self):
        self.assertEqual(blob(BASE/READER),READER_SHA)
    def test_05_six_movements(self):
        self.assertEqual(re.findall(r"^### ([IVX]+)\. ",self.chapter,re.M),["I","II","III","IV","V","VI"])
    def test_06_old_movement_bodies_still_source_exact(self):
        old=self.orig.split("### I. An ordinary morning beneath an extraordinary weight",1)[1].split("\n---\n\n### Editorial handoff",1)[0]
        self.assertIn(old,self.chapter)
    def test_07_substantial_sixth_movement(self):
        self.assertGreaterEqual(len(self.scene.split()),1900)
        for phrase in ("You can't withdraw a roof","She had drawn what the bowl allowed her to observe","No message had come from Mev","Mara"):
            self.assertIn(phrase,self.scene)
    def test_08_pov_and_authentication_firewall(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake",self.chapter)
        self.assertIn("UNAUTHENTICATED",self.chapter)
        self.assertIn("secondary-world invention",self.chapter)
        for forbidden in ("Edrin","Edin","ESPN final","2026 championship belt"):
            self.assertNotIn(forbidden,self.scene)
    def test_09_open_loops(self):
        for p in ("letter","Pell","freight","kiln","unconfirmed","no wedding"):
            self.assertIn(p.lower(),self.chapter.lower())
    def test_10_source_manifest_31_parts(self):
        self.assertEqual([n for n,*_ in self.rows],list(range(1,32)))
        self.assertEqual(self.rows[-1],(31,NEW,NEW_SHA,9996))
    def test_11_previous_30_manifest_unchanged(self):
        self.assertEqual(self.rows[:30],self.oldrows)
    def test_12_balanced_component_markers(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "),31)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "),31)
    def test_13_all_31_components_source_exact(self):
        for n,name,sha,w in self.rows:
            with self.subTest(part=n):
                source=(BASE/name).read_text()
                self.assertEqual(blob(BASE/name),sha)
                self.assertEqual(len(source.split()),w)
                self.assertEqual(body(self.reader,name,sha),source.rstrip("\n"))
    def test_14_previous_30_component_bodies_unchanged(self):
        for n,name,sha,w in self.oldrows:
            with self.subTest(part=n):
                self.assertEqual(body(self.reader,name,sha),body(self.prior,name,sha))
    def test_15_total_words(self):
        self.assertEqual(len(self.chapter.split()),9996)
        self.assertEqual(sum(w for *_,w in self.rows),224038)
        self.assertIn("Source component words including metadata: 224038",self.reader)
    def test_16_archive_unchanged(self):
        self.assertEqual(blob(ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"),ARCHIVE_SHA)
    def test_17_protected_hard_canon_unchanged(self):
        for p,sha in PROTECTED.items():
            with self.subTest(path=p):
                self.assertEqual(blob(ROOT/p),sha)
    def test_18_next_chapter_retains_pell_return(self):
        nxt=(BASE/"THE_COAT_THAT_DID_NOT_BELONG_CHAPTER_35_NONCANON.md").read_text()
        self.assertIn("The man on the upper steps was wearing a coat too large for him.",nxt)
        self.assertIn("Pell",nxt)
        self.assertIn("the wedding between Lysa and Corin never took place",nxt)
    def test_19_arch_33_to_34_geography(self):
        prev=(BASE/"THE_FEAST_WITH_NO_VOWS_BRANCHES_ABOVE_GATE_CH33_V2_NONCANON.md").read_text()
        self.assertIn("The bound branches remained above the gate",prev)
        self.assertIn("Bees had gathered on the central branch",self.chapter)
        self.assertIn("the gate stood where it always had",self.chapter)
    def test_20_noncanonical_release_holds(self):
        self.assertIn("NO MERGE / NO PUBLICATION / NO CANON PROMOTION",self.reader)
        self.assertIn("FOUNDER-ONLY CANON & PUBLICATION APPROVAL",self.reader)
        self.assertIn("INDEPENDENT EDITORIAL HOLD",self.chapter)
    def test_21_no_new_false_2016_matchup_fact(self):
        for p in ("scoring slot remains UNAUTHENTICATED","No new historical league facts"):
            self.assertIn(p,self.reader)
    def test_22_new_characters_not_canon_owners(self):
        self.assertIn("Seli, Mara, their mother",self.chapter)
        self.assertIn("invented fictional supporting-world details",self.chapter)
        self.assertNotIn("Mara's interior",self.chapter)
if __name__=="__main__":
    unittest.main()
