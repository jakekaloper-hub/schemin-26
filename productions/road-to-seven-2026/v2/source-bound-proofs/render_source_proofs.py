import os,json,base64,html,pathlib,subprocess
R=pathlib.Path("/tmp/road7-audit-checkout-20261118")
B=R/"productions/road-to-seven-2026"
O=B/"v2/source-bound-proofs"
O.mkdir(parents=True,exist_ok=True)
names=["Slob on my Dobb","El Niño","D0nkey K0ng","His Majesty's Blood","Dr. Duckhook","Seven Deadly Chins","Red Leopards","The Chili Cheesers","The LLC","ObiWan Jacoby","Three Dreaded Snake","Mud Dogs"]
ids=["CHAR-JORDAN-HOLLINGSHEAD","CHAR-MANNING-WELTY","CHAR-WILSON-LOOK","CHAR-AUSTIN-BYARS","CHAR-ZACH-WILSON","CHAR-BEN-WHIPPLE","CHAR-KEVIN-ZEEK","CHAR-BRANDON-PRYOR","CHAR-DAVID-BABB","CHAR-JAKE-KALOPER","CHAR-PHILLIP-PITTS","CHAR-BOBBY-MITCHELL"]
titles=["THE SUMMIT","THE PURSUIT","THE THRESHOLD","THE CUT LINE","THE WAR LEDGER","THE LAST FOUR STEPS"]
sub=["NOT YET CLINCHED","THE DIVISION IS THE KEY","THE FIRST ELIMINATION IS POSSIBLE","SEVENTH PLACE IS NOT PERMANENT","EIGHT WINS IS NOT CERTAINTY","ALL TWELVE REMAIN ALIVE"]
accent=["#83c2d4","#d8ad67","#9cb78f","#de7262","#c3a7db","#9cbb9c"]
def img(i):
 p=R/"canon/characters/assets/lineups/2026-10-18-crops"/(ids[i]+".png")
 return "data:image/png;base64,"+base64.b64encode(p.read_bytes()).decode()
imgs=[img(i) for i in range(12)]
# Chili October22 visual lock: published Week10 action is more current than the generic Oct18 crop.
imgs[7]="data:image/png;base64,"+base64.b64encode((B/"v2/source-bound-proofs/reference/CHILI_W10_ACTION_CROP.png").read_bytes()).decode()
def E(x):return html.escape(str(x),quote=True)
css="""
*{box-sizing:border-box}html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#07131c;color:#f1e4cf;font-family:Georgia,serif}
.sheet{width:1080px;height:1920px;position:relative;padding:55px;background:radial-gradient(ellipse 850px 1100px at 55% 25%,#264352,#07131c 73%)}
.top{height:230px;border-bottom:2px solid #b0a48d;position:relative}
.eyebrow{font:700 18px Arial;letter-spacing:4px;color:#afbfc4}
.top h1{font:700 83px Georgia;color:#fff2cf;margin:23px 0 5px;letter-spacing:-2px}
.top h2{font:700 18px Arial;color:var(--accent);letter-spacing:4px;margin:0}
.pageno{position:absolute;right:0;top:0;font:700 58px Georgia;color:var(--accent)}
.twopov{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:22px;height:1510px}
.pov{position:relative;min-width:0}
.art{position:relative;height:670px;overflow:hidden;background:radial-gradient(ellipse,#244453,#091821 75%);border-top:4px solid var(--accent);border-bottom:1px solid #95aea6}
.art img{width:100%;height:630px;object-fit:contain}
.identity{position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,#05131d 31%);padding:22px 12px 12px;display:flex;gap:10px;align-items:end}
.identity b{font:700 47px Georgia;color:var(--accent)}.identity span{font:700 26px Georgia;color:white;line-height:1}.identity small{display:block;font:700 14px Arial;color:#b3cecf;margin-top:8px;letter-spacing:1.5px}
.outlook{margin:18px 0;display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #859d96;padding:6px 3px 15px}
.outlook small{font:700 16px Arial;letter-spacing:2px;color:#bdccd0}.outlook strong{font:700 58px Georgia;color:var(--accent)}
.branches{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.branches div{background:#19323c;padding:17px 6px;text-align:center;border-top:3px solid #6e999e}
.branches small{font:700 15px Arial;color:#a6c5c8}.branches strong{display:block;font:700 31px Georgia;color:#fff}
.note{margin-top:19px;padding:16px;background:#0e232e;border-left:5px solid var(--accent);font:700 22px/1.35 Georgia}
.note b{display:block;color:var(--accent);font:700 17px Arial;letter-spacing:2px;margin-bottom:7px}
.body{font:25px/1.31 Georgia;color:#e4e6e0;margin-top:16px}
.fork{font:700 18px Arial;color:var(--accent);margin-top:16px;line-height:1.3}
.foot{display:flex;justify-content:space-between;border-top:1px solid #829a9a;padding-top:17px;font:700 15px Arial;color:#aabfc2;letter-spacing:1px}
.sheet.pursuit .pov:first-child .art{clip-path:polygon(0 0,100% 0,93% 100%,0 100%);height:710px}
.sheet.threshold .pov:last-child .art{transform:translateY(33px)}
.sheet.cut .pov:first-child .art{transform:rotate(-2deg)}
.sheet.cut .pov:last-child .art{transform:rotate(2deg)}
.sheet.ledger .pov:first-child .art{height:710px}
.sheet.last .pov:last-child .art{transform:translateY(30px)}
.cover{padding:60px;background:radial-gradient(circle at 50% 2%,#31546b,#0c1924 70%)}
.cover h1{font:700 112px/1 Georgia;margin:45px 0 17px;color:#fff1ca}
.cover h1 i{color:#e6be7e}
.cover h2{font:700 22px Arial;letter-spacing:3px;color:#c8d4ce}
.cover .statistics{display:flex;justify-content:space-around;margin:35px 0;border-block:2px solid #bcab84;padding:25px}
.cover .statistics b{font:700 64px Georgia;color:#eacb94}
.cover .statistics span{display:block;font:700 16px Arial;letter-spacing:2px;color:#d0d7d4}
.list{display:grid;grid-template-columns:1fr 1fr;gap:12px 14px}
.rank{display:flex;align-items:center;gap:12px;height:177px;background:#16313d;border:1px solid #718e96;padding:10px}
.rank img{height:140px;width:105px;object-fit:contain}
.rank .seed{font:700 37px Georgia;color:#ddbd83}
.rank div{flex:1;font:700 21px Georgia;color:white}
.rank div small{display:block;font:700 14px Arial;color:#abd0d0;margin-top:10px}
.rank strong{font:700 28px Georgia;color:#f4dbb7}
.cover-end{font:700 20px/1.7 Arial;letter-spacing:1px;color:#e2d3b7;text-align:center;margin-top:30px}
.runway{position:absolute;left:55px;right:55px;bottom:102px;height:175px;background:#071b26ee;border-top:2px solid var(--accent);border-bottom:1px solid #8e9c8a;padding:9px 13px;z-index:3}
.runlabel{font:700 15px Arial;letter-spacing:2px;color:var(--accent);margin-bottom:7px}
.runrow{display:flex;align-items:center;height:51px;border-top:1px solid #45616c52}
.runrow>strong{font:700 18px Georgia;color:#f3dfb7;width:190px;white-space:nowrap}
.runweeks{display:grid;grid-template-columns:repeat(4,1fr);flex:1;gap:8px}
.runweeks div{font:700 15px Arial;white-space:nowrap;color:white;overflow:hidden}
.runweeks small{color:var(--accent);padding-right:8px}
.exact{font:700 16px Arial;color:#f1c7a6;letter-spacing:.6px;text-align:center;border-top:1px solid #45616c52;padding-top:5px}

"""
def item(t):
 i=t["seed"]-1
 return '<div class="rank"><span class="seed">{:02d}</span><img src="{}"><div>{}<small>{}</small></div><strong>{:.2f}%</strong></div>'.format(t['seed'],imgs[i],E(t['team']),E(t['record']),t['baseline'])
SCHEDULE=[
["El Niño","Chili","Duckhook","Red"],
["Slob","Chins","HMB","LLC"],
["HMB","ObiWan","Snake","Mud"],
["DK","LLC","Niño","Chins"],
["LLC","Red","Slob","Chili"],
["Mud","Niño","LLC","HMB"],
["Snake","Duckhook","Chili","Slob"],
["ObiWan","Slob","Red","Duckhook"],
["Duckhook","HMB","Chins","Niño"],
["Chili","DK","Mud","Snake"],
["Red","Mud","DK","ObiWan"],
["Chins","Snake","ObiWan","DK"]
]
EXACT=[
"9 WINS GUARANTEES ENTRY. THE SUMMIT IS NOT CLINCHED.",
"DK W12 OVER OBIWAN + W13 OVER SNAKE GUARANTEES BURGERS.",
"CHINS CAN ELIMINATE MUD IN WEEK 11; DUCKHOOK FACES THREE REMATCHES.",
"SEED SEVEN CAN CHANGE HANDS. CHILI AND RED MEET IN WEEK 13.",
"A VENDOR 100% SAMPLE IS NOT AN EXACT EIGHT-WIN GUARANTEE.",
"MUD MUST WIN ALL FOUR. SNAKE IS NOT ELIMINATED BY A WEEK 11 LOSS."
]
def runway(idx):
  a=2*idx
  parts=[]
  for i in (a,a+1):
    cells="".join("<div><small>W{}</small><b>{}</b></div>".format(j+11,E(n)) for j,n in enumerate(SCHEDULE[i]))
    parts.append('<div class="runrow"><strong>{}</strong><div class="runweeks">{}</div></div>'.format(E(names[i]),cells))
  return '<aside class="runway"><div class="runlabel">THE FOUR-WEEK RUNWAY · SCHEDULE IS NOT OUTCOME</div>{}<div class="exact">{}</div></aside>'.format("".join(parts),E(EXACT[idx]))
def page1():
 odds=json.loads((B/"evidence/FFHUB_LIVE_W11_2026-11-18_SUMMARY.json").read_text())
 return '<div class="sheet cover"><div class="eyebrow">SCHEMIN COMMONWEALTH · A STANDALONE PLAYOFF SPECIAL</div><h1>THE ROAD<br>TO <i>SEVEN</i></h1><h2>THE POSTSEASON BEGINS BEFORE THE PLAYOFFS.</h2><div class="statistics"><div><b>12</b><span>ALIVE</span></div><div><b>7</b><span>BERTHS</span></div><div><b>4</b><span>WEEKS</span></div></div><div class="list">'+''.join(item(dict(team=n,seed=i+1,record=["6–4"]*6+["5–5"]*2+["4–6"]*3+["2–8"])[i] if False else dict(team=n,seed=i+1,record=(["6–4"]*6+["5–5"]*2+["4–6"]*3+["2–8"])[i],baseline=next(x["baseline_pct"] for x in odds["teams"] if x["team"]==n))) for i,n in enumerate(names))+'</div><div class="cover-end">6 TEAMS AT 6–4 · 2 AT 5–5 · 3 AT 4–6 · MUD 2–8<br>EVERYONE ALIVE · NOBODY CLINCHED · FFHUB 18 NOV 2026</div></div>'
def pov(o):
 i=o["seed"]-1
 f=o["future_fork"]
 return '<article class="pov"><div class="art"><img src="{}"><div class="identity"><b>{:02d}</b><span>{}<small>{}</small></span></div></div><div class="outlook"><small>PLAYOFF OUTLOOK</small><strong>{}</strong></div><div class="branches"><div><small>W11 WIN</small><strong>{}</strong></div><div><small>W11 LOSS</small><strong>{}</strong></div></div><div class="note"><b>THE NEXT TEST</b>W11 vs {}</div><div class="body">{}</div><div class="fork">FUTURE HINGE: W{} vs {} · IF WIN {} · IF LOSS {}</div></article>'.format(imgs[i],o["seed"],E(o["team"]),E(o["record"]),o["playoff_probability"],o["if_w11_win"],o["if_w11_loss"],E(o["team"] if False else next(x["week11_opponent"] for x in json.loads((B/"evidence/FFHUB_LIVE_W11_2026-11-18_SUMMARY.json").read_text())["teams"] if x["team"]==o["team"])),E(o["narrative_body"]),f["week"],E(f["opponent"]),f["if_win"],f["if_loss"])
def inner(i):
 d=json.loads((B/"folios"/("RT7-P{:02d}".format(i))/"RENDER_INPUT.json").read_text())
 idx=i-2
 return '<div class="sheet {}" style="--accent:{}"><div class="top"><div class="eyebrow">THE ROAD TO SEVEN / THE FINAL FOUR REGULAR-SEASON WEEKS</div><div class="pageno">{:02d}<small>/07</small></div><h1>{}</h1><h2>{}</h2></div><div class="twopov">{}{}</div>{}<div class="foot"><span>OFFICIAL SEEDS AND RECORDS AFTER WEEK 10</span><span>FFHUB · 10,000 SAMPLES · 18 NOV</span></div></div>'.format(['summit','pursuit','threshold','cut','ledger','last'][idx],accent[idx],i,E(titles[idx]),E(sub[idx]),pov(d["overlays"][0]),pov(d["overlays"][1]),runway(idx))
for i in range(1,8):
 body=page1() if i==1 else inner(i)
 (O/"RT7-P{:02d}.html".format(i)).write_text('<!DOCTYPE html><html><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+body+'</body></html>')
node="""
const fs=require('fs'),puppeteer=require('/Users/jakekaloper/.npm/_npx/4b4c857f6efdfb61/node_modules/puppeteer');
(async()=>{let b;try{b=await puppeteer.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--no-first-run','--disable-extensions','--disable-gpu']});
let p=await b.newPage();await p.setViewport({width:1080,height:1920,deviceScaleFactor:1});
for(let i=1;i<=7;i++){let n='RT7-P'+String(i).padStart(2,'0');await p.goto('file://'+process.argv[2]+'/'+n+'.html',{waitUntil:'load'});await p.screenshot({path:process.argv[2]+'/'+n+'-SOURCE-PROOF.png',type:'png',captureBeyondViewport:false});console.log(n,fs.statSync(process.argv[2]+'/'+n+'-SOURCE-PROOF.png').size)}}finally{if(b)await b.close()}})().catch(e=>{console.error(e.stack);process.exitCode=1});
"""
(O/"render.js").write_text(node)
p=subprocess.run(["node",str(O/"render.js"),str(O)],capture_output=True,text=True,timeout=140)
print("RESULT",p.returncode,p.stdout,p.stderr)
assert p.returncode==0
