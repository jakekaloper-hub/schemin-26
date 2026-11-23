"""Regression tests for Week 11's scene-to-folio identity gate."""

import contextlib
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from validate_atlas_routes import check_scene_sites


ROOT = Path(__file__).resolve().parents[2]
WEEK = Path("memo-os/week-11")
BINDINGS = WEEK / "sets/location-bindings.json"
RECEIPT = WEEK / "preproduction/WEEK11_PRE_RENDER_REFERENCE_RECEIPT.json"
DESK = WEEK / "preproduction/WEEK11_LOCATION_DESK.json"
SCORES = WEEK / "preproduction/SUNDAY_2024_ET_SOURCE.json"
CONTROL = Path("world/location-control-plane")
REGISTRY = CONTROL / "registries/PARENT_SUBLOCATION_REGISTRY.json"
OWNERS = Path("world/data/owner_domains.json")
PRIMARIES = Path("canon/characters/reference_sources_v1.json")


def row(records, key, value):
    return next(record for record in records if record[key] == value)


class SceneIdentityTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        scenes = json.loads((ROOT / BINDINGS).read_text())["matchups"]
        cards = [CONTROL / "locations" / scene["location_id"] / "CARD.json" for scene in scenes]
        for path in [BINDINGS, RECEIPT, DESK, SCORES, REGISTRY, OWNERS, PRIMARIES, *cards]:
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, target)

    def gate(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return check_scene_sites(self.root)

    def load(self, path):
        return json.loads((self.root / path).read_text())

    def save(self, path, value):
        (self.root / path).write_text(json.dumps(value))

    def test_native_records_pass(self):
        self.assertTrue(self.gate())

    def test_reordered_inputs_pass(self):
        sources = [
            (BINDINGS, "matchups"), (RECEIPT, "matchups"),
            (SCORES, "week11_games"), (DESK, "folios"),
        ]
        for path, field in sources:
            doc = self.load(path)
            doc[field].reverse()
            if path == RECEIPT:
                for record in doc[field]:
                    record["cast"].reverse()
            self.save(path, doc)
        self.assertTrue(self.gate())

    def test_two_existing_sites_exchanged_between_games_fail(self):
        doc = self.load(BINDINGS)
        dunk = row(doc["matchups"], "matchup", "W11-G03")
        office = row(doc["matchups"], "matchup", "W11-G06")
        for field in ["location_id", "sublocation_handle"]:
            dunk[field], office[field] = office[field], dunk[field]
        self.save(BINDINGS, doc)
        self.assertFalse(self.gate())

    def test_missing_or_duplicate_scene_identity_fails(self):
        for path, key in [(BINDINGS, "matchup"), (RECEIPT, "id"), (SCORES, "game")]:
            field = "week11_games" if path == SCORES else "matchups"
            original = self.load(path)
            for mutation in ["omit", "duplicate"]:
                with self.subTest(path=path, mutation=mutation):
                    records = list(original[field])
                    if mutation == "omit":
                        records.pop()
                    else:
                        records[-1] = {**records[-1], key: records[0][key]}
                    self.save(path, {**original, field: records})
                    self.assertFalse(self.gate())
            self.save(path, original)

    def test_incorrect_or_duplicate_cast_fails(self):
        for substitute in ["CHAR-DAVID-BABB", "CHAR-BRANDON-PRYOR"]:
            with self.subTest(substitute=substitute):
                scenes = self.load(BINDINGS)
                dunk = row(scenes["matchups"], "matchup", "W11-G03")
                dunk["character_ids"] = [substitute, "CHAR-BRANDON-PRYOR"]
                self.save(BINDINGS, scenes)
                self.assertFalse(self.gate())

    def test_transposed_individual_receipt_identities_fail(self):
        for field in ["team", "character_id"]:
            with self.subTest(field=field):
                receipt = json.loads((ROOT / RECEIPT).read_text())
                jake, brandon = row(receipt["matchups"], "id", "W11-G03")["cast"]
                jake[field], brandon[field] = brandon[field], jake[field]
                self.save(RECEIPT, receipt)
                self.assertFalse(self.gate())

    def test_wrong_issue_fails(self):
        cases = [
            (BINDINGS, "week", 10),
            (RECEIPT, "season", 2025),
            (SCORES, "league_id", "999"),
            (SCORES, "season", 2025),
            (SCORES, "observed_at", "2026-11-16T01:24:20.535441+00:00"),
        ]
        for path, key, wrong in cases:
            with self.subTest(path=path, key=key):
                doc = self.load(path)
                self.save(path, {**doc, key: wrong})
                self.assertFalse(self.gate())
                self.save(path, doc)

    def test_other_cast_members_primary_receipt_fails(self):
        receipt = self.load(RECEIPT)
        jake, brandon = row(receipt["matchups"], "id", "W11-G03")["cast"]
        jake["registered_primary"] = brandon["registered_primary"]
        self.save(RECEIPT, receipt)
        self.assertFalse(self.gate())

    def test_private_interview_substituted_for_f16_fails(self):
        desk = self.load(DESK)
        ladder = row(desk["folios"], "folio", "F16")
        private = row(desk["folios"], "folio", "F31")
        for key in ["status", "location_ids", "selected_handle_ids"]:
            ladder[key] = private[key]
        self.save(DESK, desk)
        self.assertFalse(self.gate())

    def test_valid_feature_from_another_folio_fails(self):
        desk = self.load(DESK)
        ladder = row(desk["folios"], "folio", "F16")
        office = row(desk["folios"], "folio", "F22")
        ladder["selected_handle_ids"] = office["selected_handle_ids"]
        self.save(DESK, desk)
        self.assertFalse(self.gate())

    def test_duplicate_or_missing_selected_folio_fails(self):
        original = self.load(DESK)
        for mutation in ["omit", "duplicate"]:
            with self.subTest(mutation=mutation):
                folios = [f for f in original["folios"] if f["folio"] != "F16"]
                if mutation == "duplicate":
                    folios.append(row(folios, "folio", "F15"))
                self.save(DESK, {**original, "folios": folios})
                self.assertFalse(self.gate())

    def test_cross_assigned_folios_fail(self):
        receipt = self.load(RECEIPT)
        dunk = row(receipt["matchups"], "id", "W11-G03")["rehearsal_folios"]
        office = row(receipt["matchups"], "id", "W11-G06")["rehearsal_folios"]
        dunk[-1], office[-1] = office[-1], dunk[-1]
        self.save(RECEIPT, receipt)
        self.assertFalse(self.gate())

    def test_location_work_instructions_must_use_the_scene_cast(self):
        desk = self.load(DESK)
        base = row(desk["locations"], "location_id", "LOC-TRADE-JEDI-MOUNTAIN-BASE")
        base["week11"]["character_ids"][1] = "CHAR-DAVID-BABB"
        self.save(DESK, desk)
        self.assertFalse(self.gate())

    def test_folio_removed_from_both_receipt_and_page_list_fails(self):
        receipt = self.load(RECEIPT)
        row(receipt["matchups"], "id", "W11-G03")["rehearsal_folios"].remove(16)
        self.save(RECEIPT, receipt)
        desk = self.load(DESK)
        desk["folios"].remove(row(desk["folios"], "folio", "F16"))
        self.save(DESK, desk)
        self.assertFalse(self.gate())

    def test_silently_dropped_or_repeated_scene_folio_fails(self):
        for pages in [[14, 15], [14, 15, 15, 16]]:
            with self.subTest(pages=pages):
                receipt = self.load(RECEIPT)
                row(receipt["matchups"], "id", "W11-G03")["rehearsal_folios"] = pages
                self.save(RECEIPT, receipt)
                self.assertFalse(self.gate())

    def test_missing_reference_receipt_fails(self):
        (self.root / RECEIPT).unlink()
        self.assertFalse(self.gate())


if __name__ == "__main__":
    unittest.main()
