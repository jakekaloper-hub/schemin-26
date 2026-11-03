"""2016 Chapters I–X seven-part NONCANON developmental reader: source, POV and continuity guards.

Producer-authored, mechanical checks only. Passing is not an independent review.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
READER = BASE / "READING_COPY_2016_CAUSAL_CH01_10_SEVEN_PARTS_SOUND_FACE_V2_NONCANON.md"
PREVIOUS = BASE / "READING_COPY_2016_CAUSAL_CH01_09_SIX_PARTS_BELL_AND_WHEEL_NONCANON.md"
CHAPTER = BASE / "THE_BOARD_WITH_THE_HIDDEN_CRACK_SOUND_FACE_CH10_V2_NONCANON.md"
ORIGINAL = BASE / "THE_BOARD_WITH_THE_HIDDEN_CRACK_CHAPTER_10_NONCANON.md"
READER_SHA = "59a7f7d37068853330d85732963315f2a16cfdc4"
PREVIOUS_SHA = "20030dbef3d1cf0d6f4c55140c747aeb84e5c609"
CHAPTER_SHA = "6ba2cac1764c28ac0a5ffc75818b9dc0db5b7d42"
ORIGINAL_SHA = "88bb693c735c4e999ecb6db396dabe71a85a768c"
SOURCES = [
("THE_ROOF_AND_THE_UNCLAIMED_BOWL_2016_CH01_02_CONSOLIDATED_NONCANON.md","011a098cdd760cd820e9fc818ae24097375d3c8e",3564),
("THE_CLOTH_AND_THE_LOCK_2016_CH03_04_CONSOLIDATED_NONCANON.md","ccf74ae267e3ffd9ae679c2744c11198e07b7293",7742),
("THE_WEIGHT_OF_DRY_GRAIN_CHAPTER_05_NONCANON.md","40d12860e93d9393b18d7771c427061c82e46c8c",4733),
("THE_SILENCE_IN_THE_SECOND_PRINTING_CHAPTER_06_NONCANON.md","4e3d655895847e9910b7e8c69349fb2b09c94b",4303),
("THE_WHEEL_THAT_COULD_NOT_SIGN_2016_CH07_08_INTEGRATED_NONCANON.md","0a1bdc02d3c0122f6deaec8b8b4422c0090ac2e1",11131),
("THE_BELL_THAT_WAS_NOT_A_SUMMONS_CHAPTER_09_NONCANON.md","5ea06fabbf2c3c32000d6c8d36077280508c1efa",5261),
("THE_BOARD_WITH_THE_HIDDEN_CRACK_SOUND_FACE_CH10_V2_NONCANON.md",CHAPTER_SHA,6589),
]
PROTECTED = {
"living-novel/manuscript/PROLOGUE_DRAFT_V1.md":"5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
"living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md":"26a17f05eb0565e7648c29add03ee9580ec933c3",
"living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md":"30fcf23a3eb8872fa0fb4dff029fe30044141121",
"living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md":"49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
WRAP = re.compile(r"<!-- BEGIN 2016_CAUSAL ([^\n]+) \| git_blob ([0-9a-f]{40}) -->\n\n([\s\S]*?)\n\n<!-- END 2016_CAUSAL ([^\n]+) -->")
ROW = re.compile(r"^\| (\d+) \| `([^`]+)` \| `([0-9a-f]{40})` \| (\d+) \|$",re.M)

def blob(path):
    raw=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\\0"+raw).hexdigest()

class SevenPartSoundFaceReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reader=READER.read_text(encoding="utf-8")
        cls.chapter=CHAPTER.read_text(encoding="utf-8")
        cls.previous=PREVIOUS.read_text(encoding="utf-8")
        cls.wraps=WRAP.findall(cls.reader)
        cls.rows=ROW.findall(cls.reader.split("## Part 1 —",1)[0])
        cls.oldwraps=WRAP.findall(cls.previous)

    def test_01_reader_exact_commit_blob(self):
        self.assertEqual(blob(READER),READER_SHA)

    def test_02_previous_reader_unchanged(self):
        self.assertEqual(blob(PREVIOUS),PREVIOUS_SHA)

    def test_03_original_chapter_preserved(self):
        self.assertEqual(blob(ORIGINAL),ORIGINAL_SHA)

    def test_04_new_chapter_pinned(self):
        self.assertEqual(blob(CHAPTER),CHAPTER_SHA)

    def test_05_seven_source_exact_wrappers(self):
        self.assertEqual(len(self.wraps),7)
        self.assertEqual(len(self.rows),7)
        for index,(source,wrap,row) in enumerate(zip(SOURCES,self.wraps,self.rows),1):
            name,sha,words=source
            with self.subTest(part=index):
                self.assertEqual([wrap[0],wrap[1],wrap[3]],[name,sha,name])
                self.assertEqual([int(row[0]),row[1],row[2],int(row[3])],[index,name,sha,words])
                self.assertEqual(blob(BASE/name),sha)
                body=(BASE/name).read_text(encoding="utf-8")
                self.assertEqual(wrap[2],body.rstrip("\n"))
                self.assertEqual(len(body.split()),words)

    def test_06_six_prior_bodies_preserved(self):
        self.assertEqual(self.wraps[:6],self.oldwraps)

    def test_07_words_and_original_chapter_span(self):
        self.assertEqual(sum(x[2] for x in SOURCES),43323)
        self.assertIn("43323",self.reader)
        self.assertIn("seven parts / ten original causal chapter positions",self.reader)

    def test_08_new_intervening_movement_and_headings(self):
        headings=re.findall(r"(?m)^### ([IVX]+)\. ",self.chapter)
        self.assertEqual(headings,["I","II","III","IV","V","VI"])
        self.assertIn("### IV. The sound face of a promise",self.chapter)
        self.assertIn("### V. The price of finishing",self.chapter)
        self.assertIn("### VI. A place in the room",self.chapter)

    def test_09_sequence_preserves_wheel_bell_board(self):
        self.assertLess(self.reader.index("The boards were due at dawn"),self.reader.index("The bell was hanging in the gatehouse"))
        self.assertLess(self.reader.index("The bell was hanging in the gatehouse"),self.reader.index("The first thing Jake found missing"))
        self.assertLess(self.chapter.index("The cracked board had scarcely reached the reject rack"),self.chapter.index("For the rest of the afternoon he worked"))

    def test_10_gate_not_repaired_or_certified(self):
        for phrase in ["No structural timber supplied","Damaged hinge not inspected","Gate condition unchanged by this visit","REJECTED — NOT FOR FITTING"]:
            self.assertIn(phrase,self.chapter)
        self.assertNotIn("the gate was repaired",self.chapter.lower())

    def test_11_nonowner_agency_without_pov_violation(self):
        for phrase in ["The boy repeated the answer badly","The daughter returned the strip, not the board","He went out"]:
            self.assertIn(phrase,self.chapter)
        self.assertNotRegex(self.chapter,r"(?m)^### (?:Edrin|Edin|Oren)\\b")
        self.assertIn("CHAR-JAKE-KALOPER",self.chapter)

    def test_12_no_false_settlement(self):
        for phrase in ["unfinished and unturned","supplier remained unpaid","unopened","UNCERTIFIED","unrecovered"]:
            self.assertIn(phrase.lower(),self.reader.lower())

    def test_13_source_history_identities_firewalled(self):
        for phrase in ["distinct Austin-named teams","before any postseason outcome", "human-owner"]:
            self.assertIn(phrase.lower(),self.reader.lower())

    def test_14_candidate_only_no_release(self):
        for phrase in ["NONCANON","NO MERGE","NO PUBLICATION","NO CANON PROMOTION","FOUNDER-ONLY"]:
            self.assertIn(phrase,self.reader)

    def test_15_four_protected_2026_files_pinned(self):
        for path,sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(blob(ROOT/path),sha)

if __name__=="__main__":
    unittest.main()
