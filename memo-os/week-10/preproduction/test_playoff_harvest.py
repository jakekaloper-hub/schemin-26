"""Regression checks for the scoped Week 10 source-to-render integration."""
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from integrate_playoff_harvest import SELECTED, snapshot_digest, synchronize

P = Path(__file__).resolve().parent


def read(name, root=P):
    return json.loads((root / name).read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prompt_section(prompt, heading, next_heading):
    return json.loads(prompt.split("\n\n" + heading + "\n", 1)[1]
                     .split("\n\n" + next_heading + "\n", 1)[0])


class PlayoffHarvest(unittest.TestCase):
    def setUp(self):
        self.h = read("playoff-harvest.json")
        self.i = read("issue-previs.json")
        self.pages = {p["page_id"]: p for p in self.i["pages"]}

    def test_league_snapshot_matches_finalized_issue(self):
        h, facts = self.h, read("facts.json")
        self.assertEqual((h["league_id"], h["season"], h["through_week"]), (1417621, 2026, 10))
        self.assertEqual(h["canonical_fact_bundle_sha256"], digest(P / "facts.json"))
        self.assertEqual(len(facts["teams"]), 12)
        self.assertTrue(facts["finality"]["all_six_decided"])
        self.assertEqual(facts["rules"]["playoff_berths"], h["rules"]["playoff_berths"])
        # Complete provider rows and replay witnesses belong to the protected
        # artifact. Bind this public receipt to the exact reviewed payload.
        self.assertEqual(h["protected_artifact"]["sha256"],
                         "9ec5f9c634326a68dab579051ba199fc766c16b21bde32e17aef4cf7dc7e3b1d")

    def test_selected_copy_reaches_every_existing_consumer(self):
        plan = read("playoff-harvest-copy.json")["pages"]
        briefs = {x["page_id"]: x for x in read("illustrated-page-briefs.json")["pages"]}
        folios = {x["page_id"]: x for x in read("storyboard-folio-plan-pass5.json")["folios"]}
        cards = {x["unit_id"]: x for x in read("storycards.json")["departments"]}
        for pid in SELECTED:
            page = self.pages[pid]
            expected = plan[pid]["publication_copy"]
            request = read("render-inputs/" + pid + "/request.json")
            for actual in (page["draft_copy"], page["draft_copy_template"],
                           briefs[pid]["publication_copy"], briefs[pid]["exact_copy_template"],
                           folios[pid]["publication_copy"], cards[page["source_card_id"]]["draft_copy"],
                           cards[page["source_card_id"]]["draft_copy_template"], request["publication_copy"]):
                self.assertEqual(actual, expected, pid)
            self.assertEqual(page["illustrated_page_brief"], briefs[pid])
            self.assertEqual(request["prompt"], page["candidate_render_prompt"])
            self.assertEqual(request["prompt"], briefs[pid]["artist_prompt"])
            self.assertEqual(prompt_section(request["prompt"], "EXACT FULL PUBLICATION COPY", "FACT POLICY"), expected)
            self.assertEqual(prompt_section(request["prompt"], "FACT POLICY", "REFERENCE IMAGES"), request["sports_policy"])
            self.assertEqual((P / "render-inputs" / pid / "full-page-prompt.md").read_text(), request["prompt"] + "\n")
            for name in ("issue-draft.md", "storyboard-folio-plan-pass5.md", "illustrated-page-briefs.md"):
                self.assertIn(expected["body"], (P / name).read_text(), name)

    def test_source_bindings_point_to_the_actual_harvest(self):
        source_hash = digest(P / "playoff-harvest.json")
        for pid in SELECTED:
            page = self.pages[pid]
            request = read("render-inputs/" + pid + "/request.json")
            bindings = [x for x in request["sports_policy"]["refresh_fields"]
                        if x.get("artifact") == "playoff-harvest.json"]
            self.assertEqual([x["selector"] for x in bindings],
                             ["/claims/" + c for c in self.h["page_claims"][pid]])
            for field in bindings:
                value = self.h["claims"][field["selector"].rsplit("/", 1)[1]]
                self.assertEqual(field["snapshot_sha256"], snapshot_digest(value))
                self.assertEqual(field["value_location"], "playoff-harvest.json#" + field["selector"])
                self.assertEqual(field["source_bundle_sha256"], source_hash)
                self.assertNotIn("snapshot_value", field)
            self.assertEqual(page["playoff_harvest_binding"]["sha256"], source_hash)
            self.assertEqual(request["sports_policy"]["source_fact_bundle_sha256"], digest(P / "facts.json"))

    def test_opposite_vendor_results_are_not_reversed(self):
        runs = {r["name"]: r for r in self.h["vendor_experiment"]["selected_runs"]}
        win = runs["W11_ObiWan_beats_Chili"]
        lose = runs["W11_Chili_beats_ObiWan"]
        self.assertEqual(win["fixedResults"], [{"week": 11, "winner": "ObiWan Jacoby", "loser": "The Chili Cheesers", "winner_id": 1, "loser_id": 7}])
        self.assertEqual(lose["fixedResults"], [{"week": 11, "winner": "The Chili Cheesers", "loser": "ObiWan Jacoby", "winner_id": 7, "loser_id": 1}])
        raw = self.h["claims"]["w11_obi_chili_vendor_split"]["raw_percentages"]
        for team, win_run, loss_run in (("ObiWan Jacoby", win, lose), ("The Chili Cheesers", lose, win)):
            self.assertEqual(raw[team]["if_win"], win_run["totals"][team])
            self.assertEqual(raw[team]["if_loss"], loss_run["totals"][team])
        callout = self.pages["W10-P31"]["draft_copy"]["callouts"][0]
        self.assertIn("ObiWan Jacoby 52% / 13%", callout["body"])
        self.assertIn("The Chili Cheesers 58% / 21%", callout["body"])
        self.assertIn("THEFFHUB", callout["heading"])
        for phrase in ("Nov. 17, 2026", "Other games simulated", "10,000", "excluding projections and NFL byes"):
            self.assertIn(phrase, callout["body"])

    def test_visible_qualifiers_and_only_mud_loss_elimination(self):
        p30 = self.pages["W10-P30"]["draft_copy"]
        self.assertIn("Record scenarios assume no tied games.", p30["body"])
        self.assertIn("eight alone does not", p30["body"])
        for pid in SELECTED:
            self.assertNotIn("must win out", json.dumps(self.pages[pid]["draft_copy"]).lower())
        self.assertEqual(read("facts.json")["week11_implications"]["only_automatic_loss_elimination_team"], "T10")
        self.assertIn("mud_official_tie_survival", self.h["claims"])

    def test_public_receipt_does_not_publish_protected_payloads(self):
        for key in ("finalized_standings", "completed_game_ledger", "remaining_fixtures", "team_povs", "evidence"):
            self.assertNotIn(key, self.h)
        text = json.dumps(self.h)
        for value in ("libfile_", "oai-library://", "/workspace/scratch/", "LLC_low_score_win_out_trial"):
            self.assertNotIn(value, text)
        self.assertEqual(len(self.h["vendor_experiment"]["selected_runs"]), 2)
        for run in self.h["vendor_experiment"]["selected_runs"]:
            self.assertNotIn("table", run)
            self.assertEqual(set(run["totals"]), {"ObiWan Jacoby", "The Chili Cheesers"})

    def test_global_production_pause_and_existing_issue_shape(self):
        manifest = read("render-inputs/manifest.json")
        self.assertEqual(manifest["page_count"], 34)
        self.assertEqual(manifest["sheet_page_counts"], [6, 6, 6, 6, 6, 4])
        self.assertNotIn("W10-P32", self.i["recommended_reading_order"])
        objects = [self.i, manifest] + [read("render-inputs/" + p + "/request.json") for p in SELECTED]
        for obj in objects:
            gate = obj["production_gate"]
            self.assertFalse(gate["image_generation_authorized"])
            self.assertFalse(gate["image_generation_executed"])
            self.assertFalse(gate["publication_approved"])
            self.assertTrue(gate["backend_source_ready"])

    def test_consumption_receipt_matches_actual_copy_and_requests(self):
        receipt = read("playoff-harvest-consumption.json")
        self.assertEqual(receipt["source_receipt"]["sha256"], digest(P / "playoff-harvest.json"))
        self.assertEqual(receipt["protected_source"], self.h["protected_artifact"])
        self.assertEqual({p["page_id"] for p in receipt["pages"] if p["disposition"] == "SELECTED_CHANGE"}, set(SELECTED))
        for page in receipt["pages"]:
            index = int(page["copy_pointer"].split("/pages/", 1)[1].split("/", 1)[0])
            self.assertEqual(self.i["pages"][index]["page_id"], page["page_id"])
            self.assertEqual(page["copy_sha256"], snapshot_digest(self.i["pages"][index]["draft_copy"]))
            self.assertEqual(page["request_sha256"], digest(P / page["request"]))

    def test_resynchronization_is_idempotent_and_rejects_stale_facts(self):
        files = ["facts.json", "playoff-harvest.json", "playoff-harvest-copy.json", "issue-previs.json",
                 "illustrated-page-briefs.json", "storyboard-folio-plan-pass5.json", "storycards.json",
                 "director-sequences.json", "render-inputs/manifest.json", "issue-draft.md",
                 "illustrated-page-briefs.md", "storyboard-folio-plan-pass5.md"]
        files += ["playoff-harvest-consumption.json"]
        files += ["render-inputs/" + pid + "/request.json" for pid in ("W10-P27", "W10-P29", "W10-P35")]
        files += ["render-inputs/" + pid + "/" + name for pid in SELECTED
                  for name in ("request.json", "full-page-prompt.md")]
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in files:
                (root / name).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(P / name, root / name)
            before = {name: digest(root / name) for name in files}
            synchronize(root)
            self.assertEqual(before, {name: digest(root / name) for name in files})
            (root / "facts.json").write_text((root / "facts.json").read_text() + "\n")
            with self.assertRaisesRegex(ValueError, "finalized source changed"):
                synchronize(root)
            self.assertEqual(before["issue-previs.json"], digest(root / "issue-previs.json"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
