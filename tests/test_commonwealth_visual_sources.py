"""Independent read-only regression checks for visual-source generation."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIS = ROOT / "docs/visual"

class VisualSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for script in ("build_command_center.py", "build_atlas.py", "build_publications.py"):
            subprocess.run([sys.executable, str(VIS / script)], cwd=ROOT, check=True, capture_output=True)

    def test_atlas_counts_and_endpoint_integrity(self):
        src = json.loads((ROOT/"world/data/locations.json").read_text())["locations"]
        routes = json.loads((ROOT/"world/data/routes.json").read_text())["routes"]
        events = json.loads((ROOT/"world/data/world_state_events.json").read_text())["events"]
        derived = json.loads((VIS/"atlas-data.json").read_text())
        self.assertEqual({x["id"] for x in src}, {x["id"] for x in derived["locations"]})
        self.assertEqual({x["id"] for x in routes}, {x["id"] for x in derived["routes"]})
        self.assertEqual({x["id"] for x in events}, {x["id"] for x in derived["events"]})
        self.assertTrue(all(r["from"] in {x["id"] for x in src} and r["to"] in {x["id"] for x in src} for r in routes))
        self.assertIn("non-metric",derived["coordinate_space"])

    def test_history_classification_preserved(self):
        src={x["id"]:x for x in json.loads((ROOT/"world/data/world_state_events.json").read_text())["events"]}
        derived=json.loads((VIS/"atlas-data.json").read_text())
        for x in derived["events"]:
            self.assertEqual(src[x["id"]]["classification"], x["classification"])
        source_state=json.loads((ROOT/"world/data/current_world_state.json").read_text())
        self.assertEqual(derived["state_as_of"],source_state["as_of"])

    def test_publications_not_promoted(self):
        src=json.loads((ROOT/"governance/publication-manifest/PUBLICATION_MANIFEST_V1.json").read_text())["publications"]
        derived=json.loads((VIS/"publications-data.json").read_text())["publications"]
        self.assertEqual({x["publication_id"]:x["release_state"] for x in src},
                         {x["publication_id"]:x["release_state"] for x in derived})

    def test_explicit_evidence_graph(self):
        import subprocess
        subprocess.run([sys.executable,str(VIS / "build_evidence_graph.py")],cwd=ROOT,check=True,capture_output=True)
        data=json.loads((VIS / "evidence-graph.json").read_text())
        ids={x["id"] for x in data["nodes"]}
        self.assertEqual(len(ids),len(data["nodes"]))
        self.assertTrue(all(x["from"] in ids and x["to"] in ids for x in data["edges"]))
        self.assertTrue(all(x["classification"]=="EXPLICIT_REFERENCE" for x in data["edges"]))
        self.assertFalse(any("MEMO_PAGE" in x["relation"] or "LEAGUE_FACT" in x["relation"] for x in data["edges"]))
        self.assertEqual(len(data["unresolved"]),14)

    def test_portal_routes_and_source_presence(self):
        records=json.loads((VIS/"command-center.json").read_text())["modules"]
        self.assertEqual(len(records),24)
        self.assertEqual(len({x["area"] for x in records}),6)
        self.assertTrue(all((ROOT/x["path"]).is_file() for x in records))
        self.assertTrue(all(x.get("panel") is None or (VIS/x["panel"]).is_file() for x in records))
        page=(VIS/"index.html").read_text()
        self.assertEqual(page.count('class="portrait"'),12)
        self.assertEqual(page.count('class="feature"'),8)
        self.assertIn('MAKES HISTORY',page)

if __name__ == "__main__":
    unittest.main()
