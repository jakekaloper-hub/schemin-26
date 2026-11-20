#!/usr/bin/env python3
"""Adversarial tests for Week 11 value-integrity validation. Stdlib only.

Run from repository root:
  python3 -m unittest discover -s memo-os/week-11 -p 'test_validate_creative_intake.py' -v
"""
import contextlib
import io
import pathlib
import shutil
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from validate_creative_intake import validate, W11, FOUND, MATRIX, SRC, REF, SYN, INDEX, RECOVERY

SOURCE = pathlib.Path("memo-os/week-9/WEEK_9_WEEK_10_PROVIDER_EVIDENCE_2026-11-20.json")
FILES = [FOUND, MATRIX, SRC, REF, SYN, INDEX, SOURCE, RECOVERY]

class Week11IntakeAdversarialTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="w11-negative-")
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        baseline = HERE.parents[1]
        for relative in FILES:
            origin = baseline / relative
            dest = self.root / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(origin, dest)

    def gate(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return validate(self.root, quiet=True)

    def edit(self, path, before, after):
        p = self.root / path
        body = p.read_text(encoding="utf-8")
        self.assertIn(before, body, "fixture precondition")
        p.write_text(body.replace(before, after, 1), encoding="utf-8")

    def test_clean_source_passes(self):
        self.assertEqual(self.gate(), 0)

    def test_rejects_changed_founder_choice_g01(self):
        self.edit(FOUND, "- **G01** — Strategic control over the Commonwealth",
                  "- **G01** — Silly underwater dance contest")
        self.assertEqual(self.gate(), 1)

    def test_rejects_changed_founder_free_text(self):
        self.edit(FOUND, "Not a golf course.",
                  "A brand-new championship golf course.")
        self.assertEqual(self.gate(), 1)

    def test_rejects_false_CJ_stroud_score(self):
        self.edit(MATRIX, "C.J. Stroud contributed **29.06 started Thursday points**",
                  "C.J. Stroud contributed **999.06 started Thursday points**")
        self.assertEqual(self.gate(), 1)

    def test_rejects_invented_week11_winner_in_raw_snapshot(self):
        self.edit(SOURCE, '"winner": "UNDECIDED"', '"winner": "HOME"')
        self.assertEqual(self.gate(), 1)

    def test_rejects_mutated_reference_fixture(self):
        self.edit(REF, '"Strategic control over the Commonwealth"',
                  '"A new, invented concept"')
        self.assertEqual(self.gate(), 1)

    def test_rejects_mislabeled_house_sixth_status(self):
        self.edit(MATRIX, "HOUSE_BOARD_STATUS_UNSPECIFIED", "OFF_BOARD")
        self.assertEqual(self.gate(), 1)

    def test_rejects_changed_espn_points_in_source_receipt(self):
        self.edit(SRC, '"points": 29.06', '"points": 99.06')
        self.assertEqual(self.gate(), 1)

    def test_rejects_misquoted_november18_ffhub_odds(self):
        self.edit(RECOVERY, "| ObiWan Jacoby | 32.45 | 52.89 | 12.77 |",
                  "| ObiWan Jacoby | 32.45 | 99.99 | 12.77 |")
        self.assertEqual(self.gate(), 1)

if __name__ == "__main__":
    unittest.main()
