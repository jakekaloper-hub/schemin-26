"""Adversarial source-joined checks for the noncanon Novel reconstruction board proposal.

Runs under the existing Schemin World Engine CI civilization test discovery.
Does not claim manuscript publication acceptance or verify image reference bytes.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "world" / "data"
BOARD = ROOT / "living-novel" / "production" / "full-rewrite-2026"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _source_maps():
    domains = load(DATA / "owner_domains.json")["domains"]
    locations = load(DATA / "locations.json")["locations"]
    contexts = load(DATA / "settlements.json")["settlements"]
    regions = load(DATA / "physical_zones.json")["regions"]
    return (
        {d["character_id"]: d for d in domains},
        {l["id"]: l for l in locations},
        {s["id"]: s for s in contexts},
        {r["id"]: r for r in regions},
    )


def verify_scene_anchor(scene: dict, locations: dict, contexts: dict, regions: dict) -> bool:
    """Fail-closed for unresolved venue; permit only matching source IDs and regions."""
    loc_id, region_id, ctx_id = (
        scene.get("location_id"), scene.get("region_id"), scene.get("world_context_id")
    )
    if not all((loc_id, region_id, ctx_id)):
        return False
    loc, ctx = locations.get(loc_id), contexts.get(ctx_id)
    return bool(
        loc and ctx and region_id in regions
        and loc.get("physical_zone_id") == region_id
        and ctx.get("physical_zone_id") == region_id
        and loc_id in ctx.get("anchor_location_ids", [])
    )


class TestNovelReconstructionBoard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.crosswalk = load(BOARD / "R2_TWELVE_OWNER_WORLD_POV_CROSSWALK_V1.json")
        cls.scenes = load(BOARD / "R2_SCENE_REGISTER_CORRECTIVE_PROPOSAL_V2.json")
        cls.domains, cls.locations, cls.contexts, cls.regions = _source_maps()

    def test_exactly_twelve_canonical_principals(self):
        ids = [o["character_id"] for o in self.crosswalk["owners"]]
        self.assertEqual(len(ids), 12)
        self.assertEqual(len(set(ids)), 12)
        self.assertEqual(set(ids), set(self.domains))
        registry = (ROOT / "canon/characters/CHARACTER_REGISTRY.yaml").read_text()
        registry_ids = set(re.findall(r"(?m)^  - \{id: (CHAR-[A-Z-]+), owner:", registry))
        self.assertEqual(set(ids), registry_ids)

    def test_source_joined_home_locations_and_regions(self):
        self.assertEqual(len(self.regions), 7)
        for row in self.crosswalk["owners"]:
            with self.subTest(row=row["character_id"]):
                d = self.domains[row["character_id"]]
                loc = self.locations[d["primary_location_id"]]
                ctx = self.contexts[row["civilization_context_id"]]
                self.assertEqual(row["home_location_id"], d["primary_location_id"])
                self.assertEqual(row["home_region_id"], loc["physical_zone_id"])
                self.assertEqual(row["home_region_id"], ctx["physical_zone_id"])
                self.assertIn(row["home_region_id"], d["physical_zone_ids"])
                self.assertEqual(row["home_location_canon_status"], loc["canon_status"])
                self.assertEqual(row["ontology_class"], d["ontology_class"])
                self.assertEqual(row["home_route_ids"], loc.get("access_route_ids", []))

    def test_rewrite_proposal_has_every_actual_pov_segment(self):
        scenes = self.scenes["scenes"]
        ids = [s["scene_id"] for s in scenes]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(scenes), 6)
        self.assertEqual(
            [s["pov_character_id"] for s in scenes if s["file"] == "CHAPTER_03_REWRITE_CANDIDATE.md"],
            ["CHAR-WILSON-LOOK", "CHAR-JAKE-KALOPER", "CHAR-AUSTIN-BYARS"],
        )
        self.assertEqual(
            {s["file"] for s in scenes},
            {
                "PROLOGUE_REWRITE_CANDIDATE.md",
                "CHAPTER_01_REWRITE_CANDIDATE.md",
                "CHAPTER_02_REWRITE_CANDIDATE.md",
                "CHAPTER_03_REWRITE_CANDIDATE.md",
            },
        )
        for s in scenes:
            self.assertIn(s["pov_character_id"], self.domains)
            self.assertTrue((BOARD / "manuscript" / s["file"]).exists())
            self.assertNotEqual(s["status"], "CANON")

    def test_known_anchors_are_geographically_valid(self):
        for s in self.scenes["scenes"]:
            if s["location_id"] is None:
                self.assertEqual(s["status"], "BLOCKED_LOCATION_EVIDENCE")
                self.assertIsNone(s["region_id"])
                self.assertIsNone(s["world_context_id"])
            else:
                self.assertTrue(
                    verify_scene_anchor(s, self.locations, self.contexts, self.regions),
                    s["scene_id"],
                )
        obi = next(s for s in self.scenes["scenes"] if s["scene_id"] == "R2-PROLOGUE-OBI")
        self.assertEqual(obi["location_id"], "LOC-TRADE-JEDI-MOUNTAIN-BASE")
        self.assertEqual(obi["world_context_id"], "SETCTX-UPPER-VALLEYS")

    def test_adversarial_wrong_region_unknown_location_and_wrong_context(self):
        good = next(s for s in self.scenes["scenes"] if s["scene_id"] == "R2-PROLOGUE-OBI")
        self.assertTrue(verify_scene_anchor(good, self.locations, self.contexts, self.regions))
        for key, bad_value in [
            ("region_id", "REG-CENTRAL-BASIN"),
            ("world_context_id", "SETCTX-CENTRAL-BASIN"),
            ("location_id", "LOC-MISSING-FICTIONAL-CITY"),
        ]:
            bad = dict(good, **{key: bad_value})
            with self.subTest(case=key):
                self.assertFalse(verify_scene_anchor(bad, self.locations, self.contexts, self.regions))

    def test_noncanon_publication_firewall(self):
        self.assertEqual(self.crosswalk["status"], "DEVELOPMENT_PROPOSAL_NOT_CANON")
        self.assertEqual(self.scenes["status"], "DEVELOPMENT_ONLY_NOT_RELEASE_ELIGIBLE")
        self.assertEqual(
            len([s for s in self.scenes["scenes"] if s["status"] == "BLOCKED_LOCATION_EVIDENCE"]),
            3,
        )
        self.assertIn("unresolved", self.crosswalk["policy"]["elemental"].lower())

    def test_canonical_manuscript_is_not_in_board_output_paths(self):
        for proposed in (
            BOARD / "R2_TWELVE_OWNER_WORLD_POV_CROSSWALK_V1.json",
            BOARD / "R2_SCENE_REGISTER_CORRECTIVE_PROPOSAL_V2.json",
        ):
            self.assertIn("production/full-rewrite-2026", proposed.as_posix())
        self.assertNotIn("living-novel/manuscript/", str(BOARD))


if __name__ == "__main__":
    unittest.main()
