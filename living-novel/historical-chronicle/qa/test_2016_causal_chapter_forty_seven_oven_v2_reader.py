"""Chapter XLVII V2 and 44-part source-exact NONCANON manuscript regressions."""
import hashlib
import importlib.util
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
QA = Path(__file__).parent
OLD = "THE_BELL_THAT_HAD_NO_OWNER_CHAPTER_47_NONCANON.md"
SCENE = "THE_BELL_THAT_HAD_NO_OWNER_THE_OVEN_WITHOUT_A_BELL_CH47_V2_SCENE_NONCANON.md"
NEW = "THE_BELL_THAT_HAD_NO_OWNER_THE_OVEN_WITHOUT_A_BELL_CH47_V2_NONCANON.md"
SHA = "47d7f0839ad61f28d5d2191640ba2ad622f4a8a7"
OLD_SHA = "c1bb3b86aa6f789d59fe2688600c10563496d5a5"
SCENE_SHA = "2856cc939b8903fc8f4abda5830d6c2718ab673d"
OLD_WORDS = 5696
SCENE_WORDS = 2237
NEW_WORDS = 7939
TOTAL_WORDS = 339262

def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
def sections(text):
    return [m.group(1).strip() for m in re.finditer(r"(?ms)^### [IVX]+\. [^\n]+\n(.*?)(?=^### [IVX]+\.|^---\n|\Z)",text)]
def mod():
    path = QA / "build_2016_causal_44_part_oven_reader.py"
    spec = importlib.util.spec_from_file_location("ch47_builder",path)
    out = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(out)
    return out

class TestChapterXLVIIBell(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = (BASE/OLD).read_text(encoding="utf-8")
        cls.scene = (BASE/SCENE).read_text(encoding="utf-8")
        cls.new = (BASE/NEW).read_text(encoding="utf-8")
        cls.builder = mod()
        cls.prior = cls.builder.prior_reader()
        cls.reader = cls.builder.build_from_repo()

    def test_01_source_git_blobs_locked(self):
        self.assertEqual(blob((BASE/OLD).read_bytes()),OLD_SHA)
        self.assertEqual(blob((BASE/SCENE).read_bytes()),SCENE_SHA)
        self.assertEqual(blob((BASE/NEW).read_bytes()),SHA)
    def test_02_substantive_original_fiction(self):
        self.assertGreaterEqual(len(self.scene.split()),2000)
        self.assertEqual(len(self.scene.split()),SCENE_WORDS)
    def test_03_chapter_words(self):
        self.assertEqual(len(self.old.split()),OLD_WORDS)
        self.assertEqual(len(self.new.split()),NEW_WORDS)
    def test_04_seven_ordered_movements(self):
        self.assertEqual(re.findall(r"(?m)^### ([IVX]+)\. ",self.new),
                         ["I","II","III","IV","V","VI","VII"])
    def test_05_six_original_movement_bodies_preserved(self):
        old=sections(self.old); new=sections(self.new)
        self.assertEqual(len(old),6)
        self.assertEqual(len(new),7)
        self.assertEqual(old,new[:5]+new[6:])
    def test_06_new_scene_embedded_once(self):
        self.assertEqual(self.new.count(self.scene.strip()),1)
    def test_07_proposed_jake_only_limited_interior(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake",self.new)
        for forbidden in ("Edrin","Edin", "Sela thought", "Fara secretly knew",
                          "Pell remembered", "Garran believed"):
            self.assertNotIn(forbidden,self.scene)
    def test_08_historical_fact_firewall(self):
        for word in ("ESPN","Flaim","Week 12","final score","standings",
                     "championship","playoffs"):
            self.assertNotIn(word,self.scene)
    def test_09_unresolved_bell_ownership_preserved(self):
        for term in ("Fara","Pell","bell","clapper","Garran","oven","loaf"):
            self.assertIn(term,self.new)
        self.assertIn("The clapper dropped into her palm.",self.new)
        self.assertIn("No common decision was entered.",self.new)
    def test_10_editorial_holds_preserved(self):
        for term in ("NONCANON", "INDEPENDENT EDITORIAL HOLD",
                     "NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            self.assertIn(term,self.new)
    def test_11_prior_43_manifest_preserved(self):
        rows=self.builder.rows(self.prior)
        self.assertEqual([x[0] for x in rows],list(range(1,44)))
        self.assertEqual(sum(x[3] for x in rows),331323)
    def test_12_new_44_manifest(self):
        rows=self.builder.rows(self.reader)
        self.assertEqual([x[0] for x in rows],list(range(1,45)))
        self.assertEqual(rows[-1],(44,NEW,SHA,NEW_WORDS))
        self.assertEqual(sum(x[3] for x in rows),TOTAL_WORDS)
    def test_13_section_markers_source_exact(self):
        self.assertEqual(self.reader.count(self.builder.BEGIN),44)
        self.assertEqual(self.reader.count(self.builder.END),44)
        self.assertEqual(self.reader.count(self.builder.TERMINAL),1)
    def test_14_prior_embedded_components_byte_exact(self):
        old_body=self.prior[self.prior.index(self.builder.BEGIN):self.prior.index(self.builder.TERMINAL)].rstrip()
        marker=f"{self.builder.BEGIN}{NEW} | git_blob {SHA} -->"
        new_body=self.reader[self.reader.index(self.builder.BEGIN):self.reader.index(marker)].rstrip()
        self.assertEqual(old_body,new_body)
    def test_15_new_embedded_chapter_source_exact(self):
        start=f"{self.builder.BEGIN}{NEW} | git_blob {SHA} -->"
        end=f"{self.builder.END}{NEW} -->"
        self.assertEqual(self.reader.split(start+"\n\n",1)[1].split("\n\n"+end,1)[0],
                         self.new.rstrip("\n"))
    def test_16_corrupted_chapter_fails_closed(self):
        with self.assertRaises(ValueError): self.builder.build(self.prior,self.new+"x")
    def test_17_prior_header_drift_fails_closed(self):
        with self.assertRaises(ValueError): self.builder.build(self.prior.replace("331323","999999",1),self.new)
    def test_18_missing_prior_component_fails_closed(self):
        with self.assertRaises(ValueError): self.builder.build(self.prior.replace(self.builder.BEGIN,"",1),self.new)
    def test_19_original_not_overwritten(self):
        self.assertTrue((BASE/OLD).exists())
    def test_20_no_canon_promotion_claim(self):
        self.assertIn("NONCANON",self.reader)
        self.assertNotIn("CANON RELEASE APPROVED",self.scene)

if __name__=="__main__": unittest.main()
