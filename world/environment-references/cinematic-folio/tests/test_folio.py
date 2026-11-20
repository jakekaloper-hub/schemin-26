"""Executable provenance and nonpromotion checks for the code-only Folio Studio."""
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

FOLIO = Path(__file__).resolve().parents[1]
ROOT = FOLIO.parents[2]
SITE = FOLIO / "site"
DATA = json.loads((SITE / "data" / "world.json").read_text())

class FolioTests(unittest.TestCase):
    def test_three_divisions_of_four(self):
        divs = DATA["divisions"]
        self.assertEqual({d["id"] for d in divs}, {"DIV-BURGERS","DIV-WINGS","DIV-PIZZA"})
        self.assertEqual([len(d["member_team_ids_2026"]) for d in divs], [4,4,4])
        self.assertEqual(len({t for d in divs for t in d["member_team_ids_2026"]}),12)
        self.assertEqual({p["team_id"] for p in DATA["characters"]},
                         {t for d in divs for t in d["member_team_ids_2026"]})

    def test_twelve_distinct_character_homes(self):
        homes = DATA["characters"]
        locations = {l["id"]:l for l in DATA["locations"]}
        self.assertEqual(len(homes),12)
        self.assertEqual(len({x["character_id"] for x in homes}),12)
        self.assertEqual(len({x["primary_location_id"] for x in homes}),12)
        for home in homes:
            loc = locations[home["primary_location_id"]]
            self.assertEqual(loc["home_character_id"],home["character_id"])
            self.assertEqual(loc["home_team"],home["team"])

    def test_zones_and_mainline_legal_routes(self):
        self.assertEqual(len(DATA["regions"]),7)
        self.assertEqual(len(DATA["routes"]),18)
        ids={l["id"] for l in DATA["locations"]}
        for route in DATA["routes"]:
            self.assertTrue({route["from"],route["to"]}.issubset(ids))
            self.assertTrue(set(route.get("via_location_ids",[])).issubset(ids))
        self.assertEqual(len(DATA["locations"]),23)

    def test_shared_march_is_not_a_division_border(self):
        loc=next(l for l in DATA["locations"] if l["id"]=="LOC-TDS-CHILI-SHARED-MARCH")
        self.assertEqual(set(loc["membership_overlays"]),{"DIV-BURGERS","DIV-WINGS"})
        self.assertIsNone(loc["division_id"])
        self.assertIn("nonexclusive",DATA["division_law"].lower())

    def test_structural_references_are_exact_approved_bytes(self):
        for loc in DATA["locations"]:
            ref=loc["structural_reference"]
            real=ROOT / ref["source_path"]
            local=SITE / ref["local_path"]
            self.assertTrue(real.is_file() and local.is_file())
            a=hashlib.sha256(real.read_bytes()).hexdigest()
            b=hashlib.sha256(local.read_bytes()).hexdigest()
            self.assertEqual(ref["sha256"],a)
            self.assertEqual(a,b)
            self.assertIsNone(loc["cinematic_asset"]["approved_reference_uri"])
            self.assertEqual(loc["cinematic_asset"]["status"],"MISSING_APPROVED_CINEMATIC_REFERENCE")

    def test_no_cinematic_image_generated(self):
        image_paths=list(FOLIO.rglob("*.png"))+list(FOLIO.rglob("*.webp"))+list(FOLIO.rglob("*.jpg"))
        self.assertEqual(image_paths,[],"No image-generation artifacts are allowed in code-only branch")

    def test_state_asof_not_misrepresented_as_today(self):
        self.assertEqual(DATA["world_state_as_of"],"end_of_week_3_2026")
        self.assertIn("not verified",DATA["world_state_warning"])
        self.assertTrue(any(e["id"]=="EVT-W3-MIRE-HILL" for e in DATA["events"]))

    def test_cross_pr_199_union_not_main(self):
        preview=DATA["cross_pr"]
        self.assertEqual(len(preview["proposals"]),199)
        self.assertEqual(preview["concordance"]["shared_ids"],103)
        self.assertEqual(preview["concordance"]["pr324_only_ids"],52)
        self.assertEqual(preview["concordance"]["pr325_only_ids"],44)
        self.assertEqual(sum(x["source_class"]=="ACTIVE_MAIN_LOC" for x in preview["proposals"]),23)
        self.assertEqual(sum(x["source_class"]=="MAIN_EDITORIAL_CANDIDATE" for x in preview["proposals"]),48)
        self.assertFalse(any(x["production_access"]!="DRAFT_ONLY_NO_CANON_PROMOTION" for x in preview["proposals"]))

    def test_23_node_45_edge_causeway(self):
        island=DATA["cross_pr"]["island"]
        nodes={n["id"] for n in island["nodes"]}
        self.assertEqual(len(nodes),23)
        self.assertEqual(len(island["edges"]),45)
        self.assertEqual(len(island["venues"]),9)
        for edge in island["edges"]:
            self.assertIn(edge["from"],nodes)
            self.assertIn(edge["to"],nodes)
        # The mainland approach to the proposed island must connect via the
        # actual proposed causeway spine, never an invented direct teleport.
        adjacency={}
        for edge in island["edges"]:
            adjacency.setdefault(edge["from"],set()).add(edge["to"])
            adjacency.setdefault(edge["to"],set()).add(edge["from"])
        visited={"MAINLAND_PUBLIC_LITTORAL"}
        stack=list(visited)
        while stack:
            for next_node in adjacency.get(stack.pop(),[]):
                if next_node not in visited:
                    visited.add(next_node);stack.append(next_node)
        self.assertIn("LAST_FIELD",visited)
        self.assertIn("LOSERS_BEACH",visited)
        self.assertIn("CAUSEWAY_RIDGE",visited)
        self.assertIsNone(next(n for n in island["nodes"] if n["id"]=="CAUSEWAY_RIDGE")["coordinates"])
        self.assertFalse(island["main_world_mutated"])

    def test_copy_no_character_gallery_bytes(self):
        self.assertEqual(DATA["cross_pr"]["character_library"]["count"],12)
        self.assertFalse(any("canon/characters/assets" in str(p) for p in SITE.rglob("*")))
        self.assertTrue(all(x["portrait_display_permission"]=="INTERNAL_REVIEW_ONLY_NOT_BUNDLED"
                            for x in DATA["characters"]))

    def test_all_folio_input_sources_sha_match(self):
        for source in DATA["source_sha256"].values():
            f=ROOT / source["path"]
            self.assertEqual(hashlib.sha256(f.read_bytes()).hexdigest(),source["sha256"])

    def test_frontend_structure_and_offline(self):
        html=(SITE/"index.html").read_text()
        js=(SITE/"app.js").read_text()
        self.assertEqual(html.count('class="view"'),5)
        for name in ("atlas","divisions","locations","island","proposals","sources"):
            self.assertIn('data-view="'+name+'"',html)
            self.assertIn('id="view-'+name+'"',html)
        self.assertIn('DOMContentLoaded',js)
        self.assertNotIn("eval(",js)
        self.assertNotIn("document.write(",js)
        self.assertNotIn("innerHTML =",js)
        self.assertNotIn("generateImage",js)
        self.assertNotIn("openai.com",html+js)
        self.assertNotIn("cdn.",html+js)

    def test_compilation_reproducible(self):
        result=subprocess.run([sys.executable,str(FOLIO/"build_folio.py"),"--check"],
                              capture_output=True,text=True,cwd=ROOT,check=True)
        self.assertIn("PASS",result.stdout)

if __name__=="__main__":
    unittest.main()
