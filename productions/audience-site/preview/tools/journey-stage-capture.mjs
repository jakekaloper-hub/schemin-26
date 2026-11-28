#!/usr/bin/env node
/**
 * Opt-in physical-GPU screenshot evidence for the existing, unpublished
 * world -> place -> recorded history -> same place -> world journey.
 * No publishing, canon writes, external requests or third-party dependencies.
 * Usage: node journey-stage-capture.mjs /path/observer.html /new/evidence/dir EXPECTED_SOURCE_SHA
 */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {spawn,execFileSync} from 'node:child_process';
import {existsSync,mkdirSync,mkdtempSync,readFileSync,rmSync,writeFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {resolve,join} from 'node:path';
import {pathToFileURL} from 'node:url';

const [observerArg,outArg,expectedSha]=process.argv.slice(2);
assert.ok(observerArg&&outArg&&/^[0-9a-f]{40}$/.test(expectedSha||''),'Usage: observer.html NEW_OUTPUT_DIR EXPECTED_SOURCE_SHA');
const observer=resolve(observerArg),out=resolve(outArg);
assert.ok(existsSync(observer),'SOURCE_OBSERVER_MISSING');
assert.ok(!existsSync(out),'REFUSE_TO_OVERWRITE_EVIDENCE');
const repo=resolve(import.meta.dirname,'../../../..');
const sourceSha=execFileSync('git',['rev-parse','HEAD'],{cwd:repo,encoding:'utf8'}).trim();
assert.equal(sourceSha,expectedSha,'SOURCE_HEAD_DRIFT');
const chrome=process.env.CHROME_BIN||(process.platform==='darwin'
 ? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome':'/usr/bin/google-chrome');
assert.ok(existsSync(chrome),'PHYSICAL_CHROME_UNAVAILABLE');
const scratch=mkdtempSync(join(tmpdir(),'commonwealth-journey-stage-'));
const pending=new Map(),errors=[],externalRequests=[],frames=[];
let browser=null,ws=null,nextId=0,historyCount=0,historyCamera=null,returnCamera=null,calm=null;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function until(fn,what,timeout=45000){
 const deadline=Date.now()+timeout;
 while(Date.now()<deadline){const value=await fn();if(value)return value;await sleep(170);}
 throw Error('TIMEOUT_'+what);
}
function cdp(method,params={}){
 return new Promise((ok,fail)=>{
  const id=++nextId;pending.set(id,{ok,fail});
  ws.send(JSON.stringify({id,method,params}));
 });
}
async function evaluate(expression){
 const value=await cdp('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true,userGesture:true});
 if(value.exceptionDetails)throw Error('EVAL_ERROR: '+(value.exceptionDetails.exception?.description||value.exceptionDetails.text));
 return value.result?.value;
}
const click=selector=>evaluate('(()=>{const el=document.querySelector('+JSON.stringify(selector)+');if(!el||el.hidden||el.disabled)throw Error("MISSING_CONTROL");el.click();return true})()');
const state=()=>evaluate('(()=>({state:__observerDebug.state(),stats:__observerDebug.stats(),camera:__observerDebug.camera(),places:__observerDebug.bindings().length,unchanged:__observerDebug.sourceUnchanged(),fallback:!document.querySelector("#fallback").hidden}))()');
function sameCamera(a,b){
 const left=[...a.target,a.distance,a.yaw,a.pitch],right=[...b.target,b.distance,b.yaw,b.pitch];
 assert.equal(left.length,6);assert.equal(right.length,6);
 for(let i=0;i<6;i++)assert.ok(Number.isFinite(left[i])&&Number.isFinite(right[i])
  &&Math.abs(left[i]-right[i])<=(i<4?.002:.00002),'RETURN_CAMERA_CHANGED_AT_'+i);
}
async function record(file,stage,placeId=null){
 const s=await state();
 assert.equal(s.stats.renderer,'three-webgl2','GPU_RENDERER_NOT_ACTIVE');
 assert.ok(s.stats.frames>0&&s.unchanged&&!s.fallback,'INVALID_OBSERVER_STATE');
 assert.equal(s.places,23,'ATLAS_SITE_COUNT_CHANGED');
 assert.equal(s.state.locationId||null,placeId,'WRONG_STAGE_LOCATION');
 const data=(await cdp('Page.captureScreenshot',{format:'png',fromSurface:true,captureBeyondViewport:false})).data;
 const bytes=Buffer.from(data,'base64');
 assert.equal(bytes.subarray(0,8).toString('hex'),'89504e470d0a1a0a','BAD_PNG');
 const width=bytes.readUInt32BE(16),height=bytes.readUInt32BE(20);
 assert.ok(width>=1000&&height>=600,'BAD_CAPTURE_RESOLUTION');
 frames.push({file,stage,locationId:placeId,camera:s.camera,waterTime:s.stats.waterTime,
  width,height,sha256:createHash('sha256').update(bytes).digest('hex'),bytes});
}
async function main(){
 browser=spawn(chrome,['--headless=new','--no-first-run','--no-default-browser-check',
  '--disable-background-networking','--disable-extensions','--no-proxy-server',
  '--remote-debugging-port=0','--user-data-dir='+scratch,
  '--window-size=1440,900','--force-device-scale-factor=1',
  '--force-prefers-reduced-motion=no-preference','about:blank'],{stdio:'ignore'});
 const port=await until(()=>{const file=join(scratch,'DevToolsActivePort');return existsSync(file)?+readFileSync(file,'utf8').split('\n')[0]:null;},'CHROME_PORT',20000);
 const page=await until(async()=>{try{const rows=await(await fetch('http://127.0.0.1:'+port+'/json/list')).json();return rows.find(row=>row.type==='page'&&row.webSocketDebuggerUrl);}catch{return null;}},'CHROME_PAGE',12000);
 ws=new WebSocket(page.webSocketDebuggerUrl);
 await new Promise((ok,fail)=>{ws.addEventListener('open',ok,{once:true});ws.addEventListener('error',()=>fail(Error('CDP_CONNECT_FAILED')),{once:true});});
 ws.addEventListener('message',e=>{
  const m=JSON.parse(e.data);
  if(m.id){const p=pending.get(m.id);if(!p)return;pending.delete(m.id);if(m.error)p.fail(Error(JSON.stringify(m.error)));else p.ok(m.result);return;}
  if(m.method==='Network.requestWillBeSent'&&/^https?:|^wss?:/.test(m.params?.request?.url||''))externalRequests.push(m.params.request.url);
  if(m.method==='Runtime.exceptionThrown')errors.push(m.params?.exceptionDetails?.text||'Runtime exception');
  if(m.method==='Runtime.consoleAPICalled'&&m.params?.type==='error')errors.push(m.params.args?.map(x=>x.value||x.description||'').join(' '));
  if(m.method==='Log.entryAdded'&&m.params?.entry?.level==='error'&&!/favicon\.ico/.test(m.params.entry.url||''))errors.push(m.params.entry.text);
 });
 for(const method of ['Runtime.enable','Page.enable','Network.enable','Log.enable'])await cdp(method);
 await cdp('Page.navigate',{url:pathToFileURL(observer).href});
 const ready=await until(async()=>{try{const s=await state();return s?.stats?.frames>0?s:null;}catch{return null;}},'FIRST_GPU_FRAME');
 assert.equal(ready.stats.renderer,'three-webgl2','CANVAS_IS_NOT_GPU_EVIDENCE');
 assert.equal(ready.stats.prepared,true,'THREE_SHADER_NOT_READY');
 assert.ok(ready.stats.siteLocations===23&&ready.places===23&&ready.unchanged&&!ready.fallback,'SOURCE_DRIFT');
 assert.doesNotMatch(ready.stats.gpuRenderer||'',/SwiftShader|Software Rasterizer|llvmpipe|UNAVAILABLE/i,'SOFTWARE_RENDERER');
 if(ready.state.phase==='REVEALING')await click('#skipReveal');
 await until(async()=>{const s=await state();return s.state.phase==='EXPLORING'&&s.stats.frames>1?s:null;},'EXPLORING',15000);
 // Begin ordinary water motion before testing historical replay isolation.
 if(await evaluate('document.querySelector("#motionToggle").getAttribute("aria-pressed")')==='true')await click('#motionToggle');
 const initialWater=(await state()).stats.waterTime;
 await until(async()=>{const s=await state();return s.stats.waterTime>initialWater?s:null;},'MOVING_WATER_BEFORE_HISTORY',12000);
 await sleep(850);
 await record('01-unlabeled-world.png','WORLD',null);
 const catalogue=await evaluate('(()=>{const c=JSON.parse(document.querySelector("#catalog").textContent);return {asOf:c.stateAsOf,historyStatus:c.history?.status,publicationAuthorized:c.publicationAuthorized??false}})()');
 await click('#placesToggle');
 assert.equal(await evaluate('document.querySelectorAll("#placeList button[data-place]").length'),23,'HIDDEN_ATLAS_PLACES');
 await click('[data-place="LOC-COUNTRY-CLUB-JACKSON"]');
 await until(async()=>{const s=await state();return s.state.locationId==='LOC-COUNTRY-CLUB-JACKSON'?s:null;},'JACKSON');
 assert.equal(await evaluate('document.querySelector("#placeName").textContent'),'Country Club of Jackson');
 assert.equal(await evaluate('document.querySelector("#openHistory").hidden'),false);
 await sleep(2300);
 await record('02-country-club-jackson.png','PLACE','LOC-COUNTRY-CLUB-JACKSON');
 historyCamera=await evaluate('__observerDebug.camera()');
 await click('#openHistory');
 assert.equal(await evaluate('document.querySelector("#historyDialog").open'),true,'HISTORY_NOT_OPEN');
 historyCount=await evaluate('document.querySelectorAll("#historyEntries article").length');
 assert.ok(historyCount>0,'NO_LOCATION_EXACT_HISTORY');
 const frozen=await state();
 assert.ok(frozen.stats.waterTime>0,'HISTORY_MUST_START_WITH_MOVING_WATER');
 await sleep(350);
 const frozenLater=await state();
 assert.equal(frozenLater.stats.waterTime,frozen.stats.waterTime,'HISTORY_REPLAY_NOT_ISOLATED');
 await record('03-recorded-jackson-history.png','HISTORY','LOC-COUNTRY-CLUB-JACKSON');
 await click('#historyBack');
 assert.equal(await evaluate('document.querySelector("#historyDialog").open'),false);
 returnCamera=await evaluate('__observerDebug.camera()');
 sameCamera(historyCamera,returnCamera);
 await until(async()=>{const s=await state();return s.stats.waterTime>frozen.stats.waterTime?s:null;},'ORDINARY_WATER_RESUMES_AFTER_HISTORY',12000);
 await record('04-return-same-jackson-view.png','SAME_PLACE_RETURN','LOC-COUNTRY-CLUB-JACKSON');
 await click('#inspectorWorld');
 assert.equal(await evaluate('document.querySelector("#inspector").hidden'),true);
 await sleep(1500);
 await record('05-return-unlabeled-world.png','WORLD_RETURN',null);
 await click('#infoToggle');await click('#demoLoss');
 calm=await evaluate('__observerDebug.weather()');
 assert.equal(calm.status,'GLOBAL_CALM','EL_NINO_LOSS_NOT_CALM');
 assert.deepEqual(calm.affectedZoneIds,[],'GLOBAL_CALM_HAS_STORM_ZONES');
 await click('#infoClose');
 if(await evaluate('document.querySelector("#motionToggle").getAttribute("aria-pressed")')==='true')await click('#motionToggle');
 const before=await state();
 await until(async()=>{const s=await state();return s.stats.waterTime>before.stats.waterTime?s:null;},'ORDINARY_WATER_DURING_CALM',12000);
 await click('#placesToggle');await click('[data-place="LOC-TDS-WATERFALL-TEMPLE"]');
 await sleep(2300);
 await record('06-waterfall-temple-global-calm.png','CALM_WATERFALL','LOC-TDS-WATERFALL-TEMPLE');
 const count=await evaluate('document.querySelectorAll("#placeList button[data-place]").length');
 assert.equal(count,23);
 assert.deepEqual(externalRequests,[],'UNEXPECTED_EXTERNAL_REQUESTS');
 assert.deepEqual(errors,[],'BROWSER_ERRORS');
 assert.ok(await evaluate('__observerDebug.sourceUnchanged()'),'SOURCE_MUTATION');
 // Commit evidence only after every browser safety and source check has passed.
 mkdirSync(out,{recursive:false});
 for(const f of frames)writeFileSync(join(out,f.file),f.bytes);
 const manifest={
  kind:'UNPUBLISHED_REAL_GPU_JOURNEY_EVIDENCE',sourceSha,sourceStateAsOf:catalogue.asOf,
  historyStatus:catalogue.historyStatus,publicationAuthorized:false,originalMemoImages:0,
  visualAcceptance:'NOT_REVIEWED',browser:'Chrome headless physical WebGL2',
  gpu:ready.stats.gpuRenderer,atlasLocations:count,
  historyLocationId:'LOC-COUNTRY-CLUB-JACKSON',historyEntryCount:historyCount,
  historyCameraPreserved:true,historyWaterPaused:true,
  historyPausedWaterSampleStart:frozen.stats.waterTime,
  historyPausedWaterSampleEnd:frozenLater.stats.waterTime,
  preHistoryWaterAdvanced:true,resumedWaterAfterHistory:true,
  elNinoSyntheticLossStatus:calm.status,stormZonesDuringCalm:calm.affectedZoneIds,
  ordinaryWaterAdvancedDuringCalm:true,externalRequests,errors,
  stages:frames.map(({bytes,...safe})=>safe)
 };
 assert.equal(catalogue.publicationAuthorized,false,'PUBLICATION_AUTHORITY_CHANGED');
 writeFileSync(join(out,'manifest.json'),JSON.stringify(manifest,null,2)+'\n');
 console.log('GPU_JOURNEY_STAGE_EVIDENCE_PASS '+JSON.stringify({sourceSha,gpu:manifest.gpu,frames:frames.length,historyCount,stages:manifest.stages.map(f=>f.stage)}));
}
try{await main();}catch(e){console.error('GPU_JOURNEY_STAGE_EVIDENCE_FAIL '+(e?.stack||e));process.exitCode=1;}
finally{
 try{ws?.close();}catch{}
 try{browser?.kill('SIGTERM');}catch{}
 await sleep(550);
 try{if(browser?.exitCode===null)browser.kill('SIGKILL');}catch{}
 try{rmSync(scratch,{recursive:true,force:true,maxRetries:8,retryDelay:220});}
 catch(e){console.warn('CHROME_TEMP_CLEANUP_WARNING '+(e?.code||e));}
}

