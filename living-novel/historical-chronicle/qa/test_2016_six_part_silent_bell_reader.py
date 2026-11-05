"""Regression for 2016 six-part noncanon wheel-and-bell developmental reading."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
READER = BASE / "READING_COPY_2016_CAUSAL_CH01_09_SIX_PARTS_BELL_AND_WHEEL_NONCANON.md"
PREVIOUS = BASE / "READING_COPY_2016_CAUSAL_CH01_08_FIVE_PARTS_WHEEL_THAT_COULD_NOT_SIGN_NONCANON.md"
IX = BASE / "THE_BELL_THAT_WAS_NOT_A_SUMMONS_CHAPTER_09_NONCANON.md"
READER_SHA = "20030dbef3d1cf0d6f4c55140c747aeb84e5c609"
PREVIOUS_SHA = "24a99b967b944bd12ecd1e452d3f4f026426af77"
IX_SHA = "5ea06fabbf2c3c32000d6c8d36077280508c1efa"
PARTS = [
("THE_ROOF_AND_THE_UNCLAIMED_BOWL_2016_CH01_02_CONSOLIDATED_NONCANON.md","011a098cdd760cd820e9fc818ae24097375d3c8e",3564),
("THE_CLOTH_AND_THE_LOCK_2016_CH03_04_CONSOLIDATED_NONCANON.md","ccf74ae267e3ffd9ae679c2744c11198e07b7293",7742),
("THE_WEIGHT_OF_DRY_GRAIN_CHAPTER_05_NONCANON.md","40d12860e93d9393b18d7771c427061c82e46c8c",4733),
("THE_SILENCE_IN_THE_SECOND_PRINTING_CHAPTER_06_NONCANON.md","4e3d655895847e9910b7e8c69349fb2b09c94b4b",4303),
("THE_WHEEL_THAT_COULD_NOT_SIGN_2016_CH07_08_INTEGRATED_NONCANON.md","0a1bdc02d3c0122f6deaec8b8b4422c0090ac2e1",11131),
("THE_BELL_THAT_WAS_NOT_A_SUMMONS_CHAPTER_09_NONCANON.md","5ea06fabbf2c3c32000d6c8d36077280508c1efa",5261),
]
WRAP=re.compile(r"<!-- BEGIN 2016_CAUSAL ([^\n]+) \| git_blob ([0-9a-f]{40}) -->\n\n([\s\S]*?)\n\n<!-- END 2016_CAUSAL ([^\n]+) -->")
ROW=re.compile(r"^\| (\d+) \| `([^`]+)` \| `([0-9a-f]{40})` \| (\d+) \|$",re.M)
PROTECTED={
"living-novel/manuscript/PROLOGUE_DRAFT_V1.md":"5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
"living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md":"26a17f05eb0565e7648c29add03ee9580ec933c3",
"living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md":"30fcf23a3eb8872fa0fb4dff029fe30044141121",
"living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md":"49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc"
}
def blob(f):
    b=f.read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

class SixPartBellReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text=READER.read_text(encoding="utf-8")
        cls.wraps=WRAP.findall(cls.text)
        cls.rows=ROW.findall(cls.text.split("## Part 1 —",1)[0])

    def test_01_reader_sha(self):
        self.assertEqual(blob(READER),READER_SHA)

    def test_02_prior_five_part_reading_preserved(self):
        self.assertEqual(blob(PREVIOUS),PREVIOUS_SHA)

    def test_03_six_sources_exact_and_ordered(self):
        self.assertEqual(len(self.wraps),6)
        self.assertEqual(len(self.rows),6)
        for i,(source,wrap,row) in enumerate(zip(PARTS,self.wraps,self.rows),1):
            name,sha,words=source
            with self.subTest(i=i):
                self.assertEqual([wrap[0],wrap[1],wrap[3]],[name,sha,name])
                self.assertEqual([int(row[0]),row[1],row[2],int(row[3])],[i,name,sha,words])
                self.assertEqual(blob(BASE/name),sha)
                body=(BASE/name).read_text(encoding="utf-8")
                self.assertEqual(wrap[2],body.rstrip("\n"))
                self.assertEqual(len(body.split()),words)

    def test_04_word_math(self):
        self.assertEqual(sum(p[2] for p in PARTS),36734)
        self.assertIn("36734 words",self.text)
        self.assertEqual(blob(IX),IX_SHA)

    def test_05_continuity_bell_after_wheel(self):
        self.assertLess(self.text.index("The boards were due at dawn"),self.text.index("The bell was hanging in the gatehouse"))
        self.assertIn("the great wheel",self.text.lower())
        self.assertIn("the silent bell",self.text.lower())
        self.assertIn("gatehouse",self.wraps[5][2].lower())
        self.assertIn("No one is opening the eastern room because a bell rings",self.text)

    def test_06_human_owner_identity_firewall(self):
        self.assertIn("separate slots ID 8",self.text)
        self.assertIn("ID 12",self.text)
        self.assertIn("historical human-owner binding unknown",self.text.lower())
        self.assertIn("before any postseason event",self.text.lower())

    def test_07_exclusive_proposed_owner_view(self):
        self.assertIn("CHAR-JAKE-KALOPER",self.wraps[5][2])
        self.assertNotRegex(self.text,r"(?m)^### (?:Edrin|Edin|Oren)\b")

    def test_08_open_loops_not_automatically_solved(self):
        for phrase in ["UNFINISHED AND UNTURNED","UNOPENED","UNSAFE","unrecovered","unpaid"]:
            self.assertIn(phrase.lower(),self.wraps[5][2].lower())

    def test_09_four_hard_canon_files_untouched(self):
        for path,expected in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(blob(ROOT/path),expected)

    def test_10_release_hold(self):
        for phrase in ["NONCANON","NO MERGE","NO CANON PROMOTION","UMPIRE HOLD","FOUNDER-ONLY"]:
            self.assertIn(phrase,self.text)

if __name__=="__main__":
    unittest.main()
