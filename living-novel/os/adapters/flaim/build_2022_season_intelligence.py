"""Source-only 2022 season intelligence. No projected grades or inferred transactions."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/"living-novel/production/full-rewrite-2026/evidence"
def build():
    draft=json.loads((BASE/"G01_2015_2026_DRAFT_HISTORY_PROVIDER_PICKS.json").read_text())
    season=next(s for s in draft["seasons"] if s["season"]==2022)
    schedule=json.loads((BASE/"G01_2022_FLAIM_WEEK_BY_WEEK_MATCHUP_EXTRACT.json").read_text())["rows"]
    snapshots=json.loads((BASE/"G01_2022_RED_WEEKLY_ROSTER_SNAPSHOTS.json").read_text())["snapshots"]
    names={}
    for r in schedule:
        for side in ("home","away"):
            if r.get(f"{side}_team_id") is not None:
                names[r[f"{side}_team_id"]]=r.get(f"{side}_name")
    teams=[]
    for team_id in range(1,13):
        picks=sorted((p for p in season["picks"] if p["team"]==team_id),key=lambda p:p["overall"])
        arc=[]
        w=l=0
        for wk in range(1,18):
            matches=[m for m in schedule if m["week"]==wk and team_id in (m.get("home_team_id"),m.get("away_team_id"))]
            for m in matches:
                if m["winner"] in ("HOME","AWAY") and m.get("away_team_id") is not None:
                    winner=m["home_team_id"] if m["winner"]=="HOME" else m["away_team_id"]
                    if wk<=14:
                        w+=winner==team_id
                        l+=winner!=team_id
            arc.append({"week":wk,"records":len(matches),"regular_record_after_week":f"{w}-{l}" if wk<=14 else None,
                        "opponents":[m["away_team_id"] if m.get("home_team_id")==team_id else m["home_team_id"] for m in matches if m.get("away_team_id") is not None],
                        "matchup_tiers":[m["tier"] for m in matches]})
        teams.append({"historical_team_id":team_id,"historical_name":names.get(team_id),"owner_identity":"UNKNOWN",
                      "draft_profile":{"pick_count":len(picks),"keeper_flag_count":sum(bool(p["keeper"]) for p in picks),
                                       "first_three_overall_picks":[p["overall"] for p in picks[:3]],
                                       "preseason_grade":"UNAVAILABLE_NO_VINTAGE_PROJECTIONS"},
                      "regular_season_record":f"{w}-{l}","weekly_sequence":arc})
    diffs=[]
    for a,b in zip(snapshots,snapshots[1:]):
        old={str(p["id"]):p["name"] for p in a["players"]}
        new={str(p["id"]):p["name"] for p in b["players"]}
        diffs.append({"from_week":a["week"],"to_week":b["week"],
                     "appeared":[{"id":p,"name":new[p]} for p in sorted(new.keys()-old.keys())],
                     "departed":[{"id":p,"name":old[p]} for p in sorted(old.keys()-new.keys())],
                     "cause":"UNKNOWN_NOT_A_CONFIRMED_TRADE_OR_WAIVER"})
    return {"season":2022,"source_scope":"Flaim league 1417621 verified drafts, scores, selected Red roster snapshots",
            "fiction_status":"NOT_A_MANUSCRIPT","as_of": "POST_2022_RETROSPECTIVE",
            "owner_identity_policy":"NO_HISTORICAL_PERSON_ATTRIBUTION_WITHOUT_INDEPENDENT_EVIDENCE",
            "teams":teams,"red_roster_deltas":diffs,
            "missing":["Historical acquisition transactions","Vintage preseason ADP/projections","Reliable prior owner identities",
                       "Roster snapshots for other teams and intermediate weeks","Raw upstream ESPN checksum"]}
if __name__=="__main__":
    print(json.dumps(build(),ensure_ascii=False,indent=2))
