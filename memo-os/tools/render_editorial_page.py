#!/usr/bin/env python3
"""Deterministic Memo OS editorial PNG compositor. No independent visual certification."""
import argparse,hashlib,json
from io import BytesIO
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,features,__version__ as pillow_version
W,H=1024,1536
FONTS={"serif":"/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf","bold":"/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"}
def digest(data): return hashlib.sha256(data).hexdigest()
def render(spec_path,output_path):
    spec_path=Path(spec_path);raw=spec_path.read_bytes();s=json.loads(raw)
    if s.get("format")!="schemin-memo-editorial-v1":raise ValueError("invalid spec format")
    root=spec_path.parent.resolve();bg=(root/s["background"]).resolve()
    if not bg.is_relative_to(root):raise ValueError("unsafe background path")
    background_bytes=bg.read_bytes()
    with Image.open(BytesIO(background_bytes)) as source:
        if source.size!=(W,H):raise ValueError("invalid background dimensions")
        image=source.convert("RGB")
    draw=ImageDraw.Draw(image);used=[];receipts=[];font_receipts={};font_data={}
    if not s.get("regions"):raise ValueError("regions required")
    for r in s["regions"]:
        text=r.get("text")
        if not isinstance(text,str) or not text.strip():raise ValueError("missing editorial copy")
        x,y,w,h=[int(r[k]) for k in ("x","y","width","height")]
        if x<0 or y<0 or w<1 or h<1 or x+w>W or y+h>H:raise ValueError("region out of bounds")
        if any(x<a+c and x+w>a and y<b+d and y+h>b for a,b,c,d in used):raise ValueError("overlapping regions")
        used.append((x,y,w,h))
        face=r.get("font","serif");size=int(r.get("font_size",22))
        if face not in FONTS or size<16 or size>100:raise ValueError("font rejected")
        if face not in font_data:
            font_data[face]=Path(FONTS[face]).read_bytes()
            font_receipts[face]={"path":FONTS[face],"sha256":digest(font_data[face])}
        font=ImageFont.truetype(BytesIO(font_data[face]),size)
        leading=max(size+4,int(size*1.35));lines=[]
        for paragraph in text.split("\n"):
            if not paragraph:lines.append("");continue
            line=""
            for word in paragraph.split(" "):
                candidate=(line+" "+word).strip()
                if draw.textlength(candidate,font=font)>w:
                    if not line or draw.textlength(word,font=font)>w:raise ValueError("word exceeds box")
                    lines.append(line);line=word
                else:line=candidate
            lines.append(line)
        if len(lines)*leading>h:raise ValueError("editorial copy overflows")
        if r.get("backing",True):draw.rectangle((x,y,x+w,y+h),fill="#101820")
        for i,line in enumerate(lines):draw.text((x,y+i*leading),line,font=font,fill=r.get("color","#F7F0DE"))
        receipts.append({"role":r.get("role","body"),"text":text,"sha256":digest(text.encode()),"box":[x,y,w,h],"lines":len(lines),"font":face,"font_size":size,"line_spacing":leading,"rendered_lines":lines})
    target=Path(output_path);target.parent.mkdir(parents=True,exist_ok=True);image.save(target,"PNG")
    receipt={"status":"CANDIDATE_NOT_APPROVED","spec_sha256":digest(raw),"background_sha256":digest(background_bytes),"output_sha256":digest(target.read_bytes()),"dimensions":[W,H],"source_text_regions":receipts,"typography_environment":{"fonts":font_receipts,"pillow_version":pillow_version,"freetype_version":features.version_module("freetype2")},"visual_text_independently_verified":False,"mobile_readability_verified":False}
    target.with_suffix(".receipt.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2))
    return receipt
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("spec");p.add_argument("output");a=p.parse_args()
    print(json.dumps(render(a.spec,a.output),indent=2))
