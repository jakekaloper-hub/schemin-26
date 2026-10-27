#!/usr/bin/env python3
from pathlib import Path
import json, html, re
root=Path(__file__).resolve().parents[2]
out=root/'docs/visual'
groups={
'Executive Observatory':[('North Star','SCHEMIN_26_PROJECT_MISSION.md'),('Project Controls','PROJECT_CONTROL_REGISTRY.md'),('Architecture','docs/architecture/REPOSITORY_ARCHITECTURE_V2.md'),('Execution Registry','governance/execution-control/TASK_REGISTRY_V1.json')],
'Bullpen & Engineering':[('Bullpen Adapter','docs/architecture/BULLPEN_COMMAND_ADAPTER_V2.md'),('System Contracts','governance/SCHEMIN_OS_CONTRACT_MAP_V1.md'),('Production Charter','docs/production/EXTERNAL_AI_PRODUCTION_CHARTER.md'),('FLA Integration','docs/architecture/FLA_INTEGRATION.md')],
'Living Commonwealth':[('World Engine','world/SCHEMIN_WORLD_ENGINE_V1_1_RELEASE_RECEIPT.md'),('Atlas','world/atlas/ATLAS_V1.md'),('Character Canon','canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md'),('Interactive Atlas','world/atlas/interactive/_INDEX.md')],
'Creative Production Studio':[('Memo OS','memo-os/_INDEX.md'),('Publication Manifest','governance/publication-manifest/PUBLICATION_MANIFEST_V1.json'),('Living Novel','living-novel/NOVEL_OS.md'),('Cinematography','memo-os/cinematography/FRANK_MASI_INTEGRATION_EXECUTION_AUDIT_2026_10_21.md')],
'League & Intelligence':[('ESPN Gateway','data-gateway/SCHEMIN_26_ESPN_INGESTION_RELIABILITY_PATCH_v1.0.md'),('Data Freshness','schemas/freshness.schema.json'),('Mercer','mercer/OPERATING_CONTRACT.md'),('League Identity','README.md')],
'Governance & Knowledge':[('Source of Truth','docs/governance/SOURCE_OF_TRUTH.md'),('Release Evidence','governance/release-evidence/registry.json'),('Publication Governance','governance/publication-manifest/_INDEX.md'),('Visual Approval','canon/characters/APPROVED_LINEUP_2026_10_18.json')]
}
# Existing substantive panels; do not pretend remaining cards are completed dashboards.
PANEL_ROUTES={
 'Architecture':'systems.html',
 'North Star':'story-engine.html',
 'Publication Governance':'history.html',
 'Source of Truth':'evidence.html',
 'System Contracts':'systems.html',
 'Atlas':'atlas.html',
 'Interactive Atlas':'atlas.html',
 'Character Canon':'characters.html',
 'Visual Approval':'characters.html',
 'Release Evidence':'release.html',
 'Publication Manifest':'publications.html',
 'Memo OS':'publications.html',
}
records=[]
for area,entries in groups.items():
 for title,path in entries:
  file=root/path
  available=file.is_file()
  excerpt='Source unavailable — no state inferred'
  if available:
   data=file.read_text(encoding='utf-8')
   lines=[re.sub(r'^[#* >-]+','',x).strip() for x in data.splitlines() if x.strip() and not x.strip().startswith(('|','`'))]
   excerpt=' — '.join(lines[:2])[:250] if not path.endswith('.json') else 'Structured source registry — inspect authoritative record'
  records.append(dict(area=area,title=title,path=path,available=available,excerpt=excerpt,panel=PANEL_ROUTES.get(title)))
(out/'command-center.json').write_text(json.dumps({'classification':'internal review only','modules':records},indent=2)+'\n')
e=html.escape
nav=''.join('<a href="#s'+str(i)+'">'+e(a)+'</a>' for i,a in enumerate(groups))
sections=''
for i,area in enumerate(groups):
 sections+='<section id="s'+str(i)+'"><h2>'+e(area)+'</h2><div class="grid">'
 for m in [x for x in records if x['area']==area]:
  action=('<a href="'+e(m['panel'],quote=True)+'">Open interactive panel</a> · ' if m['panel'] else '')
  sections+='<article class="card" data-search="'+e((area+' '+m['title']+' '+m['path']).lower(),quote=True)+'"><span class="tag">'+('Source found' if m['available'] else 'Unavailable')+'</span><h3>'+e(m['title'])+'</h3><p>'+e(m['excerpt'])+'</p><small>'+e(m['path'])+'</small>'+action+'<a href="../../'+e(m['path'],quote=True)+'">Inspect source</a></article>'
 sections+='</div></section>'
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Schemin ’26 — Commonwealth Command Center</title><style>
:root{color-scheme:dark;--bg:#0d1015;--panel:#1b2029;--line:#4b515c;--gold:#ddbc83;--ink:#f4edde;--muted:#bec4c9}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 system-ui}a{color:var(--gold)}aside{position:fixed;inset:0 auto 0 0;width:265px;background:#151922;border-right:1px solid var(--line);padding:25px;overflow-y:auto}.brand{font:25px Georgia,serif;color:var(--gold)}nav{display:grid;gap:8px;margin-top:27px}nav a{padding:7px 0;text-decoration:none;color:var(--ink)}main{margin-left:265px}header{padding:65px clamp(20px,5vw,75px);background:radial-gradient(circle at 85% 0,#36312a,transparent 50%);border-bottom:1px solid var(--line)}h1{font:clamp(38px,5vw,65px)/1.06 Georgia,serif;margin:13px 0}h2{font:31px Georgia,serif}h3{font:22px Georgia,serif;margin:12px 0}.eyebrow{color:var(--gold);text-transform:uppercase;letter-spacing:.2em;font-size:11px}p{color:var(--muted)}.note{padding:18px 5%;border-bottom:1px solid #806c4c;background:#2c261e}.search{padding:23px 5%}input{padding:13px;background:var(--panel);border:1px solid var(--line);color:var(--ink);border-radius:6px;width:min(520px,100%);font:inherit}section{padding:25px 5% 45px;border-bottom:1px solid var(--line)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(245px,1fr));gap:16px}.card{border:1px solid var(--line);background:var(--panel);border-radius:10px;padding:20px;display:flex;flex-direction:column;min-height:240px}.card p{flex:1}.card small{overflow-wrap:anywhere;color:var(--muted);margin-bottom:12px}.tag{font-size:11px;color:var(--gold)}.card[hidden],section[hidden]{display:none}.actions{display:flex;gap:15px;flex-wrap:wrap;margin-top:25px}.actions a{padding:10px 14px;border:1px solid var(--gold);border-radius:5px}a:focus-visible,input:focus-visible{outline:3px solid var(--gold);outline-offset:3px}@media(max-width:850px){aside{position:static;width:auto}nav{display:flex;flex-wrap:wrap}main{margin:0}header{padding:35px 5%}}
</style></head><body><aside><div class="brand">SCHEMIN’ ’26</div><p>Commonwealth Intelligence</p><nav>'''+nav+'''<a href="story-engine.html">Story Engine</a><a href="history.html">Historical Story Explorer</a><a href="evidence.html">Evidence Graph</a><a href="atlas.html">Interactive Atlas</a><a href="systems.html">Systems Observatory</a><a href="publications.html">Publication Chronology</a><a href="characters.html">Character Image Library</a></nav></aside><main><header><span class="eyebrow">One World • Many Systems</span><h1>The Commonwealth Command Center</h1><p>A source-grounded overview of the living universe, engineering, storytelling, league intelligence and governance. Source presence does not signify acceptance or release.</p><p><strong>6 environments · 24 source modules · 12 character references</strong></p><div class="actions"><a href="characters.html">Explore character gallery</a><a href="command-center.json">View generated source index</a></div></header><div class="note"><strong>Internal development only.</strong> Records may be blocked, historical or private; these source links are not proof of operational status.</div><div class="search"><label for="q">Find a system</label><div><input type="search" id="q" placeholder="Search modules, systems and files"></div><p id="count">24 source modules</p></div>'''+sections+'''</main><script>const cards=[...document.querySelectorAll('.card')];document.querySelector('#q').addEventListener('input',ev=>{let q=ev.target.value.toLowerCase().trim(),n=0;for(let card of cards){card.hidden=!card.dataset.search.includes(q);if(!card.hidden)n++}document.querySelector('#count').textContent=n+' of 24 source modules';for(let s of document.querySelectorAll('section'))s.hidden=![...s.querySelectorAll('.card')].some(c=>!c.hidden)});</script></body></html>'''
(out/'index.html').write_text(page)
print('modules:',len(records),'found:',sum(x['available'] for x in records),'unavailable:',[x['path'] for x in records if not x['available']])
