from pathlib import Path
from html import escape
import base64,json,subprocess,tempfile,math,re
root=Path(__file__).resolve().parents[4]
pp=root/'memo-os/week-11/preproduction'
out=pp/'visual-previs'
out.mkdir(parents=True,exist_ok=True)
data=json.loads((pp/'W11_ALL_35_VISUAL_DIRECTOR_SHOT_SPECS_2026-11-23.json').read_text())
folios={int(x['id'][1:]):x for x in data['folios']}
stories={
'G01':{'title':'THE CROSSING OWES A WORKER','subtitle':"His Majesty’s Blood vs D0nkey K0ng",'img':'03-after-you-austin.png','name':'Mountain Lake Bridge','cue':'CARTER RIGHT OF WAY → SLICK FOOTING → LIVING SURVIVOR','shots':[('THE COURTESY','Cart and four hooves | public lane','Full bridge • show the waiting worker'),('THE ANSWER','Austin sees worker | belt and hoof slip','Same wind in cloak, leaves and canvas'),('THE PRICE','Only verified loser falls, resurfacing alive','Lake chop — NEVER invent river rapids')],'accent':'#f5b769'},
'G02':{'title':'THE PROMISE LOSES ITS FOOTING','subtitle':'El Niño vs Slob on my Dobb','img':'04-six-i-told-her-six.png','name':'Hearthroad / possible wetland approach','cue':'SIX O’CLOCK → SECONDARY LASH FAILS → JORDAN BRAKES','shots':[('THE PROMISE','Manning at truck window | delivery slip SIX','Same Week 10 trailer; no time teleport'),('THE GUST','TWO steel kegs fall off, remaining beer secure','Primary straps intact; gravity rules'),('THE DECISION','Jordan brakes, radios and checks safe shoulder','Wetland truck clearance remains HOLD')],'accent':'#4ec9d8'},
'G03':{'title':'THE CROWD CHANGES SIDES','subtitle':'The Chili Cheesers vs ObiWan Jacoby','img':'05-the-safest-seat.png','name':'Foot of the Eastern Ascent','cue':'OFF BOARD → ONE ACCURATE THROW → CHILI-COVERED LADDER','shots':[('THE AUDIENCE','Wet OFF BOARD notice, recovered black hat','Both owners angry at being overlooked'),('THE THROW','Brandon hits target ONCE despite upland rain','Jake submerged in thick Wolf Brand Chili'),('THE AFTERMATH','Jake face to BOTH boots, Brandon at ladder','Rain stays outside tank; score coda HOLD')],'accent':'#e8878b'},
'G04':{'title':'FIRST PALM AT THE DRY STONE','subtitle':'Red Leopards vs Three Dreaded Snake','img':'06-first-choice.png','name':'Outer waterfall-jungle boundary','cue':'KEVIN CHECKS MUD → PHILLIP SETS FINISH → SOURCE-GATED WARDROBE','shots':[('THE APPROACH','Wet visitor-side jungle, two legible paths','Kevin checks footing after Week 10 storm'),('THE RULE','Phillip ONE body / THREE post-haircut heads','Raised comparatively dry stone; mud tracks'),('THE RESULT','First palm on stone before any celebration','Florida outfit only if Red officially wins')],'accent':'#94cc82'},
'G05':{'title':'THE ROAD THAT COMES BACK','subtitle':'Seven Deadly Chins vs Mud Dogs','img':'07-the-dry-paw.png','name':'Gators & Dawgs swamp sign','cue':'HIGH FLOODLINE → BOBBY LIES → BEN RECOGNIZES THE LOOP','shots':[('THE LANDMARK','Submerged rut; sign; empty stands LEFT','Bobby dry paw and Cancún card RIGHT'),('THE LIE','Bobby deliberately sends Ben into flooded ruts','Safe raised lip survives; no island road'),('THE REALIZATION','Ben returns to same sign / Bobby smirks','Losers Beach is fear, not verified arrival')],'accent':'#b9a977'},
'G06':{'title':'THE SECOND SHEET','subtitle':'The LLC vs Dr. Duckhook','img':'08-stay-for-coffee.png','name':'Country Club of Jackson • executive office','cue':'INVESTOR CONFIDENCE → BOARD ACTION → DAVID FURIOUS','shots':[('THE OFFER','Wet key returned | first paper unsigned','OUTSIDE storm, INSIDE dry and intact'),('THE NOTICE','Duckhook quietly spoke with LLC board','David removed CEO, Zach CEO AND chairman'),('THE FURY','Babb rises, pen hits desk; Zach steady','Babb keeps fantasy team; coffee is score-only')],'accent':'#aaa4e2'}
}
def t(x,y,s,size=25,color='#f4f4f5',weight=600,anchor='start'):
 return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" font-family="Helvetica Neue, Arial, sans-serif" text-anchor="{anchor}">{escape(str(s))}</text>'
def rect(x,y,w,h,fill,stroke='none',rx=0,sw=2,opacity=1):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{opacity}"/>'
def line(x1,y1,x2,y2,color='#e5e7eb',sw=4,dash=''):
 return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="{sw}" fill="none" stroke-linecap="round" '+(f'stroke-dasharray="{dash}"' if dash else '')+'/>'
def ellipse(cx,cy,rx,ry,fill,opacity=1,stroke='none',sw=3):
 return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" opacity="{opacity}" stroke="{stroke}" stroke-width="{sw}"/>'
def poly(points,fill,stroke='none',sw=2):
 return f'<polygon points="{points}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def circle(cx,cy,r,fill,stroke='none',sw=2):
 return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def scene_art(g,p):
 c=[]
 # all geometry is symbolic composition blocking only; color/spec documents are authority
 c.append(rect(0,0,520,455,'url(#panelBg)'))
 if g=='G01':
  c +=[rect(0,328,520,127,'#264e63'),rect(43,229,433,65,'#7e7b78','#b9b6ae',8,5),
       line(43,230,476,230,'#bbb6b0',6),line(43,296,476,296,'#d2c8b7',5),
       ellipse(133,215,39,16,'#111827'),circle(131,182,21,'#5a3935'),poly('115,201 155,203 142,253 113,252','#721f2d'),
       ellipse(338,202,58,30,'#1e293b'),circle(391,171,25,'#b78c67')]
  for x in [302,331,358,384]:c.append(line(x,224,x-4,273,'#1e293b',9))
  c +=[rect(62,190,59,39,'#b3a18a','#6b5847',5),circle(76,234,13,'#131e25'),circle(109,234,13,'#131e25'),
      line(17,160,63,142,'#c9dae4',5),line(24,181,84,163,'#c9dae4',4),line(418,120,483,101,'#c9dae4',5)]
  if p==2:c +=[line(326,275,350,285,'#f8d17b',9),ellipse(354,302,52,14,'#f8d17b',.35)]
  if p==3:c +=[ellipse(396,380,52,12,'#a3d4e6',.65),circle(405,360,13,'#b78c67'),line(376,290,404,340,'#ffb86b',6,'11,9')]
 elif g=='G02':
  c +=[poly('0,332 510,311 520,455 0,455','#78674b'),rect(60,154,185,105,'#9ca3af','#edf2f7',8,5),rect(75,174,60,40,'#263847'),
      rect(250,180,170,80,'#89827a','#c9beb6',4,4),line(257,187,404,187,'#e4d1a9',6),circle(108,270,31,'#1f2937'),circle(345,270,31,'#1f2937'),
      line(415,270,500,323,'#53b9cf',7),line(30,100,5,155,'#88d4e6',6),line(102,72,62,129,'#88d4e6',4)]
  for x in [294,339,386]:c.append(ellipse(x,202,18,30,'#c1a05a',.85))
  if p==2:c +=[ellipse(430,267,17,29,'#d4b16a'),ellipse(461,300,19,30,'#d4b16a'),line(420,217,450,272,'#ffd46e',4,'8,8')]
  if p==3:c +=[rect(60,150,100,20,'#e8d8c1'),circle(110,173,13,'#b68b78'),ellipse(451,347,33,8,'#d0b066',.7),line(265,290,426,290,'#f48f78',4,'10,8')]
 elif g=='G03':
  c +=[rect(65,90,389,310,'#34495e','#e5a0a1',7,6),rect(253,178,164,185,'#9c3c3d','#f7d9c3',5,5),rect(275,202,125,117,'#7a2328'),
       circle(131,221,28,'#ddb39e'),rect(112,245,46,103,'#6b4c3b'),circle(355,266,24,'#dda98e'),
       line(36,53,5,112,'#b2deed',5),line(197,58,156,134,'#b2deed',5),line(455,53,424,115,'#b2deed',5),
       rect(275,172,124,9,'#e3d3bd')]
  if p==1:c +=[rect(112,159,137,26,'#f3b8b7'),t(181,179,'OFF BOARD',17,'#271b23',800,'middle')]
  if p==2:c +=[circle(218,194,12,'#f3ebdc'),line(225,189,279,170,'#ffda82',5,'12,8'),line(377,169,402,147,'#eaeaea',4)]
  if p==3:c +=[line(416,220,467,194,'#e8d4cb',5),rect(420,196,10,166,'#e8d4cb'),circle(353,154,21,'#dda98e'),rect(338,177,32,140,'#9c3c3d')]
 elif g=='G04':
  c +=[rect(0,342,520,113,'#3d5941'),poly('0,350 150,320 275,349 520,305 520,455 0,455','#5a513a'),
       ellipse(320,332,75,22,'#b9b5a4'),ellipse(150,210,52,31,'#883a38'),circle(158,180,25,'#c68c7c'),
       ellipse(375,248,65,41,'#536b38')]
  for x,y in [(350,189),(383,178),(413,195)]:c +=[circle(x,y,27,'#6d8552'),circle(x+4,y-5,5,'#ffd98e')]
  for x in [35,70,448,483]:c +=[line(x,70,x-15,290,'#254e3d',12),ellipse(x,90,63,18,'#2f6c54',.9)]
  for x in [93,242,396]:c +=[line(x,58,x-28,140,'#afdae0',4)]
  if p==2:c +=[line(150,282,285,329,'#ffc781',5,'15,8'),line(380,282,324,329,'#ffc781',5,'15,8')]
  if p==3:c +=[ellipse(314,323,47,9,'#d6ccbc'),line(237,305,307,328,'#ffd58a',7)]
 elif g=='G05':
  c +=[rect(0,291,520,164,'#4c6a68'),rect(18,110,200,80,'#6d533f','#e8d1a7',4,6),
       t(120,159,'GATORS & DAWGS',20,'#f6e3b6',800,'middle'),line(35,190,35,350,'#554130',12),line(195,190,195,347,'#554130',12),
       rect(365,194,113,80,'#343b3e','#e2d7cc',7,5),rect(377,204,43,31,'#84959b'),circle(385,281,24,'#151d24'),circle(453,281,24,'#151d24'),
       ellipse(252,232,42,25,'#6c5942'),circle(272,204,18,'#c68f72'),poly('242,244 279,244 270,311 238,313','#535141')]
  if p==1:c +=[rect(210,100,104,65,'#b8b38e'),t(262,134,'CANCÚN',17,'#273b38',800,'middle'),line(300,145,318,278,'#f8d383',4)]
  if p==2:c +=[line(312,303,414,322,'#f3aa76',7,'15,7'),line(412,327,320,368,'#f3aa76',7,'15,7')]
  if p==3:c +=[rect(210,102,110,50,'#bfb190'),t(265,131,'CANCÚN',17,'#273b38',800,'middle'),line(210,340,366,344,'#cbbf99',4,'11,8')]
 elif g=='G06':
  c +=[rect(34,53,180,215,'#283a54','#e3d6ca',9,6),line(121,53,121,268,'#e3d6ca',4),
       line(36,146,215,146,'#e3d6ca',4),line(45,89,85,133,'#9ecce4',6),line(133,82,194,133,'#9ecce4',6),
       rect(65,314,397,34,'#806e61'),ellipse(139,276,36,29,'#302c36'),circle(137,227,26,'#d2a58b'),
       ellipse(383,278,36,29,'#322f3f'),circle(386,226,26,'#dab097'),rect(202,267,129,52,'#dad5d0')]
  if p==1:c +=[rect(220,274,100,39,'#faf9ed'),line(231,289,310,289,'#6d7177',3)]
  if p==2:c +=[rect(207,261,120,67,'#f2efe5','#f9bc84',2,3),t(269,288,'CEO',18,'#35363b',800,'middle'),t(268,309,'CHAIR',17,'#35363b',700,'middle')]
  if p==3:c +=[line(140,252,128,193,'#e8bdb0',12),line(165,310,198,282,'#f5b55d',8),line(206,312,242,312,'#ff6b6b',5)]
 return ''.join(c)
def wrap_lines(s,limit=45):
 words=s.split();out=[];cur=''
 for x in words:
  if len(cur)+len(x)+1>limit:out.append(cur);cur=x
  else:cur=(cur+' '+x).strip()
 if cur:out.append(cur)
 return out
files=[]
for g,s in stories.items():
 png=(pp/'board-png'/s['img']).read_bytes()
 encoded=base64.b64encode(png).decode('ascii')
 acc=s['accent']
 body=[]
 body.append('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="2560" height="1440" viewBox="0 0 2560 1440">')
 body.append('<defs><linearGradient id="bg" x2="0" y2="1"><stop stop-color="#131e2c"/><stop offset="1" stop-color="#0c121b"/></linearGradient><linearGradient id="panelBg" x2="0" y2="1"><stop stop-color="#344459"/><stop offset="1" stop-color="#1a2938"/></linearGradient></defs>')
 body.append(rect(0,0,2560,1440,'url(#bg)'))
 body.append(rect(0,0,2560,12,acc))
 body.append(t(70,85,'S C H E M I N’   2 6     /     W E E K  1 1',34,acc,700))
 body.append(t(70,155,s['title'],63,'#f8fafc',800))
 body.append(t(2480,94,g+'  •  SOURCE-BOUND CINEMATIC PREVIS',26,'#a9c3d3',700,'end'))
 body.append(t(73,199,s['subtitle'],29,'#cad5df',500))
 # reference image column
 body.append(rect(58,230,585,1054,'#1b2937','#5b7081',18,3))
 body.append(rect(75,245,550,976,'#090e15'))
 body.append(f'<image x="77" y="245" width="546" height="970" preserveAspectRatio="xMidYMid meet" xlink:href="data:image/png;base64,{encoded}"/>')
 body.append(rect(75,1160,550,61,'#09101d',rx=8,opacity=.88))
 body.append(t(92,1194,'REFERENCE · EXISTING WEEK 11 STUDY',25,acc,800))
 body.append(t(77,1261,s['name'],22,'#dbe3e9',500))
 # three sequential visual storyboard frames
 for i,(h,sub,desc) in enumerate(s['shots'],start=1):
  x=682+(i-1)*623
  body.append(rect(x,232,590,905,'#1a2635','#52697b',22,3))
  body.append(rect(x+14,247,562,67,'#30435a',rx=10))
  body.append(t(x+34,288,str(i).zfill(2)+'   '+h,28,acc,800))
  body.append(f'<svg x="{x+35}" y="330" width="518" height="495" viewBox="0 0 520 455">{scene_art(g,i)}</svg>')
  body.append(rect(x+35,842,520,2,acc))
  body.append(t(x+36,888,sub,23,'#eff3f8',700))
  for jj,line_text in enumerate(wrap_lines(desc,44)[:3]):body.append(t(x+36,945+jj*36,line_text,21,'#c5d1dc',500))
  body.append(t(x+33,1094,['SETUP','ACTION','EMOTIONAL / BRANCH'][i-1],19,acc,800))
  if i<3:
   body.append(poly(f'{x+597},640 {x+614},653 {x+597},666',acc))
 # bottom line
 body.append(rect(675,1167,1845,118,'#223247','#35495d',14,2))
 body.append(t(697,1206,'SEQUENCE / PRODUCTION DECISION',23,acc,800))
 body.append(t(697,1252,s['cue'],24,'#e4edf5',650))
 body.append(line(70,1340,2480,1340,'#415365',2))
 body.append(t(70,1388,'REFERENCE / BLOCKING / CAMERA ONLY • NO FINAL SCORE, RENDER APPROVAL OR CANON CHANGE',22,'#a8b7c6',600))
 body.append(t(2480,1388,'6–SCENE STUDIO STORYBOARD · 16:9',22,acc,600,'end'))
 body.append('</svg>')
 svg=''.join(body)
 svg_tmp=Path('/tmp')/f'{g.lower()}_previs_render.svg'
 svg_tmp.write_text(svg)
 output=out/f'W11-{g}-CINEMATIC-SHOTBOARD-PREVIS.png'
 run=subprocess.run(['rsvg-convert','-o',str(output),str(svg_tmp)],capture_output=True,text=True)
 if run.returncode:raise RuntimeError(str(output)+': '+run.stderr[:1400])
 if output.stat().st_size<50000:raise RuntimeError(str(output)+' unusually small')
 files.append({'scene':g,'file':str(output.relative_to(root)),'bytes':output.stat().st_size,'study_source':s['img'],'shots':[x[0] for x in s['shots']],'state':'CAMERA_PREVIS_ONLY'})
 print('CREATED',output.name,output.stat().st_size,flush=True)
(out/'W11_SIX_SCENE_PREVIS_MANIFEST.json').write_text(json.dumps({'schema':'schemin.w11.production_storyboard.v1','style':'16:9 studio shot-previs (not native 1080x1920 final folio)','sources':'Week11 original native studies and 35-folio spec','medium':'6 PNG storyboard sheets rendered from editable SVG generator; no fiction results decided','boards':files},indent=2)+'\n')
print('DONE',len(files),'total_MB',round(sum(x['bytes'] for x in files)/1024/1024,2),flush=True)
