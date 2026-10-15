"""Chapter I full reconstruction: source/provenance/POV/temporal negative tests.

Passing proves mechanical alignment only, not a literary or canon release.
"""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BOARD=ROOT/"living-novel/production/full-rewrite-2026"
M=BOARD/"R7_CHAPTER_I_NINE_CARD_RECONSTRUCTION_REGISTER_V1.json"
DOC=json.loads(M.read_text(encoding="utf-8"))
CHAPTER=ROOT/DOC["manuscript_path"]
POV_PATTERN=re.compile(r"(?m)^\\*\\*POV: (CHAR-[A-Z-]+)\\b")
# Same Git object byte identity method used by Git itself.
def git_blob_sha(content:bytes)->str:
    return hashlib.sha1(f"blob {len(content)}\\0".encode()+content).hexdigest()

def valid_location_anchor(location_id,region_id,context_id):
    if not all((location_id,region_id,context_id)):
        return False
    locations={x["id"]:x for x in json.loads((ROOT/"world/data/locations.json").read_text())["locations"]}
    contexts={x["id"]:x for x in json.loads((ROOT/"world/data/settlements.json").read_text())["settlements"]}
    loc=locations.get(location_id); ctx=contexts.get(context_id)
    return bool(loc and ctx and loc["physical_zone_id"]==region_id
                and ctx["physical_zone_id"]==region_id
                and location_id in ctx.get("anchor_location_ids",[]))

class FullChapterOneDevelopmentGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text=CHAPTER.read_text(encoding="utf-8")
        cls.historical=(ROOT/DOC["canonical_source"]).read_text(encoding="utf-8")

    def test_manuscript_substantial_and_not_canonical(self):
        self.assertGreater(len(self.text.split()),5800)
        self.assertLess(len(self.text.split()),11000)
        self.assertEqual(DOC["status"],"FULL_LENGTH_DEVELOPMENT_CANDIDATE_NOT_CANON")
        self.assertIn("NONCANON CANDIDATE",self.text[:600])
        self.assertNotEqual(self.text,self.historical)

    def test_hard_canon_original_blob_unchanged(self):
        self.assertEqual(
            git_blob_sha((ROOT/DOC["canonical_source"]).read_bytes()),
            DOC["canonical_source_blob_sha"],
        )

    def test_precise_pov_sections_three_unique_owners(self):
        passages=list(POV_PATTERN.finditer(self.text))
        owners=[m.group(1) for m in passages]
        self.assertEqual(len(passages),4)
        self.assertEqual(owners,["CHAR-JAKE-KALOPER","CHAR-BRANDON-PRYOR",
                                 "CHAR-AUSTIN-BYARS","CHAR-JAKE-KALOPER"])
        self.assertEqual(len(set(owners)),3)
        self.assertEqual(owners,[s["owner_id"] for s in DOC["pov_segments"]])
        for i,m in enumerate(passages):
            end=passages[i+1].start() if i+1<len(passages) else len(self.text)
            self.assertGreater(len(self.text[m.start():end].split()),500)

    def test_nine_source_cards_accounted_without_forcing_nine_povs(self):
        cards=DOC["card_fate"]
        self.assertEqual(len(cards),9)
        self.assertEqual(
            {c["card"] for c in cards},
            {f"CHAPTER_01_S{i:02d}" for i in range(1,10)},
        )
        self.assertIn("DRAMATIZED_EXISTING_PILOT_INCORPORATED",
                      {x["status"] for x in cards})
        self.assertEqual(DOC["migrations"]["source_ch1_sections"],9)
        self.assertEqual(DOC["migrations"]["source_ch2_sections"],10)
        self.assertEqual(DOC["policy"]["pov_cap"],3)

    def test_week1_scores_match_hard_manuscript_witness(self):
        for item in DOC["score_witness"]:
            w=item["winner"]; l=item["loser"]
            a=f'{item["winner_points"]:.2f}';b=f'{item["loser_points"]:.2f}'
            pattern=re.compile(re.escape(w)+r"\\s+—\\s+"+re.escape(a)+r"\\s+"+
                               re.escape(l)+r"\\s+—\\s+"+re.escape(b),re.I)
            self.assertRegex(self.historical,pattern)
            self.assertIn(a,self.text)
            self.assertIn(b,self.text)
        self.assertEqual(len(DOC["score_witness"]),6)

    def test_belt_and_fictional_supporting_person_agency(self):
        self.assertEqual(DOC["policy"]["belt_owner_after_week1"],"CHAR-AUSTIN-BYARS")
        self.assertIn("He had not lost the Belt.",self.text)
        self.assertIn("A boy stopped him at the archive steps",self.text)
        self.assertIn("They're mine to deliver",self.text)
        self.assertNotRegex(self.text,re.compile(r"\\bEdrin(?: Vale)?\\b|\\bEdin\\b",re.I))

    def test_location_checks_fail_closed_for_three_unresolved_places(self):
        unresolved=0
        for s in DOC["pov_segments"]:
            valid=valid_location_anchor(s["location_id"],s["region_id"],s["settlement_context_id"])
            if s["location_id"] is None:
                unresolved+=1
                self.assertFalse(valid)
                self.assertIn("UNRESOLVED",s["site_status"])
            else:
                self.assertTrue(valid,s["segment"])
        self.assertEqual(unresolved,3)
        # Negative cases: wrong region, fake proper noun, wrong settlement.
        self.assertFalse(valid_location_anchor("LOC-LEAGUE-ARCHIVE","REG-UPPER-VALLEYS","SETCTX-CENTRAL-BASIN"))
        self.assertFalse(valid_location_anchor("LOC-INVENTED-SITE","REG-CENTRAL-BASIN","SETCTX-CENTRAL-BASIN"))
        self.assertFalse(valid_location_anchor("LOC-LEAGUE-ARCHIVE","REG-CENTRAL-BASIN","SETCTX-UPPER-VALLEYS"))

    def test_prologue_precedence_and_no_unauthorized_promotion(self):
        p=DOC["privileged_opening_candidate"]
        self.assertEqual(p["repository_pr"],130)
        self.assertIn("PROLOGUE_TWELVE_POV_EDITORIAL_CANDIDATE_V4R2.md",p["path"])
        self.assertEqual(p["status"],"PREFERRED_NONCANON_PROLOGUE_RETAINED_UNCHANGED")
        self.assertEqual(DOC["policy"]["output_release"],"HOLD_NO_FOUNDER_OR_INDEPENDENT_UMPIRE_APPROVAL")
        self.assertEqual(DOC["policy"]["source_venues_unknown_count"],3)

    def test_adversarial_wrong_result_and_false_canon(self):
        sample=DOC["score_witness"][-1]
        self.assertNotEqual(141.71,sample["winner_points"])
        self.assertNotEqual("CHAR-JAKE-KALOPER",DOC["policy"]["belt_owner_after_week1"])
        self.assertNotIn("CANON_APPROVED",DOC["status"])

if __name__=="__main__":
    unittest.main()
