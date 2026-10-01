import json
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
PLAN=ROOT/"planning"/"character-native-render"
REG=json.loads((ROOT/"canon"/"characters"/"reference_sources_v1.json").read_text())
MATRIX=json.loads((PLAN/"PHASE_1_SOURCE_BYTE_PORTABILITY_MATRIX_2026-10-01.json").read_text())
GAPS=json.loads((PLAN/"PROGRAM_GAP_REGISTER_V1.json").read_text())

class Phase1SourceByteHoldTests(unittest.TestCase):
    def test_matrix_covers_exactly_12_registered_characters(self):
        self.assertEqual(len(REG["entries"]),12)
        self.assertEqual(len(MATRIX["entries"]),12)
        self.assertEqual(
            {x["character_id"] for x in REG["entries"]},
            {x["character_id"] for x in MATRIX["entries"]},
        )

    def test_library_metadata_matches_registered_sizes(self):
        expected={x["character_id"]:x["observed_library_size_bytes"] for x in REG["entries"]}
        for row in MATRIX["entries"]:
            self.assertEqual(row["observed_library_size_bytes"],expected[row["character_id"]])
            self.assertEqual(row["library_record"],"FOUND")
            self.assertEqual(row["library_size_match"],"PASS")

    def test_no_fresh_hash_is_claimed_without_bytes(self):
        for row in MATRIX["entries"]:
            self.assertEqual(row["fresh_sha256"],"NOT_RUN_BYTES_UNAVAILABLE")
            self.assertEqual(row["clean_context_binary_retrieval"],"NOT_PROVEN")
            self.assertEqual(row["target_repository_asset"],"ABSENT")

    def test_gap_is_fail_closed_on_exact_transport_blocker(self):
        gap=next(x for x in GAPS["gaps"] if x["id"]=="CNR-GAP-001")
        self.assertEqual(gap["status"],"HOLD_AUTHORIZED_RAW_BYTE_EXPORT_UNAVAILABLE")
        self.assertEqual(gap["blocker_type"],"provider_capability")

    def test_phase1_probe_would_not_pass_without_all_repo_assets(self):
        missing=[ROOT/x["repository_path"] for x in REG["entries"] if not (ROOT/x["repository_path"]).exists()]
        self.assertEqual(len(missing),12)

if __name__=="__main__":
    unittest.main(verbosity=2)
