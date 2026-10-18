"""Validate pixel-only panel derivatives; forbid source supersession and false QA."""
import hashlib,json,struct,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
RECEIPT=ROOT/"canon/characters/lineup_2026_10_18/NAMEPLATE_TRIMMED_DERIVATIVES_2026_10_18.json"
MASTER=ROOT/"canon/characters/APPROVED_LINEUP_2026_10_18.json"

class TrimmedLineupDerivativeTests(unittest.TestCase):
    def test_original_lineup_unmodified_and_twelve_derivatives_are_traced(self):
        doc=json.loads(RECEIPT.read_text()); master=json.loads(MASTER.read_text())
        original=ROOT/master["stored_repository_path"]
        self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(),master["sha256"])
        self.assertEqual(doc["approved_lineup_sha256"],master["sha256"])
        self.assertEqual(len(doc["items"]),12)
        self.assertEqual(len({i["character_id"] for i in doc["items"]}),12)
        self.assertEqual({i["character_id"] for i in doc["items"]},
                         {m["character_id"] for m in master["individuals"]})
        self.assertTrue(doc["original_master_unchanged"])
        self.assertTrue(doc["existing_twelve_original_crops_unchanged"])

    def test_pixel_crop_lineage_and_strict_qa_hold(self):
        doc=json.loads(RECEIPT.read_text())
        self.assertFalse(doc["all_images_subject_isolated"])
        self.assertEqual(doc["release_status"],"NOT_PRODUCTION_RENDER_REFERENCE")
        members={x["character_id"]:x for x in json.loads(MASTER.read_text())["individuals"]}
        for r in doc["items"]:
            cid=r["character_id"]
            original=members[cid]["crop_rectangle_top_left"]
            crop=r["source_rectangle_top_left"]
            self.assertEqual(crop["x"],original["x"])
            self.assertEqual(crop["y"],original["y"])
            self.assertEqual(crop["width"],original["width"])
            self.assertGreater(crop["height"],0)
            self.assertLess(crop["height"],original["height"])
            self.assertEqual(r["source_crop_sha256"],members[cid]["crop_sha256"])
            p=ROOT/r["repository_path"]
            data=p.read_bytes()
            self.assertEqual(data[:8],b"\x89PNG\r\n\x1a\n")
            width,height=struct.unpack(">II",data[16:24])
            self.assertEqual((width,height),(crop["width"],crop["height"]))
            self.assertEqual(hashlib.sha256(data).hexdigest(),r["derived_sha256"])
            self.assertEqual(len(data),r["byte_size"])
            self.assertEqual(r["subject_isolation_qa"],"ISOLATION_QA_HOLD")
            self.assertFalse(r["rendering_eligible"])
            self.assertFalse(r["source_primary_supersession"])

if __name__=="__main__":
    unittest.main()
