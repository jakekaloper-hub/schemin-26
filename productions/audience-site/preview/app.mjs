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
let inspectionReturnFocus=canvas,infoFromInspector=false;
function dispatch(a){state=transitionObserver(state,a);return state;}
function showFallback(reason){
 const firstLoss=$('#fallback').hidden;
 cancelWorldGesture();
 ready=false;cancelAnimationFrame(frameId);$('#fallback').hidden=false;$('#fallbackReason').textContent=reason;$('#splash').hidden=true;$('#skipReveal').hidden=true;
 // Let a current read-only modal finish; its exit hands focus to the same source place.
 if(firstLoss&&!historySession&&!memorySession)restoreFallbackPlace(selected?.id);
}
function escapePanels(){infoFromInspector=false;for(const id of ['#placesPanel','#infoPanel','#inspector'])$(id).hidden=true;$('#placesToggle').setAttribute('aria-expanded','false');$('#tooltip').hidden=true;}
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
function restoreFallbackPlace(locationId,restoreHistoryFocus=false){
  if($('#fallback').hidden)return false;
  const place=bindings.find(p=>p.id===locationId);
  const button=place&&Array.from($('#fallbackPlaces').children).find(b=>b.dataset.fallbackPlace===place.id);
  if(place&&button)renderFallbackPlace(place,button,restoreHistoryFocus);
  else $('#retry').focus();
  return true;
}
for(const p of bindings){
  $('#placeList').append(indexButton(p));
  const b=fallbackNode('button',p.name);
  b.type='button';b.dataset.fallbackPlace=p.id;b.addEventListener('click',()=>renderFallbackPlace(p,b));$('#fallbackPlaces').append(b);
}
/* FALLBACK_JOURNEY_END */
// Reflect the last explicit viewpoint, not an exact camera pose after manual orbit.
function syncViewControls(mode){
 for(const b of document.querySelectorAll('[data-view]')){const active=b.dataset.view===mode;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));}
 const wetlands=$('#wetlandsView'),active=mode==='WETLANDS';wetlands.classList.toggle('active',active);wetlands.setAttribute('aria-pressed',String(active));
}
function select(id){
 if(!canControl())return;
 // The place index becomes hidden upon selection; never strand keyboard focus there.
 const fromIndex=$('#placeList').contains(document.activeElement);
 inspectionReturnFocus=fromIndex?$('#placesToggle'):canvas;
 dispatch({type:'inspect',id});syncViewControls(null);
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
function wholeWorld(){if(!canControl())return;const fromInspector=$('#inspector').contains(document.activeElement);dispatch({type:'world_view'});selected=null;target=nearestObserverViewYaw(camera,defaultCamera());syncViewControls('AERIAL');escapePanels();if(paused)camera=structuredClone(target);if(fromInspector)(inspectionReturnFocus?.isConnected?inspectionReturnFocus:canvas).focus({preventScroll:true});}
$('#placesToggle').onclick=()=>{const open=$('#placesPanel').hidden;escapePanels();$('#placesPanel').hidden=!open;$('#placesToggle').setAttribute('aria-expanded',String(open));if(open)$('#placeSearch').focus();};
$('#placesClose').onclick=()=>{escapePanels();$('#placesToggle').focus();};
function closeInfo(){
 const restore=infoFromInspector&&selected&&canControl();
 escapePanels();
 if(restore){$('#inspector').hidden=false;$('#inspectSource').focus({preventScroll:true});}
 else $('#infoToggle').focus({preventScroll:true});
}
$('#infoToggle').onclick=()=>{if(!$('#infoPanel').hidden){closeInfo();return;}escapePanels();$('#infoPanel').hidden=false;};
$('#infoClose').onclick=closeInfo;
$('#inspectorClose').onclick=closeInspector;$('#inspectSource').onclick=()=>{infoFromInspector=true;$('#infoPanel').hidden=false;$('#inspector').hidden=true;$('#infoClose').focus({preventScroll:true});};
$('#placeSearch').oninput=e=>{for(const b of $('#placeList').children)b.hidden=!b.textContent.toLowerCase().includes(e.target.value.toLowerCase());};
$('#returnWorld').onclick=wholeWorld;$('#inspectorWorld').onclick=wholeWorld;
$('#wetlandsView').onclick=()=>{
 if(!canControl())return;
 const fromInspector=$('#inspector').contains(document.activeElement);
 const overview=regionOverviewCamera(bindings,'REG-SOUTHERN-WETLANDS',canvas.clientWidth/Math.max(1,canvas.clientHeight));
 dispatch({type:'world_view'});selected=null;escapePanels();target=nearestObserverViewYaw(camera,overview);syncViewControls('WETLANDS');
 if(paused)camera=structuredClone(target);
 if(fromInspector)(inspectionReturnFocus?.isConnected?inspectionReturnFocus:canvas).focus({preventScroll:true});
};
for(const b of document.querySelectorAll('[data-view]'))b.onclick=()=>{if(!canControl())return;dispatch({type:'camera',mode:b.dataset.view});target=modeCamera(b.dataset.view,selected?.renderAnchor||[0,0,0]);if(!selected&&b.dataset.view==='AERIAL')target=defaultCamera();target=nearestObserverViewYaw(camera,target);syncViewControls(b.dataset.view);if(paused)camera=structuredClone(target);};
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
function cancelWorldGesture(){
 // Clear ownership before releasing capture: lostpointercapture may fire
 // during release or later, and must not act on the retired gesture.
 const captured=[...pointers.keys()];
 pointers.clear();pointerStart=null;dragDistance=0;pinchDistance=null;pinchCenter=null;multiTouchGesture=false;
 for(const id of captured){
  try{if(canvas.hasPointerCapture(id))canvas.releasePointerCapture(id);}catch{} // Pointer may already have ended.
 }
 $('#tooltip').hidden=true;canvas.style.cursor='grab';
}
canvas.addEventListener('contextmenu',e=>e.preventDefault());
canvas.addEventListener('pointerdown',e=>{
 // Only primary pan/tap and secondary orbit own the world gesture.
 if(!canControl()||(e.button!==0&&e.button!==2))return;
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
 // A fast release can arrive without its final pointermove. Use the
 // down-to-up displacement as well as the accumulated delivered movement.
 const releaseDistance=pointerStart?Math.abs(e.clientX-pointerStart.x)+Math.abs(e.clientY-pointerStart.y):Infinity;
 // Orbit intent (even without motion) is never place inspection.
 if(pointerStart&&!pointerStart.orbit&&e.button===0&&!multiTouchGesture&&dragDistance<8&&releaseDistance<8&&canControl()){
  const p=renderer.pick(e.clientX,e.clientY);if(p)select(p.id);
 }
 if(!pointers.size){
  pointerStart=null;pinchDistance=null;pinchCenter=null;multiTouchGesture=false;
 }else{
  pointerStart=null;pinchDistance=null;pinchCenter=null;dragDistance=99;
 }
}
canvas.addEventListener('pointerup',up);
function cancelPointer(e){
 // Implicit capture loss after pointerup is normal; never reset another
 // pointer's active gesture in response to an already released/unknown ID.
 if(!pointers.delete(e.pointerId))return;
 pointerStart=null;pinchDistance=null;pinchCenter=null;dragDistance=99;
 multiTouchGesture=pointers.size>0;
}
canvas.addEventListener('pointercancel',cancelPointer);
canvas.addEventListener('lostpointercapture',cancelPointer);
canvas.addEventListener('pointerleave',()=>$('#tooltip').hidden=true);
canvas.addEventListener('wheel',e=>{
 if(!canControl())return;
 e.preventDefault();
 // WheelEvent deltas may be CSS pixels, lines or pages depending on device/browser.
 // Read deltaMode first; some browsers expose compatibility units otherwise.
 const mode=e.deltaMode,delta=e.deltaY*(mode===1?16:mode===2?Math.max(1,canvas.clientHeight):1);
 if(!Number.isFinite(delta))return;
 target=cameraStep(target,{zoom:delta*.07});if(paused)camera=structuredClone(target);$('#tooltip').hidden=true;
},{passive:false});
function handleWorldKey(e){
 // A recorded-history or memory dialog (and graphics fallback) owns its own keys.
 if(e.defaultPrevented||!canControl())return;
 if(e.key==='Escape'){
  if(!$('#infoPanel').hidden){e.preventDefault();closeInfo();return;}
  const opener=!$('#placesPanel').hidden?$('#placesToggle'):!$('#inspector').hidden?inspectionReturnFocus:null;
  if(!opener)return;
  e.preventDefault();escapePanels();
  (opener.isConnected?opener:canvas).focus({preventScroll:true});return;
 }
 // Keep search, native controls and assistive keyboard navigation independent.
 if(e.target!==canvas&&e.target!==document.body)return;
 if(e.altKey||e.ctrlKey||e.metaKey)return;
 // Match pointer panning in the current target view rather than fixed Atlas axes.
 const c=Math.cos(target.yaw),s=Math.sin(target.yaw);
 const action={ArrowLeft:{panX:-3*c,panZ:3*s},ArrowRight:{panX:3*c,panZ:-3*s},ArrowUp:{panX:-3*s,panZ:-3*c},ArrowDown:{panX:3*s,panZ:3*c},'+':{zoom:-10},'=':{zoom:-10},'-':{zoom:10}}[e.key];
 // Shift+arrows give keyboard-only spectators the same orbit/tilt capability as drag.
 const orbit=e.shiftKey?{ArrowLeft:{yaw:-.12},ArrowRight:{yaw:.12},ArrowUp:{pitch:.08},ArrowDown:{pitch:-.08}}[e.key]:null;
 if(action){e.preventDefault();target=cameraStep(target,orbit||action);if(paused)camera=structuredClone(target);}
}
document.addEventListener('keydown',handleWorldKey);

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
// Every existing renderer owns its own ordinary water optics. In particular,
// Canvas2D already draws surface-contact, terrain-masked sheen strokes; a second
// screen-space pass would bypass those visibility checks. Ambient owns rain only.
/** World-projected synthetic weather optics within EXISTING region bounds.
 * This is not simulated hydrology or a new Atlas location; ordinary environment
 * motion is independent of the result-driven weather demonstration.
 * The 110-drop per-zone budget is intentionally invariant across renderers.
 */
/** Observer-camera eye is identical to the existing Three/native/Canvas viewport fit.
 * Terrain-only rain visibility must never invent a new camera, terrain or weather fact. */
function stormCameraEye(c,width,height){
 if(!c||!Array.isArray(c.target)||c.target.length!==3||![...c.target,c.distance,c.yaw,c.pitch,width,height].every(Number.isFinite)||width<=0||height<=0||c.distance<=0)throw Error('INVALID_STORM_CAMERA');
 const fit=Math.max(1,1.25/(width/height));
 const d=c.distance*(c.distance>100?fit:Math.min(fit,1.25)),t=c.target;
 return [t[0]+Math.sin(c.yaw)*Math.cos(c.pitch)*d,t[1]+Math.sin(c.pitch)*d,t[2]+Math.cos(c.yaw)*Math.cos(c.pitch)*d];
}
/** Bounded terrain line-of-sight samples, not a GPU depth test or building mask.
 * Only the already-rendered source-derived terrain footprint can block overlay rain. */
function stormTerrainVisible(eye,point,heightAt){
 if(!Array.isArray(eye)||!Array.isArray(point)||eye.length!==3||point.length!==3||![...eye,...point].every(Number.isFinite)||typeof heightAt!=='function')throw Error('INVALID_STORM_RAY');
 const dx=point[0]-eye[0],dy=point[1]-eye[1],dz=point[2]-eye[2];
 const steps=Math.min(8,Math.max(2,Math.ceil(Math.hypot(dx,dz)/20)));
 for(let i=1;i<steps;i++){
  const f=i/steps,x=eye[0]+dx*f,z=eye[2]+dz*f;
  if(Math.abs(x)>110||Math.abs(z)>110)continue;
  const h=heightAt(x,z);
  if(!Number.isFinite(h)||h>eye[1]+dy*f+.35)return false;
 }
 return true;
}
function projectedStormRain(bounds,phase,heightAt,project,count=110,eye=null){
 if(!Array.isArray(bounds)||bounds.length!==4||bounds.some(v=>!Number.isFinite(v))||bounds[0]>=bounds[2]||bounds[1]>=bounds[3]||!Number.isFinite(phase)||typeof heightAt!=='function'||typeof project!=='function'||!Number.isInteger(count)||count<0||count>110||(eye!==null&&(!Array.isArray(eye)||eye.length!==3||!eye.every(Number.isFinite))))throw Error('INVALID_STORM_RAIN_SAMPLE');
 const frac=v=>v-Math.floor(v),[x1,y1,x2,y2]=bounds,segments=[];
 for(let i=0;i<count;i++){
  const u=frac(Math.sin((i+1)*127.1)*43758.5453),v=frac(Math.sin((i+1)*311.7)*21431.517);
  const x=(x1+(x2-x1)*u-50)*2,z=(50-(y1+(y2-y1)*v))*2;
  const ground=heightAt(x,z);if(!Number.isFinite(ground))continue;
  const rise=2+14*frac((i+1)*.61803398875-phase*.23);
  const top=[x-.22,ground+rise+1.4,z+.1],bottom=[x,ground+rise,z];
  if(eye&&(!stormTerrainVisible(eye,top,heightAt)||!stormTerrainVisible(eye,bottom,heightAt)))continue;
  const a=project(top),b=project(bottom);
  if(!a||!b||![a.x,a.y,a.depth,b.x,b.y,b.depth].every(Number.isFinite)||a.depth< -1||a.depth>1||b.depth< -1||b.depth>1)continue;
  segments.push({a,b});
 }
 return segments;
}
const zoneBounds={'REG-EASTERN-STORM-COAST':[68,25,100,88],'REG-INNER-SEA-LITTORAL':[55,0,100,25],'REG-CENTRAL-BASIN':[25,30,72,58],'REG-UPPER-VALLEYS':[20,55,75,78]};
function drawAmbient(t){
 if(!ambientCtx||!renderer)return;
 const [w,h]=sizeAmbientCanvas(ambient,ambientCtx,innerWidth,innerHeight,window.devicePixelRatio);
 ambientCtx.clearRect(0,0,w,h);
 // Synthetic storm presence is a bounded optical cue, not a weather feed.
 // World-space drops follow existing source-zone rectangles and the 3D camera;
 // bounded terrain line-of-sight rejects obscured drops; buildings are not depth-tested.
 const rainEye=demo>0?stormCameraEye(camera,Math.max(1,canvas.clientWidth||w),Math.max(1,canvas.clientHeight||h)):null;
 if(demo>0)for(const id of weather.affectedZoneIds){
  const bounds=zoneBounds[id];if(!bounds)continue;
  ambientCtx.strokeStyle='rgba(205,222,222,.24)';ambientCtx.lineWidth=.72;
  for(const {a,b} of projectedStormRain(bounds,t,(x,z)=>renderer.height(x,z),point=>renderer.project(point),110,rainEye)){
   ambientCtx.beginPath();ambientCtx.moveTo(a.x,a.y);ambientCtx.lineTo(b.x,b.y);ambientCtx.stroke();
  }
 }
}

function draw(t){if(!$('#fallback').hidden||!renderer)return;frameId=requestAnimationFrame(draw);if(memorySession||historySession){lastTime=t;return;}const dt=Math.min(.05,(t-lastTime)/1000||.016);lastTime=t;if(!paused&&!document.hidden)animationTime+=dt;
 if(state.phase==='REVEALING'){const elapsed=(t-revealStart)/2200,f=clamp01(elapsed),s=f*f*(3-2*f);camera={...target,distance:280-(280-target.distance)*s,pitch:1.18-(1.18-target.pitch)*s,yaw:-.11+(.11+target.yaw)*s,target:[...target.target]};if(f===1){dispatch({type:'reveal_finished'});finishReveal();}}
 else if(state.phase==='EXPLORING'&&!paused){const f=1-Math.exp(-dt*6);for(const k of ['distance','pitch','yaw'])camera[k]+=(target[k]-camera[k])*f;camera.target=camera.target.map((v,i)=>v+(target.target[i]-v)*f);}
 const clock=observerClock(new Date().toISOString()),light=illustrativeLight(clock.hour+clock.minute/60);renderer.render(camera,animationTime,{strength:light.strength,storm:demo||0,paused});if(!$('#fallback').hidden)return;drawAmbient(animationTime);
 if(state.phase==='EXPLORING'&&t-revealStart>11000)$('#hint').style.opacity='0';
}
function clamp01(v){return Math.max(0,Math.min(1,v));}
window.__observerDebug={state:()=>structuredClone(state),bindings:()=>structuredClone(bindings),weather:()=>structuredClone(weather),metadata:()=>structuredClone(metadata),sourceUnchanged:()=>JSON.stringify(catalog)===original,stats:()=>renderer?.stats,camera:()=>structuredClone(camera),loseContext:()=>renderer?.loseContext()};
// Graphics loss is terminal for this preview instance; retry is an explicit reload.
frameId=requestAnimationFrame(()=>{
 if(!$('#fallback').hidden)return;
 frameId=requestAnimationFrame(async()=>{
  if(!$('#fallback').hidden)return;
  try{
   renderer=createWorldRenderer(canvas,bindings,{onContextLost:()=>showFallback('The graphics context was lost. The source Atlas is still available below.')});
   if(!$('#fallback').hidden)return;
   dispatch({type:'asset_ready',id:'geometry'});
   if(renderer.prepare)await renderer.prepare(camera);
   if(!$('#fallback').hidden)return;
   dispatch({type:'asset_ready',id:'renderer'});
   renderer.render(camera,0,{strength:1});
   if(!$('#fallback').hidden)return;
   frameId=requestAnimationFrame(()=>{
    if(!$('#fallback').hidden)return;
    dispatch({type:'asset_ready',id:'first-frame'});revealStart=performance.now();splash.classList.add('out');
    if(state.phase==='REVEALING'){$('#skipReveal').hidden=false;setTimeout(()=>splash.hidden=true,1200);}else finishReveal();
    frameId=requestAnimationFrame(draw);
   });
  }catch(e){
   if(!$('#fallback').hidden)return;
   try{dispatch({type:'asset_failed',id:'geometry'});}catch{}
   showFallback('3D initialization did not complete. '+String(e.message));
  }
 });
});
// A persisted pagehide freezes this document for browser back/forward navigation.
 // Keep its one existing animation loop and renderer alive; the browser resumes them.
window.addEventListener('pagehide',e=>{cancelWorldGesture();if(e.persisted)return;cancelAnimationFrame(frameId);renderer?.dispose();});
window.addEventListener('pageshow',e=>{if(e.persisted)lastTime=performance.now();});

// Leaving the active document retires only world input, never the renderer or camera.
window.addEventListener('blur',cancelWorldGesture);
document.addEventListener('visibilitychange',()=>{if(document.hidden)cancelWorldGesture();});
