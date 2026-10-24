"""Tests for development-only rewrite scene segmentation and fail-closed venue review."""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import importlib.util
spec=importlib.util.spec_from_file_location(
    "rewrite_gate",ROOT/"living-novel/os/qa/twelve_owner_rewrite_gate.py"
)
gate=importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
canonical_owner_ids=gate.canonical_owner_ids
validate_rewrite_scene=gate.validate_rewrite_scene
BASE=ROOT/"living-novel/production/full-rewrite-2026"

POV_LINE=re.compile(r"\*\*POV:[^\n]*?(CHAR-[A-Z-]+)\*\*")

class RewriteCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.register=json.loads((BASE/"SCENE_REGISTER.json").read_text(encoding="utf-8"))

    def test_four_draft_files_and_six_actual_pov_segments(self):
        reg=self.register
        self.assertEqual(reg["status"],"DEVELOPMENT_CANDIDATE_NOT_CANON")
        self.assertEqual(len(reg["scenes"]),6)
        groups={}
        for scene in reg["scenes"]:
            groups.setdefault(scene["file"],[]).append(scene)
        self.assertEqual(len(groups),4)
        self.assertEqual(sorted(map(len,groups.values())),[1,1,1,3])
        for file,scenes in groups.items():
            text=(BASE/"manuscript"/file).read_text(encoding="utf-8")
            self.assertGreater(len(text.split()),300)
            headers=list(POV_LINE.finditer(text))
            scenes=sorted(scenes,key=lambda x:x["scene_part"])
            self.assertEqual(len(headers),len(scenes),file)
            for index,scene in enumerate(scenes):
                start=headers[index].start()
                stop=headers[index+1].start() if index+1<len(headers) else len(text)
                segment=text[start:stop]
                self.assertEqual(scene["scene_part"],index+1)
                self.assertEqual(scene["pov_character_id"],headers[index].group(1))
                errors=validate_rewrite_scene({**scene,"manuscript_text":segment})
                if scene["status"]=="BLOCKED_LOCATION_EVIDENCE":
                    self.assertIn("SHARED_WORLD_CONTEXT_REQUIRED",errors)
                else:
                    self.assertEqual(errors,[],(file,scene["scene_id"],errors))
                self.assertFalse(gate.OLD_POV_NAMES.search(segment))
                for match in re.findall(r"CHAR-[A-Z-]+",segment):
                    self.assertIn(match,canonical_owner_ids())

    def test_chapter_three_three_distinct_owner_povs(self):
        scenes=[
            s for s in self.register["scenes"]
            if s["file"]=="CHAPTER_03_REWRITE_CANDIDATE.md"
        ]
        self.assertEqual(
            [s["pov_character_id"] for s in sorted(scenes,key=lambda s:s["scene_part"])],
            ["CHAR-WILSON-LOOK","CHAR-JAKE-KALOPER","CHAR-AUSTIN-BYARS"],
        )

    def test_three_explicit_location_holds(self):
        held=[s for s in self.register["scenes"] if s["status"]=="BLOCKED_LOCATION_EVIDENCE"]
        self.assertEqual(len(held),3)
        for s in held:
            self.assertIsNone(s["location_id"])
            self.assertIsNone(s["region_id"])
            self.assertIsNone(s["world_context_id"])

    def test_source_proposal_matches_active_development_register(self):
        proposal=json.loads(
            (BASE/"R2_SCENE_REGISTER_CORRECTIVE_PROPOSAL_V2.json").read_text(encoding="utf-8")
        )
        by_id={s["scene_id"]:s for s in self.register["scenes"]}
        self.assertEqual(set(by_id),{s["scene_id"] for s in proposal["scenes"]})
        for s in proposal["scenes"]:
            active=by_id[s["scene_id"]]
            for key in ("file","scene_part","pov_character_id","location_id","region_id",
                        "world_context_id","time_cutoff","status","evidence_ref"):
                self.assertEqual(active[key],s[key],(s["scene_id"],key))

    def test_legacy_is_not_overwritten(self):
        original=(ROOT/"living-novel/manuscript/PROLOGUE_DRAFT_V1.md")
        self.assertTrue(original.exists())
        self.assertNotEqual((BASE/"manuscript/PROLOGUE_REWRITE_CANDIDATE.md").read_text(),
                            original.read_text())

if __name__=="__main__":
    unittest.main()
