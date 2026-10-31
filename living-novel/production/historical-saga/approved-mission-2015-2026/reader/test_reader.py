"""Technical checks only: these do not certify prose, canon or publication."""
import hashlib
import json
from html.parser import HTMLParser
import unittest
from pathlib import Path

import build_reader as reader


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.scripts = [], [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a":
            self.links.append(attrs.get("href", ""))
        if tag == "script" or any(k.startswith("on") for k in attrs):
            self.scripts.append(tag)


class ReaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = reader.build()
        cls.page = Page()
        cls.page.feed((reader.HERE / "index.html").read_text())

    def test_every_original_source_matches_frozen_git_blob(self):
        inventory = json.loads((reader.INVENTORY / "MANUSCRIPT_INVENTORY.json").read_text())
        self.assertGreater(len(inventory["sources"]), 40)
        for row in inventory["sources"]:
            data = (reader.ROOT / row["path"]).read_bytes()
            git_blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
            self.assertEqual(git_blob, row["baseline_git_blob"], row["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"])

    def test_legacy_pov_sources_not_active_reader(self):
        paths = {row["path"] for row in self.manifest["manuscripts"]}
        for filename in reader.LEGACY_READER_EXCLUDED:
            self.assertNotIn("living-novel/manuscript/" + filename, paths)
        self.assertTrue(all("approved-mission-2015-2026/manuscript/" in p for p in paths))

    def test_actual_prose_included_and_matches_manifest(self):
        page = (reader.HERE / "index.html").read_text()
        self.assertEqual(len(reader.mission_manuscripts()), len(self.manifest["manuscripts"]))
        for row in self.manifest["manuscripts"]:
            path = reader.ROOT / row["path"]
            self.assertEqual(reader.digest(path), row["sha256"])
            self.assertIn(reader.render_markdown(path.read_text()), page)
            self.assertEqual(row["status"], "DRAFT_NONCANON_NO_RELEASE_APPROVAL")

    def test_final_reader_contains_actual_manuscript(self):
        self.assertGreater(len(self.manifest["manuscripts"]), 0,
                           "Reader assembly remains pending until actual mission prose exists.")

    def test_explicit_non_the_title_is_included(self):
        expected = reader.MISSION / "manuscript/2026-week5/A_DOOR_WIDE_ENOUGH_NONCANON.md"
        self.assertIn(expected, reader.mission_manuscripts())
        self.assertIn(reader.relative(expected), {entry["path"] for entry in self.manifest["manuscripts"]})

    def test_explicit_story_order_and_unknown_lane_rejection(self):
        paths = [Path(folder) / "THE_TEST.md" for folder in
                 ("2026-week6-wetland", "2024-title", "2026-week6", "2026-week4", "2025-reckoning", "2026", "2026-week5", "2015-jake-week1", "2015-jake-arc", "2016-jake-arc")]
        self.assertEqual([p.parent.name for p in sorted(paths, key=reader.manuscript_order)],
                         ["2015-jake-week1", "2015-jake-arc", "2016-jake-arc", "2024-title", "2025-reckoning", "2026", "2026-week4", "2026-week5", "2026-week6", "2026-week6-wetland"])
        with self.assertRaisesRegex(ValueError, "resolve its cutoff"):
            reader.manuscript_order(Path("2015") / "THE_UNBOUND_PAST.md")
        with self.assertRaisesRegex(ValueError, "resolve its cutoff"):
            reader.manuscript_order(Path("2022-semifinal") / "THE_DISPUTED_ASSOCIATION.md")
        self.assertEqual(reader.SCENE_LANES["2026"][1], "After Chapter III; before Week 4 results")
        self.assertIn("no Week 7 result", reader.SCENE_LANES["2026-week6"][1])
        self.assertIn("display order only", reader.SCENE_LANES["2026-week6-wetland"][1])
        actual = [entry["scene_lane_order"] for entry in self.manifest["manuscripts"]]
        self.assertEqual(actual, sorted(actual))

    def test_historical_disclosure_counts_only_included_text(self):
        current = [Path("2026") / "THE_PRESENT.md"]
        no_history = reader.scope_disclosure(current)
        self.assertIn("No new historical manuscript is included yet", no_history)
        self.assertNotIn("1 proposed historical sequence", no_history)
        with_history = reader.scope_disclosure(current + [Path("2024-title") / "THE_TITLE.md"])
        self.assertIn("1 proposed historical sequence(s) and 1 current-2026 sequence(s)", with_history)
        self.assertIn("No historical season is complete", with_history)
        self.assertIn("Raw human-owner identity remains UNKNOWN", with_history)
        for entry in self.manifest["manuscripts"]:
            if entry["scope"] == "EVENT_SCOPED_HISTORICAL_FICTION":
                self.assertEqual(entry["raw_human_owner_status"], "UNKNOWN")
                if "fictional_binding_audit_sha256" in entry:
                    self.assertEqual(entry["fictional_binding_audit_sha256"], reader.digest(reader.HISTORICAL_BINDING_AUDIT))
                else:
                    self.assertEqual(entry["identity_basis"], "USER_ATTESTED_IDENTITY_PLUS_PROVIDER_CONNECTED_ACCOUNT_CONTINUITY")
                    self.assertEqual(entry["connected_account_audit_sha256"], reader.digest(reader.CONNECTED_ACCOUNT_AUDIT))

    def test_local_links_and_coverage_source_resolve(self):
        for target in self.page.links:
            if target and not target.startswith(("#", "https://", "http://")):
                self.assertTrue((reader.HERE / target).exists(), target)
        coverage = self.manifest["coverage_source"]
        self.assertIsNotNone(coverage, "Coverage register required for final reader assembly")
        self.assertEqual(reader.digest(reader.ROOT / coverage["path"]), coverage["sha256"])

    def test_unique_anchors_and_resolvable_internal_links(self):
        self.assertEqual(len(self.page.ids), len(set(self.page.ids)))
        for target in self.page.links:
            if target.startswith("#"):
                self.assertIn(target[1:], self.page.ids)

    def test_source_html_cannot_execute(self):
        attack = '# <script>alert("x")</script>\n\n<img src=x onerror=alert(1)>\n\n[bad](javascript:alert(1))'
        rendered = reader.render_markdown(attack)
        parser = Page()
        parser.feed(rendered)
        self.assertEqual(parser.scripts, [])
        self.assertEqual(parser.links, [])
        self.assertIn("&lt;script&gt;", rendered)
        self.assertEqual(self.page.scripts, [])

    def test_explicit_partial_status_and_no_acceptance_claim(self):
        self.assertEqual(self.manifest["status"], "PARTIAL_DRAFT_PREVIEW_NOT_PUBLICATION")
        page = (reader.HERE / "index.html").read_text()
        self.assertIn("not a finished saga or canonical release", page)
        self.assertIn(reader.scope_disclosure(reader.mission_manuscripts()), page)
        self.assertIn("Broader 2015–2025 coverage remains incomplete", page)
        self.assertIn("../evidence/HISTORICAL_BINDING_AUDIT_2022_2025.md", self.page.links)
        self.assertIn("../CANDIDATE_EVENT_LINKS.json", self.page.links)
        self.assertIn("../ALL_SEASON_PROGRESS.json", self.page.links)
        self.assertIn("../evidence/HISTORICAL_UNBLOCK_CHECK_2026_10_24.md", self.page.links)
        self.assertIn("../evidence/provider-readback/READBACK_INDEX.json", self.page.links)
        self.assertIn('lang="en"', page)
        self.assertIn('name="viewport"', page)


if __name__ == "__main__":
    unittest.main()
