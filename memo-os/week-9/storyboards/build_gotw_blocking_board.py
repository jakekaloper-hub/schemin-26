"""Deterministic rough blocking study, not final character artwork or result authority."""
from pathlib import Path
from html import escape
import json

OUT = Path(__file__).parent
parts=[]
def add(s): parts.append(s)
def text(x,y,s,size=14,weight='normal',anchor='start',fill='#30302d'):
    add(f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">{escape(s)}</text>')
def path(d,fill='none',stroke='#30302d',w=2,extra=''):
    add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {extra}/>')
def line(x1,y1,x2,y2,w=2,stroke='#30302d',extra=''):
    add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{w}" stroke-linecap="round" {extra}/>')
def ellipse(x,y,rx,ry,fill='none',stroke='#30302d',w=2):
    add(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{w}"/>')
def rect(x,y,w,h,fill='none',stroke='#30302d',sw=2):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def arrow(d): path(d,stroke='#72716b',w=2,extra='stroke-dasharray="6 5" marker-end="url(#arrow)"')
def clubhouse(x=35,y=80,s=1):
    add(f'<g transform="translate({x} {y}) scale({s})" opacity=".78">')
    rect(0,26,135,62,'#e7e4da'); path('M-8 26 L67 -7 L143 26 Z','#bab8af')
    rect(49,0,35,26,'#d7d4ca');path('M44 0 L67 -19 L89 0 Z','#aeaca4')
    for xx in [12,35,87,110]:rect(xx,40,12,23,'#aaa89f',sw=1)
    rect(56,46,22,42,'#aaa89f',sw=1)
    for xx in [49,83]:line(xx,27,xx,88,2)
    line(-10,92,145,92,2)
    add('</g>')
def tree(x,y,s=1):
    add(f'<g transform="translate({x} {y}) scale({s})" opacity=".65">')
    path('M0 0 L-2 -63 M-1 -30 L-22 -50 M-1 -43 L18 -68 M-2 -55 L-12 -76',w=2)
    for xx,yy,rx in [(-19,-70,18),(0,-86,21),(21,-74,18),(-3,-60,29)]:ellipse(xx,yy,rx,16,'#ddd9cf',w=.8)
    add('</g>')
def env(pond=True,wide=False):
    rect(0,0,720,340,'#f4f1e8','none',0)
    ellipse(545,62,29,29,'#dedbcf','none',0)
    path('M0 155 Q110 123 215 151 T430 153 T720 128',stroke='#9c9a91',w=1.5)
    path('M0 195 Q160 166 355 193 T720 183',stroke='#aeaba1',w=1)
    path('M0 310 Q200 271 395 300 T720 279',stroke='#c3bfb4',w=1)
    clubhouse(44,70,.75 if not wide else .9)
    for x,y,s in [(5,159,.85),(180,152,.65),(660,145,.85),(702,154,.8),(214,145,.5)]:tree(x,y,s)
    if pond:
        path('M500 217 Q580 193 720 217 L720 306 Q584 309 488 270 Q460 240 500 217Z','#d2d5d1','#969b97',1)
        for x,y in [(530,240),(615,256),(565,276),(675,231)]:line(x,y,x+40,y,1,'#8b9691')
    for x in range(20,700,65):path(f'M{x} 330 l4 -9 m-4 9 l-5 -5',stroke='#b4afa4',w=.8)
def duck_head(x=0,y=-100,s=1,face=1):
    add(f'<g transform="translate({x} {y}) scale({s*face} {s})">')
    path('M-11 11 Q-24 1 -17 -14 Q-10 -25 4 -20 Q17 -18 17 -3 L20 8 L7 20 L-5 17Z','#fffdf6',w=1.6)
    path('M10 -2 Q26 -4 38 3 Q39 8 26 10 L12 8Z','#c3bda9',w=1.6)
    path('M-21 -17 Q-15 -32 9 -27 L19 -17 L32 -15 Q19 -9 -23 -13Z','#727b6b',w=1.7)
    ellipse(10,-7,2.3,2.9,'#252723','none',0)
    path('M-10 14 l-5 5 m2 -8 l-6 3',stroke='#8d8b81',w=1)
    add('</g>')
def human_head(x=0,y=-100,s=1,face=1):
    add(f'<g transform="translate({x} {y}) scale({s*face} {s})">')
    path('M-15 6 Q-24 -6 -14 -23 Q2 -35 18 -17 L20 -3 L25 4 L18 7 L14 20 L0 23 L-12 14Z','#e5dfd2',w=1.6)
    path('M-18 -10 Q-27 -19 -14 -22 Q-17 -31 -7 -29 Q-1 -38 4 -29 Q14 -34 17 -24 Q25 -25 22 -16 L15 -11 L10 -20 L5 -15 L0 -23 L-7 -15 L-12 -20Z','#9f9682',w=1.6)
    line(8,-1,15,-3,1.4);ellipse(13,1,1.3,1.8,'#32332d','none',0)
    path('M20 12 l-7 2 m-17 4 l5 3 m-10 -5 l3 4',stroke='#6e675b',w=1)
    add('</g>')
def figure(kind,x,y,s=1,pose='stand',face=1):
    add(f'<g transform="translate({x} {y}) scale({s*face} {s})">')
    ellipse(0,3,37,5,'#c9c5ba','none',0)
    # Two connected legs, sports feet.
    if pose=='swing':
        path('M-8 -33 L-18 -11 L-30 0 L-14 1 L1 -20 L7 -31Z','#c2b9a6',w=1.7)
        path('M8 -33 L22 -8 L37 -2 L36 4 L19 4 L4 -12 L-1 -30Z','#d0c6b3',w=1.7)
    else:
        path('M-11 -36 L-22 -4 L-30 0 L-29 5 L-10 4 L2 -31Z','#c2b9a6',w=1.7)
        path('M3 -34 L12 -4 L9 2 L29 3 L30 -2 L22 -6 L18 -36Z','#d0c6b3',w=1.7)
    if kind=='human':
        path('M-19 -77 Q-32 -47 -30 -24 L-8 -31 L16 -25 L27 -32 L16 -76Z','#989481',w=1.8)
        path('M-12 -76 L12 -74 L17 -32 L-14 -31Z','#d8d1c0',w=1.5)
        path('M-22 -77 Q-17 -92 -4 -89 L18 -76 L5 -66Z','#797d6b',w=1.7)
        line(-14,-42,17,-40,3,'#82755e')
    else:
        path('M-17 -77 L16 -77 L22 -35 L-16 -33Z','#73806e',w=1.7)
        path('M-9 -77 L0 -61 L10 -77Z','#f6f1e3',w=1.3)
        path('M-18 -77 L-24 -66 L-18 -48',stroke='#c4bca9',w=8)
    shoulderL=(-16,-72);shoulderR=(15,-72)
    if pose=='swing': arms=[(shoulderL,(-18,-96),(9,-119)),(shoulderR,(36,-100),(9,-119))];club=(9,-119,-57,-149)
    elif pose=='recover':arms=[(shoulderL,(10,-57),(40,-81)),(shoulderR,(45,-58),(40,-81))];club=(40,-81,88,-125)
    elif pose=='offer': arms=[(shoulderL,(-23,-47),(-19,-22)),(shoulderR,(37,-67),(53,-66))];club=None
    elif pose=='receive':arms=[(shoulderL,(-25,-48),(-17,-25)),(shoulderR,(38,-59),(51,-65))];club=None
    elif pose=='putt':arms=[(shoulderL,(0,-53),(24,-40)),(shoulderR,(35,-56),(24,-40))];club=(24,-40,66,0)
    elif pose=='slump':arms=[(shoulderL,(-25,-49),(-22,-21)),(shoulderR,(26,-49),(42,-34))];club=(42,-34,54,4)
    else:arms=[(shoulderL,(-24,-48),(-19,-22)),(shoulderR,(29,-51),(32,-27))];club=(32,-27,42,4)
    for a,b,c in arms:
        path(f'M{a[0]} {a[1]} L{b[0]} {b[1]} L{c[0]} {c[1]}',stroke='#33352f',w=9)
        path(f'M{a[0]} {a[1]} L{b[0]} {b[1]} L{c[0]} {c[1]}',stroke='#ebe5d5',w=6)
        ellipse(c[0],c[1],4,4,'#eee5d5',w=1)
    if club:
        a,b,c,d=club;line(a,b,c,d,2.5);line(c,d,c+13,d-1,4)
    # Neck/head retained as simple approved-identity silhouettes.
    if kind=='duck':duck_head(0,-99,1)
    else:human_head(0,-101,1)
    if pose=='slump':path('M0 -79 L9 -83',stroke='#55564b',w=2)
    add('</g>')
def flag(x,y):
    line(x,y,x,y-87,2);path(f'M{x} {y-87} l34 9 l-34 13Z','#8b9484',w=1.5);ellipse(x,y,8,3,'#636959','none',0)
def ball(x,y):ellipse(x,y,4,4,'#fffefa','#30302d',1.4)

def frame(i,head,cap1,cap2,draw,alternate=False):
    col=i%3;row=i//3;x=60+col*768;y=180+row*510
    add(f'<g id="frame-{i+1}" transform="translate({x} {y})">')
    rect(0,0,744,466,'#fbf9f1','#7b7a72',1.4)
    rect(0,0,744,40,'#404940' if alternate else '#e3dfd3','none',0)
    text(16,27,head,20,'bold',fill='#fffdf5' if alternate else '#30302d')
    add('<g transform="translate(12 48)" clip-path="url(#sceneClip)">');draw();add('</g>')
    line(14,398,730,398,1,'#d1ccbe')
    text(16,423,cap1,17);text(16,448,cap2,17)
    add('</g>')

def scene1():
    env();figure('duck',287,248,.60);figure('human',360,251,.64)
    line(30,224,30,290,2);line(154,224,154,290,2);rect(23,203,139,45,'#ece7d8',sw=1)
    text(92,222,'CHARITY',13,'bold','middle');text(92,240,'CLASSIC',13,'bold','middle')
    arrow('M260 275 Q320 272 370 266')
def scene2():
    env();figure('duck',230,305,1.55,'offer');figure('human',474,305,1.55,'receive',-1)
    rect(322,191,63,38,'#fffdf5',sw=1.3)
    for yy in [201,210,219]:line(334,yy,373,yy,1,'#9c998d')
    line(260,146,440,146,1,'#b9b5a9',extra='stroke-dasharray="5 6"')
def scene3():
    env();figure('human',155,280,1.05);figure('duck',355,310,1.55,'swing')
    ball(590,126);arrow('M392 288 Q475 148 590 126');path('M298 107 Q262 122 257 161',stroke='#aaa597',w=1,extra='marker-end="url(#arrow)"')
    line(306,309,382,309,1,'#7a7c6f')
def scene4():
    env();path('M91 275 Q165 237 336 263 Q433 298 369 323 Q224 346 77 314Z','#ddd5bf','#9d947f',1)
    figure('duck',552,245,.88);figure('human',239,311,1.58,'recover')
    for dx,dy in [(65,-28),(90,-42),(105,-61),(118,-80),(85,-66),(65,-53),(120,-38)]:
        path(f'M295 302 Q{300+dx*.5} {285+dy} {300+dx} {300+dy}',stroke='#b5aa8e',w=1)
    ball(456,169);arrow('M315 291 Q380 194 456 169')
def scene5():
    rect(0,0,720,340,'#efeadf','none',0)
    path('M30 340 Q45 193 128 176 L210 195 L266 340Z','#87907d',w=2)
    path('M445 340 L470 180 L567 176 Q676 223 698 340Z','#98927f',w=2)
    duck_head(170,132,3.4);human_head(554,130,3.5,-1)
    path('M291 90 L426 90',stroke='#b8b1a1',w=1,extra='stroke-dasharray="5 6"')
    rect(290,237,130,83,'#faf7ed',sw=1.2)
    for yy in [253,270,287]:line(310,yy,401,yy,1,'#b1aa9a')
    text(354,333,'NO SCORE SHOWN',11,'normal','middle')
def scene6():
    env();path('M84 260 Q199 152 419 175 Q527 198 508 255 Q341 322 96 292Z','#e1e4d7','#808b78',1.2)
    path('M480 196 Q550 225 545 286',stroke='#8b927e',w=1.5)
    flag(424,234);ball(300,265);figure('duck',217,275,.76,'putt');figure('human',113,276,.78)
    arrow('M457 248 Q495 268 548 279')
    text(276,309,'BALL',13,'bold');text(399,153,'FLAG',13,'bold');text(475,323,'SLOPED APRON',13,'bold');text(605,281,'POND',13,'bold')
def scene7():
    env();figure('human',518,240,.90);figure('duck',238,330,1.90,'putt')
    ball(387,330);flag(453,303)
    # Small isolated grip detail, not an extra limb in the main shot.
    rect(31,35,147,106,'#f9f5eb','#aaa496',1)
    line(68,48,145,128,4,'#545b50');ellipse(95,80,16,9,'#e4ddcb',w=1);ellipse(112,95,16,9,'#e4ddcb',w=1)
    text(45,131,'GRIP / STILL BALL',10,'bold')
def scene8a():
    env();path('M160 289 Q280 211 454 215 L507 268 L450 302Z','#e1e4d7','#a1a88e',1)
    figure('human',140,284,1.13);figure('duck',288,299,1.24,'slump');flag(421,256)
    arrow('M363 270 Q414 251 453 263 Q498 286 583 276')
    ball(577,276)
    for d in ['M579 270 l-12 -15','M584 266 l4 -20','M590 270 l16 -12']:path(d,stroke='#6f817c',w=2)
    ellipse(588,281,22,5,'none','#6f817c',1)
def scene8b():
    env();path('M280 290 Q371 196 484 215 L503 263 L440 304Z','#e1e4d7','#a1a88e',1)
    figure('human',157,303,1.22,'slump');figure('duck',332,297,1.12,'putt');flag(445,298)
    ball(422,298);arrow('M400 298 L438 298')
    ball(194,320)
    for xx in range(170,220,8):path(f'M{xx} 332 l-4 -14 m4 14 l5 -9',stroke='#8e927e',w=1.2)

add('<svg xmlns="http://www.w3.org/2000/svg" width="2400" height="1790" viewBox="0 0 2400 1790" role="img" aria-label="Nine-frame rough storyboard for Duckhook and ObiWan charity golf, with two clearly conditional endings">')
add('<defs><clipPath id="sceneClip"><rect width="720" height="340"/></clipPath><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8" fill="none" stroke="#72716b" stroke-width="1.2"/></marker></defs>')
rect(0,0,2400,1790,'#f4f0e5','none',0)
text(60,66,'SCHEMIN ’26  /  WEEK 9  /  GAME OF THE WEEK',23,'bold')
text(60,119,'THE CHARITY CLASSIC',42,'bold')
text(2340,68,'DR. DUCKHOOK × OBIWAN JACOBY',24,'bold','end')
text(2340,108,'ROUGH BLOCKING BOARD · P04–P07',20,'normal','end')
line(60,145,2340,145,2)
frame(0,'01 / P04 — THE MORNING PROMISE','CCOJ at sunrise. Host and visitor enter a calm world.','Clubhouse left. Water hazard right. No result implied.',scene1)
frame(1,'02 / P04 — COURTESY WITH AN EDGE','Duckhook offers the scorecard; ObiWan accepts.','The invitation becomes a personal rematch.',scene2)
frame(2,'03 / P05 — THE HOST’S FIRST STATEMENT','One driver, two hands, complete follow-through.','ObiWan watches outside the swing arc.',scene3)
frame(3,'04 / P05 — THE VISITOR’S ANSWER','ObiWan rotates through a sand-recovery attempt.','Club, ball and sand read as separate elements.',scene4)
frame(4,'05 / P05 — THE SMILES DISAPPEAR','A glance and a tightening grip change the relationship.','No fabricated golf score or premature winner.',scene5)
frame(5,'06 / P06 — SHOW THE RISK FIRST','Ball → flag → sloped apron → pond, in one view.','The audience sees the danger before the shot.',scene6)
frame(6,'07 / P06 — BEFORE THE STROKE','The grip steadies. The opponent waits. Hold the moment.','PAGE TURN: choose only the verified result branch.',scene7)
frame(7,'08A / P07 — IF OBIWAN WINS','Duckhook overhits; the established slope feeds the pond.','HYPOTHETICAL ENDING A — not a reported result.',scene8a,True)
frame(8,'08B / P07 — IF DUCKHOOK WINS','ObiWan’s mishit ends in rough; Duckhook stays composed.','HYPOTHETICAL ENDING B — mutually exclusive with A.',scene8b,True)
line(60,1730,2340,1730,1,'#a6a092')
text(60,1762,'VISUAL REHEARSAL ONLY · Simplified identity silhouettes, not final character art or image acceptance.',18)
text(2340,1762,'No final score · No chosen winner · No phase-completion claim',18,'normal','end')
add('</svg>')
svg='\n'.join(parts)+'\n'
(OUT/'W09_GOTW_ROUGH_BLOCKING_BOARD_V1.svg').write_text(svg)
print('SVG',len(svg),'bytes; 9 panels; 7 shared beats + 2 alternative endings')
