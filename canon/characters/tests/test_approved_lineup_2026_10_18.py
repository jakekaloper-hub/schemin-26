"""Locked Commissioner lineup artifact, twelve derivatives, source and Atlas firewall."""
import hashlib
import json
import re
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[3]
LOCK=ROOT/"canon/characters/APPROVED_LINEUP_2026_10_18.json"
EXPECTED="24cd6adf9654e598c97a6588afc07603d5adcc40c276eba07e7c86c0d438e7b2"

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

class ApprovedLineupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc=json.loads(LOCK.read_text())
        cls.reg=json.loads((ROOT/"canon/characters/reference_sources_v1.json").read_text())
        cls.dom=json.loads((ROOT/"world/data/owner_domains.json").read_text())

    def test_exact_master_binary_and_identity_set(self):
        d=self.doc
        p=ROOT/d["stored_repository_path"]
        self.assertEqual(d["sha256"],EXPECTED)
        self.assertEqual(sha(p),EXPECTED)
        self.assertEqual(p.stat().st_size,3751835)
        self.assertEqual((d["width"],d["height"]),(1448,1086))
        self.assertEqual(len(d["individuals"]),12)
        ids=[x["character_id"] for x in d["individuals"]]
        self.assertEqual(len(set(ids)),12)
        self.assertEqual(set(ids),{x["character_id"] for x in self.reg["entries"]})
        self.assertEqual(set(ids),{x["character_id"] for x in self.dom["domains"]})
        self.assertIn("COMMISSIONER_APPROVED",d["status"])

    def test_crops_and_delta_provenance(self):
        boxes=[]
        for r in self.doc["individuals"]:
            cid=r["character_id"]
            crop=ROOT/r["crop"]
            self.assertEqual(sha(crop),r["crop_sha256"],cid)
            x=r["crop_rectangle_top_left"]
            self.assertGreater(x["width"],0)
            self.assertGreater(x["height"],0)
            self.assertLessEqual(x["x"]+x["width"],1448)
            self.assertLessEqual(x["y"]+x["height"],1086)
            boxes.append((x["x"],x["y"],x["width"],x["height"]))
            delta=json.loads((ROOT/r["appearance_delta"]).read_text())
            self.assertEqual(delta["character_id"],cid)
            self.assertEqual(delta["lineup_parent_sha256"],EXPECTED)
            self.assertEqual(delta["derived_crop_sha256"],r["crop_sha256"])
            self.assertEqual(delta["derived_crop_classification"],"DERIVED_APPROVED_LINEUP_CROP")
            self.assertFalse(delta["primary_source_supersession_approved"])
            self.assertEqual(delta["physical_engine_delta"]["height_mass_and_movement_ranges"],
                             "UNKNOWN_NOT_ESTABLISHED_BY_LINEUP")
            self.assertTrue(delta["approved_visual_assertions"]["negative_rules"])
        self.assertEqual(len(set(boxes)),12)
        self.assertEqual(sum(w*h for x,y,w,h in boxes),1448*1086)
        for i,a in enumerate(boxes):
            for b in boxes[i+1:]:
                self.assertFalse(
                    a[0]<b[0]+b[2] and b[0]<a[0]+a[2]
                    and a[1]<b[1]+b[3] and b[1]<a[1]+a[3]
                )

    def test_hmb_correction_and_dk_old_source_quarantine_remain(self):
        hmb=self.doc["supporting_hmb_correction"]
        self.assertEqual(sha(ROOT/hmb["path"]),hmb["sha256"])
        self.assertEqual(hmb["size_bytes"],(ROOT/hmb["path"]).stat().st_size)
        h=next(x for x in self.doc["individuals"] if x["character_id"]=="CHAR-AUSTIN-BYARS")
        delta=json.loads((ROOT/h["appearance_delta"]).read_text())
        self.assertIn("red eyes",str(delta).lower())
        dk=json.loads((ROOT/"canon/characters/VISUAL_REFERENCE_AUTHORITY_V1.json").read_text())
        conflict=next(x for x in dk["source_visual_conflicts"] if x["character_id"]=="CHAR-WILSON-LOOK")
        self.assertEqual(conflict["state"],"ACTIVE_CANON_VISUAL_CONFLICT_HOLD")
        self.assertFalse(any(x.get("new_primary_commissioner_approved",False) for x in self.doc["individuals"]))

    def test_spatial_never_invents_terrain_dimensions(self):
        d=json.loads((ROOT/"world/location-control-plane/evidence/APPROVED_LINEUP_SPATIAL_RECONCILIATION_2026_10_18.json").read_text())
        self.assertEqual(d["lineup_parent_sha256"],EXPECTED)
        self.assertTrue(d["existing_world_canon_unchanged"])
        self.assertEqual(d["metric_geometry_state"],"HOLD_UNTIL_MEASURED")
        self.assertEqual(len(d["subjects"]),12)
        own={x["character_id"]:x for x in self.dom["domains"]}
        for x in d["subjects"]:
            self.assertEqual(x["primary_location_id"],own[x["character_id"]]["primary_location_id"])
            self.assertEqual(set(x["region_ids"]),set(own[x["character_id"]]["physical_zone_ids"]))

if __name__=="__main__":
    unittest.main()
