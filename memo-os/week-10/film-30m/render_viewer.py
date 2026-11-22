#!/usr/bin/env python3
"""Standalone, offline source-linked 186-panel storyboard contact-sheet viewer."""
from pathlib import Path
from html import escape
import json

HERE=Path(__file__).resolve().parent
board=json.loads((HERE/"film_storyboard_v1.json").read_text(encoding="utf-8"))
COLORS={"00_PROLOGUE":"#9192a7","01_RODEO":"#c89365","02_STORM":"#7099b8",
"03_WEATHER":"#85aabc","04_TEMPLE":"#b3b08b","05_SWAMP":"#93ad88",
"06_RESULTS":"#b7a58b","07_BIRTHDAY":"#e2b27f","08_THRONE":"#a0b1d5",
"09_AFTERSHOCK":"#b3b8b8"}
LABELS={"00_PROLOGUE":"Opening / The Record","01_RODEO":"The Highland Rodeo",
"02_STORM":"The Storm","03_WEATHER":"The Roads Between","04_TEMPLE":"The Temple",
"05_SWAMP":"The Swamp","06_RESULTS":"Public Consequences","07_BIRTHDAY":"The Birthday",
"08_THRONE":"The Field Throne","09_AFTERSHOCK":"The Next Crossing"}

def e(text):
    return escape(str(text or ""),quote=True)

def schematic(s,sh):
    a=s["act"]; col=COLORS[a]
    if a=="01_RODEO":
        shapes='<ellipse cx="330" cy="173" rx="155" ry="44" fill="none" stroke="#e4c7a5" stroke-width="3"/><path d="M264 173v-33l18-17 20 17v33m-38 0-19 28m37-28-4 29m19-29 8 27m-4-27 22 27m0-56q55-61 82 0" stroke="#e2cda8" stroke-width="4" fill="none"/><rect x="460" y="102" width="65" height="95" stroke="#b9a07a" stroke-width="3" stroke-dasharray="5 4" fill="none"/>'
    elif a=="02_STORM":
        shapes='<path d="M0 180q90-25 150 0t170 0t230 0" stroke="#add1e4" fill="none" stroke-width="6"/><path d="M340 197v-113m0 16-44 44m44-42 54 40" stroke="#b7c1ad" stroke-width="8"/><path d="M370 155l-54 52" stroke="#d5c7b2" stroke-width="5"/><path d="M80 196v-73h65v73" fill="none" stroke="#d4c2a4" stroke-width="4"/>'
    elif a=="04_TEMPLE":
        shapes='<path d="M250 35v135h270" stroke="#d0cead" fill="none" stroke-width="7"/><circle cx="350" cy="122" r="16" fill="#9da38d"/><circle cx="383" cy="118" r="16" fill="#9da38d"/><circle cx="416" cy="121" r="16" fill="#9da38d"/><path d="M383 135v48" stroke="#9da38d" stroke-width="19"/><path d="M100 210l27-70 31 70m-32-50V96" stroke="#d6ae87" stroke-width="7" fill="none"/>'
    elif a=="05_SWAMP":
        shapes='<path d="M0 220h550" stroke="#aec1a1" stroke-width="8"/><rect x="235" y="135" width="155" height="48" stroke="#ded0aa" fill="#23302f" stroke-width="4"/><rect x="389" y="145" width="53" height="38" stroke="#ded0aa" fill="#23302f" stroke-width="4"/><circle cx="268" cy="190" r="14" stroke="#ded0aa" fill="#152128" stroke-width="4"/><circle cx="410" cy="190" r="14" stroke="#ded0aa" fill="#152128" stroke-width="4"/><path d="M115 187v-43l-20-17m20 17 25-18m-25 62-20 28m21-28 25 25" stroke="#cad6ba" stroke-width="6" fill="none"/>'
    elif a=="07_BIRTHDAY":
        shapes='<path d="M90 221h370" stroke="#c69a73" stroke-width="9"/><rect x="275" y="148" width="120" height="62" fill="#5c4540" stroke="#e3bf91" stroke-width="4"/><path d="M335 148v62m-60-34h120" stroke="#f3dfb7" stroke-width="8"/><path d="M335 148q-45-35-44 0m44 0q42-35 44 0" stroke="#f3dfb7" stroke-width="4" fill="none"/>'
    elif a=="08_THRONE":
        shapes='<path d="M10 229l190-99 280 99" stroke="#b6bdcf" stroke-width="7" fill="none"/><path d="M355 196v-87l-34-19-34 19v87M280 200h92" stroke="#d7cba7" stroke-width="8" fill="none"/><path d="M172 34l-43 82 26-6-32 75" stroke="#bad9fc" stroke-width="9" fill="none"/>'
    elif a in ("03_WEATHER","09_AFTERSHOCK"):
        shapes='<path d="M10 221h530M73 219q90-150 182 0M255 219q96-150 200 0" stroke="#b5b8b8" stroke-width="10" fill="none"/><path d="M0 236q90-24 177 0t180 0t195 0" stroke="#89bdd0" stroke-width="5" fill="none"/>'
    else:
        shapes='<rect x="125" y="72" width="310" height="151" fill="#13212c" stroke="#c2baaa" stroke-width="4"/><path d="M155 117h250m-250 35h250m-250 35h250" stroke="#758da0" stroke-width="4"/>'
    label=sh["source_kind"].upper()
    return ('<div class="frame"><svg viewBox="0 0 550 300" role="img" aria-label="Conceptual blocking schematic, not generated frame">'
        '<rect width="550" height="300" fill="#14202b"/>'
        '<path d="M0 140q120-95 250 0t300-5v165H0z" fill="'+col+'" opacity=".16"/>'
        '<path d="M0 207L140 150 260 200 365 137 550 194" stroke="'+col+'" stroke-width="3" fill="none" opacity=".55"/>'
        '<path d="M28 28h40m-40 0v34m496-34h-40m40 0v34M28 273h40m-40 0v-34m496 34h-40m40 0v-34" stroke="#b0b6b9" stroke-width="2" fill="none"/>'
        +shapes+'<text x="24" y="286" fill="#e8ddc4" font-family="monospace" font-size="13">'+e(sh["id"])+' '+e(sh["start"])+'</text>'
        '</svg><b>'+label+' / LAYOUT SCHEMATIC</b></div>')

css="""
:root{color-scheme:dark;--bg:#0b111a;--card:#182431;--edge:#41505f;--warm:#ebc583;--text:#f0eee7;--muted:#aebcc8}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:var(--text);background:radial-gradient(ellipse at 80% -10%,#27394b,transparent 55%),var(--bg);font:14px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
a{color:var(--warm)}a:hover{text-decoration:none}h1,h2,h3{font-family:Georgia,serif}h1{font-size:clamp(32px,4vw,54px);margin:12px 0;line-height:1.1}h2{font-size:30px;margin:0 0 8px}
.top{padding:26px max(25px,calc((100vw - 1460px)/2));background:#101720;border-bottom:1px solid var(--edge)}
.kicker{color:var(--warm);font-weight:800;letter-spacing:.16em;text-transform:uppercase;font-size:11px}.muted{color:var(--muted)}
.lead{max-width:850px;margin:14px 0 24px;color:#becad3}
.chips{display:flex;gap:9px;flex-wrap:wrap}.chip{padding:7px 12px;border:1px solid #6a736e;border-radius:25px;background:#1f2b36;font-size:12px}
.counts{display:flex;gap:25px;flex-wrap:wrap;margin:26px 0}.count strong{font:650 29px Georgia,serif;display:block}.count span{color:#acb8bf;letter-spacing:.11em;text-transform:uppercase;font-size:10px}
body>main{max-width:1490px;padding:22px 25px 65px;margin:auto}.timeline{display:flex;height:17px;overflow:hidden;border-radius:9px;border:1px solid #617080;margin:15px 0 8px}.timeline a{display:block;border-right:1px solid #08111a}
.tlegend{display:flex;gap:12px;flex-wrap:wrap;margin:12px 0 25px}.tlegend a{font-size:11px;text-decoration:none;padding:6px 9px;border:1px solid #405165;border-radius:15px}
.explain{margin:15px 0 25px;padding:14px 18px;background:#1b2632;border:1px solid #425463;border-radius:9px}
.index{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:26px}.index a{padding:6px 10px;text-decoration:none;background:#1b2834;border:1px solid #374c59;border-radius:5px;font-size:12px}
.scene{border:1px solid #4c5c69;border-radius:12px;background:linear-gradient(125deg,#1b2935,#121c26);margin:17px 0;scroll-margin-top:20px}
.scene>summary{cursor:pointer;padding:21px 23px;list-style:none;display:flex;justify-content:space-between;gap:15px;align-items:center}
.scene>summary::-webkit-details-marker{display:none}.scene>summary:before{content:"+";color:var(--warm);font-size:26px;margin-right:8px}.scene[open]>summary:before{content:"−"}
.scene>summary .headtitle{flex:1}.scene>summary p{margin:2px 0;color:#acb7c1}.scene>summary h2{margin:1px 0 3px}
.scene>summary .tc{font:650 20px Georgia,serif;text-align:right;white-space:nowrap}
.inside{padding:0 23px 24px}.cols{display:grid;grid-template-columns:3fr 2fr;gap:15px;margin:0 0 16px}
@media(max-width:920px){.cols{grid-template-columns:1fr}.scene>summary .tc{font-size:15px}}
.panel{background:#101a25;border:1px solid #3d5060;border-radius:8px;padding:16px}
.panel h3{font:800 11px system-ui;letter-spacing:.14em;text-transform:uppercase;color:#e7bf86;margin:0 0 10px}
.panel p{margin:4px 0 10px}.copy{font:15px/1.7 Georgia,serif;white-space:pre-wrap}
.refs{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}.ref{width:96px;border:1px solid #435565;background:#12202b;border-radius:4px;overflow:hidden}.ref img{height:90px;width:100%;object-fit:contain}.ref span{display:block;font-size:9px;color:#b2c0ca;padding:4px;word-break:break-word}
.shots{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:12px}
.shot{border:1px solid #4b5d67;background:#172431;border-radius:8px;overflow:hidden}.shot-head{padding:9px 12px;display:flex;justify-content:space-between;color:#f2ddaf}
.frame{position:relative;aspect-ratio:16/9;border-block:1px solid #334554}.frame svg{width:100%;height:100%}.frame b{font:700 9px system-ui;position:absolute;left:8px;top:8px;padding:4px 7px;background:#0d1729db;color:#edddb7;letter-spacing:.08em}
.shot p{margin:7px 12px;font-size:12px}.shot p:last-child{margin-bottom:13px}.shot small{color:#98a8b6}
.stat{border-top:1px solid #344453;padding-top:10px;margin-top:10px;color:#c4cfce}footer{padding:28px;color:#97aab9;border-top:1px solid #41515c}
"""
parts=['<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Schemin 26 / Week 10 Film Storyboard</title><style>',css,
'</style></head><body><header class="top"><div class="kicker">Schemin ’26 / Memo OS / Film Department</div>',
'<h1>WEEK 10<br>The Commonwealth Cut</h1>',
'<p class="lead">A source-governed 30-minute motion-picture storyboard adapted from all 34 existing Week 10 folios. Expand any scene to inspect its camera coverage, pacing, geographical locks, reference assets and sound cues. Each illustrated frame is a <strong>blocking schematic, not a completed generated shot</strong>.</p>',
'<div class="chips"><span class="chip">CANDIDATE · NO ART APPROVAL</span><span class="chip">18 DIRECTORS REMAIN CANONICAL</span><span class="chip">12 SPECIALISTS = METHOD LENSES ONLY</span></div>',
'<div class="counts"><div class="count"><strong>30:00</strong><span>Exact timeline</span></div><div class="count"><strong>34</strong><span>Source folios</span></div>',
'<div class="count"><strong>'+str(board["runtime"]["shot_count"])+'</strong><span>Boarded shots</span></div><div class="count"><strong>6</strong><span>Matchups</span></div></div></header><main>',
'<div class="timeline">']
for act,seconds in board["runtime"]["seconds_by_act"].items():
    parts.append('<a title="'+e(LABELS[act])+' · '+str(seconds)+' seconds" href="#'+e(act)+'" style="width:'+f"{seconds/1800*100:.4f}"+'%;background:'+COLORS[act]+'"></a>')
parts+=['</div><div class="tlegend">']
for act,seconds in board["runtime"]["seconds_by_act"].items():
    parts.append('<a href="#'+e(act)+'">'+e(LABELS[act])+' · '+str(round(seconds/60,1))+' min</a>')
parts+=['</div><div class="explain"><strong>Open a scene to view its shot panels.</strong> Camera angles and blocking are source-anchored; original shot IDs are retained. Image slots point to canon/character reference art when those assets exist in the same local checkout. These are reference images, not generated storyboard frames. Proposed 16:9 film framing does not alter the original 9:16 memo masters.</div><div class="index">']
for scene in board["scenes"]:
    parts.append('<a href="#'+e(scene["id"])+'">'+str(scene["order"]).zfill(2)+' · '+e(scene["folio"])+'</a>')
parts+=['</div>']
prev=None
for s in board["scenes"]:
    if s["act"]!=prev:
        parts.append('<h2 class="kicker" id="'+e(s["act"])+'" style="margin-top:35px">'+e(LABELS[s["act"]])+'</h2>')
    prev=s["act"]
    parts.append('<details class="scene" id="'+e(s["id"])+'"'+(' open' if s["order"]==1 else '')+'><summary><div class="headtitle"><div class="kicker">'+e(s["folio"])+' · SCENE '+str(s["order"]).zfill(2)+'</div><h2>'+e(s["title"])+'</h2><p>'+e(" × ".join(s["characters"]) or "Commonwealth intelligence / editorial")+' · '+str(s["board_shot_count"])+' shots</p></div><div class="tc">'+e(s["start"])+' → '+e(s["end"])+'<div style="font:11px system-ui;color:#b6c6cf">'+str(s["duration_s"])+' seconds</div></div></summary><div class="inside"><div class="cols"><div class="panel"><h3>Source narration and scene premise</h3><p class="copy">'+e(s["publication_copy"].get("body",""))+'</p><p><a href="https://github.com/jakekaloper-hub/schemin-26/blob/memo-week10-preproduction-20261116/'+e(s["source_request"])+'">Controlling source packet</a></p></div><div class="panel"><h3>Audio and physical production</h3><p><b>Ambience:</b> '+e(s["sound"]["ambience"])+'</p><p><b>Score:</b> '+e(s["sound"]["original_music_brief"])+'</p><p><b>Foley:</b> '+e(s["sound"]["foley"])+'</p><p><b>Time logic:</b> '+e(s["time_logic"])+'</p><p><b>Scene exit:</b> '+e(s["transition"])+'</p><h3>Reference images / not story frames</h3><div class="refs">')
    if s["reference_images"]:
        for ref in s["reference_images"][:4]:
            parts.append('<div class="ref"><img loading="lazy" src="../../../'+e(ref["path"])+'" alt="Original reference image only"><span>'+e(ref.get("character_id") or ref.get("role") or "Source")+'</span></div>')
    else: parts.append('<small>No direct character portrait required for this source page.</small>')
    parts.append('</div><p class="muted">'+str(s["narration_words"])+' source words · '+str(s["narration_at_145wpm_s"])+' seconds at 145 wpm. Dialogue/ADR not locked.</p></div></div><div class="kicker" style="margin:18px 0 11px">Sequential shot cards · editorial coverage</div><div class="shots">')
    for sh in s["shots"]:
        parts.append('<article class="shot"><div class="shot-head"><b>'+e(sh["id"])+'</b><span>'+e(sh["start"][3:])+'–'+e(sh["end"][3:])+' · '+str(sh["duration_s"])+'s</span></div>'+schematic(s,sh)+'<p><b>Camera:</b> '+e(sh["camera"])+'</p><p><b>Blocking:</b> '+e(sh["blocking"])+'</p><p><b>Dramatic purpose:</b> '+e(sh["dramatic_purpose"])+'</p><p><b>Movement:</b> '+e(sh["movement"])+'</p><p class="stat"><small>Source: '+e(sh["source_beat_id"])+' · '+e(sh["recommended_capture"])+'</small></p></article>')
    parts.append('</div><div class="panel" style="margin-top:16px"><h3>Continuity and vetoes</h3><p><b>Do not alter:</b> '+e(" · ".join(s["forbidden_mutations"]) or "All source-canon boundaries")+'</p><p><b>End state:</b> '+e(" · ".join(s["continuity_out"]))+'</p><p><b>Stage:</b> STAGED BOARD ONLY. Independently verify faces, geography, sound, rights and release before filming.</p></div></div></details>')
parts.append('</main><footer>Source branch: memo-week10-preproduction-20261116 · 34 original folios preserved. The twelve named real production specialists and eight Inklings authors are published-method reference lenses, not personal participants. This board claims no release approval or generated footage.</footer></body></html>')
(HERE/"storyboard_viewer.html").write_text("".join(parts),encoding="utf-8")
print("viewer:",(HERE/"storyboard_viewer.html").stat().st_size,"bytes; scenes",len(board["scenes"]),"shots",board["runtime"]["shot_count"])
