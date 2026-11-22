#!/usr/bin/env node
/** Optional real-GPU smoke for the source-built unpublished observer.
 * Requires Node 22+ and installed Chrome. No new package, API, or service.
 * Usage: node tools/webgl2-journey-smoke.mjs /absolute/path/to/observer.html
 */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {spawn} from 'node:child_process';
import {existsSync,mkdirSync,mkdtempSync,readFileSync,rmSync,writeFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import {pathToFileURL} from 'node:url';

const captureOption=process.argv.indexOf('--capture-dir');
const temporalOption=process.argv.indexOf('--temporal-dir');
assert.ok((captureOption<0&&temporalOption<0&&process.argv.length===3)
 ||(process.argv.length===5&&((captureOption===3&&temporalOption<0)||(temporalOption===3&&captureOption<0))),
 'Optional capture argument: --capture-dir or --temporal-dir /new/private/evidence/directory');
const captureDir=captureOption<0?null:resolve(process.argv[4]);
const temporalDir=temporalOption<0?null:resolve(process.argv[4]);
if(captureDir)assert.ok(!existsSync(captureDir),'CAPTURE_DIRECTORY_EXISTS: refusal to overwrite evidence');
if(temporalDir)assert.ok(!existsSync(temporalDir),'TEMPORAL_DIRECTORY_EXISTS: refusal to overwrite evidence');
const captured=[],temporalCaptures=[];
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
async function captureCandidate(file,placeId){
 if(!captureDir)return;
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
 captured.push({file,placeId,frames:s.stats.frames,bytes,width,height});
}
async function captureTemporalFrame(file,waterTime){
 const s=await snapshot();
 assert.equal(s.stats.renderer,'three-webgl2','Temporal evidence requires physical WebGL2');
 assert.equal(s.state.locationId,'LOC-TDS-WATERFALL-TEMPLE','Temporal evidence changed source site');
 assert.ok(s.stats.frames>0&&s.sourceUnchanged&&!s.fallback,'Invalid temporal capture');
 const {data}=await cdp('Page.captureScreenshot',{format:'png',fromSurface:true,captureBeyondViewport:false});
 const bytes=Buffer.from(data,'base64');
 assert.equal(bytes.subarray(0,8).toString('hex'),'89504e470d0a1a0a');
 const width=bytes.readUInt32BE(16),height=bytes.readUInt32BE(20);
 assert.ok(width>=1000&&height>=600,'Unexpected temporal screenshot dimensions');
 temporalCaptures.push({file,waterTime,frames:s.stats.frames,bytes,width,height});
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
 if(temporalDir){
  // Evidence-only: inspect two real Temple frames under global calm from the same settled viewpoint.
  await click('#placesToggle');
  await click('[data-place="LOC-TDS-WATERFALL-TEMPLE"]');
  assert.equal(await evaluate('document.querySelector("#placeName").textContent'),'Podium Shadow Waterfall Temple');
  await delay(3200);
  const cameraBefore=await evaluate('__observerDebug.camera()');
  const t0=(await snapshot()).stats.waterTime;
  await captureTemporalFrame('01-temple-global-calm.png',t0);
  await delay(1000);
  const t1=(await snapshot()).stats.waterTime;
  assert.ok(t1>t0+.2,'Real water time did not advance between physical GPU frames');
  await captureTemporalFrame('02-temple-global-calm.png',t1);
  assertHistoricalViewRestored(cameraBefore,await evaluate('__observerDebug.camera()'));
  assert.notEqual(createHash('sha256').update(temporalCaptures[0].bytes).digest('hex'),
   createHash('sha256').update(temporalCaptures[1].bytes).digest('hex'),
   'GPU scene frames unexpectedly byte-identical during ordinary motion');
  await click('#inspectorWorld');
 }
 await click('#motionToggle');
 const stopped=await snapshot();await delay(600);
 assert.equal((await snapshot()).stats.waterTime,stopped.stats.waterTime,'Explicit pause did not freeze water');
 assert.equal((await snapshot()).sourceUnchanged,true,'Canonical source mutated during journey');
 const errors=[...runtimeExceptions,...consoleErrors].filter(x=>!/favicon\.ico/.test(x));
 assert.deepEqual(errors,[],'Browser/GLSL errors: '+errors.join(' | '));
 assert.deepEqual(externalRequests,[],'External network requests from offline observer');
 if(temporalDir){
  assert.equal(temporalCaptures.length,2,'Missing Waterfall Temple temporal coverage');
  mkdirSync(temporalDir,{recursive:true});
  for(const shot of temporalCaptures)writeFileSync(join(temporalDir,shot.file),shot.bytes,{flag:'wx'});
  writeFileSync(join(temporalDir,'manifest.json'),JSON.stringify({
   status:'CANDIDATE_NOT_APPROVED',publicationAuthorized:false,
   evidenceType:'PHYSICAL_GPU_TEMPORAL_SCENE_FRAMES_NOT_ISOLATED_WATER_PIXEL_PROOF',
   syntheticScenario:'verified El Nino loss to GLOBAL_CALM',
   weatherStatus:calm.status,renderer:first.stats.renderer,gpu:first.gpu,
   sourceRevision:await evaluate('JSON.parse(document.querySelector("#catalog").textContent).sourceRevision'),
   placeId:'LOC-TDS-WATERFALL-TEMPLE',cameraViewHeld:true,
   ordinaryWaterAdvanced:true,sourceUnchanged:true,
   captures:temporalCaptures.map(({file,waterTime,frames,bytes,width,height})=>
    ({file,waterTime,frames,bytes:bytes.length,width,height,sha256:createHash('sha256').update(bytes).digest('hex')}))
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
  candidateCaptures:captured.map(c=>c.file),temporalCaptures:temporalCaptures.map(c=>c.file)
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
