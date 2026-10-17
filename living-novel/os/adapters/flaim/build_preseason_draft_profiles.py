"""Derive preseason *draft construction* profiles, never ex-post fake forecasts.

Inputs are season's own ESPN/Flaim completed draft picks. Outputs are descriptive
and time-bounded, suitable for story-room research, NOT provider-issued draft grades.
"""
from __future__ import annotations
import json
from collections import Counter, defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
EVIDENCE=ROOT/"living-novel/production/full-rewrite-2026/evidence"

def build_profiles(boards):
    result=[]
    for board in boards:
        year=board["year"]
        if not board.get("success") or board.get("draft",{}).get("status")!="complete":
            raise ValueError(f"{year}: draft not confirmed")
        selections=board["picks"]
        by_team=defaultdict(list)
        for pick in selections:
            if pick.get("placement",{}).get("status")!="confirmed":
                raise ValueError(f"{year}: unconfirmed draft placement")
            team=pick.get("selectionTeamId")
            if team is None:raise ValueError(f"{year}: missing selection team")
            by_team[str(team)].append(pick)
        if len(by_team)!=12:raise ValueError(f"{year}: expected 12 drafting teams; found {len(by_team)}")
        teams=[]
        for team_id,picks in sorted(by_team.items(),key=lambda x:int(x[0])):
            ordered=sorted(picks,key=lambda p:(p.get("overallPick",999),p["round"]))
            top=[{"round":p["round"],"overall_pick":p.get("overallPick"),
                  "player_id":p.get("playerId"),"player_name":p.get("playerName"),
                  "position":p.get("playerPosition"),"is_keeper":p.get("isKeeper")}
                 for p in ordered if p["round"]<=3]
            team_name=(board.get("teams") or {}).get(team_id)
            teams.append({"historical_team_slot":int(team_id),"historical_team_name":team_name,
                          "current_owner_identity":"UNKNOWN_UNLESS_INDEPENDENTLY_VERIFIED",
                          "picks_recorded":len(picks),"keeper_flagged_picks":sum(p.get("isKeeper") is True for p in picks),
                          "first_three_rounds":top,"rounds":sorted({p["round"] for p in picks}),
                          "draft_construction_observations":{"top_three_picks":len(top),
                             "draft_pick_positions":[p.get("overallPick") for p in top]},
                          "actual_preseason_prediction":"NOT_AVAILABLE_FROM_DRAFT_BOARD",
                          "talent_adjusted_draft_grade":"UNSCORED_NEEDS_HISTORICALLY_DATED_ADP_OR_PROJECTIONS",
                          "season_end_outcome":"SEPARATE_EVIDENCE_DO_NOT_BACKFILL_INTO_PRESEASON"})
        result.append({"season":year,"draft_status":"confirmed","total_picks":len(selections),
                       "keeper_flags_meaning":"provider-flagged only; zero flags do not prove there were no keepers",
                       "teams":teams})
    return result

def run():
    boards=[]
    for name in ["G01_DRAFT_BOARDS_2015_2020.json","G01_DRAFT_BOARDS_2021_2026.json"]:
        boards+=json.loads((EVIDENCE/name).read_text(encoding="utf-8"))["drafts"]
    return {"scope":"PRESEASON_DRAFT_CONSTRUCTION_ONLY","league_id":"1417621",
            "source":"Flaim completed ESPN draft boards 2015-2026",
            "method":"Confirmed picks grouped by historical selecting team, not projected owner; top 3 rounds, pick count and provider keeper flags",
            "guardrails":["No future-season results included","No independent owner attribution",
                          "No subjective or numerical grade without dated ADP/projection source",
                          "No claim ESPN supplied preseason predictions"],"seasons":build_profiles(boards)}

if __name__=="__main__":
    print(json.dumps(run(),indent=2,ensure_ascii=False))
