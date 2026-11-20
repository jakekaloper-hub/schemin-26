/* Manual local Chrome DevTools integration smoke (no images or screenshots). */
import assert from "node:assert/strict";
const http=process.env.FOLIO_DEVTOOLS_HTTP||"http://127.0.0.1:9228";
const url=process.env.FOLIO_LOCAL_URL||"http://127.0.0.1:8891/index.html";
const page=await fetch(http+"/json/new?about:blank",{method:"PUT"}).then(r=>r.json());
assert(page,"Chrome DevTools session has no page");
const socket=new WebSocket(page.webSocketDebuggerUrl);
await new Promise((resolve,reject)=>{socket.addEventListener("open",resolve,{once:true});socket.addEventListener("error",reject,{once:true});});
let sequence=0;
const pending=new Map(),exceptions=[];
socket.addEventListener("message",event=>{
  const frame=JSON.parse(event.data);
  if(frame.method==="Runtime.exceptionThrown")exceptions.push(JSON.stringify(frame.params.exceptionDetails));
  if(pending.has(frame.id)){
    const {resolve,reject}=pending.get(frame.id);pending.delete(frame.id);
    if(frame.error)reject(new Error(JSON.stringify(frame.error)));else resolve(frame.result);
  }
});
function send(method,params={}){
  const id=++sequence;
  socket.send(JSON.stringify({id,method,params}));
  return new Promise((resolve,reject)=>pending.set(id,{resolve,reject}));
}
const evaluate=async(expression)=>{
  const r=await send("Runtime.evaluate",{expression,returnByValue:true,awaitPromise:true});
  if(r.exceptionDetails)throw new Error(r.exceptionDetails.text+" "+JSON.stringify(r.exceptionDetails.exception));
  return r.result.value;
};
await send("Runtime.enable");
await send("Page.enable");
await send("Page.navigate",{url});
await new Promise(r=>setTimeout(r,2200));
const stats=await evaluate('({ ready:document.readyState, metric:document.querySelectorAll(".metric").length, sites:document.querySelectorAll(".site-card").length, regions:document.querySelectorAll("#region-grid .region-card").length, owners:document.querySelectorAll(".owner-card").length, venues:document.querySelectorAll(".venue-card").length, proposals:document.querySelectorAll(".proposal-item").length, packets:document.querySelectorAll(".packet-card").length, packetRegions:document.querySelectorAll("#packet-regions .region-card").length, hasMap:!!document.querySelector("#world-map svg"), error:document.querySelector("#error").textContent })');
console.log("DOM_STATS",JSON.stringify(stats));
assert.equal(stats.metric,6);
assert.equal(stats.sites,23);
assert.equal(stats.regions,7);
assert.equal(stats.owners,12);
assert.equal(stats.venues,9);
assert.equal(stats.proposals,199);
assert.equal(stats.packets,23);
assert.equal(stats.packetRegions,7);
assert.equal(stats.hasMap,true);
assert.equal(stats.error,"");
const exportHref=await evaluate('document.querySelector("#view-production a[download]")?.href');
assert(exportHref.endsWith("/data/production_packets.json"));
const exported=await fetch(exportHref).then(async response=>{
  assert.equal(response.status,200);
  return response.json();
});
assert.equal(exported.location_packet_count,23);
assert.equal(exported.region_packet_count,7);
assert.equal(exported.governance.output_is_image,false);
assert(exported.locations.every(packet=>packet.render_permitted===false));
const screens={};
for(const v of ["divisions","locations","island","proposals","production","sources"]){
  screens[v]=await evaluate('(()=>{document.querySelector("[data-view='+"'"+v+"'"+']").click();return {active:document.querySelector("#view-'+v+'").classList.contains("is-visible"),title:document.querySelector("#view-title").textContent};})()');
  assert.equal(screens[v].active,true);
}
const keyboardMap=await evaluate('(()=>{document.querySelector("[data-view=atlas]").click();const point=Array.from(document.querySelectorAll("[data-location-id]")).find(n=>n.getAttribute("data-location-id")==="LOC-MUD-DOGS-SWAMP");point.focus();point.dispatchEvent(new KeyboardEvent("keydown",{key:"Enter",bubbles:true}));return {selected:document.activeElement.getAttribute("data-location-id"),inspected:document.querySelector("#atlas-inspector .big-title")?.textContent};})()');
assert.deepEqual(keyboardMap,{selected:"LOC-MUD-DOGS-SWAMP",inspected:"Mud Dogs Swamp"});
const filtered=await evaluate('(()=>{document.querySelector("[data-view=locations]").click();const input=document.querySelector("#loc-search");input.value="MUD-DOGS";input.dispatchEvent(new Event("input",{bubbles:true}));const n=document.querySelectorAll(".site-card").length;input.value="";input.dispatchEvent(new Event("input",{bubbles:true}));return n;})()');
assert.equal(filtered,1);
const keyboardIsland=await evaluate('(()=>{document.querySelector("[data-view=island]").click();const node=Array.from(document.querySelectorAll("[data-island-node]")).find(n=>n.getAttribute("data-island-node")==="LAST_FIELD");node.focus();node.dispatchEvent(new KeyboardEvent("keydown",{key:"Enter",bubbles:true}));return {selected:document.activeElement.getAttribute("data-island-node"),inspected:document.querySelector("#island-inspector .big-title")?.textContent};})()');
assert.equal(keyboardIsland.selected,"LAST_FIELD");
assert.equal(keyboardIsland.inspected,"Last Field championship stadium");
const packetFiltered=await evaluate('(()=>{document.querySelector("[data-view=production]").click();const field=document.querySelector("#packet-search");field.value="MUD-DOGS";field.dispatchEvent(new Event("input",{bubbles:true}));const n=document.querySelectorAll(".packet-card").length;field.value="";field.dispatchEvent(new Event("input",{bubbles:true}));return n;})()');
assert.equal(packetFiltered,1);
const filterContinuity=await evaluate('(()=>{const value=(selector,titleSelector)=>{const f=document.querySelector(selector);f.value="LEAGUE-CHAMBER";f.dispatchEvent(new Event("input",{bubbles:true}));f.value="MUD-DOGS";f.dispatchEvent(new Event("input",{bubbles:true}));const title=document.querySelector(titleSelector)?.textContent;f.value="";f.dispatchEvent(new Event("input",{bubbles:true}));return title;};document.querySelector("[data-view=locations]").click();const location=value("#loc-search","#location-detail h2");document.querySelector("[data-view=production]").click();const packet=value("#packet-search","#packet-inspector h2");return {location,packet};})()');
assert.deepEqual(filterContinuity,{location:"Mud Dogs Swamp",packet:"Mud Dogs Swamp"});
const proposalFiltered=await evaluate('(()=>{document.querySelector("[data-view=proposals]").click();const s=document.querySelector("#proposal-scope");s.value="only325";s.dispatchEvent(new Event("change",{bubbles:true}));return document.querySelectorAll(".proposal-item").length;})()');
assert.equal(proposalFiltered,44);
const islandLines=await evaluate('(()=>{document.querySelector("[data-view=island]").click();const a=document.querySelectorAll("#island-stage .island-line").length;const i=document.querySelector("#all-island-edges");i.checked=true;i.dispatchEvent(new Event("change",{bubbles:true}));return [a,document.querySelectorAll("#island-stage .island-line").length];})()');
assert.equal(islandLines[1],45);
const seasonCounts=await evaluate('(()=>{const select=document.querySelector("#island-era");const before=document.querySelectorAll("#island-years .season-card").length;select.value="2020";select.dispatchEvent(new Event("change",{bubbles:true}));const one=document.querySelectorAll("#island-years .season-card").length;const year=document.querySelector("#island-years .season-card h3")?.textContent;select.value="all";select.dispatchEvent(new Event("change",{bubbles:true}));return [before,one,year];})()');
assert.deepEqual(seasonCounts,[11,1,"2020"]);
const sourceLinks=await evaluate('(()=>{document.querySelector("[data-view=sources]").click();const a=Array.from(document.querySelectorAll("#source-list a"));return {folio:a.find(x=>x.textContent.includes("LOC_FOLIO_MANIFEST"))?.href,island:a.find(x=>x.textContent.includes("ISLAND_CAUSEWAY_TOPOLOGY"))?.href,main:a.find(x=>x.textContent.includes("world/data/locations.json"))?.href};})()');
assert(sourceLinks.folio.includes("/blob/feat/commonwealth-cinematic-loc-folio-20261120/world/environment-references/cinematic-folio/"),"Draft folio linked under wrong branch");
assert(sourceLinks.island.includes("/blob/b32ecbc46e82133f7197fc8802a85e6b59abc44a/planning/postseason/"),"Island source not pinned to PR322 exact commit");
assert(sourceLinks.main.includes("/blob/main/world/data/locations.json"),"Main location source not linked to authoritative main");
await send("Emulation.setDeviceMetricsOverride",{width:390,height:844,deviceScaleFactor:2,mobile:true});
await new Promise(r=>setTimeout(r,350));
const mobile=await evaluate('(async()=>{const report={};for(const tab of document.querySelectorAll(".nav-tab")){tab.click();await new Promise(r=>setTimeout(r,45));report[tab.dataset.view]=document.documentElement.scrollWidth;}return {width:window.innerWidth,panels:report};})()');
for(const [name,width] of Object.entries(mobile.panels)){
  assert(width<=mobile.width+2,"Unexpected 390px overflow in "+name+": "+width);
}
assert.equal(exceptions.length,0,"Browser exceptions: "+exceptions.join("; "));
console.log("PASS Seven-view browser navigation, keyboard focus, production packets, source links, chronology, 390px layout",JSON.stringify({screens,keyboardMap,keyboardIsland,filtered,packetFiltered,proposalFiltered,islandLines,seasonCounts,mobile}));
socket.close();
await fetch(http+"/json/close/"+page.id).catch(()=>{});
