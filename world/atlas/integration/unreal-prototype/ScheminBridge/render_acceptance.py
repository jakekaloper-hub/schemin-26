"""Fail-closed rendered-preview audit. A successful commandlet is not image proof."""
import json,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parent
IMAGE=ROOT/"generated/rendered_showcase_preview.png"
OUT=ROOT/"generated/render_acceptance.json"
result={"preview":str(IMAGE),"render_verified":False,"status":"BLOCKED","reason":"NO_RENDER_OUTPUT"}
if IMAGE.exists():
 data=IMAGE.read_bytes()
 if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data)>=24:
  w,h=struct.unpack(">II",data[16:24])
  result.update({"width":w,"height":h,"bytes":len(data)})
  if w>=640 and h>=360 and len(data)>10000:
   result.update({"render_verified":True,"status":"FILE_VALIDATED_IMAGE_NOT_VISUALLY_REVIEWED","reason":"Awaiting independent visual inspection"})
  else:result["reason"]="IMAGE_TOO_SMALL_OR_INVALID"
 else:result["reason"]="NOT_PNG"
OUT.write_text(json.dumps(result,indent=2)+"\n")
print("RENDER_AUDIT",result["status"],result["reason"])
