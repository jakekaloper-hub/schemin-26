#!/usr/bin/env python3
import json, os, pathlib, time, urllib.request
from datetime import datetime, timezone
LEAGUE_ID=os.getenv("LEAGUE_ID","1417621")
SEASON=os.getenv("SEASON","2026")
OUT=pathlib.Path("data/snapshots")/LEAGUE_ID
OUT.mkdir(parents=True,exist_ok=True)
BASE=f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{SEASON}/segments/0/leagues/{LEAGUE_ID}"
url=BASE+"?view=mTeam&view=mRoster&view=mMatchup&view=mSettings&view=mStatus"
def validate(d):
    if str(d.get("id")) != LEAGUE_ID: raise ValueError("wrong league id")
    if len(d.get("teams",[])) != 12: raise ValueError("expected 12 teams")
    for k in ("schedule","settings","status"):
        if k not in d: raise ValueError(k+" missing")
last=None
for attempt in range(4):
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"Schemin26DataGateway/1.0","Accept":"application/json"})
        with urllib.request.urlopen(req,timeout=20) as r: data=json.load(r)
        validate(data)
        now=datetime.now(timezone.utc).isoformat()
        env={"meta":{"league_id":int(LEAGUE_ID),"season":int(SEASON),"source":"espn-lm-api-reads","fetched_at":now,"stale":False,"failure_reason":None},"data":data}
        tmp=OUT/"latest.json.tmp"; tmp.write_text(json.dumps(env,separators=(",",":"))); tmp.replace(OUT/"latest.json")
        (OUT/"manifest.json").write_text(json.dumps(env["meta"],indent=2))
        print("Validated ESPN snapshot",now); raise SystemExit(0)
    except Exception as e:
        last=str(e); print("attempt failed:",last)
        if attempt<3: time.sleep(2**attempt)
raise SystemExit("ESPN refresh failed: "+str(last))
