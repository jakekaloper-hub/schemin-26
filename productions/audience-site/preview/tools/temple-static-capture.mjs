#!/usr/bin/env node
/**
 * Opt-in physical-GPU screenshot evidence for the existing, unpublished
 * Temple vegetation or Jackson bridge inspection at fixed synthetic noon and phase zero.
 * No publishing, canon writes, external requests or third-party dependencies.
 * Usage: node temple-static-capture.mjs /path/observer.html /new/evidence/dir EXPECTED_SOURCE_SHA [temple|jackson]
 */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {spawn,execFileSync} from 'node:child_process';
import {existsSync,mkdirSync,mkdtempSync,readFileSync,rmSync,writeFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {resolve,join} from 'node:path';
import {pathToFileURL} from 'node:url';

const [observerArg,outArg,expectedSha,preset='temple',...extra]=process.argv.slice(2);
const presets={temple:{site:'LOC-TDS-WATERFALL-TEMPLE',distances:[51,44]},jackson:{site:'LOC-COUNTRY-CLUB-JACKSON',distances:[60,30]}};
assert.ok(Object.hasOwn(presets,preset)&&extra.length===0,'UNKNOWN_CAPTURE_PRESET');
const {site,distances}=presets[preset];
assert.ok(observerArg&&outArg&&/^[0-9a-f]{40}$/.test(expectedSha||''),'Usage: observer.html NEW_OUTPUT_DIR EXPECTED_SOURCE_SHA');
const observer=resolve(observerArg),out=resolve(outArg);
assert.ok(existsSync(observer),'SOURCE_OBSERVER_MISSING');
assert.ok(!existsSync(out),'REFUSE_TO_OVERWRITE_EVIDENCE');
const repo=resolve(import.meta.dirname,'../../../..');
const toolCheckoutBase=execFileSync('git',['rev-parse','HEAD'],{cwd:repo,encoding:'utf8'}).trim();
execFileSync('git',['cat-file','-e',expectedSha+'^{commit}'],{cwd:repo});
const chrome=process.env.CHROME_BIN||(process.platform==='darwin'
 ? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome':'/usr/bin/google-chrome');
assert.ok(existsSync(chrome),'PHYSICAL_CHROME_UNAVAILABLE');
const scratch=mkdtempSync(join(tmpdir(),'commonwealth-journey-stage-'));
const pending=new Map(),errors=[],externalRequests=[],frames=[];
let browser=null,ws=null,nextId=0;
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
  '--force-prefers-reduced-motion=reduce','about:blank'],{stdio:'ignore'});
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

 await cdp('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]});
 const syntheticUtc='2026-11-25T17:00:00.000Z';
 await cdp('Page.addScriptToEvaluateOnNewDocument',{source:`{const Native=Date,fixed=Native.parse(${JSON.stringify(syntheticUtc)});globalThis.Date=class extends Native{constructor(...args){super(...(args.length?args:[fixed]));}static now(){return fixed;}};}`});
 await cdp('Page.navigate',{url:pathToFileURL(observer).href});
 const ready=await until(async()=>{try{const s=await state();return s?.stats?.frames>0?s:null;}catch{return null;}},'FIRST_GPU_FRAME');
 assert.equal(ready.stats.renderer,'three-webgl2');assert.equal(ready.stats.prepared,true);
 assert.doesNotMatch(ready.stats.gpuRenderer||'',/SwiftShader|Software Rasterizer|llvmpipe|UNAVAILABLE/i);
 if(ready.state.phase==='REVEALING')await click('#skipReveal');
 await until(async()=>{const s=await state();return s.state.phase==='EXPLORING'?s:null;},'EXPLORING');
 const catalog=await evaluate('JSON.parse(document.querySelector("#catalog").textContent)');
 assert.equal(catalog.sourceRevision,expectedSha);
 assert.equal(await evaluate('document.querySelector("#motionToggle").getAttribute("aria-pressed")'),'true');
 assert.equal(await evaluate('new Date().toISOString()'),syntheticUtc);
 await click('#infoToggle');await click('#demoLoss');
 assert.equal(await evaluate('__observerDebug.weather().status'),'GLOBAL_CALM');
 await click('#infoClose');await click('#placesToggle');
 assert.equal(await evaluate('document.querySelectorAll("#placeList button[data-place]").length'),23);
 await click('[data-place="'+site+'"]');
 await sleep(500);
 for(const [stage,distance] of [['standard',distances[0]],['closer',distances[1]]]){
   const prior=(await state()).camera.distance;
   // Fractional wheel delta via the existing spectator event handler; no camera state mutation.
   await evaluate(`document.querySelector('#world').dispatchEvent(new WheelEvent('wheel',{deltaY:${(distance-prior)/.07},bubbles:true,cancelable:true}))`);
   assert.ok(Math.abs((await state()).camera.distance-distance)<1e-9,'CAMERA_DISTANCE_NOT_MATCHED');
   await sleep(450);
   assert.equal((await state()).stats.waterTime,0);
   await record(stage+'.png',stage,site);
   await sleep(350);
   await record(stage+'-repeat.png',stage,site);
   const [a,b]=frames.slice(-2);sameCamera(a.camera,b.camera);
   assert.equal(a.sha256,b.sha256,'UNSTABLE_PAUSED_FRAME');
   assert.equal(a.waterTime,0);assert.equal(b.waterTime,0);
 }
 assert.ok(frames[2].camera.distance<frames[0].camera.distance,'ZOOM_NOT_APPLIED');
 assert.deepEqual(errors,[]);assert.deepEqual(externalRequests,[]);
 assert.ok((await state()).unchanged);
 mkdirSync(out,{recursive:false});
 for(const f of frames.filter(x=>!x.file.includes('-repeat')))writeFileSync(join(out,f.file),f.bytes,{flag:'wx'});
 const manifest={preset,sourceSha:expectedSha,toolCheckoutBase,observerSha256:createHash('sha256').update(readFileSync(observer)).digest('hex'),sourceStateAsOf:catalog.stateAsOf,syntheticUtc,weather:'SYNTHETIC_GLOBAL_CALM',gpu:ready.stats.gpuRenderer,atlasLocations:23,publicationAuthorized:false,visualAcceptance:'NOT_REVIEWED',browserErrors:errors.length,externalRequests:externalRequests.length,frames:frames.map(({bytes,...f})=>({...f,bytes:bytes.length,retained:!f.file.includes('-repeat')}))};
 writeFileSync(join(out,'manifest.json'),JSON.stringify(manifest,null,2)+'\n',{flag:'wx'});
 console.log(JSON.stringify(manifest));
}
try{await main();}finally{ws?.close();browser?.kill();await sleep(300);rmSync(scratch,{recursive:true,force:true});}
