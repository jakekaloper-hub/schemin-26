#!/usr/bin/env python3
"""W10-M01: a 42-second moving stunt-blocking previsualization using original drawn shapes.

Not a source-approved art render; no body motion capture, identity, or human voice approval.
No paid inference or downloaded model weights.
"""
from __future__ import annotations
import hashlib, json, math, os, random, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
BOARD=json.loads((HERE/"film_storyboard_v1.json").read_text())
PAGES=["W10-P05","W10-P06","W10-P07"]
shots=[s for sc in BOARD["scenes"] if sc["folio"] in PAGES for s in sc["shots"]]
assert len(shots)>0
OUT=HERE/"proofs"/"M01_RODEO_STUNT_PREVIS"
OUT.mkdir(parents=True,exist_ok=True)
W,H,FPS=960,540,12
DURATION=42
RNG=np.random.default_rng(2226)
FRAME_COUNT=DURATION*FPS
def font(size,bold=False):
    options=["/System/Library/Fonts/Supplemental/Arial Bold.ttf","/System/Library/Fonts/Supplemental/Arial.ttf"] if bold else ["/System/Library/Fonts/Supplemental/Arial.ttf"]
    for p in options:
        try:return ImageFont.truetype(p,size)
        except OSError:pass
    return ImageFont.load_default()

# Genuine 2.5D visual-development environment; all performers below are schematic previsualization proxies.
xx,yy=np.meshgrid(np.arange(W,dtype=np.float32),np.arange(H,dtype=np.float32))
sky=np.clip(yy/410,0,1)
base=np.zeros((H,W,3),np.float32)
for c,(top,bottom) in enumerate(zip((22,39,57),(50,46,49))):
    base[:,:,c]=top*(1-sky)+bottom*sky
ground=yy>315
for k,val in enumerate((37,35,35)):
    base[:,:,k]=np.where(ground,val+(yy-315)*0.09,base[:,:,k])
# Warm genuine practical lamp sources, separate from meteorological color.
for cx,cy,strength in [(120,284,1.2),(420,264,.6),(820,283,1.0)]:
    radial=np.exp(-((xx-cx)**2+(yy-cy)**2)/(2*125**2))*strength
    base[:,:,0]+=radial*45
    base[:,:,1]+=radial*26
    base[:,:,2]+=radial*8
base=np.clip(base+RNG.normal(0,1.8,(H,W,1)),0,255).astype("uint8")
BACK=Image.fromarray(base,"RGB")
D0=ImageDraw.Draw(BACK)
# Soaked dirt, curved arena rail, controlled public exit geography.
for j in range(18):
    y=344+j*15
    D0.line([(10,y),(W-10,y+int(j*0.7))],fill=(55+j//4,53+j//5,48),width=1)
D0.ellipse((45,305,940,598),outline=(132,101,73),width=8)
D0.ellipse((98,331,888,585),outline=(75,68,58),width=2)
# Gallery rail and sheltered overhang
D0.polygon([(0,292),(960,280),(960,318),(0,316)],fill=(52,51,50))
D0.line((0,292,960,280),fill=(151,125,86),width=5)
for x in range(15,960,85):
    D0.line((x,300,x+4,370),fill=(65,59,53),width=8)
# Locked but passable service gate on rear-left screen geography x 755-835 (fixed over shots).
D0.rectangle((110,232,186,324),fill=(26,34,42),outline=(161,133,94),width=5)
D0.line((110,282,186,282),fill=(93,78,56),width=3)
D0.text((94,212),"SERVICE GATE",fill=(208,180,124),font=font(14,True))
# Stand lamps/amber pools in audience space, far silhouette spectators
for x in [110,430,820]:
    D0.line((x,287,x,245),fill=(61,62,60),width=6)
    D0.ellipse((x-8,239,x+8,254),fill=(255,181,90))
for i in range(31):
    x=20+i*31;y=290+(i%3)*4
    D0.ellipse((x,y-38,x+11,y-24),fill=(13,24,32))
    D0.rectangle((x-2,y-23,x+12,y+7),fill=(13,24,32))
D0.line((0,317,960,303),fill=(150,117,75),width=3)
# Mud reflections and tramline groove connected to Chili's skid.
for i in range(45):
    px=int(RNG.integers(40,925));py=int(RNG.integers(360,520))
    width=int(RNG.integers(8,45))
    D0.line((px,py,px+width,py),fill=(92,82,71),width=1)

def lerp(a,b,x):
    return a+(b-a)*max(0,min(1,x))
def phase(t):
    if t<8:return "OPENING / PUBLIC LAUGH","W10-P05"
    if t<17:return "THE SECOND IMITATION","W10-P05"
    if t<21:return "THE OPEN GATE","W10-P05 → P06"
    if t<27:return "TORSO LOOP → SLIP","W10-P06"
    if t<35:return "THE KNOT / MANUAL","W10-P07"
    return "THE PUBLIC COST","W10-P07"

def actor_chili(draw,x,y,scale=1,fall=0,imitate=0):
    # The colored silhouettes are rig stand-ins; original raster appearance is QA reference only.
    s=scale
    if fall:
        body_y=y+int(15*fall)
        draw.ellipse((x-55*s,body_y+20*s,x+63*s,body_y+31*s),fill=(19,21,22))
        draw.polygon([(x-47*s,body_y-12*s),(x+36*s,body_y-18*s),(x+55*s,body_y+22*s),(x-26*s,body_y+20*s)],fill=(106,41,34),outline=(176,95,63))
        draw.ellipse((x+40*s,body_y-26*s,x+69*s,body_y+2*s),fill=(72,49,43))
        draw.polygon([(x+34*s,body_y-23*s),(x+75*s,body_y-25*s),(x+88*s,body_y-19*s),(x+23*s,body_y-18*s)],fill=(55,43,32))
        draw.polygon([(x-46*s,body_y+10*s),(x-63*s,body_y+25*s),(x-48*s,body_y+33*s),(x-18*s,body_y+21*s)],fill=(35,37,36))
        return (x+5*s,body_y-5*s)
    draw.ellipse((x-17*s,y+13*s,x+25*s,y+22*s),fill=(18,19,21))
    draw.line((x-12*s,y-12*s,x-14*s,y+17*s),fill=(44,38,36),width=max(2,int(14*s)))
    draw.line((x+13*s,y-10*s,x+16*s,y+17*s),fill=(43,36,33),width=max(2,int(14*s)))
    draw.polygon([(x-28*s,y-81*s),(x+28*s,y-85*s),(x+35*s,y-18*s),(x-31*s,y-18*s)],fill=(114,41,34),outline=(192,87,56))
    draw.polygon([(x-25*s,y-76*s),(x-50*s,y-20*s),(x-25*s,y-10*s),(x-11*s,y-53*s)],fill=(81,26,24))
    draw.polygon([(x+20*s,y-72*s),(x+44*s,y-14*s),(x+31*s,y-9*s),(x+6*s,y-49*s)],fill=(81,27,24))
    ax=x+25*s;ay=y-51*s
    if imitate>0:
        draw.line((ax,ay,ax+18*s,y-39*s),fill=(128,49,31),width=max(2,int(8*s)))
    draw.ellipse((x-15*s,y-110*s,x+17*s,y-78*s),fill=(91,61,42))
    draw.ellipse((x-32*s,y-108*s,x+38*s,y-102*s),fill=(37,30,26))
    draw.polygon([(x-15*s,y-109*s),(x-6*s,y-129*s),(x+18*s,y-125*s),(x+26*s,y-108*s)],fill=(50,39,26),outline=(183,120,71))
    draw.line((x-17*s,y-25*s,x+17*s,y-25*s),fill=(182,136,83),width=max(2,int(5*s)))
    return (x,y-53*s)

def actor_dk(draw,x,y,scale=1,arm=0):
    s=scale
    draw.ellipse((x-72*s,y-64*s,x+85*s,y-23*s),fill=(35,39,42),outline=(106,94,72),width=3)
    draw.polygon([(x-55*s,y-27*s),(x+60*s,y-27*s),(x+80*s,y-40*s),(x+70*s,y+1*s),(x-64*s,y+1*s)],fill=(72,35,29))
    for i,leg_x in enumerate((-58,-15,33,68)):
        hoof_x=x+leg_x*s
        d=(12 if i%2 else 0)
        draw.line((hoof_x,y-30*s,hoof_x+(d-6)*s,y+36*s),fill=(34,38,39),width=max(2,int(13*s)))
        draw.ellipse((hoof_x-18*s,y+27*s,hoof_x+15*s,y+44*s),fill=(21,23,25),outline=(105,95,72))
    draw.ellipse((x-40*s,y-158*s,x+28*s,y-53*s),fill=(35,37,40),outline=(123,97,62),width=3)
    draw.polygon([(x-34*s,y-128*s),(x+26*s,y-130*s),(x+34*s,y-84*s),(x-34*s,y-87*s)],fill=(115,40,36),outline=(193,151,91))
    draw.ellipse((x-26*s,y-195*s,x+18*s,y-151*s),fill=(30,33,35),outline=(127,105,75))
    draw.ellipse((x-19*s,y-180*s,x+7*s,y-168*s),fill=(79,76,67))
    draw.ellipse((x-13*s,y-184*s,x-7*s,y-180*s),fill=(238,166,81))
    draw.ellipse((x+1*s,y-184*s,x+7*s,y-180*s),fill=(238,166,81))
    draw.line((x+21*s,y-127*s,x+45*s,y-(80+35*arm)*s),fill=(40,39,38),width=max(2,int(15*s)))
    draw.ellipse((x+30*s,y-(90+35*arm)*s,x+53*s,y-(69+35*arm)*s),fill=(47,43,38))
    draw.line((x-29*s,y-123*s,x-47*s,y-73*s),fill=(39,38,37),width=max(2,int(15*s)))
    return (x+45*s,y-(83+35*arm)*s)

# Frame rendering. Subtle camera move, not an unsourced physical environment expansion.
writer=imageio_ffmpeg.write_frames(str(OUT/"W10_M01_stunt_previs_silent.mp4"),(W,H),fps=FPS,
    codec="libx264",pix_fmt_in="rgb24",macro_block_size=2,output_params=["-crf","22","-preset","veryfast","-movflags","+faststart"])
writer.send(None)
for fi in range(FRAME_COUNT):
    t=fi/FPS
    image=BACK.copy()
    draw=ImageDraw.Draw(image)
    # Palette choreography and action cause follow P05–P07.
    dkx=745
    if t<17:cx=475
    elif t<22:cx=lerp(475,260,(t-17)/5)
    elif t<26:cx=lerp(260,230,(t-22)/4)
    else:cx=230
    fall=0 if t<24.5 else (t-24.5)/2.5 if t<27 else 1
    imitation=max(0,1-abs(t-12)/4)
    arm=max(0,min(1,(t-16)/3))
    # Route rope to the chest, not neck, and respect actor hands.
    hand=actor_dk(draw,dkx,395,1.02,arm)
    torso=actor_chili(draw,cx,408,0.91,fall=fall,imitate=imitation)
    if t>=17:
        rope_y=torso[1]+(0 if fall else 5)
        progress=max(0,min(1,(t-18)/3))
        endx=lerp(dkx-25,cx,progress)
        endy=lerp(hand[1],rope_y,progress)
        points=[]
        for k in range(28):
            z=k/27
            xx2=lerp(hand[0],endx,z)
            yy2=lerp(hand[1],endy,z)+math.sin(math.pi*z)*(22 if t<21 else 12)
            points.append((int(xx2),int(yy2)))
        draw.line(points,fill=(226,191,131),width=3)
        if t>=20.5:
            # Lasso is around upper torso visible as loop; no neck constriction.
            if fall:
                draw.ellipse((cx-44,torso[1]-18,cx+40,torso[1]+22),outline=(227,193,128),width=4)
            else:
                draw.ellipse((cx-32,torso[1]-26,cx+30,torso[1]+21),outline=(227,193,128),width=4)
    if 21<t<27:
        draw.line((cx-21,446,cx-110,472),fill=(116,92,68),width=3)
    # Hat dropped during caught turn and stays visible in the final payoff.
    if t>24.5:
        draw.ellipse((cx-118,451,cx-32,460),fill=(43,36,29))
        draw.polygon([(cx-98,455),(cx-82,429),(cx-61,428),(cx-53,455)],fill=(46,35,28),outline=(146,117,78))
    if t>=30:
        # Provisional handwork is indicated by coordinated repeated movements, not a magically appearing knot.
        progress=max(0,min(1,(t-30)/5))
        draw.ellipse((cx-2-10*progress,torso[1]-2,cx+10+10*progress,torso[1]+8),outline=(247,211,144),width=4)
    # Intentional weather: gust-dependent streaks, wet soil reflectivity kept under actor.
    rain=random.Random(fi*721+400)
    for k in range(42):
        x0=rain.randint(0,W);y0=rain.randint(0,H)
        length=rain.randint(6,18)
        draw.line((x0,y0,x0-4,y0+length),fill=(112,140,157),width=1)
    # Cinematic masks: stage band/shot assignment and proof watermark.
    draw.rectangle((0,0,W,74),fill=(11,16,22))
    top,page=phase(t)
    draw.text((22,12),"SCHEMIN ’26  /  WEEK 10  /  M01 — HIGHLAND RODEO",font=font(18,True),fill=(227,190,118))
    draw.text((22,44),top,font=font(15),fill=(219,219,211))
    draw.text((W-177,44),page,font=font(14),fill=(171,185,187))
    draw.rectangle((0,H-45,W,H),fill=(11,15,20))
    draw.text((22,H-31),"MOTION-BLOCKING PREVIS  •  NO APPROVED CHARACTER RENDER  •  SOURCE P05–P07",font=font(12),fill=(188,200,201))
    draw.text((W-132,H-31),f"TIME {t:05.1f}s",font=font(13,True),fill=(227,190,118))
    writer.send(np.asarray(image,dtype=np.uint8).tobytes())
writer.close()

# Original ambient + dynamic specific action foley, no copyrighted theme.
SR=24000
tt=np.arange(int(SR*DURATION),dtype=np.float32)/SR
rng=np.random.default_rng(20771)
wind_knots=rng.normal(0,1,int(DURATION*16)+1)
wind=np.interp(tt,np.linspace(0,DURATION,len(wind_knots)),wind_knots)
rain=rng.normal(0,1,tt.size)
amb=0.018*wind + 0.006*rain
chords=(np.sin(2*np.pi*73.4*tt)+.38*np.sin(2*np.pi*110*tt)+.22*np.sin(2*np.pi*146.8*tt))
music_env=.5+.3*np.sin(tt*.4)
music=0.020*chords*music_env
fx=np.zeros_like(amb)

def hit(moment,amp=0.15,freq=126,decay=15):
    start=int(moment*SR)
    if start<0 or start>=len(fx):return
    n=min(int(SR*.28),len(fx)-start)
    ph=np.arange(n,dtype=np.float32)/SR
    fx[start:start+n]+=amp*np.sin(2*np.pi*freq*ph)*np.exp(-decay*ph)
for sec in (16.9,17.8,18.6,21.1,22.2,23.5,26.0,30.1,32.3,34.1):
    hit(sec,.09,125,11)
hit(23.1,.24,93,8);hit(26.4,.32,76,10)
for sec in (19.6,20.5):
    hit(sec,.045,430,11)
# Crowd-react pulse, low and quiet without imitating words.
crowd_env=np.exp(-((tt-13.3)/2.7)**2)*.012 + np.exp(-((tt-37)/2.4)**2)*.009
fx+=rng.normal(0,1,len(tt))*crowd_env
audio=np.clip(amb+music+fx,-.86,.86)
for stem_name,stem in [('AMB',amb),('FX',fx),('MX',music)]:
    with wave.open(str(OUT/f'W10_M01_{stem_name}_original_24k.wav'),'wb') as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(SR)
        f.writeframes((np.clip(stem,-.92,.92)*32767).astype('<i2').tobytes())
with wave.open(str(OUT/"W10_M01_original_ambience_foley.wav"),"wb") as f:
    f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR)
    f.writeframes((audio*32767).astype("<i2").tobytes())

receipt={
    "id":"SCHEMIN-W10-M01-BLOCKING-PROOF-20261122",
    "status":"RENDERED_AS_NONCANONICAL_ANIMATIC",
    "warning":"2D schematic stage and actor silhouette proxies; NOT photorealistic video, approved character pixels, valid neck/stunt rig, lip-synced dialogue or finished scene",
    "source":["W10-P05","W10-P06","W10-P07"],
    "source_shots":len(shots),
    "duration_sec":DURATION,"fps":FPS,"size":[W,H],
    "video":str(OUT/"W10_M01_stunt_previs_silent.mp4"),
    "audio":str(OUT/"W10_M01_original_ambience_foley.wav"),
    "video_sha256":hashlib.sha256((OUT/"W10_M01_stunt_previs_silent.mp4").read_bytes()).hexdigest(),
    "audio_sha256":hashlib.sha256((OUT/"W10_M01_original_ambience_foley.wav").read_bytes()).hexdigest(),
    "render_method":"Local Pillow/NumPy schematic geometry, imageio-ffmpeg, original synthesized ambience and Foley. No Hugging Face inference.",
    "authoritative_asset_references":"P05–P07 reference SHA lists in film_storyboard_v1.json; do not substitute generated silhouettes for canonical reference bytes",
    "qa_gate":{"source_story_sequence":"TESTABLE","character_appearance":"NOT_PASSED","full_body_mechanics":"SCHEMATIC_ONLY","audio_originality":"ORIGINAL_SYNTH","Umpire":"PENDING"}
}
(OUT/"PREVIS_RENDER_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({k:receipt[k] for k in ("status","duration_sec","fps","size","source_shots","video_sha256","audio_sha256")},indent=2))
