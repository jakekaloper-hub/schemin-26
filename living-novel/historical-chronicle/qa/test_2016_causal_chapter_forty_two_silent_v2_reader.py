"""NONCANON 2016 Chapter XLII V2: source-exact 39-part reader and POV/authority gates."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
ORIGINAL = "THE_STAGE_BENEATH_THE_SHORT_AWNING_CHAPTER_42_NONCANON.md"
SCENE = "THE_STAGE_BENEATH_THE_SHORT_AWNING_PART_THAT_MADE_NO_SOUND_CH42_V2_SCENE_NONCANON.md"
CHAPTER = "THE_STAGE_BENEATH_THE_SHORT_AWNING_PART_THAT_MADE_NO_SOUND_CH42_V2_NONCANON.md"
PRIOR = "READING_COPY_2016_CAUSAL_CH01_41_THIRTY_EIGHT_PARTS_PATCH_NONCANON.md"
READER = "READING_COPY_2016_CAUSAL_CH01_42_THIRTY_NINE_PARTS_SILENT_ENDING_NONCANON.md"
SHAS = {
    ORIGINAL: "6294ffee1d478a493091a532451cdbb9f867f917",
    SCENE: "255d0bec68aee083c8e83d9e411d77f413022bd7",
    CHAPTER: "163cecc205c244cf0b3f1f4b69fa47409c536846",
    PRIOR: "aa1137b33f35e02828296b6c671fade5b51f5044",
    READER: "6b4fb8e8fc939d55553953480879380b9ba6d3a8",
}
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def gitblob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

def rows(doc):
    result = []
    for line in doc.splitlines():
        if not line.startswith("| "):
            continue
        cells = [x.strip() for x in line.split("|")]
        if len(cells) != 6 or not cells[1].isdigit():
            continue
        try:
            result.append((int(cells[1]), cells[2].strip(chr(96)), cells[3].strip(chr(96)), int(cells[4])))
        except ValueError:
            continue
    return result

def embedded(doc, filename, sha):
    begin = "<!-- BEGIN 2016_CAUSAL " + filename + " | git_blob " + sha + " -->"
    end = "<!-- END 2016_CAUSAL " + filename + " -->"
    assert doc.count(begin) == 1 and doc.count(end) == 1
    return doc.split(begin + "\n\n", 1)[1].split("\n\n" + end, 1)[0]

class FortyTwoSilentEndingV2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = (BASE / ORIGINAL).read_text()
        cls.scene = (BASE / SCENE).read_text()
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.prior = (BASE / PRIOR).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.prevrows = rows(cls.prior)
        cls.currentrows = rows(cls.reader)
    def test_01_pinned_five_blobs(self):
        for f, sha in SHAS.items():
            with self.subTest(file=f):
                self.assertEqual(gitblob(BASE / f), sha)
    def test_02_scene_substantive(self):
        self.assertGreater(len(self.scene.split()), 2200)
    def test_03_chapter_has_seven_movements(self):
        self.assertEqual(re.findall(r"^### ([IVX]+)\.", self.chapter, re.M), ["I","II","III","IV","V","VI","VII"])
    def test_04_exact_old_six_movements(self):
        def narrative(s):
            return s.split("### I.", 1)[1].split("\n---\n\n### Editorial handoff", 1)[0]
        restored = narrative(self.chapter).replace(self.scene.strip() + "\n\n", "").replace(
            "### VII. After the last bowl", "### VI. After the last bowl")
        self.assertEqual(restored, narrative(self.original))
    def test_05_embedded_scene_exactly_once(self):
        self.assertEqual(self.chapter.count(self.scene.strip()), 1)
    def test_06_manifest_39_and_prefix(self):
        self.assertEqual(len(self.prevrows), 38)
        self.assertEqual(len(self.currentrows), 39)
        self.assertEqual(self.prevrows, self.currentrows[:38])
        self.assertEqual(self.currentrows[-1], (39, CHAPTER, SHAS[CHAPTER], 10693))
    def test_07_previous_38_embedded_bodies_exact(self):
        for n, filename, sha, _ in self.prevrows:
            with self.subTest(part=n):
                self.assertEqual(embedded(self.reader, filename, sha), embedded(self.prior, filename, sha))
    def test_08_all_39_embedded_sources_exact(self):
        for n, filename, sha, count in self.currentrows:
            with self.subTest(part=n):
                src = (BASE / filename).read_text().rstrip("\n")
                self.assertEqual(gitblob(BASE / filename), sha)
                self.assertEqual(embedded(self.reader, filename, sha), src)
                self.assertEqual(len(src.split()), count)
    def test_09_counts(self):
        self.assertEqual(len(self.chapter.split()), 10693)
        self.assertEqual(sum(r[3] for r in self.currentrows), 298246)
        self.assertIn("Source component words including metadata: 298246", self.reader)
    def test_10_exact_markers(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 39)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 39)
    def test_11_limited_principal_pov(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
    def test_12_no_external_interior_claims(self):
        for phrase in ("Sela thought", "Hessa knew", "Orin wondered", "Vera realized", "Edrin thought", "Edin remembered"):
            self.assertNotIn(phrase, self.scene)
    def test_13_motivated_scene_objects(self):
        for phrase in ("Nella", "Tam", "Orin", "Vera", "Fara", "Eren", "Meric", "wooden cup", "bridge", "stones"):
            self.assertIn(phrase, self.scene)
    def test_14_stage_not_fabricated_as_finished(self):
        self.assertIn("It was not Meric's proposed stage; that had not been made.", self.scene)
        self.assertIn("UNBUILT", self.chapter)
    def test_15_no_scoring_in_fiction(self):
        for phrase in ("ESPN", "Flaim", "playoff", "championship"):
            self.assertNotIn(phrase, self.scene)
    def test_16_main_hard_canon_bytes(self):
        for p, sha in PROTECTED.items():
            with self.subTest(path=p):
                self.assertEqual(gitblob(ROOT / p), sha)
    def test_17_2016_archive_unchanged(self):
        f = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(gitblob(f), "6dbec1fe2537139f3a97c6a78250e2bae082a518")
    def test_18_historical_fiction_firewall(self):
        for phrase in ("UNAUTHENTICATED", "NONCANON", "NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            self.assertIn(phrase, self.chapter)
            self.assertIn(phrase, self.reader)
    def test_19_past_open_loops(self):
        for phrase in ("second horse", "Esi's letter", "escaped bird", "kiln passage", "Hessa's missing sister"):
            self.assertIn(phrase, self.chapter)
    def test_20_no_hard_canon_promotion(self):
        self.assertIn("Independent Authors Council", self.reader)
        self.assertIn("Umpire", self.reader)
        self.assertIn("Founder", self.reader)

if __name__ == "__main__":
    unittest.main()
