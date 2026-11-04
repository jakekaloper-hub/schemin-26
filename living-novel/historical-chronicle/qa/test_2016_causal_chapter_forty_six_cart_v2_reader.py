"""Chapter XLVI V2 noncanon source-exact reader, continuity and release firewall.
These tests do NOT stand in for a human or independently authenticated Umpire review.
"""
import hashlib
import importlib.util
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
OLD = "THE_DISTANCE_BETWEEN_TWO_GATES_CHAPTER_46_NONCANON.md"
SCENE = "THE_DISTANCE_BETWEEN_TWO_GATES_CART_WITHOUT_A_STRAIGHT_WHEEL_CH46_V2_SCENE_NONCANON.md"
NEW = "THE_DISTANCE_BETWEEN_TWO_GATES_CART_WITHOUT_A_STRAIGHT_WHEEL_CH46_V2_NONCANON.md"
H = {
    OLD: "9c866df37a5bebe0b244b55921e1bf28aa75e06d",
    SCENE: "8bf57ce9ee5e7d7ed3754d167b7f3bfd5353b4b7",
    NEW: "7d13718436fd4a84d37ba5093a920052bb870787"
}
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
def parts(doc):
    return [x.split("\n---\n", 1)[0].strip() for x in re.split(r"(?m)^### [IVX]+\. [^\n]+\n", doc)[1:]]
def load_builder():
    p = Path(__file__).with_name("build_2016_causal_43_part_cart_reader.py")
    spec = importlib.util.spec_from_file_location("causal_43_reader",p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

class TestCausalXLVICart(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = (BASE/OLD).read_text(encoding="utf-8")
        cls.scene = (BASE/SCENE).read_text(encoding="utf-8")
        cls.new = (BASE/NEW).read_text(encoding="utf-8")
        cls.mod = load_builder()
        cls.prior = cls.mod.prior_reader()
        cls.reader = cls.mod.build_from_repo()

    def test_01_blob_sha_sources_locked(self):
        for n, sha in H.items():
            with self.subTest(n=n):
                self.assertEqual(blob((BASE/n).read_bytes()), sha)
    def test_02_substantial_new_scene(self):
        self.assertGreaterEqual(len(self.scene.split()), 2000)
    def test_03_new_chapter_word_count(self):
        self.assertEqual(len(self.new.split()), 7833)
    def test_04_original_word_count(self):
        self.assertEqual(len(self.old.split()), 5586)
    def test_05_seven_movements(self):
        self.assertEqual(re.findall(r"(?m)^### ([IVX]+)\. ",self.new),
                         ["I","II","III","IV","V","VI","VII"])
    def test_06_six_original_movement_bodies_exact(self):
        original, revised = parts(self.old), parts(self.new)
        self.assertEqual(len(original),6)
        self.assertEqual(len(revised),7)
        self.assertEqual(original, revised[:4]+revised[5:])
    def test_07_scene_embedded_once(self):
        self.assertEqual(self.new.count(self.scene.strip()),1)
    def test_08_no_unlicensed_protagonist(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake",self.new)
        self.assertIn("CHAR-JAKE-KALOPER",self.new)
        for banned in ("Edrin","Edin"):
            self.assertNotIn(banned,self.scene)
    def test_09_no_supporting_character_interior_grabs(self):
        for banned in ("Sela thought", "Nella knew", "Tam wondered", "Tavi realized",
                       "Tavi remembered", "Sela believed", "Nella decided she felt"):
            with self.subTest(banned=banned): self.assertNotIn(banned,self.scene)
    def test_10_causal_objects_and_choices_present(self):
        for required in ("Tavi","Sela","Nella","Tam","Jake","wheel","fruit",
                         "cart","gate","crate","notches","worn path"):
            with self.subTest(required=required): self.assertIn(required,self.scene)
    def test_11_no_fabricated_league_results(self):
        for prohibited in ("ESPN", "Flaim", "Week 12", "standings",
                           "championship", "final score", "playoffs"):
            with self.subTest(prohibited=prohibited):
                self.assertNotIn(prohibited,self.scene)
    def test_12_prior_42_manifest_preserved(self):
        rows=self.mod.rows(self.prior)
        self.assertEqual(len(rows),42)
        self.assertEqual(sum(x[3] for x in rows),323490)
    def test_13_new_43_manifest(self):
        rows=self.mod.rows(self.reader)
        self.assertEqual([x[0] for x in rows],list(range(1,44)))
        self.assertEqual(rows[-1],(43,NEW,H[NEW],7833))
    def test_14_43_component_markers(self):
        self.assertEqual(self.reader.count(self.mod.BEGIN),43)
        self.assertEqual(self.reader.count(self.mod.END),43)
        self.assertEqual(self.reader.count(self.mod.TERMINAL),1)
    def test_15_prior_42_embedded_sections_exact(self):
        prior=self.prior[self.prior.index(self.mod.BEGIN):self.prior.index(self.mod.TERMINAL)].rstrip()
        start=f"{self.mod.BEGIN}{NEW} | git_blob {H[NEW]} -->"
        updated=self.reader[self.reader.index(self.mod.BEGIN):self.reader.index(start)].rstrip()
        self.assertEqual(updated,prior)
    def test_16_new_component_embed_exact(self):
        start=f"{self.mod.BEGIN}{NEW} | git_blob {H[NEW]} -->"
        end=f"{self.mod.END}{NEW} -->"
        self.assertEqual(self.reader.split(start+"\n\n",1)[1].split("\n\n"+end,1)[0],
                         self.new.rstrip("\n"))
    def test_17_word_sum_exact(self):
        self.assertEqual(sum(r[3] for r in self.mod.rows(self.reader)),331323)
        self.assertIn("Source component words including metadata: 331323",self.reader)
    def test_18_corrupted_source_fails_closed(self):
        with self.assertRaises(ValueError): self.mod.build(self.prior,self.new+"corrupted")
    def test_19_incomplete_predecessor_fails_closed(self):
        begin=self.mod.BEGIN
        with self.assertRaises(ValueError): self.mod.build(self.prior.replace(begin,"",1),self.new)
    def test_20_protected_2026_sources_unchanged(self):
        for p,sha in PROTECTED.items():
            with self.subTest(path=p): self.assertEqual(blob((ROOT/p).read_bytes()),sha)
    def test_21_2016_league_archive_unchanged(self):
        p=ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(blob(p.read_bytes()),"6dbec1fe2537139f3a97c6a78250e2bae082a518")
    def test_22_no_promotion_or_independent_review_claim(self):
        for guard in ("NONCANON","INDEPENDENT EDITORIAL HOLD","NO MERGE",
                      "NO CANON PROMOTION","NO PUBLICATION","Outstanding:"):
            self.assertIn(guard,self.new)
    def test_23_original_source_still_exists(self):
        self.assertTrue((BASE/OLD).exists())
    def test_24_chapter47_readiness_not_misrepresented(self):
        self.assertIn("the river",self.new)
        self.assertIn("Corin",self.new)
        self.assertIn("Lysa",self.new)
        self.assertIn("four",self.old)
if __name__=="__main__": unittest.main()
