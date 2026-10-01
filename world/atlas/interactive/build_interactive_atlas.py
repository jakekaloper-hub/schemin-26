#!/usr/bin/env python3
from __future__ import annotations
import html, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
DATA=ROOT/"world"/"data"
LCP=ROOT/"world"/"location-control-plane"/"registries"
OUT=ROOT/"world"/"atlas"/"interactive"/"SCHEMIN_ATLAS_INTERACTIVE.html"

def load(p): return json.loads(p.read_text())

def main():
    zones=load(DATA/"physical_zones.json")["regions"]
    locs=load(DATA/"locations.json")["locations"]
    routes=load(DATA/"routes.json")["routes"]
    divs=load(DATA/"divisions.json")["divisions"]
    state=load(DATA/"current_world_state.json")
    candidates=load(DATA/"atlas_location_candidates.json")["candidates"]
    refs=load(LCP/"LOCATION_REFERENCE_REGISTRY.json")["locations"]
    refmap={x["location_id"]:x for x in refs}
    payload={
      "meta":{"coordinate_space":"schemin-local-v1 abstract/non-metric","active_location_count":len(locs),"route_count":len(routes),"zone_count":len(zones),"candidate_count":len(candidates)},
      "zones":zones,"locations":locs,"routes":routes,"divisions":divs,"state":state,
      "references":refmap,
      "candidate_catalog":[{"id":c["id"],"name":c["working_name"],"status":c["lifecycle_status"],"zones":c.get("likely_physical_zone_ids",[]),"class":c["location_class"],"championship_only":c.get("championship_only",False)} for c in candidates]
    }
    j=json.dumps(payload,separators=(",",":"),ensure_ascii=False).replace("</","<\\/")
    doc=f'''<!doctype html>
<html><head><meta charset="utf-8"><title>Schemin '26 Interactive Atlas</title>
<style>
body{{margin:0;font-family:system-ui;background:#f3efe4;color:#171717}}
header{{padding:14px 18px;border-bottom:1px solid #999;display:flex;gap:18px;align-items:center;flex-wrap:wrap}}
main{{display:grid;grid-template-columns:minmax(0,1fr) 340px;height:calc(100vh - 74px)}}
#map{{width:100%;height:100%;background:#ede7d8}}
aside{{overflow:auto;border-left:1px solid #999;padding:16px;background:#faf7ef}}
.zone{{fill:none;stroke:#777;stroke-dasharray:6 5}}
.route{{stroke:#555;stroke-width:2}}
.loc{{cursor:pointer;stroke:#111;stroke-width:1.5}}
.loc.dim{{opacity:.13}} .route.dim{{opacity:.08}}
.state-ring{{fill:none;stroke:#111;stroke-width:3;stroke-dasharray:3 2}}
small,.muted{{color:#666}}
button,select,label{{font:inherit}}
#candidatePanel{{display:none;margin-top:22px;padding-top:14px;border-top:1px solid #bbb}}
body.editorial #candidatePanel{{display:block}}
a{{color:inherit}}
</style></head>
<body>
<header>
<strong>SCHEMIN '26 — INTERACTIVE ATLAS</strong>
<span class="muted">abstract / non-metric topology</span>
<label>Division <select id="division"><option value="ALL">All</option><option>DIV-BURGERS</option><option>DIV-WINGS</option><option>DIV-PIZZA</option><option value="NEUTRAL">Neutral/shared</option></select></label>
<label><input id="stateToggle" type="checkbox"> historical/current-state overlay</label>
<span class="muted">Editorial catalog: append ?editorial=1</span>
</header>
<main><svg id="map" viewBox="0 0 1000 1000" aria-label="Schemin world atlas"></svg><aside>
<h2 id="title">Select a location</h2><div id="detail">Click an active LOC marker.</div>
<div id="candidatePanel"><h3>Editorial candidates</h3><p class="muted">Catalog only. No map coordinates are asserted.</p><div id="candidates"></div></div>
</aside></main>
<script id="atlas-data" type="application/json">{j}</script>
<script>
const D=JSON.parse(document.getElementById('atlas-data').textContent);
const svg=document.getElementById('map'), NS='http://www.w3.org/2000/svg';
const sx=x=>50+x*9, sy=y=>950-y*9;
const el=(tag,a={{}})=>{{const n=document.createElementNS(NS,tag);Object.entries(a).forEach(([k,v])=>n.setAttribute(k,v));return n;}};
const locBy=Object.fromEntries(D.locations.map(x=>[x.id,x]));
const routeEls=[],locEls=[];
D.zones.forEach(z=>{{const [xmin,ymin,xmax,ymax]=z.abstract_bounds;const r=el('rect',{{x:sx(xmin),y:sy(ymax),width:(xmax-xmin)*9,height:(ymax-ymin)*9,class:'zone'}});svg.append(r);const t=el('text',{{x:sx(xmin)+5,y:sy(ymax)+16,'font-size':11}});t.textContent=z.name;svg.append(t);}});
D.routes.forEach(r=>{{let via=r.via_location_ids||[];if(!via.length&&r.via_location_id)via=[r.via_location_id];const chain=[r.from,...via,r.to];for(let i=0;i<chain.length-1;i++){{const a=locBy[chain[i]],b=locBy[chain[i+1]];if(!a?.abstract_position||!b?.abstract_position)continue;const l=el('line',{{x1:sx(a.abstract_position[0]),y1:sy(a.abstract_position[1]),x2:sx(b.abstract_position[0]),y2:sy(b.abstract_position[1]),class:'route'}});l.dataset.route=r.id;svg.append(l);routeEls.push(l);}}}});
const markerClass=l=>l.division_id||'NEUTRAL';
D.locations.forEach(l=>{{if(!l.abstract_position)return;const g=el('g',{{class:'location'}});const c=el('circle',{{cx:sx(l.abstract_position[0]),cy:sy(l.abstract_position[1]),r:7,class:'loc','data-division':markerClass(l),'data-location':l.id}});const txt=el('text',{{x:sx(l.abstract_position[0])+10,y:sy(l.abstract_position[1])-9,'font-size':10}});txt.textContent=l.name;g.append(c,txt);svg.append(g);locEls.push({{g,c,l}});c.addEventListener('click',()=>show(l));}});
function show(l){{document.getElementById('title').textContent=l.name;const s=D.state.locations[l.id]||[];const ref=D.references[l.id]||{{}};document.getElementById('detail').innerHTML='<p><b>'+l.id+'</b></p><p>Zone: '+l.physical_zone_id+'</p><p>Type: '+l.location_type+'</p><p>Canon: '+l.canon_status+'</p><p>Landmarks: '+(l.persistent_landmarks||[]).join(', ')+'</p><p>Access: '+(l.access_route_ids||[]).join(', ')+'</p><p>Current state: '+(s.join(' | ')||'no additional mutation asserted')+'</p>'+(ref.approved_structural_reference_uris?.[0]?'<p><a href="../../environment-references/plates/'+l.id+'/STRUCTURAL_PLATE.svg">Open structural plate</a></p>':'');}}
function apply(){{const f=document.getElementById('division').value;locEls.forEach(x=>x.g.classList.toggle('dim',f!=='ALL'&&markerClass(x.l)!==f));routeEls.forEach(x=>x.classList.toggle('dim',f!=='ALL'));document.querySelectorAll('.state-ring').forEach(x=>x.remove());if(document.getElementById('stateToggle').checked){{Object.keys(D.state.locations).forEach(id=>{{const l=locBy[id];if(!l?.abstract_position)return;svg.append(el('circle',{{cx:sx(l.abstract_position[0]),cy:sy(l.abstract_position[1]),r:12,class:'state-ring'}}));}});}}}}
document.getElementById('division').addEventListener('change',apply);document.getElementById('stateToggle').addEventListener('change',apply);
if(new URLSearchParams(location.search).get('editorial')==='1')document.body.classList.add('editorial');
document.getElementById('candidates').innerHTML=D.candidate_catalog.map(c=>'<p><b>'+c.name+'</b><br><small>'+c.id+' · '+c.status+' · '+c.zones.join(', ')+'</small></p>').join('');
apply();
</script></body></html>'''
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(doc)
    print(OUT)

if __name__=="__main__": main()
