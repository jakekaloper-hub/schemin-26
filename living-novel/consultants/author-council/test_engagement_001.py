import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parent
ENG=ROOT/"engagements"/"NOVEL-AUTHOR-CONSULT-2026-10-01-001"

class Engagement001Tests(unittest.TestCase):
    def test_freeze_and_closeout_exist(self):
        for name in [
            "00_EVIDENCE_FREEZE.md","01_SELECTION_MANIFEST.md","02_SOURCE_PACKET.md",
            "FINAL_RECONCILIATION.md","IMPLEMENTATION_DECISION.md","AUDIT_RECEIPT.md","_INDEX.md"
        ]:
            self.assertTrue((ENG/name).exists(),name)

    def test_all_four_rounds_have_seven_consultants(self):
        suffixes={"round-1":"_R1.md","round-2":"_R2.md","round-3":"_R3.md","round-4":"_R4.md"}
        for round_name,suffix in suffixes.items():
            files=list((ENG/round_name).glob(f"*{suffix}"))
            self.assertEqual(len(files),7,(round_name,[f.name for f in files]))

    def test_cross_examination_exists_after_each_round(self):
        for n in range(1,5):
            self.assertTrue((ENG/f"BULLPEN_CROSS_EXAMINATION_R{n}.md").exists())

    def test_round_reconciliation_exists_for_first_three(self):
        for n in range(1,4):
            self.assertTrue((ENG/f"ROUND_{n}_RECONCILIATION.md").exists())

    def test_freeze_pins_expected_repository_cutoff(self):
        text=(ENG/"00_EVIDENCE_FREEZE.md").read_text()
        self.assertIn("967435b15ba1250e1c4f6166a5fd9143dbd65f53",text)
        self.assertIn("HARD MANUSCRIPT CANON / CLOSED",text)

    def test_final_reconciliation_preserves_closed_manuscripts(self):
        text=(ENG/"FINAL_RECONCILIATION.md").read_text()
        for name in [
            "PROLOGUE_DRAFT_V1.md",
            "CHAPTER_01_THE_FIRST_ANSWER.md",
            "CHAPTER_02_WHAT_COMES_BACK.md"
        ]:
            self.assertIn(name,text)

if __name__=="__main__":
    unittest.main(verbosity=2)
