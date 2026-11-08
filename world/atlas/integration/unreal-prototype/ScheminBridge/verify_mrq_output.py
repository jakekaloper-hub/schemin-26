"""Verify native Unreal MRQ PNG outputs from bounded game-world rendering."""
import json,struct,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
out=ROOT/"generated/mrq_frames/Commonwealth_0000.png"
receipt=ROOT/"generated/mrq_render_acceptance.json"
result={"source":"UNREAL_MOVIE_RENDER_QUEUE_GAME_WORLD","png_path":str(out),
"image_file_verified":False,"visual_review_completed":False,
"canon_promotion":False,"status":"BLOCKED"}
if out.exists():
    data=out.read_bytes()
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data)>=24:
        width,height=struct.unpack(">II",data[16:24])
        result.update({"width":width,"height":height,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()})
        if width==640 and height==360 and len(data)>10000:
            result.update({"image_file_verified":True,"status":"RENDER_FILE_PASS_VISUAL_REVIEW_PENDING"})
receipt.write_text(json.dumps(result,indent=2)+"\n")
print("MRQ_RENDER_ACCEPTANCE",result["status"])
if not result["image_file_verified"]:raise SystemExit(2)
