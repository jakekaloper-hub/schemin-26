"""Read-only, as-of-scene Author Memory hydration atop existing Novel/World sources."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
EVIDENCE=ROOT/"living-novel/production/full-rewrite-2026/evidence"
def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))
def _module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def hydrate(*, character_id:str, scene_year:int, scene_week:int, historical_identity_links=None):
    """Source facts visible by scene time; not a persisted memory store or approval."""
    if not isinstance(scene_year,int) or not 2015 <= scene_year <= 2026:
        raise ValueError("scene year outside recovered evidence horizon")
    if not isinstance(scene_week,int) or not 1 <= scene_week <= 19:
        raise ValueError("invalid scene week")
    owner_domains=_load(ROOT/"world/data/owner_domains.json")
    rows=[]
    for year in range(2015, min(scene_year, 2025)+1):
        if year == 2022:
            archive=_load(EVIDENCE/"G01_2022_FLAIM_WEEK_BY_WEEK_MATCHUP_EXTRACT.json")
            rows.extend(dict(r,season=year) for r in archive["rows"])
        else:
            archive=_load(EVIDENCE/f"G01_{year}_FULL_WEEKLY_MATCHUPS.json")
            for period in archive["weeks"]:
                for game in period["matchups"]:
                    rows.append({"season":year,"week":period["week"],
                        "home_team_id":game.get("home_id"),"away_team_id":game.get("away_id"),
                        "home_points":game.get("hp"),"away_points":game.get("ap"),
                        "winner":game.get("winner"),"source_period":game.get("period"),
                        "source_tier":game.get("tier")})
    reader=_module("author_reader",ROOT/"living-novel/os/adapters/author_context_reader.py")
    context=reader.author_context(character_id=character_id,scene_year=scene_year,scene_week=scene_week,
                                   owner_domains=owner_domains,historical_rows=rows,
                                   known_identity_links=historical_identity_links)
    memory=_load(ROOT/"world/data/world_memory.json")
    visible=[]
    withheld=0
    for e in memory.get("events",[]):
        era=e.get("era")
        try: year=int(era)
        except (ValueError,TypeError): withheld+=1; continue
        week=e.get("week")
        if not isinstance(week,int) or (year,week)>(scene_year,scene_week):
            withheld+=1; continue
        visible.append({"id":e["event_id"],"season":year,"week":week,"source":e.get("source",[]),
                        "location_id":e.get("location"),"memory_class":e.get("memory_class"),
                        "status":"WORLD_SOURCE_RECORD_NOT_CHARACTER_PERSONAL_KNOWLEDGE"})
    division=_module("division_reader",ROOT/"living-novel/os/adapters/season_division_reader.py")
    division_state=division.season_divisions(season=scene_year,
                          division_data=_load(ROOT/"world/data/divisions.json"))
    team_id=next(d["team_id"] for d in owner_domains["domains"] if d["character_id"]==character_id)
    context["world_memory_events_as_of_scene"]=visible
    context["world_memory_withheld_future_or_unresolved"]=withheld
    context["period_division_id"]=division_state["assignments"].get(team_id)
    context["period_division_status"]=division_state["status"]
    context["author_context_status"]="SOURCE_BOUNDED_READ_ONLY_PARTIAL"
    context["persistent_bullpen_memory_connected"]=False
    context["world_memory_source"]="world/data/world_memory.json"
    return context
if __name__=="__main__":
    print(json.dumps(hydrate(character_id="CHAR-JAKE-KALOPER",scene_year=2026,scene_week=3),indent=2))
