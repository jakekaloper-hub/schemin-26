#!/usr/bin/env python3
import os,sys,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
checks={
"vendored workflow":ROOT/"cinema/vendor/filmclusive/wan22-image-ref-video-ref.json",
"shot manifest":ROOT/"cinema/production/week-2-special-delivery.shots.json",
"api workflow":ROOT/"cinema/runtime/api/wan22-animate.json",
}
failed=False
for name,p in checks.items():
 ok=p.exists() and p.stat().st_size>2
 print(("PASS" if ok else "WAIT"),name,":",p)
 if name!="api workflow": failed|=not ok
endpoint=os.getenv("COMFYUI_ENDPOINT","http://127.0.0.1:8188")
try:
 urllib.request.urlopen(endpoint+"/system_stats",timeout=2)
 print("PASS ComfyUI endpoint",endpoint)
except Exception:
 print("WAIT ComfyUI endpoint",endpoint)
print("READY_FOR_LOCAL_EXPORT" if not failed else "REPO_PREFLIGHT_FAILED")
sys.exit(1 if failed else 0)
