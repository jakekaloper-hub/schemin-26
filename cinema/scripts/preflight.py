#!/usr/bin/env python3
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
required=[
"cinema/vendor/filmclusive/wan22-image-ref-video-ref.json",
"cinema/production/week-2-special-delivery.json",
"archive/2026/week-2/story-package.json"
]
bad=False
for rel in required:
 p=ROOT/rel
 ok=p.exists() and p.stat().st_size>0
 print(("OK  " if ok else "MISS")+" "+rel)
 bad|=not ok
if not bad:
 w=json.loads((ROOT/required[0]).read_text())
 node_types={n.get("type") for n in w.get("nodes",[])}
 for expected in ["WanVideoDecode","WanVideoSetLoRAs","GetImageSizeAndCount","PixelPerfectResolution"]:
  print(("OK  " if expected in node_types else "MISS")+" node "+expected)
  bad|=expected not in node_types
sys.exit(1 if bad else 0)
