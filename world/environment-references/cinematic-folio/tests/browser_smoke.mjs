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
const stats=await evaluate('({ ready:document.readyState, metric:document.querySelectorAll(".metric").length, sites:document.querySelectorAll(".site-card").length, regions:document.querySelectorAll(".region-card").length, owners:document.querySelectorAll(".owner-card").length, venues:document.querySelectorAll(".venue-card").length, proposals:document.querySelectorAll(".proposal-item").length, hasMap:!!document.querySelector("#world-map svg"), error:document.querySelector("#error").textContent })');
console.log("DOM_STATS",JSON.stringify(stats));
assert.equal(stats.metric,6);
assert.equal(stats.sites,23);
assert.equal(stats.regions,7);
assert.equal(stats.owners,12);
assert.equal(stats.venues,9);
assert.equal(stats.proposals,199);
assert.equal(stats.hasMap,true);
assert.equal(stats.error,"");
const screens={};
for(const v of ["divisions","locations","island","proposals","sources"]){
  screens[v]=await evaluate('(()=>{document.querySelector("[data-view='+"'"+v+"'"+']").click();return {active:document.querySelector("#view-'+v+'").classList.contains("is-visible"),title:document.querySelector("#view-title").textContent};})()');
  assert.equal(screens[v].active,true);
}
const filtered=await evaluate('(()=>{document.querySelector("[data-view=locations]").click();const input=document.querySelector("#loc-search");input.value="MUD-DOGS";input.dispatchEvent(new Event("input",{bubbles:true}));const n=document.querySelectorAll(".site-card").length;input.value="";input.dispatchEvent(new Event("input",{bubbles:true}));return n;})()');
assert.equal(filtered,1);
const proposalFiltered=await evaluate('(()=>{document.querySelector("[data-view=proposals]").click();const s=document.querySelector("#proposal-scope");s.value="only325";s.dispatchEvent(new Event("change",{bubbles:true}));return document.querySelectorAll(".proposal-item").length;})()');
assert.equal(proposalFiltered,44);
const islandLines=await evaluate('(()=>{document.querySelector("[data-view=island]").click();const a=document.querySelectorAll("#island-stage .island-line").length;const i=document.querySelector("#all-island-edges");i.checked=true;i.dispatchEvent(new Event("change",{bubbles:true}));return [a,document.querySelectorAll("#island-stage .island-line").length];})()');
assert.equal(islandLines[1],45);
assert.equal(exceptions.length,0,"Browser exceptions: "+exceptions.join("; "));
console.log("PASS Browser DOM navigation, filters, character/LOC inventories, Island 45 links",JSON.stringify({screens,filtered,proposalFiltered,islandLines}));
socket.close();
await fetch(http+"/json/close/"+page.id).catch(()=>{});
