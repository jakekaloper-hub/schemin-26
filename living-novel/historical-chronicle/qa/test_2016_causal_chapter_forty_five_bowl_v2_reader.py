"""Chapter XLV V2 source-exact assembly, literature continuity and no-promotion gate.
These deterministic assertions are not an independent Authors Council/Umpire review.
"""
import hashlib
import importlib.util
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
ORIGINAL = "THE_ROAD_THAT_WOULD_NOT_WAIT_CHAPTER_45_NONCANON.md"
SCENE = "THE_ROAD_THAT_WOULD_NOT_WAIT_MEASURE_OF_EMPTY_BOWL_CH45_V2_SCENE_NONCANON.md"
CHAPTER = "THE_ROAD_THAT_WOULD_NOT_WAIT_MEASURE_OF_EMPTY_BOWL_CH45_V2_NONCANON.md"
PREV_CHAPTER = "THE_FLOOR_THAT_COULD_BE_LIFTED_BOOT_AT_THE_THRESHOLD_CH44_V2_NONCANON.md"
PAIR = "READING_COPY_2016_CAUSAL_CH44_45_TWO_CHAPTERS_BOWL_NONCANON.md"
PREVIOUS = "READING_COPY_2016_CAUSAL_CH01_44_FORTY_ONE_PARTS_BOOT_THRESHOLD_NONCANON.md"
SHA = {
    ORIGINAL: "8c36678412071e935fd6b7bf0c469a04386f6588",
    SCENE: "e5651840d264b5383d4412aaada474b976a11e86",
    CHAPTER: "60a1dfaa6e327e4cfa28aa70b4b222929ee751b8",
    PREV_CHAPTER: "d450ee2b725201f6d1660613b5880450f63c62d6",
    PAIR: "ccd1368e95b2168aa0c8eb5913b98bd6ba854cf6",
    PREVIOUS: "b8ea32a932cfeeebc0f5f359ed90eed0a776918d",
}
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
def gitblob(path):
    data=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def body_parts(doc):
    narr=doc.split("\n---\n",1)[0]
    return [x.strip() for x in re.split(r"(?m)^### [IVX]+\. [^\n]+\n",narr)[1:]]
def embed(doc,name,sha):
    a=f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    b=f"<!-- END 2016_CAUSAL {name} -->"
    assert doc.count(a)==1 and doc.count(b)==1
    return doc.split(a+"\n\n",1)[1].split("\n\n"+b,1)[0]
def rows(doc):
    p=r"(?m)^\| ([0-9]+) \| `([^`]+)` \| `([a-f0-9]{40})` \| ([0-9]+) \|$"
    return [(int(a),b,c,int(d)) for a,b,c,d in re.findall(p,doc)]
def load_builder():
    path=Path(__file__).with_name("build_2016_causal_42_part_bowl_reader.py")
    spec=importlib.util.spec_from_file_location("historical_42_builder",path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class Test2016Chapter45Bowl(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original=(BASE/ORIGINAL).read_text()
        cls.scene=(BASE/SCENE).read_text().rstrip("\n")
        cls.chapter=(BASE/CHAPTER).read_text()
        cls.prior=(BASE/PREV_CHAPTER).read_text()
        cls.pair=(BASE/PAIR).read_text()
        cls.previous=(BASE/PREVIOUS).read_text()
        cls.builder=load_builder()
        cls.generated=cls.builder.build_from_repo()
    def test_01_all_source_blobs_pinned(self):
        for n,sha in SHA.items():
            with self.subTest(n=n): self.assertEqual(gitblob(BASE/n),sha)
    def test_02_scene_substantial(self): self.assertGreaterEqual(len(self.scene.split()),2400)
    def test_03_v2_word_count(self): self.assertEqual(len(self.chapter.split()),7275)
    def test_04_original_word_count(self): self.assertEqual(len(self.original.split()),4664)
    def test_05_seven_movements(self):
        self.assertEqual(re.findall(r"(?m)^### ([IVX]+)\. ",self.chapter),["I","II","III","IV","V","VI","VII"])
    def test_06_six_prior_prose_movements_preserved(self):
        old=body_parts(self.original)
        new=body_parts(self.chapter)
        self.assertEqual(len(old),6)
        self.assertEqual(len(new),7)
        self.assertEqual(old,[new[0]]+new[2:])
    def test_07_scene_inserted_once(self): self.assertEqual(self.chapter.count(self.scene),1)
    def test_08_jake_only_principal_pov(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake",self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER",self.chapter)
        self.assertNotRegex(self.scene,r"\b(Edrin|Edin)\b")
    def test_09_no_stolen_supporting_interior(self):
        for t in ("Fara thought","Veyra knew","Sela wondered","Sol remembered","Berrit realized","Nella thought","Tam wondered"):
            with self.subTest(t=t): self.assertNotIn(t,self.scene)
    def test_10_trade_and_performance_boundaries(self):
        for token in ("voluntary", "Berrit", "Sol", "Veyra", "Fara", "Sela", "Nella", "lamp", "bowl"):
            self.assertIn(token,self.scene)
    def test_11_no_historical_score_invention(self):
        for t in ("ESPN","Flaim","standings","playoffs","Week 1","Week 2","championship"):
            self.assertNotIn(t,self.scene)
    def test_12_existing_41_part_reader_frozen(self):
        self.assertEqual(gitblob(BASE/PREVIOUS),SHA[PREVIOUS])
        self.assertEqual(len(rows(self.previous)),41)
    def test_13_adjacent_chapter_proof_source_exact(self):
        self.assertEqual(embed(self.pair,PREV_CHAPTER,SHA[PREV_CHAPTER]),self.prior.rstrip("\n"))
        self.assertEqual(embed(self.pair,CHAPTER,SHA[CHAPTER]),self.chapter.rstrip("\n"))
    def test_14_adjacent_chapter_proof_count(self):
        self.assertEqual(self.pair.count("<!-- BEGIN 2016_CAUSAL "),2)
        self.assertEqual(self.pair.count("<!-- END 2016_CAUSAL "),2)
    def test_15_full_developmental_reader_manifest(self):
        self.assertEqual([r[0] for r in rows(self.generated)],list(range(1,43)))
        self.assertEqual(rows(self.generated)[-1],(42,CHAPTER,SHA[CHAPTER],7275))
    def test_16_full_developmental_reader_source_exact(self):
        self.assertEqual(embed(self.generated,CHAPTER,SHA[CHAPTER]),self.chapter.rstrip("\n"))
        self.assertEqual(self.generated.count("<!-- BEGIN 2016_CAUSAL "),42)
        self.assertEqual(self.generated.count("<!-- END 2016_CAUSAL "),42)
    def test_17_preceding_41_components_are_preserved(self):
        for number,name,sha,words in rows(self.previous):
            with self.subTest(chapter=number):
                self.assertEqual(embed(self.generated,name,sha),embed(self.previous,name,sha))
    def test_18_42_part_word_count(self):
        self.assertEqual(sum(row[3] for row in rows(self.generated)),323490)
        self.assertIn("Source component words including metadata: 323490",self.generated)
    def test_19_fail_closed_on_missing_preceding_component(self):
        marker=f"<!-- END 2016_CAUSAL {PREV_CHAPTER} -->"
        with self.assertRaises(ValueError): self.builder.build(self.previous.replace(marker,""),self.chapter)
    def test_20_fail_closed_on_corrupted_chapter(self):
        with self.assertRaises(ValueError): self.builder.build(self.previous,self.chapter+" ALTERED")
    def test_21_protected_hard_canon_identical(self):
        for p,sha in PROTECTED.items():
            with self.subTest(path=p): self.assertEqual(gitblob(ROOT/p),sha)
    def test_22_historical_evidence_identical(self):
        p=ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(gitblob(p),"6dbec1fe2537139f3a97c6a78250e2bae082a518")
    def test_23_independent_acceptance_not_invented(self):
        for t in ("NONCANON","UNAUTHENTICATED","NO MERGE","NO CANON PROMOTION","NO PUBLICATION","NOT RECEIVED"):
            self.assertIn(t,self.chapter)
    def test_24_second_chapter_retains_continuity(self):
        for t in ("Pell", "four coins", "Esi", "twenty-one", "second horse"):
            self.assertIn(t,self.chapter)
if __name__=="__main__": unittest.main()
