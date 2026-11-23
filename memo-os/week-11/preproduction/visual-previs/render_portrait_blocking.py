from pathlib import Path
import json,hashlib,subprocess,xml.sax.saxutils as xml,re,urllib.request
ROOT=Path(__file__).resolve().parents[4]
P=ROOT/'memo-os/week-11/preproduction'
V=P/'visual-previs'
shot=json.loads((P/'W11_ALL_35_VISUAL_DIRECTOR_SHOT_SPECS_2026-11-23.json').read_text())
plan=json.loads((P/'W11_TLDRAW_SIX_STORYBOARD_IMPORT_PLAN_2026-11-23.json').read_text())
og=json.loads((P/'WEEK11_FOLIO_OG_COMPARISON.json').read_text())['folios']
by={r['folio']:r for r in og}
# 1080x1920 portrait framing normalized to 180x320. Each list defines source-specific
# foreground action, secondary actor/prop, structural reference and lettering safe zone.
# Diagrams deliberately contain no owner likeness or final game data.
# [label,x,y,w,h,color], all inside art area (0..180, 0..320)
D={
1:[('RIVAL',18,100,57,126,'blue'),('HERO',92,86,69,153,'orange'),('TITLE',15,15,150,45,'grey')],
2:[('REGISTER',13,125,154,110,'grey'),('SEAT',18,61,54,50,'blue'),('SEAT',108,61,54,50,'orange')],
3:[('LETTER',15,77,150,156,'grey'),('HAND',99,188,65,48,'orange'),('LAMP',121,30,34,46,'yellow')],
4:[('SCORE RAIL',14,52,152,160,'grey'),('OBSERVER',107,214,54,65,'blue')],
5:[('PORTRAITS',12,47,42,224,'blue'),('RANKS 1–6',63,47,105,224,'grey')],
6:[('PORTRAITS',12,47,42,224,'orange'),('RANKS 7–12',63,47,105,224,'grey')],
7:[('12 TEAM ROWS',15,48,150,222,'grey'),('7TH CUT',12,158,156,12,'yellow')],
8:[('ROAD A',12,52,156,88,'blue'),('ROAD B',12,153,156,102,'orange'),('TRAVEL',57,142,66,10,'yellow')],
9:[('WHEEL',5,191,70,81,'grey'),('4 HOOVES',88,70,82,166,'orange'),('BRIDGE',8,253,164,20,'blue')],
10:[('AUSTIN',7,82,65,170,'orange'),('WILSON',95,79,76,155,'blue'),('CARTER',83,48,36,43,'yellow')],
11:[('CARTER',9,40,61,102,'orange'),('PARAPET',10,145,160,25,'grey'),('SURVIVOR*',80,190,70,66,'blue')],
12:[('CAB / JORDAN',19,64,142,137,'orange'),('VISOR / SIX',22,26,123,32,'yellow'),('RADIO',116,211,45,52,'grey')],
13:[('TRAILER',8,81,161,83,'grey'),('2 KEGS',99,176,70,62,'orange'),('BRAKE / AXLE',11,185,78,65,'blue')],
14:[('HOUSE SHEET',14,54,152,53,'grey'),('BRANDON',19,127,63,112,'orange'),('JAKE',98,127,61,112,'blue')],
15:[('TARGET',10,63,46,52,'yellow'),('TANK / JAKE',75,89,93,154,'orange'),('BALL AXIS',20,126,50,12,'blue')],
16:[('BRANDON',12,89,60,144,'blue'),('LADDER / JAKE',95,62,75,183,'orange'),('BOOT',100,245,64,22,'grey')],
17:[('PHILLIP / 3',12,68,80,121,'blue'),('KEVIN',108,88,56,102,'orange'),('MUD / PATH',10,207,160,64,'grey')],
18:[('PHILLIP',12,75,72,115,'blue'),('KEVIN',108,80,60,113,'orange'),('DRY STONE',62,210,89,37,'yellow')],
19:[('BOBBY / PAW',9,164,66,82,'orange'),('BEN / CAB',92,74,79,158,'blue'),('SIGN / FLOOD',7,46,164,28,'grey')],
20:[('REPEATED SIGN',12,44,156,35,'grey'),('BEN / TRUCK',8,100,99,107,'blue'),('BOBBY / CARD',120,167,52,83,'orange')],
21:[('WINDOW / STORM',13,38,154,64,'blue'),('ZACH',105,119,60,94,'orange'),('GUEST / DESK',9,179,149,86,'grey')],
22:[('BAB B',10,56,68,144,'orange'),('ZACH',102,62,65,127,'blue'),('BOARD ACTION',17,205,145,65,'grey')],
23:[('WRITER',7,45,66,111,'orange'),('3 GAMES',79,55,90,196,'grey')],
24:[('3 GAMES',9,55,91,196,'grey'),('WRITER',108,47,66,110,'blue')],
25:[('RECEIPT A',16,58,148,82,'grey'),('RECEIPT B',16,157,148,82,'orange')],
26:[('STARTER',10,74,75,167,'blue'),('BENCH',95,74,75,167,'grey')],
27:[('ROSTER',11,54,158,192,'grey'),('WAIVER SLIP',21,141,136,48,'orange')],
28:[('BURGERS',14,53,152,57,'blue'),('PIZZA',14,125,152,57,'orange'),('WINGS',14,197,152,57,'yellow')],
29:[('SCORING INDEX',17,67,146,120,'grey'),('MOVEMENT',28,204,124,50,'orange')],
30:[('CHART',10,53,160,110,'blue'),('7 HONORS',14,176,152,71,'yellow'),('CLERK',116,27,52,48,'grey')],
31:[('JAKE',9,79,64,144,'blue'),('REPORTER',107,79,64,144,'orange'),('LAMP / CLIP',57,193,66,64,'grey')],
32:[('6 FIXTURES',15,47,150,200,'grey'),('VISITOR→HOST',14,255,152,23,'yellow')],
33:[('SITE A*',12,53,156,91,'blue'),('SITE B*',12,153,156,91,'orange')],
34:[('PHILLIP / 3',49,51,83,128,'blue'),('COUNTER',8,196,164,61,'orange'),('HOUSE LINES',10,16,160,27,'grey')],
35:[('LANDMARK',18,53,52,90,'grey'),('ROAD',65,133,90,126,'blue'),('HEADLIGHTS',95,206,62,32,'yellow')]
}
D[22][0]=('BABB',10,56,68,144,'orange')
assert set(D)==set(range(1,36))
palette={'orange':'#e5a35e','blue':'#669eb9','yellow':'#e0c478','grey':'#a3afb8'}
items=[]
base="https://github.com/jakekaloper-hub/schemin-26/blob/memo-v52rc-20261115-intake/memo-os/week-11/preproduction/"
for r in shot['folios']:
 n=int(r['id'][1:]);boxes=D[n]
 assert all(x>=0 and y>=0 and x+w<=180 and y+h<=284 for _,x,y,w,h,_ in boxes)
 items.append({'id':r['id'],'title':r['title'],'scene':r['story'],'lead':r['production_ownership']['lead']['discipline'],'camera':r['camera_and_composition'],'phone_test':r['phone_and_visual_quality'],'result_dependency':r['result_dependency'],'card_id':r['tldraw_card_id'],'review_id':r['tldraw_review_card_id'],'source':base+'OPEN_BOARD_PAGE_REHEARSAL.md#folio-'+r['id'][1:],'reference_study':r['study_path'],'reference_sha256':r['study_hash'],'boxes':boxes})
# Pin exact committed storyboard bytes. The old mutable URL remains in original import plan.
head='9125779051b3525d0863b1d71eda33dd2b68d94a'  # immutable audited image source revision
imports=[]
for obj in plan['items']:
 file=ROOT/obj['repository_path']; assert hashlib.sha256(file.read_bytes()).hexdigest()==obj['sha256']
 url=f'https://raw.githubusercontent.com/jakekaloper-hub/schemin-26/{head}/{obj["repository_path"]}'
 imports.append({'id':obj['target_shape_id'],'scene':obj['scene_id'],'url':url,'sha256':obj['sha256'],'bytes':obj['bytes'],'alt':obj['alt_text'],'folios':obj['folio_targets']})
data={'schema':'schemin.w11.editable-portrait-blocking.v1','page_id':plan['target_page'],'board_id':plan['board_id'],'source_commit':head,'folia':items,'gallery':imports,'scope':'SYMBOLIC_VISUAL_PREPRODUCTION_ONLY','live_status':'NOT_APPLIED_NO_RESPONSIVE_EDITOR'}
(V/'W11_EDITABLE_PORTRAIT_BLOCKING.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
# Create actual local PNG of exactly the proposed editable native geometry.
# Labels and guide colors convey staged actors/props; no fabricated final art or scores.
W,H=1835,2145
def T(x,y,t,sz=14,fill='#dce7e9',weight=400):return f'<text x="{x}" y="{y}" font-family="Helvetica Neue,Arial,sans-serif" font-size="{sz}" fill="{fill}" font-weight="{weight}">{xml.escape(str(t))}</text>'
def R(x,y,w,h,fill,stroke='none',sw=1,rx=0,opacity=1):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{opacity}"/>'
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',R(0,0,W,H,'#101b25'),T(38,52,"SCHEMIN’ 26 / WEEK 11",28,'#e0c478',700),T(38,92,'35 portrait camera-blocking compositions — production only',20,'#dce7e9',650),T(38,119,'Orange: principal action  |  Blue: opposing subject or depth  |  Grey: source prop or structure  |  Gold: critical cue  |  *: outcome-gated',13,'#aebcc5')]
for i,r in enumerate(items):
 col=i%7;row=i//7;x=38+col*253;y=153+row*393
 svg += [T(x,y,r['id']+' · '+r['scene'],15,'#e0c478',700),R(x,y+13,180,320,'#1f3040','#71869b',1,2)]
 for label,a,b,w,h,c in r['boxes']:
  svg.append(R(x+a,y+13+b,w,h,palette[c],rx=4,opacity=.92))
  # box labels tightly constrained to their own physical footprint
  fs=min(10.5,(w-8)/(max(1,len(label))*0.55))
  svg.append(T(x+a+4,y+13+b+min(16,h*.74),label,fs,'#13212c',700))
 # editorial lettering strip kept out of the scene
 svg += [R(x+8,y+297,164,28,'#12202e','#93a1ad',1,2),T(x+15,y+315,'LETTERING / SAFE',10,'#c6d2da',600)]
 title=r['title'];svg.append(T(x,y+350,title[:33],12.4,'#f2f5f7',650));svg.append(T(x,y+370,r['lead'].replace('_',' ').upper(),10.2,'#a0b6c7'))
svg += [T(38,H-28,'SOURCE-LINKED FRAMING DIAGRAMS · NOT FINAL 1080 × 1920 RASTERS · ALL SPORTS OUTCOMES REMAIN SOURCE-GATED',13,'#aebcc5',650),'</svg>']
sp=V/'W11_35_PORTRAIT_BLOCKING_PREVIEW.svg';sp.write_text('\n'.join(svg)+'\n')
png=V/'W11_35_PORTRAIT_BLOCKING_PREVIEW.png';subprocess.run(['rsvg-convert','-o',str(png),str(sp)],check=True)
print('CREATED 35 distinct portrait diagrams',png.stat().st_size,'bytes','and executable geometry JSON',len(items),'items')
