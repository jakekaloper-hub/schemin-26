#!/usr/bin/env python3
"""Export native-type source receipts for film editorial, without generating text in images."""
from __future__ import annotations
import hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent
source=Path(os.environ.get("FILM_BOARD_JSON",str(HERE/"film_storyboard_v1.json")))
board=json.loads(source.read_text(encoding="utf-8"))
script=json.loads((HERE/"SCREENPLAY_CANDIDATE_V1.json").read_text(encoding="utf-8"))
scenes={s["source_folio"]:s for s in script["scene_scripts"]}
ids={"W10-P01","W10-P04","W10-P18","W10-P34","W10-P20","W10-P24",
"W10-P25","W10-P26","W10-P27","W10-P28","W10-P29","W10-P30","W10-P31","W10-P35","W10-P33"}
cues=[]
for sc in board["scenes"]:
    page=sc["folio"]
    if page not in ids:continue
    shot=scenes[page]
    assert shot["source_publication_copy"]==sc["publication_copy"]
    cues.append({"page_id":page,"scene_id":sc["id"],"in":sc["start"],"out":sc["end"],
    "source_request":sc["source_request"],"source_sha256":sc["source_sha256"],
    "locked_publication_copy":sc["publication_copy"],"render_method":"native vector/editorial typography only",
    "render_status":"NOT_RENDERED","rights_and_data_gate":"Exact numbers, qualifiers and rows require editorial signoff"})
assert len(cues)==15
payload={"schema":"schemin.week10.film_graphics_source.v1","state":"SOURCE_LOCKED_NOT_RENDERED",
"source_storyboard":"film_storyboard_v1.json","source_storyboard_sha256":hashlib.sha256(source.read_bytes()).hexdigest(),
"native_typography_only":True,"cues":cues}
(HERE/"FILM_GRAPHICS_SOURCE_V1.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"source_graphics_pages":len(cues),"includes_all_source_copy":True},indent=2))
