#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
manifest=json.loads((ROOT/"cinema/production/week-2-special-delivery.shots.json").read_text())
out=ROOT/"cinema/runtime/jobs"; out.mkdir(parents=True,exist_ok=True)
for scene in manifest["scenes"]:
 for s in scene["shots"]:
  job={"id":s["id"],"source_image":scene["source_image"],"prompt":s["prompt"],"seed":s["seed"],"seconds":s["seconds"],"fps":manifest["defaults"]["fps"],"width":manifest["defaults"]["resolution"]["width"],"height":manifest["defaults"]["resolution"]["height"],"workflow":"cinema/runtime/api/wan22-animate.json"}
  (out/f'{s["id"]}.json').write_text(json.dumps(job,indent=2))
print("built",sum(len(x["shots"]) for x in manifest["scenes"]),"jobs")
