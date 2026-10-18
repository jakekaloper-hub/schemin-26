"""Build noncanonical, evidence-bounded historical season briefs for Novel OS."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
EVIDENCE=ROOT/"living-novel/production/full-rewrite-2026/evidence"
def build(year:int)->dict:
    if year not in range(2015,2026): raise ValueError("season outside source archive")
    if year==2022:
        raw=json.loads((EVIDENCE/"G01_2022_FLAIM_WEEK_BY_WEEK_MATCHUP_EXTRACT.json").read_text())
        games=[{"week":r["week"],"home_id":r.get("home_team_id"),
                "away_id":r.get("away_team_id"),"home_points":r.get("home_points"),
                "away_points":r.get("away_points"),"winner":r.get("winner")} for r in raw["rows"]]
    else:
        raw=json.loads((EVIDENCE/f"G01_{year}_FULL_WEEKLY_MATCHUPS.json").read_text())
        games=[{"week":block["week"],"home_id":g.get("home_id"),"away_id":g.get("away_id"),
                "home_points":g.get("hp"),"away_points":g.get("ap"),"winner":g.get("winner"),
                "source_period":g.get("period"),"source_tier":g.get("tier")}
            for block in raw["weeks"] for g in block["matchups"]]
    final_doc=json.loads((EVIDENCE/"G01_2015_2025_FLAIM_VERIFIED_CHAMPIONSHIP_ROUNDS.json").read_text())
    finals=[f for f in final_doc["finals"] if f["season"]==year]
    if len(finals)!=1: raise ValueError("missing or ambiguous verified championship")
    teams=sorted({int(t) for g in games for t in (g["home_id"],g["away_id"]) if t is not None})
    week_numbers=sorted({g["week"] for g in games})
    coverage = "PARTIAL_TEAM_ID_SOURCE_GAP" if len(teams)!=12 else "TWELVE_SLOT_MATCHUP_IDS_RESOLVED"
    return {"season":year,"status":"SOURCE_BACKED_NONCANON_STORY_ROOM", "team_identity_coverage":coverage,
      "source_paths":[str((EVIDENCE/(f"G01_{year}_FULL_WEEKLY_MATCHUPS.json" if year!=2022 else "G01_2022_FLAIM_WEEK_BY_WEEK_MATCHUP_EXTRACT.json")).relative_to(ROOT)),
          "living-novel/production/full-rewrite-2026/evidence/G01_2015_2025_FLAIM_VERIFIED_CHAMPIONSHIP_ROUNDS.json"],
      "game_row_count":len(games),"historical_team_slots":teams,"scoring_weeks":week_numbers,
      "championship":finals[0],
      "story_question":f"What did the contest for the {year} title cost its contenders, and which consequences survived the result?",
      "scene_candidates":[{"kind":"opening","anchor":"earliest verified matchups","week":week_numbers[0]},
                          {"kind":"midseason","anchor":"midseason evidence anchor","week":week_numbers[len(week_numbers)//2]},
                          {"kind":"final","anchor":"verified winner-bracket championship","week":finals[0]["final_scoring_week"]}],
      "evidence_limits":(["Team identity incomplete in provider extract; do not join unnamed rows to owner slots"] if coverage!="TWELVE_SLOT_MATCHUP_IDS_RESOLVED" else []) + ["Historical team slot is not proof of current owner identity",
          "Division memberships unknown without annual source","No vintage preseason projection assumed",
          "No trade or waiver cause derived from roster differences",
          "2015–2017 identical roster snapshots unsuitable as season-change evidence" if year<=2017 else "Two-point roster comparison does not establish transaction timeline",
          "Scoring periods may duplicate cumulative playoff information"],
      "author_admission":"Historical facts are scene anchors, not license for owner backstory, motives, quotes or canonical outcomes beyond recorded games",
      "review_status":"NOT_INDEPENDENTLY_REVIEWED"}
def build_all():return [build(year) for year in range(2015,2026)]
if __name__=="__main__":
    print(json.dumps({"story_room":build_all()},indent=2))
