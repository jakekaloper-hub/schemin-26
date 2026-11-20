"use strict";
/* Commonwealth Folio Studio — code-only, source-compiled world observer.
 * No dynamic image generation, permanent world changes or PR merges.
 * The 23 site diagrams are copied APPROVED STRUCTURAL SVG bytes, not art masters.
 */
let DATA = null;
let selectedLocation = "LOC-LEAGUE-CHAMBER";
let selectedIslandNode = "MAINLAND_PUBLIC_LITTORAL";
let selectedAtlasRegion = "all";
let focusedDivision = "all";
const svgNS = "http://www.w3.org/2000/svg";
const C = {
  "DIV-BURGERS":"#a7c3a2",
  "DIV-WINGS":"#d3a28a",
  "DIV-PIZZA":"#9daedb",
  neutral:"#b7cbd0"
};
const descriptions = {
  atlas: ["01 / THE COMMONWEALTH", "One league. One connected world.",
    "Three overlapping division affiliations, twelve inhabited homelands, seven physical zones and the registered mainland travel network."],
  divisions: ["02 / TWELVE OWNER DOMAINS", "Three divisions. Twelve distinct homelands.",
    "Burgers, Wings and Pizza are the League’s nonexclusive divisions. Every owner retains an established, geographically grounded home."],
  locations: ["03 / THE LOCATION FOLIO", "Every established LOC identifier.",
    "Twenty-three existing places and their approved structural diagrams. Cinematic images have not been generated or promoted."],
  island: ["04 / THE POSTSEASON", "A bridge to the championship.",
    "The Founder-directed Island is source-pinned from draft PR #322: a proposed mainland causeway, independent arena precincts and The Last Field."],
  proposals: ["05 / EDITORIAL ATLAS", "The rest of the proposed world.",
    "Compare every unique identifier from unmerged geography PRs #324 and #325 without upgrading proposals into physical-world canon."],
  sources: ["06 / PROVENANCE", "Proof before pictures.",
    "Exact source paths, source checksums, draft branches, structural approvals and production status remain inspectable before rendering begins."]
};
function el(tag, className, text) {
  const n = document.createElement(tag);
  if(className)n.className = className;
  if(text !== undefined && text !== null)n.textContent = String(text);
  return n;
}
function attr(n, data) {
  for(const [k,v] of Object.entries(data)) if(v !== null && v !== undefined)n.setAttribute(k,String(v));
  return n;
}
function svg(tag, attrs={}, label) {
  const n=document.createElementNS(svgNS,tag);
  attr(n,attrs);
  if(label!==undefined)n.textContent=String(label);
  return n;
}
function clear(n){n.replaceChildren();}
function byId(id){return document.getElementById(id);}
function labeled(parent,label,value) {
  const pair=el("div","fact");
  const dt=el("dt","",label), dd=el("dd","",value==null?"Not established":value);
  pair.append(dt,dd);parent.append(pair);
}
function chip(text,variant=""){
  return el("span","chip "+variant,text);
}
function link(text,url) {
  const a=el("a","source-link",text);
  attr(a,{href:url,target:"_blank",rel:"noopener noreferrer"});
  return a;
}
function linkToSource(path,ref="main"){
  const encoded=path.split("/").map(encodeURIComponent).join("/");
  return "https://github.com/jakekaloper-hub/schemin-26/blob/"+encodeURIComponent(ref)+"/"+encoded;
}
function tagList(parent,arr) {
  const c=el("div","tag-list");
  (arr||[]).forEach(t=>c.append(chip(t)));
  parent.append(c);return c;
}
function sectionBox(title,items){
  const box=el("div","box-dl");box.append(el("h3","",title));
  const list=el("ul");
  for(const item of items.length?items:["Not recorded in source"]){list.append(el("li","",item));}
  box.append(list);return box;
}
function lookupLoc(id){return DATA.locations.find(x=>x.id===id);}
function regionLabel(id){return DATA.regions.find(x=>x.id===id)?.name || id || "Unknown";}
function homeOwner(loc){return DATA.characters.find(x=>x.primary_location_id===loc.id);}
function countMetrics(){
  const stats=DATA.stats;
  const rows=[[stats.divisions,"Divisions"],[stats.homelands,"Homelands"],[stats.locations,"Active LOC IDs"],[stats.regions,"Regions"],[stats.routes,"Mainland routes"],[stats.approved_cinematic_references,"Approved cinematic PNGs"]];
  const panel=byId("metrics");clear(panel);
  for(const [n,label] of rows){
    const card=el("div","metric");card.append(el("div","num",n),el("div","label",label));panel.append(card);
  }
}
function selectView(name){
  const words=descriptions[name];if(!words)return;
  byId("section-eyebrow").textContent=words[0];
  byId("view-title").textContent=words[1];
  byId("view-description").textContent=words[2];
  document.querySelectorAll(".view").forEach(n=>n.classList.toggle("is-visible",n.id==="view-"+name));
  document.querySelectorAll(".nav-tab").forEach(n=>{
    const active=n.dataset.view===name;n.classList.toggle("active",active);
    if(active)n.setAttribute("aria-current","page");else n.removeAttribute("aria-current");
  });
  if(name==="atlas")renderWorldMap();
  if(name==="locations")renderLocationList();
  if(name==="proposals")renderProposalList();
  if(name==="island")renderIslandMap();
}
function populateSelect(selector,items){
  const target=byId(selector);
  items.forEach(item=>{
    const o=el("option","",item.label);o.value=item.value;target.append(o);
  });
}
function svgTitle(parent,text){
  parent.append(svg("title",{},text));
}
function pt(pos){
  return [65+pos[0]*9.7,610-pos[1]*5.45];
}
function locationHighlight(loc){
  if(selectedAtlasRegion!=="all"&&loc.physical_zone_id!==selectedAtlasRegion)return false;
  if(focusedDivision!=="all" && !loc.membership_overlays.includes(focusedDivision))return false;
  return true;
}
function renderWorldMap(){
  const mount=byId("world-map");clear(mount);
  const canvas=svg("svg",{viewBox:"0 0 1100 660",role:"img","aria-label":"Schematic location graph: 23 active locations, 18 routes and seven region extents"});
  const grid=svg("g");
  for(let x=0;x<=100;x+=10){
    const xval=65+x*9.7;grid.append(svg("line",{x1:xval,y1:43,x2:xval,y2:621,stroke:"#91aab5","stroke-opacity":".08","stroke-width":"1"}));
  }
  for(let y=0;y<=100;y+=10){
    const yval=610-y*5.45;grid.append(svg("line",{x1:45,y1:yval,x2:1065,y2:yval,stroke:"#91aab5","stroke-opacity":".08","stroke-width":"1"}));
  }
  canvas.append(grid);
  for(const region of DATA.regions){
    const [x0,y0,x1,y1]=region.abstract_bounds;
    const p=pt([x0,y1]),q=pt([x1,y0]);
    const rect=svg("rect",{x:p[0],y:p[1],width:q[0]-p[0],height:q[1]-p[1],rx:8,class:"map-region"});
    if(selectedAtlasRegion===region.id){rect.setAttribute("fill-opacity",".33");rect.setAttribute("stroke-opacity",".7");}
    svgTitle(rect,region.name+" · interpretive extent, not boundary");
    canvas.append(rect);
    const label=svg("text",{x:p[0]+11,y:p[1]+20,class:"map-region-label"},region.name.toUpperCase());
    canvas.append(label);
  }
  const locById=new Map(DATA.locations.map(x=>[x.id,x]));
  for(const r of DATA.routes){
    const ids=[r.from,...(r.via_location_ids||[]),...(r.via_location_id?[r.via_location_id]:[]),r.to];
    const points=ids.map(id=>pt(locById.get(id).abstract_position));
    const visible=ids.some(id=>locationHighlight(locById.get(id)));
    const line=svg("polyline",{points:points.map(p=>p.join(",")).join(" "),
      class:"map-route"+(visible&&focusedDivision!=="all"?" highlight":""),
      "stroke-opacity":visible?".55":".15"});
    svgTitle(line,r.name+" · "+r.constraints.join(", "));
    canvas.append(line);
  }
  for(const loc of DATA.locations){
    const [x,y]=pt(loc.abstract_position), active=locationHighlight(loc);
    const g=svg("g",{role:"button",tabindex:"0","aria-label":loc.name+"; "+loc.id,style:active?"":"opacity:.24"});
    const circle=svg("circle",{cx:x,cy:y,r:selectedLocation===loc.id?8:6.4,
        class:"map-pin"+(loc.owner_home?" owner":""),
        fill:C[loc.division_id]||C[loc.membership_overlays[0]]||C.neutral});
    g.append(circle);
    const label=svg("text",{x:x+9,y:y-8,class:"map-pin-label"+(active?"":" dim")},loc.name);
    g.append(label);
    const activate=()=>{selectedLocation=loc.id;renderWorldMap();renderInspector(byId("atlas-inspector"),loc);};
    g.addEventListener("click",activate);
    g.addEventListener("keydown",e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();activate();}});
    canvas.append(g);
  }
  canvas.append(svg("text",{x:35,y:645,class:"map-map-hint"},"SCHEMIN-LOCAL-V1 • ABSTRACT TOPOLOGICAL PLACEMENT • NOT A SURVEY OR OFFICIAL COASTLINE"));
  mount.append(canvas);
  renderInspector(byId("atlas-inspector"),lookupLoc(selectedLocation));
}
function renderInspector(target,loc) {
  clear(target);
  if(!loc){target.append(el("p","muted","Choose a place."));return;}
  target.append(el("div","eyebrow",loc.owner_home?"OWNER HOMELAND":"ESTABLISHED COMMONWEALTH SITE"));
  target.append(el("h2","big-title",loc.name));
  target.append(chip(loc.id));
  const wrap=el("div","tag-list");
  wrap.append(chip(loc.canon_status),chip("REGION: "+regionLabel(loc.physical_zone_id)));
  target.append(wrap);
  const data=el("dl","detail-facts");
  labeled(data,"Home affiliation",loc.home_team||"League / shared / neutral");
  labeled(data,"Current state evidence",DATA.world_state_as_of.replaceAll("_"," "));
  labeled(data,"Known landmarks",loc.persistent_landmarks.join(" • "));
  labeled(data,"Cinematic master","Not approved");
  target.append(data);
  const preview=el("img","");
  attr(preview,{src:loc.structural_reference.local_path,alt:"Approved structural (not cinematic) schematic for "+loc.name,loading:"lazy"});
  preview.style.width="100%";preview.style.borderRadius="8px";preview.style.border="1px solid #40535b";
  target.append(preview);
  target.append(el("p","muted","This diagram is an already approved structural reference, not a photograph or endorsed exterior design."));
  target.append(link("Open source Location Card ↗",linkToSource(loc.source_location_card)));
}
function renderRegions(){
  const mount=byId("region-grid");clear(mount);
  for(const reg of DATA.regions){
    const b=el("button","region-card");
    b.append(el("div","eyebrow",reg.id),el("h3","",reg.name));
    b.append(el("p","",reg.environment.terrain.join(" · ")));
    b.append(el("p","",reg.location_ids.length+" active LOC anchors"));
    b.addEventListener("click",()=>{
      selectedAtlasRegion=reg.id;focusedDivision="all";byId("atlas-div").value="all";byId("atlas-region").value=reg.id;
      selectView("atlas");byId("world-map").scrollIntoView({block:"center",behavior:"smooth"});
    });
    mount.append(b);
  }
}
function openLocation(id){
  selectedLocation=id;
  selectView("locations");
  const region=byId("loc-region"),search=byId("loc-search");
  region.value="all";search.value="";
  renderLocationList();
  renderLocationDetail();
  byId("location-detail").scrollIntoView({block:"start",behavior:"smooth"});
}
function renderDivisions(){
  const mount=byId("division-grid");clear(mount);
  for(const [i,division] of DATA.divisions.entries()){
    const group=el("article","division");
    const hd=el("div","division-hd");
    hd.append(el("div","index","DIVISION "+String(i+1).padStart(2,"0")+" • 4 FRANCHISES"));
    hd.append(el("h2","",division.name));
    hd.append(el("p","",division.core_geography));
    group.append(hd);
    const list=el("div","owner-list");
    const members=DATA.characters.filter(c=>c.division_id===division.id).sort((a,b)=>a.team_id-b.team_id);
    for(const [j,member] of members.entries()){
      const b=el("button","owner-card");
      const stack=el("div","");
      stack.append(el("strong","",member.team));
      stack.append(el("div","home",member.location));
      stack.append(el("div","owner",member.owner+" · "+member.character_id));
      b.append(el("div","n",String(j+1)),stack);
      b.addEventListener("click",()=>openLocation(member.primary_location_id));
      list.append(b);
    }
    group.append(list);mount.append(group);
  }
}
function renderLocationList(){
  const mount=byId("location-list");clear(mount);
  const q=byId("loc-search").value.toLowerCase().trim(),reg=byId("loc-region").value;
  const all=DATA.locations.filter(loc=>(reg==="all"||loc.physical_zone_id===reg)&&
    (!q||[loc.id,loc.name,regionLabel(loc.physical_zone_id),...(loc.persistent_landmarks||[])].some(s=>String(s).toLowerCase().includes(q))));
  for(const loc of all){
    const b=el("button","site-card");b.setAttribute("aria-label","Inspect "+loc.name);
    const figure=el("figure");
    const img=el("img");attr(img,{src:loc.structural_reference.local_path,loading:"lazy",
      alt:"Existing approved structural diagram for "+loc.name});
    figure.append(img);b.append(figure);
    const body=el("div","site-body");
    body.append(el("span","loc-code",loc.id),el("strong","",loc.name));
    body.append(el("small","",regionLabel(loc.physical_zone_id)));
    body.append(el("div","tag-list"));
    body.lastChild.append(chip(loc.owner_home?"HOME BASE":"SHARED / NEUTRAL"));
    b.append(body);
    b.addEventListener("click",()=>{selectedLocation=loc.id;renderLocationDetail();});
    mount.append(b);
  }
  byId("loc-empty").hidden=all.length>0;
  renderLocationDetail();
}
function renderLocationDetail(){
  const mount=byId("location-detail"),loc=lookupLoc(selectedLocation);clear(mount);
  if(!loc){mount.append(el("p","muted","Choose a site to inspect its source history."));return;}
  const header=el("div","panel-head");
  const stack=el("div");
  stack.append(el("div","eyebrow",loc.id),el("h2","",loc.name));
  header.append(stack,chip("CINEMATIC REFERENCE: MISSING","warn"));mount.append(header);
  const hero=el("div","detail-hero");
  const img=el("img");attr(img,{src:loc.structural_reference.local_path,alt:"Approved structural diagram of "+loc.name,loading:"lazy"});
  const info=el("div");info.append(el("div","eyebrow",regionLabel(loc.physical_zone_id)));
  info.append(el("p","overview","This registered location is anchored in "+regionLabel(loc.physical_zone_id)+
    ". Its known landmarks are "+loc.persistent_landmarks.join(", ")+". "+
    (loc.owner_home?"Primary homeland of "+loc.home_team+".":"Shared, institutional or historical site.")+
    " The source is structural and semantic; no cinematic exterior master has been approved."));
  const linkarea=el("div","detail-col");
  linkarea.append(link("Location source card ↗",linkToSource(loc.source_location_card)));
  linkarea.append(link("Approved structural source ↗",linkToSource(loc.structural_reference.source_path)));
  info.append(linkarea);hero.append(img,info);mount.append(hero);
  const contents=el("div","detail-col");
  contents.append(sectionBox("Landmarks & physical state",[
    ...loc.persistent_landmarks,...loc.current_world_state.map(x=>"Recorded state: "+x)]));
  contents.append(sectionBox("Road & water access",loc.full_route_ids.map(id=>{
    const r=DATA.routes.find(x=>x.id===id);return r.name+" — "+r.constraints.join(", ");
  })));
  contents.append(sectionBox("History and temporal status",loc.historical_events.length?
    loc.historical_events.map(x=>"Week "+x.week+": "+x.continuity_out.join("; ")):
    ["No additional dated physical mutation established in current source event register."]));
  contents.append(sectionBox("Production governance",[
    "Approved structural SVG: SHA256 "+loc.structural_reference.sha256.slice(0,16)+"…",
    "Current-state snapshot: "+DATA.world_state_as_of,
    "Cinematic PNG: NOT GENERATED OR APPROVED",
    "Owner or region changes require World Engine authority."]));
  mount.append(contents);
}
function islandLayout(){
  const island=DATA.cross_pr.island;
  const slots={
    mainland:[70,140],causeway:[240,140],island_north:[450,130],
    island_west:[645,170],island_east:[885,170],island_central:[645,390],
    island_south:[860,390],island_upland:[990,530]
  };
  const groups={};
  for(const n of island.nodes)(groups[n.zone]??=[]).push(n);
  const positions={};
  for(const [zone,nodes] of Object.entries(groups)){
    const [cx,cy]=slots[zone]||[520,520];
    nodes.forEach((n,i)=>{
      const cols=zone==="island_north"||zone==="island_central"?3:2;
      const row=Math.floor(i/cols),col=i%cols;
      positions[n.id]=[cx+(col-(cols-1)/2)*90,cy+row*62];
    });
  }
  // The displayed layout is deliberately *not* geospatial.
  return positions;
}
function renderIslandMap(){
  const host=byId("island-stage");clear(host);
  const island=DATA.cross_pr.island,positions=islandLayout();
  const stage=svg("svg",{viewBox:"0 0 1140 630",role:"img","aria-label":"Proposed 23-node post-season causeway topology. Schematic positions only."});
  stage.append(svg("rect",{x:15,y:25,width:240,height:570,rx:15,class:"island-band"}));
  stage.append(svg("rect",{x:270,y:25,width:845,height:570,rx:15,class:"island-band"}));
  stage.append(svg("text",{x:28,y:46,class:"island-band-label"},"MAINLAND + CAUSEWAY"));
  stage.append(svg("text",{x:290,y:46,class:"island-band-label"},"POSTSEASON PRECINCT · PROPOSED"));
  const isAll=byId("all-island-edges").checked;
  const featuredIds=["MAINLAND_PUBLIC_LITTORAL","CAUSEWAY_OUTER_GATE","CAUSEWAY_RIDGE","ISLAND_ENTRY_CHECK"];
  for(const edge of island.edges){
    const a=positions[edge.from],b=positions[edge.to];
    const featured=featuredIds.includes(edge.from)&&featuredIds.includes(edge.to)
      &&Math.abs(featuredIds.indexOf(edge.from)-featuredIds.indexOf(edge.to))===1;
    if(!featured&&!isAll)continue;
    const line=svg("line",{x1:a[0],y1:a[1],x2:b[0],y2:b[1],
      class:"island-line"+(featured?" featured":"")});
    svgTitle(line,edge.id+"; modes: "+edge.modes.join(", "));
    stage.append(line);
  }
  for(const node of island.nodes){
    const p=positions[node.id];
    const g=svg("g",{role:"button",tabindex:"0","aria-label":node.name});
    const cir=svg("circle",{cx:p[0],cy:p[1],r:node.id===selectedIslandNode?14:10,
      class:"island-node"+(node.id===selectedIslandNode?" selected":"")});
    g.append(cir);
    const short=node.name.length>23?node.name.slice(0,23)+"…":node.name;
    g.append(svg("text",{x:p[0]+12,y:p[1]+4,class:"island-label"},short));
    const activate=()=>{selectedIslandNode=node.id;renderIslandMap();renderIslandInspector();};
    g.addEventListener("click",activate);
    g.addEventListener("keydown",e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();activate();}});
    stage.append(g);
  }
  stage.append(svg("text",{x:18,y:620,class:"island-small"},"PHYSICAL GEOMETRY / SHORELINE / CAUSEWAY LOADS UNAPPROVED. POSITIONED FOR READABILITY ONLY."));
  host.append(stage);renderIslandInspector();
}
function renderIslandInspector(){
  const mount=byId("island-inspector");clear(mount);
  const island=DATA.cross_pr.island;
  const node=island.nodes.find(x=>x.id===selectedIslandNode)||island.nodes[0];
  mount.append(el("div","eyebrow","CANDIDATE NODE / UNPROMOTED"));
  mount.append(el("h2","big-title",node.name));
  mount.append(chip(node.id));
  const data=el("dl","detail-facts");
  labeled(data,"Operating precinct",node.zone.replaceAll("_"," "));
  labeled(data,"Proposed use",node.use.replaceAll("_"," "));
  labeled(data,"Status",node.status);
  labeled(data,"Coordinates","Unspecified");
  mount.append(data);
  const touched=island.edges.filter(e=>e.from===node.id||e.to===node.id);
  mount.append(el("h3","",touched.length+" documented proposed connections"));
  mount.append(sectionBox("Connected nodes",touched.map(e=>{
    const other=island.nodes.find(n=>n.id===(e.from===node.id?e.to:e.from));
    return other.name+" ("+e.modes.join(", ")+")";
  })));
  mount.append(el("p","",island.unresolved));
  mount.append(link("Original Island topology / PR #322 ↗",
    linkToSource("planning/postseason/ISLAND_CAUSEWAY_TOPOLOGY.founder_v2.json",
    "b32ecbc46e82133f7197fc8802a85e6b59abc44a")));
}
function renderVenues(){
  const target=byId("venue-grid");clear(target);
  for(const v of DATA.cross_pr.island.venues){
    const box=el("article","venue-card");
    box.append(el("div","eyebrow",v.id));
    box.append(el("h3","",v.name));
    box.append(chip(v.round_assignment||v.categories?.join(", ")||"PROPOSAL"));
    box.append(el("p","",v.morphology||"Detailed arena attributes require source review."));
    target.append(box);
  }
}
function renderProposalList(){
  const mount=byId("proposal-list");clear(mount);
  const term=byId("proposal-search").value.toLowerCase().trim();
  const scope=byId("proposal-scope").value;
  const results=DATA.cross_pr.proposals.filter(x=>{
    if(term&&![x.id,x.name,x.zone_hypothesis,...x.namespaces].some(y=>String(y||"").toLowerCase().includes(term)))return false;
    if(scope==="324"&&!x.source_prs.includes(324))return false;
    if(scope==="325"&&!x.source_prs.includes(325))return false;
    if(scope==="only324"&&!(x.source_prs.includes(324)&&!x.source_prs.includes(325)))return false;
    if(scope==="only325"&&!(x.source_prs.includes(325)&&!x.source_prs.includes(324)))return false;
    if(scope==="unmerged"&&x.source_class==="ACTIVE_MAIN_LOC")return false;
    return true;
  });
  byId("proposal-summary").textContent="Showing "+results.length+" / "+
    DATA.cross_pr.proposals.length+" exact identifiers. 23 are active main locations; proposal and topology handles remain noncanonical.";
  for(const item of results){
    const box=el("div","proposal-item");
    box.append(el("div","code",item.id));
    box.append(el("strong","",item.name));
    box.append(el("p","",item.source_class.replaceAll("_"," ")+" · PR "+
      item.source_prs.join(" + ")+" · "+(item.zone_hypothesis||"zone unresolved")));
    mount.append(box);
  }
}
function renderSources(){
  const mount=byId("source-list");clear(mount);
  for(const [key,s] of Object.entries(DATA.source_sha256)){
    const item=el("div","source-row");
    item.append(el("strong","",key.replaceAll("_"," ").toUpperCase()));
    item.append(link(s.path+" ↗",linkToSource(s.path)));
    item.append(el("code","", "sha256 "+s.sha256));
    mount.append(item);
  }
  for(const [key,s] of Object.entries(DATA.cross_pr.source_pins)){
    const item=el("div","source-row");
    item.append(el("strong","",key.replaceAll("_"," ").toUpperCase()+" · UNMERGED PR #"+s.pr));
    item.append(link(s.path+" ↗",s.url));
    item.append(el("code","",s.commit+" · sha256 "+s.sha256_bytes));
    mount.append(item);
  }
}
async function boot(){
  try{
    const response=await fetch("./data/world.json",{cache:"no-store"});
    if(!response.ok)throw Error("Unable to read compiled world data, HTTP "+response.status);
    DATA=await response.json();
    if(DATA.stats.locations!==23 || DATA.stats.homelands!==12 || DATA.stats.island_nodes_proposed!==23)
      throw Error("Dataset fails basic UI invariants");
    byId("current-state-label").textContent="World state: "+DATA.world_state_as_of;
    countMetrics();
    populateSelect("atlas-div",DATA.divisions.map(d=>({label:d.name,value:d.id})));
    populateSelect("atlas-region",DATA.regions.map(d=>({label:d.name,value:d.id})));
    populateSelect("loc-region",DATA.regions.map(d=>({label:d.name,value:d.id})));
    document.querySelectorAll(".nav-tab").forEach(button=>button.addEventListener("click",()=>selectView(button.dataset.view)));
    byId("atlas-div").addEventListener("change",e=>{focusedDivision=e.target.value;renderWorldMap();});
    byId("atlas-region").addEventListener("change",e=>{selectedAtlasRegion=e.target.value;renderWorldMap();});
    byId("loc-search").addEventListener("input",renderLocationList);
    byId("loc-region").addEventListener("change",renderLocationList);
    byId("proposal-search").addEventListener("input",renderProposalList);
    byId("proposal-scope").addEventListener("change",renderProposalList);
    byId("all-island-edges").addEventListener("change",renderIslandMap);
    renderWorldMap();renderRegions();renderDivisions();renderLocationList();renderVenues();renderIslandMap();renderProposalList();renderSources();
    selectView("atlas");
  }catch(error){
    const e=byId("error");e.hidden=false;
    e.textContent="Folio data failed to load: "+error.message+
      ". Serve this folder over localhost (python3 -m http.server), not file://.";
  }
}
document.addEventListener("DOMContentLoaded",boot);
