import importlib.util
import json
import pathlib
import tempfile
import unittest

BASE=pathlib.Path(__file__).resolve().parents[1]
ROOT=BASE.parents[1]
BUILDER=BASE/"build_public_catalog.py"

def load_builder():
    if not BUILDER.exists():
        return None
    spec=importlib.util.spec_from_file_location("audience_catalog",BUILDER)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

class PublicCatalogV2Tests(unittest.TestCase):
    def setUp(self):
        self.builder=load_builder()

    def test_story_graph_fingerprint_is_preserved(self):
        self.assertIsNotNone(self.builder,"build_public_catalog.py required")
        with tempfile.TemporaryDirectory() as td:
            data=self.builder.build_catalog(pathlib.Path(td),render=False)
        web=json.loads((ROOT/"planning/story-production-graph/generated/2026/web_index.json").read_text())
        self.assertEqual(data["meta"]["storyGraphFingerprint"],web["source_fingerprint_sha256"])
        self.assertTrue(all(m["issueId"].startswith("MEMO-2026-W") for m in data["memos"]))

    def test_all_nine_memo_records_project_without_release_promotion(self):
        self.assertIsNotNone(self.builder)
        with tempfile.TemporaryDirectory() as td:
            data=self.builder.build_catalog(pathlib.Path(td),render=False)
        memos={m["week"]:m for m in data["memos"]}
        self.assertEqual(set(memos),set(range(1,10)))
        self.assertFalse(memos[1]["available"])
        self.assertEqual(memos[1]["publicationState"],"AUTHORITY_UNRESOLVED_PARTIAL_READBACK")
        for week in (4,7,8,9):
            self.assertFalse(memos[week]["available"])
            self.assertNotEqual(memos[week]["status"],"Released edition")

    def test_story_graph_timeline_projects_42_events_without_authority_change(self):
        self.assertIsNotNone(self.builder)
        with tempfile.TemporaryDirectory() as td:
            data=self.builder.build_catalog(pathlib.Path(td),render=False)
        source=json.loads((ROOT/"planning/story-production-graph/generated/2026/timeline.json").read_text())
        self.assertEqual(len(data["timeline"]),42)
        expected={e["event_id"]:(e["evidence_status"],e["canon_status"]) for e in source["entries"]}
        for row in data["timeline"]:
            self.assertEqual((row["evidenceStatus"],row["canonStatus"]),expected[row["eventId"]])

    def test_stale_fingerprint_fails_closed(self):
        self.assertIsNotNone(self.builder)
        web=json.loads((ROOT/"planning/story-production-graph/generated/2026/web_index.json").read_text())
        timeline=json.loads((ROOT/"planning/story-production-graph/generated/2026/timeline.json").read_text())
        timeline["source_fingerprint_sha256"]="0"*64
        with tempfile.TemporaryDirectory() as td:
            td=pathlib.Path(td)
            webp=td/"web.json"; timep=td/"timeline.json"
            webp.write_text(json.dumps(web)); timep.write_text(json.dumps(timeline))
            with self.assertRaises(ValueError):
                self.builder.build_catalog(td/"out",render=False,web_index_path=webp,timeline_path=timep)

    def test_current_character_and_world_projection_resolves(self):
        self.assertIsNotNone(self.builder)
        with tempfile.TemporaryDirectory() as td:
            data=self.builder.build_catalog(pathlib.Path(td),render=False)
        self.assertEqual(len(data["characters"]),12)
        locations={x["id"] for x in data["locations"]}
        self.assertGreaterEqual(len(locations),12)
        self.assertTrue(all(x["locationId"] in locations for x in data["characters"]))
        self.assertTrue(all(r["from"] in locations and r["to"] in locations for r in data["routes"]))

    def test_library_only_projects_canon_closed_manuscripts(self):
        self.assertIsNotNone(self.builder)
        with tempfile.TemporaryDirectory() as td:
            data=self.builder.build_catalog(pathlib.Path(td),render=False)
        self.assertEqual(len(data["chapters"]),4)
        self.assertTrue(all(x["releaseState"]=="CANON_CLOSED" for x in data["chapters"]))
        self.assertTrue(all(x["text"] for x in data["chapters"]))

    def test_public_catalog_omits_internal_editorial_fields(self):
        self.assertIsNotNone(self.builder)
        with tempfile.TemporaryDirectory() as td:
            data=self.builder.build_catalog(pathlib.Path(td),render=False)
        forbidden={"open_questions","candidate_catalog","editorial_candidates","credentials","tokens","private_analysis"}
        def walk(value):
            if isinstance(value,dict):
                self.assertTrue(forbidden.isdisjoint(value.keys()),f"forbidden public keys: {forbidden & set(value)}")
                for child in value.values(): walk(child)
            elif isinstance(value,list):
                for child in value: walk(child)
        walk(data)

    def test_public_source_links_are_revision_pinned(self):
        self.assertIsNotNone(self.builder)
        with tempfile.TemporaryDirectory() as td:
            data=self.builder.build_catalog(pathlib.Path(td),render=False)
        urls=[]
        def walk(value):
            if isinstance(value,dict):
                for key,child in value.items():
                    if key=="sourceUrl" and child: urls.append(child)
                    walk(child)
            elif isinstance(value,list):
                for child in value: walk(child)
        walk(data)
        self.assertTrue(urls)
        self.assertTrue(all("/blob/"+self.builder.REVISION+"/" in u or "/media/jakekaloper-hub/schemin-26/"+self.builder.REVISION+"/" in u for u in urls))
        self.assertTrue(all("/blob/main/" not in u for u in urls))

    def test_missing_released_artifact_never_becomes_active(self):
        self.assertIsNotNone(self.builder)
        issue={
          "issue_id":"MEMO-2026-W99","week":99,"publication_state":"RELEASED",
          "source_class":"TEST","coverage_state":"TEST","binary_in_repo":True,
          "canonical_artifact":"does/not/exist.pdf","event_count":0,"encounter_count":0,
          "scene_count":0,"scene_ids":[],"consumer_jobs":[]
        }
        projected=self.builder._project_memo(issue)
        self.assertFalse(projected["available"])
        self.assertIsNone(projected.get("pdf"))

    def test_dist_data_written_and_public_projection_is_read_only(self):
        self.assertIsNotNone(self.builder)
        with tempfile.TemporaryDirectory() as td:
            out=pathlib.Path(td)
            data=self.builder.build_catalog(out,render=False)
            self.assertTrue((out/"data.json").is_file())
            self.assertEqual(data["meta"]["authority"],"READ_ONLY_PRESENTATION_PROJECTION")
            self.assertNotIn("render_queue",data)

if __name__=="__main__":
    unittest.main()
