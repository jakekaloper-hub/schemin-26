#!/usr/bin/env python3
"""Schemin Cinema local render adapter.
Posts a versioned ComfyUI workflow to a local ComfyUI server.
No paid API is required.
"""
import argparse,json,urllib.request
from pathlib import Path

def post(url,payload):
    req=urllib.request.Request(url,data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req) as r:return json.load(r)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--workflow",required=True)
    p.add_argument("--server",default="http://127.0.0.1:8188")
    args=p.parse_args()
    workflow=json.loads(Path(args.workflow).read_text())
    result=post(args.server.rstrip("/")+"/prompt",{"prompt":workflow})
    print(json.dumps(result,indent=2))

if __name__=="__main__":main()
