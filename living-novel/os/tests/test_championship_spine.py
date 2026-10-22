"""Validate derived championship index against its source ledger, without network access."""
import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
INDEX=ROOT/"living-novel/history/CHAMPIONSHIP_SUCCESSION_MACHINE_INDEX_2015_2026.json"
LEDGER=ROOT/"living-novel/history/CHAMPIONSHIP_SUCCESSION.md"

class ChampionshipSpineTests(unittest.TestCase):
    def test_years_slots_and_2026_boundary(self):
        data=json.loads(INDEX.read_text(encoding="utf-8"))
        self.assertEqual([s["season"] for s in data["seasons"]],list(range(2015,2026)))
        self.assertEqual(data["live_2026"]["status"],"IN_PROGRESS_NO_FINAL_CHAMPION")
        self.assertTrue(all(s["historical_owner_attribution"]=="UNVERIFIED" for s in data["seasons"]))

    def test_derived_records_match_existing_ledger(self):
        data=json.loads(INDEX.read_text(encoding="utf-8"))
        rows={}
        for line in LEDGER.read_text(encoding="utf-8").splitlines():
            match=re.match(r"\| (20\d\d) \| (.+?) \| (.+?) \| (.+?) \|",line)
            if match:
                rows[int(match[1])]=(match[2],match[3],match[4])
        self.assertEqual(len(rows),11)
        for s in data["seasons"]:
            champion,runner,third=rows[s["season"]]
            for actual,cell in [(s["champion"],champion),(s["runner_up"],runner),(s["third"],third)]:
                self.assertTrue(cell.startswith(actual["team_name"]+" ("),f"{s['season']} {cell}")
                self.assertTrue(cell.endswith(f"({actual['team_slot']})"),f"{s['season']} {cell}")

if __name__=="__main__":
    unittest.main()
