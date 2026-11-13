import importlib.util,sys,unittest
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/"planning/story-production-graph"
sys.path.insert(0,str(BASE))

def load(name):
    spec=importlib.util.spec_from_file_location(name,BASE/f"{name}.py")
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

season_mod=load("adapt_2026_memo_season")
chron_mod=load("build_2026_chronicle")
compiler_mod=load("build_2026_season_compiler")

class Season2026GraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.season=season_mod.compile_season()
        cls.chron=chron_mod.build()
        cls.compiler=compiler_mod.build()

    def test_all_nine_memo_cycles_are_registered(self):
        self.assertEqual([i["week"] for i in self.season["issues"]],list(range(1,10)))
        self.assertEqual(self.season["coverage"]["issue_count"],9)

    def test_external_binary_gaps_are_explicit_not_reconstructed(self):
        self.assertEqual(self.season["coverage"]["external_binary_gap_weeks"],[1,2])
        for i in self.season["issues"][:2]:
            self.assertFalse(i["binary_in_repo"])

    def test_registry_source_paths_resolve(self):
        import json
        reg=json.loads((BASE/"season_2026_memo_registry.json").read_text())
        for week in reg["weeks"]:
            for ref in week["authority_refs"]:
                self.assertTrue((ROOT/ref).exists(),f"missing authority ref: {ref}")
            for key in ("fact_source","story_source","scene_source"):
                ref=week.get(key)
                if ref:
                    self.assertTrue((ROOT/ref).exists(),f"missing {key}: {ref}")

    def test_weeks_3_to_9_have_all_six_matchup_events(self):
        counts=Counter(e["league_time"]["week"] for e in self.season["events"])
        self.assertEqual(counts,{3:6,4:6,5:6,6:6,7:6,8:6,9:6})
        self.assertEqual(len(self.season["events"]),42)

    def test_each_current_character_has_seven_recoverable_matchup_events(self):
        timelines=self.chron["character_timelines"]
        self.assertEqual(len(timelines),12)
        self.assertEqual(sorted(len(v["entries"]) for v in timelines.values()),[7]*12)

    def test_scene_hydration_spans_multiple_memo_generations(self):
        scene_weeks={s["event_id"].split("-W")[1][:2] for s in self.season["scenes"]}
        self.assertTrue({"05","06","09"}.issubset(scene_weeks))
        self.assertGreaterEqual(len(self.season["scenes"]),30)

    def test_week6_has_six_exact_location_encounters(self):
        enc=[e for e in self.season["encounters"] if e["encounter_id"].startswith("ENC-2026-W06-")]
        self.assertEqual(len(enc),6)
        self.assertTrue(all(e["location"]["location_id"].startswith("LOC-") for e in enc))

    def test_compiler_has_all_nine_issue_jobs(self):
        ids=set(self.compiler["inputs"]["memo_issue_ids"])
        self.assertEqual(ids,{f"MEMO-2026-W{i:02d}" for i in range(1,10)})
        issue_jobs=[j for j in self.compiler["jobs"] if j["job_id"].startswith("JOB-MEMO-2026-")]
        self.assertEqual(len(issue_jobs),18)

    def test_no_world_writeback_is_silently_enabled(self):
        self.assertTrue(all(e["state"]["world_writeback_allowed"] is False for e in self.season["events"]))

if __name__=="__main__":
    unittest.main()
