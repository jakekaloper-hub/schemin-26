#!/usr/bin/env node
/** Optional real-GPU smoke for the source-built unpublished observer.
 * Requires Node 22+ and installed Chrome. No new package, API, or service.
 * Usage: node tools/webgl2-journey-smoke.mjs /absolute/path/to/observer.html
 */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {verifyTemporalSceneSequence,verifyWetlandsTemporalSequences,WETLAND_TEMPORAL_SITES} from './temporal-evidence.mjs';
import {atlasViewPlan,verifyAtlasCandidateCaptures,atlasContactSheetHtml} from './atlas-view-evidence.mjs';
import {spawn} from 'node:child_process';
import {existsSync,mkdirSync,mkdtempSync,readFileSync,rmSync,writeFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import {pathToFileURL} from 'node:url';

const captureOption=process.argv.indexOf('--capture-dir');
const temporalOption=process.argv.indexOf('--temporal-dir');
const wetlandsOption=process.argv.indexOf('--wetlands-temporal-dir');
const closeupOption=process.argv.indexOf('--wetlands-closeup-dir');
const atlasOption=process.argv.indexOf('--atlas-views-dir');
const lightOption=process.argv.indexOf('--wetlands-light-dir');
const historyOption=process.argv.indexOf('--history-sweep-dir');
const dprOption=process.argv.indexOf('--dpr-evidence-dir');
const dprCheckOnly=process.argv.length===4&&process.argv[3]==='--dpr-check';
const options=[captureOption,temporalOption,wetlandsOption,closeupOption,atlasOption,lightOption,historyOption,dprOption].filter(index=>index>=0);
assert.ok((options.length===0&&(process.argv.length===3||dprCheckOnly))
 ||(options.length===1&&options[0]===3&&process.argv.length===5&&!process.argv[4].startsWith('--')),
 'Optional capture argument: --capture-dir, --temporal-dir, --wetlands-temporal-dir, --wetlands-closeup-dir or --atlas-views-dir or --wetlands-light-dir or --history-sweep-dir /new/private/evidence/directory; or --dpr-check or --dpr-evidence-dir /new/private/evidence/directory');
const dprDir=dprOption<0?null:resolve(process.argv[4]);
const dprCheck=dprCheckOnly||Boolean(dprDir);
const captureDir=captureOption<0?null:resolve(process.argv[4]);
const temporalDir=temporalOption<0?null:resolve(process.argv[4]);
const wetlandsDir=wetlandsOption<0?null:resolve(process.argv[4]);
const closeupDir=closeupOption<0?null:resolve(process.argv[4]);
const atlasDir=atlasOption<0?null:resolve(process.argv[4]);
if(captureDir)assert.ok(!existsSync(captureDir),'CAPTURE_DIRECTORY_EXISTS: refusal to overwrite evidence');
if(temporalDir)assert.ok(!existsSync(temporalDir),'TEMPORAL_DIRECTORY_EXISTS: refusal to overwrite evidence');
if(wetlandsDir)assert.ok(!existsSync(wetlandsDir),'WETLANDS_DIRECTORY_EXISTS: refusal to overwrite evidence');
if(closeupDir)assert.ok(!existsSync(closeupDir),'CLOSEUP_DIRECTORY_EXISTS: refusal to overwrite evidence');
if(atlasDir)assert.ok(!existsSync(atlasDir),'ATLAS_DIRECTORY_EXISTS: refusal to overwrite evidence');
const lightDir=lightOption<0?null:resolve(process.argv[4]);
if(lightDir)assert.ok(!existsSync(lightDir),'LIGHT_DIRECTORY_EXISTS: refusal to overwrite evidence');
const historyDir=historyOption<0?null:resolve(process.argv[4]);
if(historyDir)assert.ok(!existsSync(historyDir),'HISTORY_DIRECTORY_EXISTS: refusal to overwrite evidence');
if(dprDir)assert.ok(!existsSync(dprDir),'DPR_DIRECTORY_EXISTS: refusal to overwrite evidence');
const historySweep=[],dprObservations=[],dprCaptures=[];
let dprCamera=null;
const lightCaptures=[];
const captured=[],temporalCaptures=[],wetlandTemporalCaptures=[],wetlandCloseupCaptures=[],closeupCameras=[],atlasCaptures=[];
let atlasPlan=null;
const observer=resolve(process.argv[2]||'');
assert.ok(process.argv[2]&&existsSync(observer),'Usage: node webgl2-journey-smoke.mjs /path/to/observer.html');
const chrome=process.env.CHROME_BIN||(process.platform==='darwin'
 ? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' : '/usr/bin/google-chrome');
assert.ok(existsSync(chrome),'Chrome unavailable: set CHROME_BIN');
const scratch=mkdtempSync(join(tmpdir(),'commonwealth-webgl2-smoke-'));
const pending=new Map(),runtimeExceptions=[],consoleErrors=[],externalRequests=[];
let child,ws,nextId=0;
const delay=ms=>new Promise(r=>setTimeout(r,ms));
/** CDP samples and DOM clicks straddle animation frames: compare the view, not raw float JSON. */
function assertHistoricalViewRestored(before,after){
 const b=[...before.target,before.distance,before.yaw,before.pitch];
 const a=[...after.target,after.distance,after.yaw,after.pitch];
 const tolerance=[.002,.002,.002,.002,.00002,.00002];
 assert.equal(b.length,6,'Invalid source camera');assert.equal(a.length,6,'Invalid return camera');
 for(let i=0;i<6;i++)assert.ok(Number.isFinite(a[i])&&Number.isFinite(b[i])&&Math.abs(a[i]-b[i])<=tolerance[i],
  'Return changed historical camera at component '+i+': '+b[i]+' -> '+a[i]);
}
async function until(check,label,timeout=45000){
 const deadline=Date.now()+timeout;
 while(Date.now()<deadline){const value=await check();if(value)return value;await delay(180);}
 throw Error('TIMEOUT: '+label);
}
async function connect(url){
 ws=new WebSocket(url);
 await new Promise((ok,fail)=>{ws.addEventListener('open',ok,{once:true});ws.addEventListener('error',()=>fail(Error('CDP_CONNECT_FAILED')),{once:true});});
 ws.addEventListener('message',e=>{
  const m=JSON.parse(e.data);
  if(m.id){const req=pending.get(m.id);if(!req)return;pending.delete(m.id);if(m.error)req.fail(Error(JSON.stringify(m.error)));else req.ok(m.result);return;}
  if(m.method==='Network.requestWillBeSent'&&/^https?:|^wss?:/.test(m.params?.request?.url||''))externalRequests.push(m.params.request.url);
  if(m.method==='Runtime.exceptionThrown')runtimeExceptions.push(m.params?.exceptionDetails?.text||'Runtime exception');
  if(m.method==='Runtime.consoleAPICalled'&&m.params?.type==='error')consoleErrors.push(m.params.args?.map(x=>x.value||x.description||'').join(' ')||'console.error');
  if(m.method==='Log.entryAdded'&&m.params?.entry?.level==='error'&&!/favicon\.ico/.test(m.params.entry.url||''))consoleErrors.push(m.params.entry.text);
 });
}
function cdp(method,params={}){
 return new Promise((ok,fail)=>{const id=++nextId;pending.set(id,{ok,fail});ws.send(JSON.stringify({id,method,params}));});
}
async function evaluate(expression){
 const r=await cdp('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true,userGesture:true});
 if(r.exceptionDetails)throw Error('BROWSER_EVALUATION: '+r.exceptionDetails.text+' '+(r.exceptionDetails.exception?.description||''));
 return r.result?.value;
}
const snapshot=()=>evaluate('(()=>({state:__observerDebug.state(),stats:__observerDebug.stats(),places:__observerDebug.bindings().length,sourceUnchanged:__observerDebug.sourceUnchanged(),fallback:!document.querySelector("#fallback").hidden,gpu:__observerDebug.stats()?.gpuRenderer||"UNAVAILABLE"}))()');
async function captureCandidate(file,placeId,sink=captured){
 if(!captureDir&&!atlasDir&&!lightDir)return;
 const s=await snapshot();
 assert.equal(s.stats.renderer,'three-webgl2','Visual evidence requires real WebGL2');
 assert.ok(s.stats.frames>0&&s.sourceUnchanged&&!s.fallback,'Invalid candidate capture state');
 assert.equal(await evaluate('document.querySelector("#inspector").hidden'),placeId===null);
 if(placeId)assert.equal(await evaluate('__observerDebug.state().locationId'),placeId);
 // Screenshots are raw evidence of the actual offline canvas, not approved artwork.
 const {data}=await cdp('Page.captureScreenshot',{format:'png',fromSurface:true,captureBeyondViewport:false});
 const bytes=Buffer.from(data,'base64');
 assert.equal(bytes.subarray(0,8).toString('hex'),'89504e470d0a1a0a','Browser returned invalid PNG');
 const width=bytes.readUInt32BE(16),height=bytes.readUInt32BE(20);
 assert.ok(width>=1000&&height>=600,'Candidate capture has unexpected viewport');
 sink.push({file,placeId,frames:s.stats.frames,bytes,width,height,camera:await evaluate('__observerDebug.camera()')});
}
async function captureTemporalFrame(file,waterTime,motionState,placeId='LOC-TDS-WATERFALL-TEMPLE',sink=temporalCaptures){
 assert.ok(['MOVING','PAUSED'].includes(motionState),'Unsupported temporal capture state');
 const s=await snapshot();
 assert.equal(s.stats.renderer,'three-webgl2','Temporal evidence requires physical WebGL2');
 assert.equal(s.state.locationId,placeId,'Temporal evidence changed source site');
 assert.ok(s.stats.frames>0&&s.sourceUnchanged&&!s.fallback,'Invalid temporal capture');
 const {data}=await cdp('Page.captureScreenshot',{format:'png',fromSurface:true,captureBeyondViewport:false});
 const bytes=Buffer.from(data,'base64');
 assert.equal(bytes.subarray(0,8).toString('hex'),'89504e470d0a1a0a');
 const width=bytes.readUInt32BE(16),height=bytes.readUInt32BE(20);
 assert.ok(width>=1000&&height>=600,'Unexpected temporal screenshot dimensions');
 sink.push({file,placeId,waterTime,motionState,frames:s.stats.frames,bytes,width,height});
}
const click=selector=>evaluate('(()=>{const n=document.querySelector('+JSON.stringify(selector)+');if(!n||n.hidden||n.disabled)throw Error("MISSING_CONTROL: "+'+JSON.stringify(selector)+');n.click();return true})()');
async function main(){
 child=spawn(chrome,[
  '--headless=new','--no-first-run','--no-default-browser-check','--disable-background-networking',
  '--disable-extensions','--no-proxy-server','--remote-debugging-port=0',
  '--user-data-dir='+scratch,'--window-size=1440,900',
  '--force-prefers-reduced-motion=no-preference','about:blank'
 ],{stdio:'ignore'});
 child.on('error',e=>consoleErrors.push('CHROME_START: '+e.message));
 const port=await until(()=>{const p=join(scratch,'DevToolsActivePort');return existsSync(p)?Number(readFileSync(p,'utf8').split('\n')[0]):null;},'Chrome debugging port',20000);
 const page=await until(async()=>{try{const list=await(await fetch('http://127.0.0.1:'+port+'/json/list')).json();return list.find(x=>x.type==='page'&&x.webSocketDebuggerUrl);}catch{return null;}},'Chrome page target',10000);
 await connect(page.webSocketDebuggerUrl);
 await cdp('Runtime.enable');await cdp('Page.enable');await cdp('Log.enable');await cdp('Network.enable');
 await cdp('Page.navigate',{url:pathToFileURL(observer).href});
 const first=await until(async()=>{try{const s=await snapshot();return(s?.stats?.frames>0||s?.fallback)?s:null;}catch{return null;}},'WebGL2 first frame');
 assert.equal(first.fallback,false,'3D renderer fell into fallback');
 assert.equal(first.stats.renderer,'three-webgl2','Canvas fallback is not WebGL2 evidence');
 assert.equal(first.stats.prepared,true,'Three.js shader preparation incomplete');
 assert.ok(first.stats.frames>0,'No real 3D frame');
 assert.equal(first.places,23,'Atlas source binding count drift');
 assert.equal(first.stats.siteLocations,23,'3D adapter lost an established place');
 assert.equal(first.sourceUnchanged,true,'Catalog mutation during setup');
 assert.notEqual(first.gpu,'UNAVAILABLE','No observed GPU renderer name');
 assert.doesNotMatch(first.gpu,/SwiftShader|Software Rasterizer|llvmpipe/i,'Software rendering is not physical GPU evidence');
 if(first.state.phase==='REVEALING')await click('#skipReveal');
 await until(async()=>{const s=await snapshot();return s?.state?.phase==='EXPLORING'&&s.stats.frames>1&&s;},'exploration readiness',12000);
 if(captureDir){await delay(1450);await captureCandidate('01-unlabeled-world.png',null);}
 // Start with real moving water; the history freeze must not pass trivially on a paused host.
 if(await evaluate('document.querySelector("#motionToggle").getAttribute("aria-pressed")')==='true')await click('#motionToggle');
 const moving=await snapshot();
 await until(async()=>{const s=await snapshot();return s.stats.waterTime>moving.stats.waterTime?s:null;},'ordinary water before history',12000);
 await click('#placesToggle');
 assert.equal(await evaluate('document.querySelectorAll("#placeList button[data-place]").length'),23);
 await click('[data-place="LOC-COUNTRY-CLUB-JACKSON"]');
 assert.equal(await evaluate('document.querySelector("#placeName").textContent'),'Country Club of Jackson');
 assert.equal(await evaluate('document.querySelector("#openHistory").hidden'),false,'Jackson history unreachable');
 // Let the place-flight camera settle before saving/restoring its historical viewpoint.
 await delay(2300);
 if(captureDir)await captureCandidate('02-country-club-jackson.png','LOC-COUNTRY-CLUB-JACKSON');
 const beforeHistory=await evaluate('__observerDebug.camera()');
 await click('#openHistory');
 assert.equal(await evaluate('document.querySelector("#historyDialog").open'),true);
 assert.ok(await evaluate('document.querySelectorAll("#historyEntries article").length')>0,'No location-exact source history');
 const frozen=await snapshot();await delay(550);
 assert.equal((await snapshot()).stats.waterTime,frozen.stats.waterTime,'Historical reader advanced water');
 await click('#historyBack');
 assert.equal(await evaluate('document.querySelector("#historyDialog").open'),false);
 assertHistoricalViewRestored(beforeHistory,await evaluate('__observerDebug.camera()'));
 await click('#inspectorWorld');
 assert.equal(await evaluate('document.querySelector("#inspector").hidden'),true);
 if(historyDir){
  // Compare the actual spectator UI against the embedded, immutable source catalog,
  // including places with no exact record. Never synthesize historical entries.
  const plan=await evaluate('(()=>{const c=JSON.parse(document.querySelector("#catalog").textContent);return c.locations.map(l=>({id:l.id,name:l.name,entries:c.history.events.filter(e=>e.locationId===l.id).map(e=>({id:e.id,heading:e.year+" · Week "+e.week+" · "+e.id}))}));})()');
  assert.equal(plan.length,23);
  assert.equal(new Set(plan.map(x=>x.id)).size,23);
  for(const place of plan){
   await click('#placesToggle');
   await click('[data-place="'+place.id+'"]');
   assert.equal((await snapshot()).state.locationId,place.id);
   assert.equal(await evaluate('document.querySelector("#placeName").textContent'),place.name);
   const available=place.entries.length>0;
   assert.equal(await evaluate('document.querySelector("#openHistory").hidden'),!available,place.id);
   assert.equal(await evaluate('document.querySelector("#historyAvailability").hidden'),available,place.id);
   const row={placeId:place.id,sourceEventIds:place.entries.map(e=>e.id),historyAvailable:available};
   if(available){
    await delay(2300);
    const before=await evaluate('__observerDebug.camera()');
    const live=await snapshot();
    await click('#openHistory');
    assert.equal(await evaluate('document.querySelector("#historyDialog").open'),true);
    assert.equal(await evaluate('document.querySelector("#historyPlace").textContent'),place.name);
    assert.deepEqual(await evaluate('Array.from(document.querySelectorAll("#historyEntries article h2"),e=>e.textContent)'),place.entries.map(e=>e.heading));
    const session=await evaluate('__observerHistoryDebug.session()');
    assert.equal(session.locationId,place.id);
    assert.equal(session.worldMutationAllowed,false);
    assert.equal(session.liveWeatherAllowed,false);
    assert.equal(session.publicationAuthorized,false);
    const frozen=await snapshot();await delay(350);
    const held=await snapshot();
    assert.equal(held.stats.waterTime,frozen.stats.waterTime,place.id+' history advanced water');
    await click('#historyBack');
    assert.equal(await evaluate('document.querySelector("#historyDialog").open'),false);
    assert.equal((await snapshot()).state.locationId,place.id);
    const after=await evaluate('__observerDebug.camera()');
    assertHistoricalViewRestored(before,after);
    const resumed=await until(async()=>{const q=await snapshot();return q.stats.waterTime>held.stats.waterTime?q:null;},place.id+' ordinary water resumed',12000);
    Object.assign(row,{cameraBefore:before,cameraAfter:after,waterBefore:live.stats.waterTime,waterFrozen:frozen.stats.waterTime,waterHeld:held.stats.waterTime,waterResumed:resumed.stats.waterTime,readOnly:true});
   }else{
    assert.equal(await evaluate('__observerHistoryDebug.session()'),null);
    assert.match(await evaluate('document.querySelector("#historyAvailability").textContent'),/No location-exact World Memory entry/);
   }
   await click('#inspectorWorld');
   assert.equal(await evaluate('document.querySelector("#inspector").hidden'),true);
   assert.equal((await snapshot()).sourceUnchanged,true);
   historySweep.push(row);
  }
 }
 if(captureDir){
  for(const [id,file,title] of [
   ['LOC-TDS-WATERFALL-TEMPLE','03-waterfall-temple.png','Podium Shadow Waterfall Temple'],
   ['LOC-MUD-DOGS-SWAMP','04-mud-dogs-swamp.png','Mud Dogs Swamp']
  ]){
   await click('#placesToggle');
   await click('[data-place="'+id+'"]');
   assert.equal(await evaluate('document.querySelector("#placeName").textContent'),title);
   await delay(1800);
   await captureCandidate(file,id);
   await click('#inspectorWorld');
  }
 }
 await click('#infoToggle');await click('#demoLoss');
 const calm=await evaluate('__observerDebug.weather()');
 assert.equal(calm.status,'GLOBAL_CALM','Verified loss did not calm the world');
 assert.deepEqual(calm.affectedZoneIds,[],'Global calm retained storm zones');
 // On reduced-motion hosts the default user preference is paused. Resume via the real control.
 if(await evaluate('document.querySelector("#motionToggle").getAttribute("aria-pressed")')==='true')await click('#motionToggle');
 const a=await snapshot();
 const b=await until(async()=>{const next=await snapshot();return next.stats.waterTime>a.stats.waterTime?next:null;},'ordinary water continued during global weather calm',12000);
 if(atlasDir){
  // Candidate contact sheet: capture every existing Atlas site, never create or unlock a site.
  // Source bindings, no-login journey, verified calm and ordinary water remain authoritative.
  atlasPlan=atlasViewPlan(await evaluate('__observerDebug.bindings()'));
  for(const place of atlasPlan){
   await click('#placesToggle');
   await click('[data-place="'+place.placeId+'"]');
   assert.equal(await evaluate('document.querySelector("#placeName").textContent'),place.name,'Source place title drift');
   await delay(1900);
   await captureCandidate(place.file,place.placeId,atlasCaptures);
   await click('#inspectorWorld');
  }
  verifyAtlasCandidateCaptures(atlasPlan,atlasCaptures);
  assert.equal((await snapshot()).sourceUnchanged,true,'Atlas-wide capture mutated source');
 }
 if(lightDir){
  // Evidence-only clock substitution in this isolated Chrome session.
  // The actual source-built host still computes its own Eastern-clock lighting.
  for(const {placeId,title,slug} of WETLAND_TEMPORAL_SITES){
   await click('#placesToggle');
   await click('[data-place="'+placeId+'"]');
   assert.equal(await evaluate('document.querySelector("#placeName").textContent'),title);
   await delay(3200);
   await click('#motionToggle');
   const held=(await snapshot()).stats.waterTime;
   const camera=await evaluate('__observerDebug.camera()');
   await evaluate('globalThis.__evidenceNativeDate=globalThis.Date');
   try{
    for(const [period,iso] of [['noon','2026-11-24T17:00:00.000Z'],['midnight','2026-11-24T05:00:00.000Z']]){
     const frames=(await snapshot()).stats.frames;
     await evaluate(`(()=>{const Native=globalThis.__evidenceNativeDate;const fixed=Native.parse(${JSON.stringify(iso)});globalThis.Date=class extends Native{constructor(...args){super(...(args.length?args:[fixed]));}static now(){return fixed;}};return new Date().toISOString();})()`);
     assert.equal(await evaluate('new Date().toISOString()'),iso);
     await until(async()=>{const q=await snapshot();return q.stats.frames>frames?q:null;},'synthetic Eastern clock frame '+period,12000);
     await delay(350);
     assert.equal((await snapshot()).stats.waterTime,held,'Water phase changed during lighting comparison');
     assertHistoricalViewRestored(camera,await evaluate('__observerDebug.camera()'));
     await captureCandidate(slug+'-'+period+'.png',placeId,lightCaptures);
     Object.assign(lightCaptures.at(-1),{period,syntheticUtc:iso,waterTime:held});
    }
   }finally{await evaluate('globalThis.Date=globalThis.__evidenceNativeDate;delete globalThis.__evidenceNativeDate;');}
   assert.notDeepEqual(lightCaptures.at(-1).bytes,lightCaptures.at(-2).bytes,'No visible clock response');
   await click('#motionToggle');
   await click('#inspectorWorld');
  }
  assert.equal(lightCaptures.length,6);
 }
 if(temporalDir){
  // Evidence-only: inspect two real Temple frames under global calm from the same settled viewpoint.
  await click('#placesToggle');
  await click('[data-place="LOC-TDS-WATERFALL-TEMPLE"]');
  assert.equal(await evaluate('document.querySelector("#placeName").textContent'),'Podium Shadow Waterfall Temple');
  await delay(3200);
  const cameraBefore=await evaluate('__observerDebug.camera()');
  const t0=(await snapshot()).stats.waterTime;
  await captureTemporalFrame('01-temple-global-calm.png',t0,'MOVING');
  await delay(1000);
  const t1=(await snapshot()).stats.waterTime;
  assert.ok(t1>t0+.2,'Real water time did not advance between physical GPU frames');
  await captureTemporalFrame('02-temple-global-calm.png',t1,'MOVING');
  assertHistoricalViewRestored(cameraBefore,await evaluate('__observerDebug.camera()'));
 }
 if(wetlandsDir){
  // The three existing Wetlands sites share one actual renderer/GPU and synthetic global calm.
  // Each site proves scene movement then exact visual hold under the explicit pause control.
  for(const {placeId,title,slug} of WETLAND_TEMPORAL_SITES){
   await click('#placesToggle');
   await click('[data-place="'+placeId+'"]');
   assert.equal(await evaluate('document.querySelector("#placeName").textContent'),title);
   await delay(3200);
   const originalCamera=await evaluate('__observerDebug.camera()');
   const t0=(await snapshot()).stats.waterTime;
   await captureTemporalFrame(slug+'-01-moving.png',t0,'MOVING',placeId,wetlandTemporalCaptures);
   await delay(1000);
   const t1=(await snapshot()).stats.waterTime;
   assert.ok(t1>t0+.2,'Ordinary water time failed to advance at '+placeId);
   await captureTemporalFrame(slug+'-02-moving.png',t1,'MOVING',placeId,wetlandTemporalCaptures);
   await click('#motionToggle');
   const held=(await snapshot()).stats.waterTime;
   await delay(600);
   assert.equal((await snapshot()).stats.waterTime,held,'Water advanced after pause at '+placeId);
   await captureTemporalFrame(slug+'-03-paused-a.png',held,'PAUSED',placeId,wetlandTemporalCaptures);
   await delay(750);
   assert.equal((await snapshot()).stats.waterTime,held,'Water advanced between paused frames at '+placeId);
   await captureTemporalFrame(slug+'-04-paused-b.png',held,'PAUSED',placeId,wetlandTemporalCaptures);
   verifyTemporalSceneSequence(wetlandTemporalCaptures.slice(-4));
   assertHistoricalViewRestored(originalCamera,await evaluate('__observerDebug.camera()'));
   await click('#motionToggle');
   await click('#inspectorWorld');
  }
  verifyWetlandsTemporalSequences(wetlandTemporalCaptures);
 }
 if(closeupDir){
  // Opt-in closer evidence uses the spectator's real WheelEvent handler via Chrome
  // CDP, not internal camera mutation. This is NOT isolated water-pixel attribution.
  for(const {placeId,title,slug} of WETLAND_TEMPORAL_SITES){
   await click('#placesToggle');
   await click('[data-place="'+placeId+'"]');
   assert.equal(await evaluate('document.querySelector("#placeName").textContent'),title);
   await delay(3200);
   const before=await evaluate('__observerDebug.camera()');
   assert.ok(Number.isFinite(before.distance)&&before.distance>0,'Invalid source closeup camera');
   const wheelDelta=-Math.min(440,Math.max(190,before.distance*4));
   await cdp('Input.dispatchMouseEvent',{type:'mouseWheel',x:500,y:405,deltaX:0,deltaY:wheelDelta});
   await delay(2800);
   const close=await evaluate('__observerDebug.camera()');
   assert.ok(close.distance<before.distance*.9&&close.distance>=5,
    'Real spectator camera did not approach candidate '+placeId);
   for(let j=0;j<3;j++)assert.ok(Math.abs(close.target[j]-before.target[j])<.02,
    'Closeup wheel moved source location anchor '+placeId);
   assert.ok(Math.abs(close.yaw-before.yaw)<.02&&Math.abs(close.pitch-before.pitch)<.02,
    'Closeup wheel altered camera orientation');
   const t0=(await snapshot()).stats.waterTime;
   await captureTemporalFrame(slug+'-close-01-moving.png',t0,'MOVING',placeId,wetlandCloseupCaptures);
   await delay(1050);
   const t1=(await snapshot()).stats.waterTime;
   assert.ok(t1>t0+.2,'Ordinary water did not advance in closeup '+placeId);
   await captureTemporalFrame(slug+'-close-02-moving.png',t1,'MOVING',placeId,wetlandCloseupCaptures);
   await click('#motionToggle');
   const held=(await snapshot()).stats.waterTime;
   await delay(650);
   assert.equal((await snapshot()).stats.waterTime,held,'Water advanced after closeup pause');
   await captureTemporalFrame(slug+'-close-03-paused-a.png',held,'PAUSED',placeId,wetlandCloseupCaptures);
   await delay(750);
   assert.equal((await snapshot()).stats.waterTime,held,'Water advanced between paused closeup frames');
   await captureTemporalFrame(slug+'-close-04-paused-b.png',held,'PAUSED',placeId,wetlandCloseupCaptures);
   verifyTemporalSceneSequence(wetlandCloseupCaptures.slice(-4));
   assertHistoricalViewRestored(close,await evaluate('__observerDebug.camera()'));
   closeupCameras.push({placeId,sourceCamera:before,observedCloseupCamera:close,wheelDelta});
   await click('#motionToggle');
   await click('#inspectorWorld');
  }
  verifyWetlandsTemporalSequences(wetlandCloseupCaptures);
 }
 await click('#motionToggle');
 const stopped=await snapshot();await delay(600);
 assert.equal((await snapshot()).stats.waterTime,stopped.stats.waterTime,'Explicit pause did not freeze water');
 if(temporalDir){
  // An unchanged water clock alone cannot establish visual freeze. Retain actual GPU pixels.
  await captureTemporalFrame('03-temple-paused-a.png',stopped.stats.waterTime,'PAUSED');
  await delay(750);
  assert.equal((await snapshot()).stats.waterTime,stopped.stats.waterTime,'Water advanced between paused GPU frames');
  await captureTemporalFrame('04-temple-paused-b.png',stopped.stats.waterTime,'PAUSED');
  verifyTemporalSceneSequence(temporalCaptures);
  await click('#inspectorWorld');
 }
 if(dprCheck){
  // Change display density only, while ordinary motion is explicitly paused.
  // This exposes stale backing buffers even when the CSS viewport has not resized.
  await click('#placesToggle');
  await click('[data-place="LOC-TDS-WATERFALL-TEMPLE"]');
  await delay(dprDir?3200:600);
  const camera=await evaluate('__observerDebug.camera()');
  dprCamera=camera;
  const dimensions=await evaluate('({width:innerWidth,height:innerHeight,cssWidth:document.querySelector("#world").clientWidth,cssHeight:document.querySelector("#world").clientHeight})');
  const held=(await snapshot()).stats.waterTime;
  const syntheticUtc='2026-11-24T17:00:00.000Z';
  if(dprDir)await evaluate(`(()=>{const Native=globalThis.Date;globalThis.__dprNativeDate=Native;const fixed=Native.parse(${JSON.stringify(syntheticUtc)});globalThis.Date=class extends Native{constructor(...args){super(...(args.length?args:[fixed]));}static now(){return fixed;}};})()`);
  try{
   // The paused renderer intentionally skips unchanged signatures. Settle the
   // clock through two animation callbacks before capturing the baseline; only
   // actual backing-buffer transitions must advance the render counter.
   if(dprDir)await evaluate('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(()=>resolve(true))))');
   for(const deviceScaleFactor of [1,2,1]){
    const beforeDensity=(await snapshot()).stats;
    await cdp('Emulation.setDeviceMetricsOverride',{width:dimensions.width,height:dimensions.height,deviceScaleFactor,mobile:false});
    const expected=Math.min(deviceScaleFactor,dimensions.cssWidth<700?1.25:1.5);
    const observation=await until(async()=>{
     const o=await evaluate('(()=>{const c=document.querySelector("#world"),s=__observerDebug.stats();return {cssWidth:c.clientWidth,cssHeight:c.clientHeight,bufferWidth:c.width,bufferHeight:c.height,devicePixelRatio,pixelRatio:s.pixelRatio,waterTime:s.waterTime,renderer:s.renderer,frames:s.frames};})()');
     return o.devicePixelRatio===deviceScaleFactor&&o.pixelRatio===expected&&o.bufferWidth===Math.floor(dimensions.cssWidth*expected)&&o.bufferHeight===Math.floor(dimensions.cssHeight*expected)?o:null;
    },'display density transition '+deviceScaleFactor,12000);
    assert.equal(observation.cssWidth,dimensions.cssWidth);
    assert.equal(observation.cssHeight,dimensions.cssHeight);
    assert.equal(observation.waterTime,held,'Display density change advanced paused water');
    assert.equal(observation.renderer,'three-webgl2');
    assertHistoricalViewRestored(camera,await evaluate('__observerDebug.camera()'));
    dprObservations.push(observation);
    if(dprDir){
     if(beforeDensity.pixelRatio!==expected)assert.ok(observation.frames>beforeDensity.frames,'Density changed without a rendered frame');
     assert.equal((await snapshot()).state.locationId,'LOC-TDS-WATERFALL-TEMPLE');
     await delay(350);
     assert.equal(await evaluate('new Date().toISOString()'),syntheticUtc);
     assert.equal((await snapshot()).stats.waterTime,held);
     assertHistoricalViewRestored(camera,await evaluate('__observerDebug.camera()'));
     const {data}=await cdp('Page.captureScreenshot',{format:'png',fromSurface:true,captureBeyondViewport:false});
     const bytes=Buffer.from(data,'base64');
     assert.equal(bytes.subarray(0,8).toString('hex'),'89504e470d0a1a0a');
     const width=bytes.readUInt32BE(16),height=bytes.readUInt32BE(20);
     assert.equal(width,dimensions.width*deviceScaleFactor);
     assert.equal(height,dimensions.height*deviceScaleFactor);
     dprCaptures.push({file:'temple-'+String(dprCaptures.length+1)+'-dpr-'+deviceScaleFactor+'.png',
      bytes,width,height,syntheticUtc,observation});
    }
   }
  }finally{
   await cdp('Emulation.clearDeviceMetricsOverride');
   if(dprDir)await evaluate('globalThis.Date=globalThis.__dprNativeDate;delete globalThis.__dprNativeDate;');
  }
  assert.equal(dprObservations.length,3);
 }
 assert.equal((await snapshot()).sourceUnchanged,true,'Canonical source mutated during journey');
 const errors=[...runtimeExceptions,...consoleErrors].filter(x=>!/favicon\.ico/.test(x));
 assert.deepEqual(errors,[],'Browser/GLSL errors: '+errors.join(' | '));
 assert.deepEqual(externalRequests,[],'External network requests from offline observer');
 if(dprDir){
  assert.equal(dprCaptures.length,3);
  mkdirSync(dprDir,{recursive:false});
  for(const shot of dprCaptures)writeFileSync(join(dprDir,shot.file),shot.bytes,{flag:'wx'});
  const captures=dprCaptures.map(({file,bytes,width,height,syntheticUtc,observation})=>({
   file,width,height,syntheticUtc,observation,bytes:bytes.length,sha256:createHash('sha256').update(bytes).digest('hex')
  }));
  writeFileSync(join(dprDir,'manifest.json'),JSON.stringify({
   status:'CANDIDATE_NOT_APPROVED',publicationAuthorized:false,
   evidenceType:'PHYSICAL_GPU_EMULATED_DENSITY_PAUSED_TEMPLE_SCENE',
   placeId:'LOC-TDS-WATERFALL-TEMPLE',
   sourceRevision:await evaluate('JSON.parse(document.querySelector("#catalog").textContent).sourceRevision'),
   stateAsOf:await evaluate('JSON.parse(document.querySelector("#catalog").textContent).stateAsOf'),
   observerSha256:createHash('sha256').update(readFileSync(observer)).digest('hex'),
   renderer:first.stats.renderer,gpu:first.gpu,weatherStatus:calm.status,
   camera:dprCamera,sourceUnchanged:true,ordinaryWaterAdvanced:true,explicitPause:true,
   browserExceptions:runtimeExceptions.length,consoleErrors:consoleErrors.length,externalRequests:externalRequests.length,
   captures
  },null,2)+'\n',{flag:'wx'});
  writeFileSync(join(dprDir,'inspection.html'), '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Temple density evidence</title><style>body{font:16px system-ui;background:#15191d;color:#eee;margin:24px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}img{width:100%;height:auto}a{color:#addaff}figure{margin:0}</style><h1>Waterfall Temple — display-density inspection</h1><p>Same paused source location, camera and synthetic Eastern noon. Physical GPU with emulated device density; not physical-phone or isolated spray-pixel proof. Original screenshots are retained at their native pixel dimensions.</p><main>'+captures.map(c=>'<figure><a href="'+c.file+'"><img src="'+c.file+'" alt="Temple at device DPR '+c.observation.devicePixelRatio+'"></a><figcaption>Device DPR '+c.observation.devicePixelRatio+' · renderer ratio '+c.observation.pixelRatio+' · '+c.width+' × '+c.height+' pixels</figcaption></figure>').join('')+'</main><p><a href="manifest.json">Exact source and capture manifest</a></p></html>',{flag:'wx'});
 }
 if(historyDir){
  assert.equal(historySweep.length,23);
  mkdirSync(historyDir,{recursive:false});
  writeFileSync(join(historyDir,'manifest.json'),JSON.stringify({
   status:'CANDIDATE_NOT_APPROVED',publicationAuthorized:false,
   evidenceType:'PHYSICAL_GPU_SOURCE_BOUND_HISTORY_AVAILABILITY_AND_RETURN',
   sourceRevision:await evaluate('JSON.parse(document.querySelector("#catalog").textContent).sourceRevision'),
   stateAsOf:await evaluate('JSON.parse(document.querySelector("#catalog").textContent).stateAsOf'),
   observerSha256:createHash('sha256').update(readFileSync(observer)).digest('hex'),
   renderer:first.stats.renderer,gpu:first.gpu,weatherStatus:calm.status,
   sourceUnchanged:true,ordinaryWaterAdvanced:true,explicitPause:true,
   browserExceptions:runtimeExceptions.length,consoleErrors:consoleErrors.length,externalRequests:externalRequests.length,
   places:historySweep
  },null,2)+'\n',{flag:'wx'});
 }
 if(temporalDir){
  assert.equal(temporalCaptures.length,4,'Missing moving/paused Waterfall Temple temporal coverage');
  mkdirSync(temporalDir,{recursive:true});
  for(const shot of temporalCaptures)writeFileSync(join(temporalDir,shot.file),shot.bytes,{flag:'wx'});
  writeFileSync(join(temporalDir,'manifest.json'),JSON.stringify({
   status:'CANDIDATE_NOT_APPROVED',publicationAuthorized:false,
   evidenceType:'PHYSICAL_GPU_MOVING_AND_PAUSED_SCENE_FRAMES_NOT_ISOLATED_WATER_PIXEL_PROOF',
   syntheticScenario:'verified El Nino loss to GLOBAL_CALM',
   weatherStatus:calm.status,renderer:first.stats.renderer,gpu:first.gpu,
   sourceRevision:await evaluate('JSON.parse(document.querySelector("#catalog").textContent).sourceRevision'),
   placeId:'LOC-TDS-WATERFALL-TEMPLE',cameraViewHeld:true,
   ordinaryWaterAdvanced:true,pausedSceneHashesEqual:true,sourceUnchanged:true,
   captures:temporalCaptures.map(({file,waterTime,motionState,frames,bytes,width,height})=>
    ({file,waterTime,motionState,frames,bytes:bytes.length,width,height,sha256:createHash('sha256').update(bytes).digest('hex')}))
  },null,2)+'\n',{flag:'wx'});
 }
 if(wetlandsDir){
  const sites=verifyWetlandsTemporalSequences(wetlandTemporalCaptures);
  assert.equal((await snapshot()).sourceUnchanged,true,'Source changed before Wetlands evidence emission');
  mkdirSync(wetlandsDir,{recursive:true});
  for(const shot of wetlandTemporalCaptures)writeFileSync(join(wetlandsDir,shot.file),shot.bytes,{flag:'wx'});
  writeFileSync(join(wetlandsDir,'manifest.json'),JSON.stringify({
   status:'CANDIDATE_NOT_APPROVED',publicationAuthorized:false,
   evidenceType:'PHYSICAL_GPU_THREE_SITE_MOVING_AND_PAUSED_SCENE_FRAMES_NOT_ISOLATED_WATER_PIXEL_PROOF',
   syntheticScenario:'verified El Nino loss to GLOBAL_CALM',weatherStatus:calm.status,
   renderer:first.stats.renderer,gpu:first.gpu,
   sourceRevision:await evaluate('JSON.parse(document.querySelector("#catalog").textContent).sourceRevision'),
   cameraViewHeld:true,ordinaryWaterAdvanced:true,pausedSceneHashesEqual:true,sourceUnchanged:true,
   sites,captures:wetlandTemporalCaptures.map(({file,placeId,waterTime,motionState,frames,bytes,width,height})=>
    ({file,placeId,waterTime,motionState,frames,bytes:bytes.length,width,height,sha256:createHash('sha256').update(bytes).digest('hex')}))
  },null,2)+'\n',{flag:'wx'});
 }
 if(closeupDir){
  const sites=verifyWetlandsTemporalSequences(wetlandCloseupCaptures);
  assert.equal(closeupCameras.length,WETLAND_TEMPORAL_SITES.length,'Missing closeup camera proof');
  assert.equal((await snapshot()).sourceUnchanged,true,'Source changed before closeup evidence emission');
  mkdirSync(closeupDir,{recursive:true});
  for(const shot of wetlandCloseupCaptures)writeFileSync(join(closeupDir,shot.file),shot.bytes,{flag:'wx'});
  writeFileSync(join(closeupDir,'manifest.json'),JSON.stringify({
   status:'CANDIDATE_NOT_APPROVED',publicationAuthorized:false,
   evidenceType:'PHYSICAL_GPU_THREE_SITE_CLOSE_PERSPECTIVE_MOVING_AND_PAUSED_WHOLE_SCENE_FRAMES_NOT_ISOLATED_WATER_PIXEL_PROOF',
   syntheticScenario:'verified El Nino loss to GLOBAL_CALM',weatherStatus:calm.status,
   renderer:first.stats.renderer,gpu:first.gpu,
   sourceRevision:await evaluate('JSON.parse(document.querySelector("#catalog").textContent).sourceRevision'),
   originalHistoryJourneyPassed:true,allCurrentPlacesVisible:first.places===23,
   cameraApproachVia:'Chrome CDP mouseWheel on spectator canvas event handler',
   cameraViewHeld:true,ordinaryWaterAdvanced:true,pausedSceneHashesEqual:true,sourceUnchanged:true,
   sites,closeupCameras,
   captures:wetlandCloseupCaptures.map(({file,placeId,waterTime,motionState,frames,bytes,width,height})=>
    ({file,placeId,waterTime,motionState,frames,bytes:bytes.length,width,height,sha256:createHash('sha256').update(bytes).digest('hex')}))
  },null,2)+'\n',{flag:'wx'});
 }
 if(atlasDir){
  // Emit nothing unless all 23 physical-GPU frames and source IDs validate.
  const coverage=verifyAtlasCandidateCaptures(atlasPlan,atlasCaptures);
  assert.equal((await snapshot()).sourceUnchanged,true,'Source changed before Atlas evidence emission');
  const sourceRevision=await evaluate('JSON.parse(document.querySelector("#catalog").textContent).sourceRevision');
  const stateAsOf=await evaluate('JSON.parse(document.querySelector("#catalog").textContent).stateAsOf');
  mkdirSync(atlasDir,{recursive:true});
  for(const shot of atlasCaptures)writeFileSync(join(atlasDir,shot.file),shot.bytes,{flag:'wx'});
  writeFileSync(join(atlasDir,'manifest.json'),JSON.stringify({
   status:'CANDIDATE_NOT_APPROVED',publicationAuthorized:false,
   evidenceType:'PHYSICAL_GPU_SOURCE_ATLAS_23_PLACE_STILLS_NOT_ART_ACCEPTANCE_OR_WATER_PIXEL_PROOF',
   sourceRevision,stateAsOf,renderer:first.stats.renderer,gpu:first.gpu,
   syntheticScenario:'verified El Nino loss to GLOBAL_CALM',weatherStatus:calm.status,
   originalHistoryJourneyPassed:true,ordinaryWaterAdvanced:true,sourceUnchanged:true,coverage,
   captures:atlasCaptures.map(({file,placeId,frames,bytes,width,height,camera})=>
    ({file,placeId,frames,bytes:bytes.length,width,height,camera,sha256:createHash('sha256').update(bytes).digest('hex')}))
  },null,2)+'\n',{flag:'wx'});
  writeFileSync(join(atlasDir,'inspection.html'),
   atlasContactSheetHtml(atlasPlan,{sourceRevision,stateAsOf,gpu:first.gpu,renderer:first.stats.renderer}),
   {flag:'wx'});
 }
 if(lightDir){
  mkdirSync(lightDir,{recursive:true});
  for(const shot of lightCaptures)writeFileSync(join(lightDir,shot.file),shot.bytes,{flag:'wx'});
  writeFileSync(join(lightDir,'manifest.json'),JSON.stringify({
   status:'CANDIDATE_NOT_APPROVED',publicationAuthorized:false,
   evidenceType:'PHYSICAL_GPU_SYNTHETIC_EASTERN_NOON_MIDNIGHT_WHOLE_SCENE_COMPARISON',
   sourceRevision:await evaluate('JSON.parse(document.querySelector("#catalog").textContent).sourceRevision'),
   renderer:first.stats.renderer,gpu:first.gpu,weatherStatus:calm.status,
   syntheticClock:true,cameraViewHeld:true,waterPhaseHeld:true,ordinaryWaterAdvanced:true,
   originalHistoryJourneyPassed:true,sourceUnchanged:true,
   captures:lightCaptures.map(({file,placeId,period,syntheticUtc,waterTime,frames,bytes,width,height,camera})=>
    ({file,placeId,period,syntheticUtc,waterTime,frames,bytes:bytes.length,width,height,camera,sha256:createHash('sha256').update(bytes).digest('hex')}))
  },null,2)+'\n',{flag:'wx'});
 }
 if(captureDir){
  assert.equal(captured.length,4,'Missing candidate scene coverage');
  mkdirSync(captureDir,{recursive:true});
  for(const capture of captured)writeFileSync(join(captureDir,capture.file),capture.bytes,{flag:'wx'});
  const manifest={
   status:'CANDIDATE_NOT_APPROVED',publicationAuthorized:false,
   renderer:first.stats.renderer,gpu:first.gpu,
   sourceRevision:await evaluate('JSON.parse(document.querySelector("#catalog").textContent).sourceRevision'),
   sourcesUnchanged:true,captures:captured.map(({file,placeId,frames,bytes,width,height})=>({file,placeId,frames,bytes:bytes.length,width,height,sha256:createHash('sha256').update(bytes).digest('hex')}))
  };
  writeFileSync(join(captureDir,'manifest.json'),JSON.stringify(manifest,null,2)+'\n',{flag:'wx'});
 }
 console.log(JSON.stringify({
  result:'WEBGL2_JOURNEY_SMOKE_PASS',
  sourceRevision:await evaluate('JSON.parse(document.querySelector("#catalog").textContent).sourceRevision'),
  renderer:first.stats.renderer,gpu:first.gpu,frames:b.stats.frames,places:first.places,
  jacksonHistory:await evaluate('__observerHistoryDebug.entries("LOC-COUNTRY-CLUB-JACKSON").length'),
  weather:calm.status,ordinaryWaterAdvanced:true,historicalPause:true,explicitPause:true,sourceUnchanged:true,
  browserExceptions:runtimeExceptions.length,consoleErrors:consoleErrors.length,externalRequests:externalRequests.length,
  displayDensityObservations:dprObservations,candidateCaptures:captured.map(c=>c.file),temporalCaptures:temporalCaptures.map(c=>c.file),wetlandsTemporalCaptures:wetlandTemporalCaptures.map(c=>c.file),wetlandsCloseupCaptures:wetlandCloseupCaptures.map(c=>c.file),atlasViewCaptures:atlasCaptures.map(c=>c.file)
 }));
}
try{await main();}
catch(e){console.error('WEBGL2_JOURNEY_SMOKE_FAIL',e.stack||String(e));process.exitCode=1;}
finally{
 for(const p of pending.values())p.fail(Error('CLOSED'));pending.clear();
 try{ws?.close();}catch{}
 if(child&&!child.killed){const done=new Promise(r=>child.once('exit',r));child.kill('SIGTERM');await Promise.race([done,delay(2000)]);if(child.exitCode===null&&child.signalCode===null)child.kill('SIGKILL');}
 try{rmSync(scratch,{recursive:true,force:true});}catch{}
}
