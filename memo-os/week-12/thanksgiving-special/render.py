"""Build candidate PNGs only from repository-pinned art and data. Python 3.11+, Pillow 11.3.0.
No placeholders, no system font fallback, no release authorization."""
from pathlib import Path
import hashlib, json, subprocess, re
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
W,H=2160,3840
GOLD=(235,191,118); WHITE=(249,241,221); MUTED=(218,208,186); DARK=(20,25,24)
def read(name): return json.loads((ROOT/name).read_text(encoding="utf-8"))
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def checked(rel, sha):
    p=(ROOT/rel).resolve()
    if not p.is_relative_to(ROOT) or not p.is_file() or not re.fullmatch(r"[0-9a-f]{64}",sha) or digest(p)!=sha:
        raise ValueError("Missing or mismatched repository asset: "+rel)
    subprocess.run(["git","ls-files","--error-unmatch",str(p.relative_to(REPO))],cwd=REPO,check=True,stdout=subprocess.DEVNULL)
    return p
def bind_receipt(rec, folio_id, ids):
    if rec.get("folio")!=folio_id or sorted(rec.get("team_ids",[]))!=sorted(ids) or not rec.get("location_id") or not rec.get("provider_job_id"):
        raise ValueError("Incomplete asset binding receipt")
    checked(rec["receipt_path"],rec["receipt_sha256"])
    if rec.get("approved_by_character_authority") is not True or rec.get("approved_by_atlas_authority") is not True:
        raise ValueError("Authority approval missing")
def main():
    subprocess.run(["node",str(ROOT/"validate.mjs")],check=True)
    edition=read("edition.json"); data=read("sports-lock.json")["data"]; assets=read("asset-lock.json")
    if assets.get("state")!="ASSETS_APPROVED": raise ValueError("Asset gate blocked")
    if len(edition["fols"])!=2 or edition["format"]["count"]!=2: raise ValueError("Exactly two folios required")
    for source in edition["sources"]:
        blob=subprocess.check_output(["git","hash-object",source["path"]],cwd=REPO,text=True).strip()
        if blob!=source["blob_sha"]: raise ValueError("Source changed: "+source["path"])
    for source in read("sports-lock.json")["sources"].values():
        p=ROOT/source["path"] if source["path"]=="provider-snapshot.json" else REPO/source["path"]
        if subprocess.check_output(["git","hash-object",str(p)],cwd=REPO,text=True).strip()!=source["blob_sha"]: raise ValueError("Sports source changed")
    fonts={k:checked(v["path"],v["sha256"]) for k,v in assets["fonts"].items()}
    if set(fonts)!={"heading","body"}: raise ValueError("Missing approved font")
    def font(k,size): return ImageFont.truetype(str(fonts[k]),size)
    def single(draw,text,x,y,width,size=68,minimum=48,kind="heading",color=WHITE):
        for n in range(size,minimum-1,-2):
            f=font(kind,n)
            if draw.textlength(text,font=f)<=width:
                draw.text((x,y),text,font=f,fill=color,anchor="lt"); return
        raise ValueError("Text cannot fit without violating minimum: "+text)
    def wrap(draw,text,x,y,width,lines=3,size=55,color=MUTED):
        f=font("body",size); out=[]; line=""
        for word in text.split():
            trial=(line+" "+word).strip()
            if draw.textlength(trial,font=f)<=width: line=trial
            else:
                if not line: raise ValueError("Word too wide: "+word)
                out.append(line);line=word
        if line:out.append(line)
        if len(out)>lines:raise ValueError("Copy overflow: "+text)
        for i,line in enumerate(out):draw.text((x,y+i*(size+8)),line,font=f,fill=color,anchor="lt")
    def artwork(key,folio_id,ids,w,h):
        r=assets["images"][key];bind_receipt(r,folio_id,ids)
        p=checked(key,r["sha256"])
        with Image.open(p) as im:
            if im.format!="PNG" or im.width<w or im.height<h: raise ValueError("Artwork too small / not PNG: "+key)
            return ImageOps.fit(im.convert("RGB"),(w,h),centering=(0.5,0.5))
    def header(folio):
        im=Image.new("RGB",(W,H),DARK); d=ImageDraw.Draw(im)
        d.rectangle((0,0,W,12),fill=GOLD)
        single(d,"SCHEMIN’ ’26  /  THANKSGIVING SPECIAL",70,65,2020,62,52,color=GOLD)
        single(d,folio["title"],70,160,2020,112,80)
        single(d,folio["subtitle"],70,300,2020,65,50,kind="body",color=MUTED)
        return im,d
    def footer(d,id,line):
        d.line((70,3675,2090,3675),fill=GOLD,width=3)
        single(d,line,70,3700,1900,50,42,kind="body",color=MUTED)
        single(d,id,2000,3700,100,54,48,color=GOLD)
    f1,f2=edition["fols"]; teams={t["id"]:t for t in data["teams"]}
    assert [t["team_id"] for t in f1["teams"]]==[t["id"] for t in data["teams"]]
    assert [(m["winner"],m["loser"]) for m in f2["matchups"]]==[(m["winner"],m["loser"]) for m in data["rematches"]]
    expected={x["asset"] for x in f1["teams"]+f2["matchups"]}
    if set(assets["images"])!=expected:raise ValueError("Asset set must equal 12 portraits + 6 matchups")
    im,d=header(f1)
    for g,division in enumerate(["Burgers","Wings","Pizza"]):
        base=425+g*1060
        single(d,division.upper()+" DIVISION",70,base,2020,65,54,color=GOLD)
        for k,e in enumerate(f1["teams"][4*g:4*g+4]):
            t=teams[e["team_id"]];x=70+(k%2)*1020;y=base+95+(k//2)*475
            d.rectangle((x,y,x+990,y+450),fill=(33,37,32),outline=GOLD,width=2)
            im.paste(artwork(e["asset"],"F01",[t["id"]],350,446),(x+2,y+2))
            tx=x+372
            wrap(d,t["name"],tx,y+28,595,2,59,WHITE)
            single(d,t["record"],tx,y+160,580,76,65,color=GOLD)
            for i,v in enumerate(t["ribbon"]):
                a=tx+i*53;d.rectangle((a,y+250,a+48,y+305),fill=(43,103,78) if v=="W" else (125,57,50))
                d.text((a+24,y+277),v,font=font("body",39),anchor="mm",fill=WHITE)
            wrap(d,e["caption"],tx,y+320,595,2,49)
    footer(d,"F01","Through Week 11 • W/L markers run from Week 1 to Week 11 • ESPN")
    output=[(f1,im)]
    im,d=header(f2)
    for i,(e,m) in enumerate(zip(f2["matchups"],data["rematches"])):
        y=435+i*520
        d.rectangle((70,y,2090,y+490),fill=(33,37,32),outline=GOLD,width=2)
        im.paste(artwork(e["asset"],"F02",[m["winner"],m["loser"]],850,486),(72,y+2))
        x=950
        wrap(d,m["winner_name"]+" × "+m["loser_name"],x,y+24,1110,2,68,WHITE)
        single(d,"W4 WINNER: "+m["winner_name"],x,y+180,1110,48,42,color=GOLD)
        single(d,m["week4_score"],x,y+245,1110,90,70)
        wrap(d,e["caption"],x,y+350,1110,2,55)
    footer(d,"F02","Week 4 final scores • Week 12 results undecided • ESPN")
    output.append((f2,im))
    out=ROOT/"candidate";out.mkdir(exist_ok=True)
    receipt={"state":"CANDIDATES_ONLY_NOT_RELEASED","source_edition_sha256":digest(ROOT/"edition.json"),"sports_sha256":digest(ROOT/"sports-lock.json"),"asset_lock_sha256":digest(ROOT/"asset-lock.json"),"renderer_sha256":digest(Path(__file__)),"files":[]}
    for f,im in output:
        p=out/f["output"];im.save(p,"PNG",compress_level=9)
        proof=out/(p.stem+".phone.png");im.resize((390,693),Image.Resampling.LANCZOS).save(proof,"PNG")
        receipt["files"].append({"folio":f["id"],"path":str(p.relative_to(ROOT)),"sha256":digest(p),"phone_path":str(proof.relative_to(ROOT)),"phone_sha256":digest(proof),"dimensions":[W,H]})
    (out/"render-receipt.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    print("Two candidates rendered. Independent review required before release.")
if __name__=="__main__":main()
