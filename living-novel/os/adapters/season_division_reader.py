"""Temporal division binding for Novel OS: never inherit 2026 division membership backward."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

def season_divisions(*, season: int, division_data: dict, season_evidence: dict | None = None) -> dict:
    """Resolve actual team-to-division assignments only for an explicitly evidenced year."""
    if not isinstance(season,int) or not 2015 <= season <= 2026:
        raise ValueError("season outside supported League Chronicle range")
    data_year=division_data.get("season")
    if season_evidence is not None:
        if season_evidence.get("season") != season:
            raise ValueError("historical division evidence year mismatch")
        source=season_evidence.get("source")
        groups=season_evidence.get("divisions")
        if not source or not isinstance(groups,list):
            raise ValueError("historical division assignment requires explicit source")
        result={}
        for div in groups:
            for team in div.get("team_ids",[]):
                team=int(team)
                if team in result: raise ValueError(f"duplicate team division assignment {team}")
                result[team]=div["id"]
        return {"season":season,"assignments":result,"status":"SEASON_VERIFIED","source":source}
    if season != data_year:
        return {"season":season,"assignments":{},"status":"UNKNOWN_HISTORICAL_DIVISIONS",
                "source":None,"reason":"2026 assignments cannot be retroactively used for other seasons"}
    result={}
    for div in division_data["divisions"]:
        for team in div.get("member_team_ids_2026",[]):
            if team in result: raise ValueError("duplicated current team division membership")
            result[team]=div["id"]
    return {"season":season,"assignments":result,"status":"SOURCE_BOUND_2026",
            "source":"world/data/divisions.json"}

if __name__=="__main__":
    division_data=json.loads((ROOT/"world/data/divisions.json").read_text())
    for season in range(2015,2027):
        r=season_divisions(season=season,division_data=division_data)
        print(season,r["status"],len(r["assignments"]))
