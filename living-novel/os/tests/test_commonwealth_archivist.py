import json
import tempfile
import unittest
from pathlib import Path
from living_novel_archivist_test_support import load_archivist

build = load_archivist()

class CommonwealthArchivistTests(unittest.TestCase):
    def test_provenance_and_event_join(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/"world/data").mkdir(parents=True)
            payloads={
                "locations.json":{"locations":[{"id":"LOC-A","name":"A","canon_status":"PERMANENT_CANON","source_provenance":["a.md"]}]},
                "world_state_events.json":{"events":[{"id":"E-1","week":3,"location_id":"LOC-A","event_type":"scar","classification":"WORLD_CANON","source_provenance":["b.md"],"continuity_out":["scar remains"]}]},
                "location_relationship_graph.json":{"relationships":[{"type":"WITHIN","from":"LOC-A","to":"REG-X"}]}
            }
            for name,data in payloads.items():
                (root/"world/data"/name).write_text(json.dumps(data))
            r=build(root)
            self.assertEqual(r["counts"]["events"],1)
            self.assertEqual(r["entries"][0]["events"][0]["source_provenance"],["b.md"])
            self.assertEqual(r["findings"],[])
    def test_orphan_event_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/"world/data").mkdir(parents=True)
            for name,obj in [
                ("locations.json",{"locations":[]}),
                ("world_state_events.json",{"events":[{"id":"X","location_id":"LOC-MISSING","source_provenance":["a"]}]}),
                ("location_relationship_graph.json",{"relationships":[]})]:
                (root/"world/data"/name).write_text(json.dumps(obj))
            self.assertEqual(build(root)["findings"][0]["code"],"ORPHAN_EVENT_LOCATION")

if __name__=="__main__":
    unittest.main()
