"""Historical artwork-only candidate composition; no new likeness generation.
The source folios are recovered, inspected public Schemin artwork. Do not confuse
the illustrated moments with Week 12 outcomes. This is a review candidate, not release."""
import hashlib,json,subprocess,io,math,random
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageEnhance,ImageFilter
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
OUT=ROOT/"historical-candidates"
OUT.mkdir(exist_ok=True)
def read(n):return json.loads((ROOT/n).read_text())
data=read("sports-lock.json")["data"]
edition=read("edition.json")
register=read("week9-week10-visual-reference-register.json")
ref=register["week9"]["source_revision"]
def git(*args):return subprocess.check_output(["git",*args],cwd=REPO)
def load_page(p):
    raw=git("show",ref+":"+p["path"])
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==p["sha"]
    return Image.open(io.BytesIO(raw)).convert("RGB")
pages={p["page"]:load_page(p) for p in register["week9"]["pages"]}
# Hand-selected, normalized regions from actual inspected Week 9 folios.
# Crop source lettering out. Avoid treating scene-specific equipment as new canon.
bounds={
1:(5,.60,.19,.97,.73),12:(5,.02,.18,.49,.72),
10:(9,.06,.15,.58,.40),9:(9,.04,.52,.51,.81),
2:(12,.04,.16,.56,.42),11:(12,.015,.55,.50,.82),
7:(18,.02,.28,.44,.67),8:(18,.69,.22,.98,.67),
5:(21,.015,.24,.55,.72),4:(21,.59,.28,.985,.73),
3:(23,.015,.17,.52,.44),6:(23,.44,.44,.99,.75)}
assert set(bounds)==set(range(1,13))
def crop(id):
    p,x0,y0,x1,y1=bounds[id];im=pages[p];w,h=im.size
    return im.crop((round(x0*w),round(y0*h),round(x1*w),round(y1*h)))
portraits={i:crop(i) for i in bounds}
team={t["id"]:t for t in data["teams"]}
S=2; W,H=1080*S,1920*S
gold="#D9B16B";light="#F8E9CF";muted="#C7B99E";red="#8A3930";green="#327450"
FONTROOT=Path("/usr/share/fonts/truetype/dejavu")
fonts={"display":FONTROOT/"DejaVuSerif-Bold.ttf","body":FONTROOT/"DejaVuSans.ttf","serif":FONTROOT/"DejaVuSerif.ttf","bold":FONTROOT/"DejaVuSans-Bold.ttf"}
def font(k,n):return ImageFont.truetype(str(fonts[k]),round(n*S))
def box(d,xy,fill=None,outline=None,width=1):
    d.rectangle(tuple(round(i*S) for i in xy),fill=fill,outline=outline,width=round(width*S))
def line(d,xy,fill=gold,width=1):d.line(tuple(round(i*S) for i in xy),fill=fill,width=round(width*S))
def txt(d,s,x,y,k="body",n=25,color=light,anchor="lt"):
    d.text((round(x*S),round(y*S)),str(s),font=font(k,n),fill=color,anchor=anchor)
def width(d,s,k,n):return d.textlength(s,font=font(k,n))/S
def fit(d,s,x,y,maxw,k="display",n=40,minn=20,color=light,anchor="lt"):
    while n>minn and width(d,s,k,n)>maxw:n-=1
    assert width(d,s,k,n)<=maxw,("overflow",s,maxw,n)
    txt(d,s,x,y,k,n,color,anchor)
def wrap(d,s,x,y,maxw,k="body",n=24,maxlines=3,color=muted,leading=1.18,minn=19):
    for size in range(n,minn-1,-1):
        lines=[]; cur=""
        for word in s.split():
            t=(cur+" "+word).strip()
            if cur and width(d,t,k,size)>maxw:lines.append(cur);cur=word
            else:cur=t
        if cur:lines.append(cur)
        if len(lines)<=maxlines and all(width(d,t,k,size)<=maxw for t in lines):
            for i,t in enumerate(lines):txt(d,t,x,y+i*size*leading,k,size,color)
            return len(lines)*size*leading
    raise ValueError(("wrap overflow",s,maxw))
def paste(im,source,xy):
    x,y,w,h=map(lambda v:round(v*S),xy)
    art=ImageOps.fit(source,(w,h),method=Image.Resampling.LANCZOS,centering=(.5,.44))
    im.paste(art,(x,y))
def canvas():
    # Subtle warm paper/stone grain with radial autumn glow, no AI-repaint of art.
    rng=random.Random(26)
    small=Image.new("RGB",(270,480))
    px=small.load()
    for y in range(480):
        for x in range(270):
            q=max(0,1-math.hypot((x-135)/220,(y-120)/470))
            z=rng.randrange(-4,5)
            px[x,y]=(max(0,int(19+25*q+z)),max(0,int(18+13*q+z)),max(0,int(15+5*q+z)))
    im=small.resize((W,H),Image.Resampling.BICUBIC);d=ImageDraw.Draw(im)
    for pad,sw,col in [(9,2,gold),(15,1,"#79592E"),(21,1,"#4F3F2C")]:
        box(d,(pad,pad,1080-pad,1920-pad),outline=col,width=sw)
    # restrained filigree, autumn leaf-like ornamental shapes
    for x,flip in [(28,1),(1052,-1)]:
        for y,fy in [(27,1),(1893,-1)]:
            line(d,(x,y,x+flip*85,y),gold,2);line(d,(x,y,x,y+fy*85),gold,2)
            for i in range(4):
                a=x+flip*(12+i*12);b=y+fy*(12+i*6)
                d.ellipse((int((a-5)*S),int((b-3)*S),int((a+5)*S),int((b+3)*S)),outline=gold,width=S)
    return im,d
def header(d,title,deck):
    txt(d,"S C H E M I N ’ 2 6   •   T H A N K S G I V I N G",540,38,"bold",21,gold,"mt")
    line(d,(66,72,1014,72),"#967644",1)
    fit(d,title,540,86,970,"display",51,34,light,"mt")
    fit(d,deck,540,147,960,"serif",26,21,muted,"mt")
def footer(d,page,caption):
    line(d,(38,1857,1042,1857),gold,1)
    fit(d,caption,540,1871,960,"body",21,17,muted,"mt")
    txt(d,page,540,1901,"bold",16,gold,"ms")
def card(im,d,t,e,x,y):
    box(d,(x,y,x+494,y+242),"#25231E","#80663C",1)
    paste(im,portraits[t["id"]],(x+3,y+3,189,236))
    box(d,(x+3,y+3,x+192,y+239),outline=gold,width=1)
    tx=x+204
    wrap(d,t["name"],tx,y+12,280,"bold",27,2,light,1.1,23)
    txt(d,t["record"],tx,y+77,"display",43,gold)
    for i,v in enumerate(t["ribbon"]):
        xx=tx+i*25
        box(d,(xx,y+130,xx+23,y+157),green if v=="W" else red)
        txt(d,v,xx+11.5,y+143.5,"bold",18,light,"mm")
    wrap(d,e["caption"],tx,y+169,276,"body",23,3,muted,1.14,19)
f1,f2=edition["fols"]
im,d=canvas();header(d,"Eleven Weeks. Twelve Destinies.","The Commonwealth • 2026 regular-season journeys")
for g,division in enumerate(["Burgers","Wings","Pizza"]):
    y=195+g*548
    txt(d,division.upper()+" DIVISION",40,y,"display",29,gold)
    line(d,(40,y+35,1040,y+35),"#8F7548")
    for k,e in enumerate(f1["teams"][4*g:4*g+4]):
        card(im,d,team[e["team_id"]],e,38+(k%2)*510,y+46+(k//2)*250)
footer(d,"FOLIO 01 / 02","Weeks 1–11 • W / L from left to right • ESPN")
p1=OUT/f1["output"];im.save(p1,compress_level=6)
im,d=canvas();header(d,"The Reckoning — Week XII","Six Week 4 rematches. Three divisional weeks remain.")
for i,(e,m) in enumerate(zip(f2["matchups"],data["rematches"])):
    assert (e["winner"],e["loser"])==(m["winner"],m["loser"])
    y=199+i*269
    box(d,(38,y,1042,y+249),"#27231E","#967644",1)
    # Pictured as separate archival portraits; no manufactured matchup result.
    for j,id in enumerate([m["winner"],m["loser"]]):
        paste(im,portraits[id],(41+j*168,y+3,165,243))
        box(d,(41+j*168,y+3,206+j*168,y+246),outline="#B89555")
    x=389
    wrap(d,m["winner_name"]+" × "+m["loser_name"],x,y+12,640,"bold",31,2,light,1.12,26)
    fit(d,"WEEK 4 • "+m["winner_name"]+" won",x,y+86,640,"bold",21,19,gold)
    txt(d,m["week4_score"],x,y+113,"display",44,light)
    wrap(d,e["caption"],x,y+168,640,"body",24,2,muted,1.12,21)
    txt(d,"ARCHIVE PORTRAITS",42,y+225,"bold",11,light)
footer(d,"FOLIO 02 / 02","Week 4 finals • Week 12 undecided • Archival imagery")
p2=OUT/f2["output"];im.save(p2,compress_level=6)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
receipt={"state":"TWO_ARCHIVAL_ARTWORK_CANDIDATES__NOT_RELEASE_APPROVED","source_commit":ref,"source_pages":[{"page":p["page"],"path":p["path"],"git_blob":p["sha"]} for p in register["week9"]["pages"]],"crop_bounds":bounds,"source_hashes":{n:sha(ROOT/n) for n in ["sports-lock.json","edition.json","week9-week10-visual-reference-register.json"]},"fonts":{k:{"file":v.name,"sha256":sha(v)} for k,v in fonts.items()},"limitations":["Historical screenshot crops, not newly staged Week 12 scenes.","Week 10 screenshot extraction unavailable; Week 11 Chili omitted.","No independent character/Atlas/Umpire signoff; original generation route remains blocked."],"outputs":[]}
for p in [p1,p2]:
    with Image.open(p) as pic:
        assert pic.size==(2160,3840)
        proof=OUT/(p.stem+".phone.png");pic.resize((390,693),Image.Resampling.LANCZOS).save(proof)
    receipt["outputs"].append({"file":p.name,"sha256":sha(p),"phone":proof.name,"phone_sha256":sha(proof),"size":[2160,3840]})
(OUT/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt["outputs"],indent=2))
