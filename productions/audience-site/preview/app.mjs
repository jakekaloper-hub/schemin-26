/* Mount the source foundation into a private, offline observer preview. */
const {createObserver,transitionObserver}=ObserverWorld;
const {observerClock,resolveObserverWeather}=ObserverWeather;
const {spatialBindings,defaultCamera,cameraStep,modeCamera,locationCamera,regionOverviewCamera,nearestObserverViewYaw,illustrativeLight,previewMetadata}=Spatial;
const createWorldRenderer=(canvas,bindings,options)=>{
 if(THREE){try{return ThreeWorldRenderer.createThreeWorldRenderer(THREE,canvas,bindings,{...options,buildWorldGeometry:WorldRenderer.buildWorldGeometry,buildRegionalAssets:RegionalAssets.buildRegionalAssets,buildAtlasSiteAssets:AtlasSites.buildAtlasSiteAssets,atlasSiteIds:AtlasSites.supportedAtlasSiteIds()});}catch(e){if(e.message!=='WEBGL2_UNAVAILABLE')throw e;}}
 return WorldRenderer.createWorldRenderer(canvas,bindings,options);
};
const $=s=>document.querySelector(s);
const catalog=JSON.parse($('#catalog').textContent),original=JSON.stringify(catalog),bindings=spatialBindings(catalog),metadata=previewMetadata(catalog);
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
if(matchMedia('(pointer:coarse)').matches)$('#hint').textContent='Drag to pan · Two-finger rotate or pinch · Tap a place';
let returning=false;try{returning=sessionStorage.getItem('commonwealth-observer-seen')==='1';}catch{}
let state=createObserver({locationIds:bindings.map(p=>p.id),criticalAssetIds:['geometry','renderer','first-frame'],reducedMotion:reduced,returning});
let renderer,camera=defaultCamera(),target=defaultCamera(),paused=reduced,animationTime=0,lastTime=0,frameId=0,revealStart=0,weather={status:'NOT_CONNECTED',affectedZoneIds:[]},demo=null,ready=false;
let selected=null,pointerStart=null,dragDistance=0,pointers=new Map(),pinchDistance=null,pinchCenter=null,multiTouchGesture=false;
const canvas=$('#world'),splash=$('#splash');
let inspectionReturnFocus=canvas;
function dispatch(a){state=transitionObserver(state,a);return state;}
function showFallback(reason){ready=false;cancelAnimationFrame(frameId);$('#fallback').hidden=false;$('#fallbackReason').textContent=reason;$('#splash').hidden=true;$('#skipReveal').hidden=true;}
function escapePanels(){for(const id of ['#placesPanel','#infoPanel','#inspector'])$(id).hidden=true;$('#placesToggle').setAttribute('aria-expanded','false');$('#tooltip').hidden=true;}
function indexButton(p){const b=document.createElement('button');b.type='button';b.textContent=p.name;b.dataset.place=p.id;b.addEventListener('click',()=>select(p.id));return b;}
/* FALLBACK_JOURNEY_START: source-bound read-only navigation when graphics are unavailable. */
function fallbackNode(tag,text){const n=document.createElement(tag);n.textContent=text;return n;}
function fallbackRecordList(parent,label,values){
  if(!Array.isArray(values)||!values.length)return;
  const s=document.createElement('section'),h=fallbackNode('h4',label),ul=document.createElement('ul');
  for(const v of values)ul.append(fallbackNode('li',v));
  s.append(h,ul);parent.append(s);
}
function renderFallbackHistory(place,indexButton){
  // Recheck location, event and publication authority on every entry.
  const events=PlaceHistory.historyForLocation(catalog,place.id),detail=$('#fallbackDetail');
  detail.replaceChildren();
  const back=fallbackNode('button','← Return to '+place.name);
  back.type='button';back.onclick=()=>renderFallbackPlace(place,indexButton,true);
  detail.append(back,
    fallbackNode('h2','Recorded history · '+place.name),
    fallbackNode('p','Source World Memory · '+catalog.history.status.replaceAll('_',' ')+' · recorded as '+catalog.stateAsOf.replaceAll('_',' ')+'. Historical entries do not establish present-day conditions, approved geometry or released story canon.'));
  for(const event of events){
    const article=document.createElement('article');article.className='fallback-history-record';
    article.append(fallbackNode('h3',event.year+' · Week '+event.week+' · '+event.id),fallbackNode('p','Historical source record · read-only'));
    for(const [key,label] of [['physical','Recorded physical effects'],['social','Recorded social effects'],['reputation','Recorded reputation effects'],['institutional','Recorded institutional effects']])fallbackRecordList(article,label,event.effects?.[key]);
    if(event.expiryCondition)article.append(fallbackNode('p','Source expiry condition: '+event.expiryCondition));
    if(event.supersededBy)article.append(fallbackNode('p','Source supersession: '+event.supersededBy));
    fallbackRecordList(article,'Source receipt paths (not public links)',event.sourceReceipts);
    detail.append(article);
  }
  back.focus();
}
function renderFallbackPlace(place,indexButton,restoreHistoryFocus=false){
  const detail=$('#fallbackDetail');detail.replaceChildren();
  const title=fallbackNode('h2',place.name);title.tabIndex=-1;
  detail.append(title,fallbackNode('p',place.canonStatus.replaceAll('_',' ')+' · '+place.landmarks.join(' · ')+'. Source Atlas location; regional visual forms are candidates, not verified present-day conditions.'));
  const listBack=fallbackNode('button','← All Atlas places');
  listBack.type='button';listBack.onclick=()=>{detail.replaceChildren();indexButton.focus();};
  detail.append(listBack);
  let entries;
  try{entries=PlaceHistory.historyForLocation(catalog,place.id);}
  catch{
    detail.append(fallbackNode('p','Recorded history is unavailable because this source snapshot did not pass its read-only authority checks.'));
    title.focus();return;
  }
  if(!entries.length){
    detail.append(fallbackNode('p','No location-exact World Memory entry is available for this place in this source snapshot. The place remains visible.'));
    title.focus();return;
  }
  const read=fallbackNode('button','Read recorded place history · '+entries.length+' '+(entries.length===1?'entry':'entries'));
  read.type='button';read.dataset.fallbackHistory=place.id;
  read.onclick=()=>renderFallbackHistory(place,indexButton);
  detail.append(fallbackNode('p','Recorded history belongs only to this location and is not live world state.'),read);
  if(restoreHistoryFocus)read.focus();else title.focus();
}
for(const p of bindings){
  $('#placeList').append(indexButton(p));
  const b=fallbackNode('button',p.name);
  b.type='button';b.addEventListener('click',()=>renderFallbackPlace(p,b));$('#fallbackPlaces').append(b);
}
/* FALLBACK_JOURNEY_END */
function select(id){
 if(state.phase!=='EXPLORING'||state.inputOwner!=='WORLD')return;
 // The place index becomes hidden upon selection; never strand keyboard focus there.
 const fromIndex=$('#placeList').contains(document.activeElement);
 inspectionReturnFocus=fromIndex?$('#placesToggle'):canvas;
 dispatch({type:'inspect',id});
 selected=bindings.find(p=>p.id===id);
 escapePanels();
 target=locationCamera(bindings,id);
 target.target[1]=renderer?renderer.height(target.target[0],target.target[2]):0;
 const framing=renderer?.siteView?.(id);if(framing)target={...target,...framing};target=nearestObserverViewYaw(camera,target);
 $('#placeRegion').textContent=selected.zoneId.replace(/^REG-/,'').replaceAll('-',' ');
 $('#placeName').textContent=selected.name;
 $('#landmarks').textContent=selected.landmarks.join(' · ');
 $('#placeStatus').textContent=selected.canonStatus.replaceAll('_',' ')+' · '+catalog.stateAsOf.replaceAll('_',' ');
 $('#inspector').hidden=false;
 updateMemoryEntry();updateHistoryEntry();
 if(paused)camera=structuredClone(target);
 if(fromIndex){const heading=$('#placeName');heading.tabIndex=-1;heading.focus({preventScroll:true});}
}
function closeInspector(){
 $('#inspector').hidden=true;
 (inspectionReturnFocus?.isConnected?inspectionReturnFocus:canvas).focus({preventScroll:true});
}
function wholeWorld(){if(state.phase!=='EXPLORING')return;const fromInspector=$('#inspector').contains(document.activeElement);dispatch({type:'world_view'});selected=null;target=nearestObserverViewYaw(camera,defaultCamera());escapePanels();if(paused)camera=structuredClone(target);if(fromInspector)(inspectionReturnFocus?.isConnected?inspectionReturnFocus:canvas).focus({preventScroll:true});}
$('#placesToggle').onclick=()=>{const open=$('#placesPanel').hidden;escapePanels();$('#placesPanel').hidden=!open;$('#placesToggle').setAttribute('aria-expanded',String(open));if(open)$('#placeSearch').focus();};
$('#placesClose').onclick=()=>{escapePanels();$('#placesToggle').focus();};
$('#infoToggle').onclick=()=>{const open=$('#infoPanel').hidden;escapePanels();$('#infoPanel').hidden=!open;};$('#infoClose').onclick=()=>{escapePanels();$('#infoToggle').focus();};
$('#inspectorClose').onclick=closeInspector;$('#inspectSource').onclick=()=>{$('#infoPanel').hidden=false;$('#inspector').hidden=true;$('#infoClose').focus({preventScroll:true});};
$('#placeSearch').oninput=e=>{for(const b of $('#placeList').children)b.hidden=!b.textContent.toLowerCase().includes(e.target.value.toLowerCase());};
$('#returnWorld').onclick=wholeWorld;$('#inspectorWorld').onclick=wholeWorld;
$('#wetlandsView').onclick=()=>{
 if(!canControl())return;
 const fromInspector=$('#inspector').contains(document.activeElement);
 const overview=regionOverviewCamera(bindings,'REG-SOUTHERN-WETLANDS',canvas.clientWidth/Math.max(1,canvas.clientHeight));
 dispatch({type:'world_view'});selected=null;escapePanels();target=nearestObserverViewYaw(camera,overview);
 if(paused)camera=structuredClone(target);
 if(fromInspector)(inspectionReturnFocus?.isConnected?inspectionReturnFocus:canvas).focus({preventScroll:true});
};
for(const b of document.querySelectorAll('[data-view]'))b.onclick=()=>{if(state.phase!=='EXPLORING')return;dispatch({type:'camera',mode:b.dataset.view});target=modeCamera(b.dataset.view,selected?.renderAnchor||[0,0,0]);if(!selected&&b.dataset.view==='AERIAL')target=defaultCamera();target=nearestObserverViewYaw(camera,target);for(const x of document.querySelectorAll('[data-view]'))x.classList.toggle('active',x===b);if(paused)camera=structuredClone(target);};
function setPaused(v){paused=v;$('#motionToggle').setAttribute('aria-pressed',String(paused));$('#motionToggle').textContent=paused?'▷':'Ⅱ';$('#motionToggle').setAttribute('aria-label',paused?'Resume environmental motion':'Pause environmental motion');if(paused)camera=structuredClone(target);}
$('#motionToggle').onclick=()=>setPaused(!paused);setPaused(paused);
function syntheticWeather(wins){const now=new Date(),checked=new Date(now.getTime()-60000),until=new Date(now.getTime()+3600000);const matches=wins===0?[{week:9,season:2026,completion:'FINAL',evidenceStatus:'VERIFIED',outcome:'LOSS'}]:Array.from({length:wins+1},(_,i)=>({week:9-i,season:2026,completion:'FINAL',evidenceStatus:'VERIFIED',outcome:i<wins?'WIN':'LOSS'}));return resolveObserverWeather({mode:'LIVE',now:now.toISOString(),weatherRegions:catalog.weatherRegions,resultEvidence:{characterId:'CHAR-MANNING-WELTY',season:2026,latestCompletedWeek:9,sourceReceipts:['SYNTHETIC_PREVIEW_FIXTURE_NOT_LEAGUE_DATA'],checkedAt:checked.toISOString(),validUntil:until.toISOString(),matches}});}
function setDemo(wins){demo=wins;weather=syntheticWeather(wins);$('#notice').hidden=false;$('#notice').textContent=`WEATHER DEMONSTRATION · ${wins===0?'loss → global calm':wins+' win'+(wins===1?'':'s')+' → storm shading'} · synthetic inputs`;}
$('#demoLoss').onclick=()=>setDemo(0);$('#demoWin').onclick=()=>setDemo(1);$('#demoStreak').onclick=()=>setDemo(3);$('#clearDemo').onclick=()=>{demo=null;weather={status:'NOT_CONNECTED',affectedZoneIds:[]};$('#notice').hidden=true;};
$('#sourceDetails').textContent=`Source ${catalog.sourceRevision.slice(0,8)} · State recorded as ${catalog.stateAsOf.replaceAll('_',' ')}. Historical/source status is not reclassified as current by this preview.`;
$('#skipReveal').onclick=()=>{if(state.phase==='REVEALING'){dispatch({type:'skip_reveal'});finishReveal();}};
$('#retry').onclick=()=>location.reload();
function finishReveal(){camera=structuredClone(target);$('#skipReveal').hidden=true;splash.classList.add('out');setTimeout(()=>splash.hidden=true,reduced?0:1200);try{sessionStorage.setItem('commonwealth-observer-seen','1');}catch{}ready=true;}
function canControl(){return !memorySession&&!historySession&&state.phase==='EXPLORING'&&state.inputOwner==='WORLD'&&$('#fallback').hidden;}
canvas.addEventListener('contextmenu',e=>e.preventDefault());
canvas.addEventListener('pointerdown',e=>{
 if(!canControl())return;
 canvas.setPointerCapture(e.pointerId);
 pointers.set(e.pointerId,[e.clientX,e.clientY]);
 $('#tooltip').hidden=true;
 if(pointers.size===1){
  pointerStart={x:e.clientX,y:e.clientY,lastX:e.clientX,lastY:e.clientY,orbit:e.shiftKey||e.button===2};
  dragDistance=0;multiTouchGesture=false;pinchDistance=null;pinchCenter=null;
 }else{
  // A second finger changes the gesture owner; neither release can select a place.
  multiTouchGesture=true;pointerStart=null;dragDistance=99;
  if(pointers.size===2){
   const [a,b]=[...pointers.values()];
   pinchDistance=Math.hypot(a[0]-b[0],a[1]-b[1]);
   pinchCenter=[(a[0]+b[0])/2,(a[1]+b[1])/2];
  }else{pinchDistance=null;pinchCenter=null;}
 }
});
canvas.addEventListener('pointermove',e=>{
 if(!canControl())return;
 if(pointers.has(e.pointerId)){
  pointers.set(e.pointerId,[e.clientX,e.clientY]);
  if(pointers.size===2){
   const [a,b]=[...pointers.values()],d=Math.hypot(a[0]-b[0],a[1]-b[1]);
   const center=[(a[0]+b[0])/2,(a[1]+b[1])/2];
   if(pinchDistance!==null&&pinchCenter){
    target=cameraStep(target,{zoom:(pinchDistance-d)*.25,yaw:-(center[0]-pinchCenter[0])*.006,pitch:(center[1]-pinchCenter[1])*.004});
   }
   pinchDistance=d;pinchCenter=center;dragDistance=99;
   if(paused)camera=structuredClone(target);
   return;
  }
  // After multi-touch ends, the remaining finger cannot jump into a pan/tap.
  if(multiTouchGesture)return;
  if(pointerStart){
   const dx=e.clientX-pointerStart.lastX,dy=e.clientY-pointerStart.lastY;
   dragDistance+=Math.abs(dx)+Math.abs(dy);pointerStart.lastX=e.clientX;pointerStart.lastY=e.clientY;
   if(pointerStart.orbit)target=cameraStep(target,{yaw:-dx*.006,pitch:dy*.004});
   else{const scale=target.distance*.0015;target=cameraStep(target,{panX:(-dx*Math.cos(target.yaw)+dy*Math.sin(target.yaw))*scale,panZ:(dx*Math.sin(target.yaw)+dy*Math.cos(target.yaw))*scale});}
   if(paused)camera=structuredClone(target);
  }
  return;
 }
 if(e.pointerType==='mouse'){
  const p=renderer.pick(e.clientX,e.clientY);$('#tooltip').hidden=!p;canvas.style.cursor=p?'pointer':'grab';
  if(p){$('#tooltip').textContent=p.name;$('#tooltip').style.left=Math.min(e.clientX+18,innerWidth-250)+'px';$('#tooltip').style.top=Math.max(8,e.clientY-40)+'px';}
 }
});
function up(e){
 if(!pointers.has(e.pointerId))return;
 pointers.delete(e.pointerId);
 if(!multiTouchGesture&&dragDistance<8&&canControl()){
  const p=renderer.pick(e.clientX,e.clientY);if(p)select(p.id);
 }
 if(!pointers.size){
  pointerStart=null;pinchDistance=null;pinchCenter=null;multiTouchGesture=false;
 }else{
  pointerStart=null;pinchDistance=null;pinchCenter=null;dragDistance=99;
 }
}
canvas.addEventListener('pointerup',up);
canvas.addEventListener('pointercancel',e=>{
 pointers.delete(e.pointerId);
 pointerStart=null;pinchDistance=null;pinchCenter=null;dragDistance=99;
 multiTouchGesture=pointers.size>0;
});
canvas.addEventListener('pointerleave',()=>$('#tooltip').hidden=true);
canvas.addEventListener('wheel',e=>{if(!canControl())return;e.preventDefault();target=cameraStep(target,{zoom:e.deltaY*.07});if(paused)camera=structuredClone(target);$('#tooltip').hidden=true;},{passive:false});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){escapePanels();canvas.focus();return;}if(/INPUT|TEXTAREA/.test(e.target.tagName)||!canControl())return;const action={ArrowLeft:{panX:-3},ArrowRight:{panX:3},ArrowUp:{panZ:-3},ArrowDown:{panZ:3},'+':{zoom:-10},'=':{zoom:-10},'-':{zoom:10}}[e.key];if(action){e.preventDefault();target=cameraStep(target,action);if(paused)camera=structuredClone(target);}});

const ambient=$('#ambient'),ambientCtx=ambient.getContext('2d');
/* Keep fine atmospheric details sharp on high-density viewports while all
 * renderer.project positions, clipping and hit areas remain in CSS pixels.
 * Cap backing density to bound GPU memory on high-DPR mobile displays. */
function sizeAmbientCanvas(surface,context,cssWidth,cssHeight,pixelRatio){
 const w=Math.max(1,Math.round(Number.isFinite(cssWidth)?cssWidth:1));
 const h=Math.max(1,Math.round(Number.isFinite(cssHeight)?cssHeight:1));
 const ratio=Number.isFinite(pixelRatio)?Math.max(1,Math.min(2,pixelRatio)):1;
 const pw=Math.max(1,Math.round(w*ratio)),ph=Math.max(1,Math.round(h*ratio));
 if(surface.width!==pw)surface.width=pw;
 if(surface.height!==ph)surface.height=ph;
 // Setting a canvas dimension resets its 2D transform; reassert on every frame.
 context.setTransform(pw/w,0,0,ph/h,0,0);
 return [w,h];
}
// WebGL shaders already shade and animate their own physical water. A second
// screen-space sheen would render above land/buildings without depth testing.
// Keep this illustrative optical cue only for the Canvas2D compatibility path.
function needsAmbientFallbackGlints(rendererName){
 return rendererName==='canvas2d-spatial-fallback';
}
const zoneBounds={'REG-EASTERN-STORM-COAST':[68,25,100,88],'REG-INNER-SEA-LITTORAL':[55,0,100,25],'REG-CENTRAL-BASIN':[25,30,72,58],'REG-UPPER-VALLEYS':[20,55,75,78]};
function drawAmbient(t){
 if(!ambientCtx||!renderer)return;
 const [w,h]=sizeAmbientCanvas(ambient,ambientCtx,innerWidth,innerHeight,window.devicePixelRatio);
 ambientCtx.clearRect(0,0,w,h);
 if(needsAmbientFallbackGlints(renderer.stats?.renderer))for(let i=0;i<120;i++){const x=Math.sin(i*42.31)*125,z=Math.cos(i*19.27)*130;if(renderer.height(x,z)>-.3)continue;const p=renderer.project([x,-.15,z]);if(!p)continue;const alpha=(.08+.08*Math.sin(t*.65+i))*.6;ambientCtx.strokeStyle=`rgba(220,230,212,${alpha})`;ambientCtx.lineWidth=.8;ambientCtx.beginPath();ambientCtx.ellipse(p.x,p.y,3+2*Math.sin(t*.3+i),.6,0,0,Math.PI*2);ambientCtx.stroke();}
 if(demo>0)for(const id of weather.affectedZoneIds){const bounds=zoneBounds[id];if(!bounds)continue;const [x1,y1,x2,y2]=bounds;const ps=[[x1,y1],[x2,y1],[x2,y2],[x1,y2]].map(([x,y])=>renderer.project([(x-50)*2,9,(50-y)*2]));if(ps.some(p=>!p))continue;ambientCtx.save();ambientCtx.beginPath();ps.forEach((p,i)=>i?ambientCtx.lineTo(p.x,p.y):ambientCtx.moveTo(p.x,p.y));ambientCtx.closePath();ambientCtx.clip();ambientCtx.strokeStyle='rgba(205,222,222,.24)';ambientCtx.lineWidth=.65;for(let i=0;i<110;i++){const x=((i*127.3+t*12)%w+w)%w,y=((i*79.4+t*140)%h+h)%h;ambientCtx.beginPath();ambientCtx.moveTo(x,y);ambientCtx.lineTo(x-3,y+9);ambientCtx.stroke();}ambientCtx.restore();}
}

function draw(t){frameId=requestAnimationFrame(draw);if(!renderer)return;if(memorySession||historySession){lastTime=t;return;}const dt=Math.min(.05,(t-lastTime)/1000||.016);lastTime=t;if(!paused&&!document.hidden)animationTime+=dt;
 if(state.phase==='REVEALING'){const elapsed=(t-revealStart)/2200,f=clamp01(elapsed),s=f*f*(3-2*f);camera={...target,distance:280-(280-target.distance)*s,pitch:1.18-(1.18-target.pitch)*s,yaw:-.11+(.11+target.yaw)*s,target:[...target.target]};if(f===1){dispatch({type:'reveal_finished'});finishReveal();}}
 else if(state.phase==='EXPLORING'&&!paused){const f=1-Math.exp(-dt*6);for(const k of ['distance','pitch','yaw'])camera[k]+=(target[k]-camera[k])*f;camera.target=camera.target.map((v,i)=>v+(target.target[i]-v)*f);}
 const clock=observerClock(new Date().toISOString()),light=illustrativeLight(clock.hour+clock.minute/60);renderer.render(camera,animationTime,{strength:light.strength,storm:demo||0,paused});drawAmbient(animationTime);
 if(state.phase==='EXPLORING'&&t-revealStart>11000)$('#hint').style.opacity='0';
}
function clamp01(v){return Math.max(0,Math.min(1,v));}
window.__observerDebug={state:()=>structuredClone(state),bindings:()=>structuredClone(bindings),weather:()=>structuredClone(weather),metadata:()=>structuredClone(metadata),sourceUnchanged:()=>JSON.stringify(catalog)===original,stats:()=>renderer?.stats,camera:()=>structuredClone(camera),loseContext:()=>renderer?.loseContext()};
requestAnimationFrame(()=>requestAnimationFrame(async()=>{try{renderer=createWorldRenderer(canvas,bindings,{onContextLost:()=>showFallback('The graphics context was lost. The source Atlas is still available below.')});dispatch({type:'asset_ready',id:'geometry'});if(renderer.prepare)await renderer.prepare(camera);dispatch({type:'asset_ready',id:'renderer'});renderer.render(camera,0,{strength:1});requestAnimationFrame(()=>{dispatch({type:'asset_ready',id:'first-frame'});revealStart=performance.now();splash.classList.add('out');if(state.phase==='REVEALING'){$('#skipReveal').hidden=false;setTimeout(()=>splash.hidden=true,1200);}else finishReveal();frameId=requestAnimationFrame(draw);});}catch(e){try{dispatch({type:'asset_failed',id:'geometry'});}catch{}showFallback('3D initialization did not complete. '+String(e.message));}}));
window.addEventListener('pagehide',()=>{cancelAnimationFrame(frameId);renderer?.dispose();});
