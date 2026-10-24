"""Regression: all eleven recoverable league seasons are present and final rounds agree."""
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/"living-novel/production/full-rewrite-2026/evidence"
class ChronologyCoverage(unittest.TestCase):
    def read(self,y):
        f=BASE/(f"G01_{y}_FULL_WEEKLY_MATCHUPS.json" if y!=2022 else "G01_2022_FLAIM_WEEK_BY_WEEK_MATCHUP_EXTRACT.json")
        return json.loads(f.read_text())
    def test_all_historical_years_retrieved(self):
        for y in range(2015,2026):
            with self.subTest(season=y):
                d=self.read(y)
                weeks=d.get("weeks",d.get("weeks_queried"))
                self.assertEqual(len(weeks),17)
                self.assertEqual([w["week"] for w in weeks],list(range(1,18)))
    def test_actual_year_specific_coverage(self):
        for y in range(2015,2026):
            with self.subTest(season=y):
                d=self.read(y)
                if y==2022:
                    n=len(d["rows"])
                    filled=17
                else:
                    n=sum(len(w["matchups"]) for w in d["weeks"])
                    filled=sum(bool(w["matchups"]) for w in d["weeks"])
                self.assertEqual(filled,16 if 2017<=y<=2020 else 17)
                self.assertEqual(n,97 if 2017<=y<=2020 else (102 if y in (2015,2016) else 105))
    def test_final_round_consistent_with_ledger(self):
        finals=json.loads((BASE/"G01_2015_2025_FLAIM_VERIFIED_CHAMPIONSHIP_ROUNDS.json").read_text())["finals"]
        for e in finals:
            y=e["season"]
            d=self.read(y)
            w=e["final_scoring_week"]
            games=[x for x in (d["rows"] if y==2022 else d["weeks"][w-1]["matchups"]) if x["week"]==w] if y==2022 else d["weeks"][w-1]["matchups"]
            def home(x):return x.get("home_team_id",x.get("home_id"))
            def away(x):return x.get("away_team_id",x.get("away_id"))
            t=[x for x in games if x.get("tier")=="WINNERS_BRACKET" and home(x) is not None and away(x) is not None]
            with self.subTest(year=y):
                self.assertEqual(len(t),1)
                x=t[0]
                self.assertEqual({home(x),away(x)},{e["winner_team_id"],e["runnerup_team_id"]})
                self.assertEqual(sorted([x.get("home_points",x.get("hp")),x.get("away_points",x.get("ap"))]),sorted([e["winner_points"],e["runnerup_points"]]))
    def test_missing_17th_is_not_fabricated(self):
        for y in range(2017,2021):
            self.assertEqual(self.read(y)["weeks"][16]["matchups"],[])
if __name__=="__main__":unittest.main()
