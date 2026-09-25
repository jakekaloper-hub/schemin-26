#!/usr/bin/env python3
"""Submit a pinned ComfyUI API workflow to a local/remote ComfyUI server."""
import json, os, sys, urllib.request
server=os.environ.get("COMFYUI_URL","http://127.0.0.1:8188")
workflow_path=sys.argv[1]
with open(workflow_path,"r",encoding="utf-8") as f: prompt=json.load(f)
req=urllib.request.Request(server+"/prompt",data=json.dumps({"prompt":prompt}).encode(),headers={"Content-Type":"application/json"})
with urllib.request.urlopen(req) as r: print(r.read().decode())
