/* Private historical-art overlay. Loaded after the existing observer app.
 * No world-event write, release promotion, artifact reinterpretation or new scene art. */
const {validateMemoryIndex,memoryForLocation,openMemory,navigateMemory,memoryAssetResult,memoryView,closeMemory,memoryCoverage}=EditionMemory;
const rawMemoryIndex=JSON.parse($('#memoryIndex').textContent);
const memoryIndex=rawMemoryIndex===null?{memories:[],source:null,publicationAuthorized:false,scope:'PRIVATE_LOCAL'}:validateMemoryIndex(rawMemoryIndex,bindings.map(x=>x.id));
const memoryAssets=JSON.parse($('#memoryAssets').textContent);
const memoryDialog=$('#memoryDialog');
const memoryImage=$('#memoryImage');
let memorySession=null,memoryGeneration=0,memoryZoom=false,memoryPreviousFocus=null;
const memoryButtons=[];
function selectedMemory(){return selected?memoryForLocation(memoryIndex,selected.id):null;}
function updateMemoryEntry(){const m=selectedMemory();$('#openMemory').hidden=!m;$('#memoryAvailability').hidden=Boolean(m);$('#openMemory').textContent=m?'ENTER WEEK 9 · '+m.pages.length+' PAGES':'';}
function currentMemory(){return memorySession?memoryIndex.memories.find(m=>m.id===memorySession.memoryId):null;}
function layoutMemoryImage(){
 if(!memorySession)return;
 const original=memorySession.view==='FOLIO',vp=$('#memoryViewport'),ap=$('#memoryAperture');
 vp.classList.toggle('original',original);vp.classList.toggle('zoomed',memoryZoom&&original);
 $('#memoryView').textContent=original?'Scene detail':'Original page';$('#memoryZoom').hidden=!original;
 $('#memoryZoom').textContent=memoryZoom?'Fit page':'Zoom';
 if(original){ap.style.cssText='';memoryImage.style.cssText='';return;}
 const p=currentMemory().pages[memorySession.pageIndex];
 // Artwork apertures never include extra source text merely to fill portrait space.
 // Portrait entry uses the whole original folio; scenic detail remains optional.
 const crop=p.crop;
 const [x0,y0,x1,y1]=crop,cw=x1-x0,ch=y1-y0,ar=p.width*cw/(p.height*ch);
 const w=Math.max(vp.clientWidth,vp.clientHeight*ar),h=w/ar;
 ap.style.cssText=`width:${w}px;height:${h}px;left:${(vp.clientWidth-w)/2}px;top:${(vp.clientHeight-h)/2}px`;
 memoryImage.style.cssText=`width:${100/cw}%;height:${100/ch}%;left:${-100*x0/cw}%;top:${-100*y0/ch}%;`;
}
function syncMemoryChrome(){
 const m=currentMemory(),p=m.pages[memorySession.pageIndex];
 $('#memoryTitle').textContent=p.title;$('#memoryPage').textContent=`${memorySession.pageIndex+1} / ${m.pages.length}`;
 $('#memoryPeriod').textContent=`2026 · WEEK 9 · RECORDED ARTWORK`;
 $('#memoryPrevious').disabled=memorySession.pageIndex===0;$('#memoryNext').disabled=memorySession.pageIndex===m.pages.length-1;
 $('#memoryProvenance').textContent=`Original source: Week 9 PDF, page ${p.pdfPage}. Scene detail is a crop; Original page shows the complete unaltered folio. Private preview—not present-day world state.`;
 for(const b of memoryButtons){const active=Number(b.dataset.memoryPage)===memorySession.pageIndex;b.setAttribute('aria-current',active?'page':'false');}
 layoutMemoryImage();
}
async function showMemoryPage(){
 if(!memorySession)return;
 const generation=memoryGeneration,token=memorySession.loadToken,m=currentMemory(),page=m.pages[memorySession.pageIndex];
 $('#memoryLoading').hidden=false;$('#memoryFailure').hidden=true;memoryImage.hidden=true;
 syncMemoryChrome();
 try{
  const source=memoryAssets[page.id];if(!source||!source.startsWith('data:image/jpeg;base64,'))throw Error('IMAGE_BYTES_UNAVAILABLE');
  const decoded=new Image();decoded.src=source;await decoded.decode();
  if(!memorySession||generation!==memoryGeneration||token!==memorySession.loadToken)return;
  if(decoded.naturalWidth!==page.width||decoded.naturalHeight!==page.height)throw Error('SOURCE_IMAGE_DIMENSIONS_MISMATCH');
  memorySession=memoryAssetResult(memorySession,token,true);memoryImage.src=source;memoryImage.alt=page.alt;
  memoryImage.hidden=false;$('#memoryLoading').hidden=true;layoutMemoryImage();
 }catch(err){
  if(!memorySession||generation!==memoryGeneration||token!==memorySession.loadToken)return;
  memorySession=memoryAssetResult(memorySession,token,false);$('#memoryLoading').hidden=true;$('#memoryFailure').hidden=false;
  $('#memoryFailureText').textContent='This original page could not be opened. Retry or return to the same place in the Atlas.';
 }
}
function enterMemory(){
 if(!selected||!canControl())return;
 const m=selectedMemory();if(!m)return;
 memoryPreviousFocus=document.activeElement;
 // Freeze precisely the current observation position, even during a camera approach.
 memorySession=openMemory(memoryIndex,selected.id,camera);if(innerWidth<700)memorySession=memoryView(memorySession,'FOLIO');memoryGeneration++;memoryZoom=false;
 target=structuredClone(camera);pointers.clear();pointerStart=null;pinchDistance=null;
 memoryButtons.length=0;$('#memoryPages').replaceChildren();
 for(let i=0;i<m.pages.length;i++){const b=document.createElement('button');b.type='button';b.textContent=String(i+1).padStart(2,'0');b.dataset.memoryPage=i;b.setAttribute('aria-label',m.pages[i].title);b.onclick=()=>{memorySession=navigateMemory(memorySession,memoryIndex,i-memorySession.pageIndex);memoryZoom=false;showMemoryPage();};memoryButtons.push(b);$('#memoryPages').append(b);}
 document.body.classList.add('memory-open');memoryDialog.showModal();$('#memoryBack').focus();showMemoryPage();
}
function exitMemory(){
 if(!memorySession)return;
 const restore=closeMemory(memorySession);memorySession=null;memoryGeneration++;memoryZoom=false;
 camera=structuredClone(restore.camera);target=structuredClone(restore.camera);
 memoryDialog.close();document.body.classList.remove('memory-open');
 memoryImage.removeAttribute('src');memoryImage.hidden=true;
 lastTime=performance.now();if(!restoreFallbackPlace(restore.locationId)&&memoryPreviousFocus?.isConnected)memoryPreviousFocus.focus();
}
function nextMemory(delta){if(!memorySession)return;memorySession=navigateMemory(memorySession,memoryIndex,delta);memoryZoom=false;showMemoryPage();}
$('#openMemory').onclick=enterMemory;$('#memoryBack').onclick=exitMemory;
$('#memoryPrevious').onclick=()=>nextMemory(-1);$('#memoryNext').onclick=()=>nextMemory(1);
$('#memoryView').onclick=()=>{memorySession=memoryView(memorySession,memorySession.view==='FOLIO'?'SCENE':'FOLIO');memoryZoom=false;layoutMemoryImage();};
$('#memoryZoom').onclick=()=>{memoryZoom=!memoryZoom;layoutMemoryImage();};
$('#memoryRetry').onclick=showMemoryPage;
memoryDialog.addEventListener('cancel',e=>{e.preventDefault();exitMemory();});
document.addEventListener('keydown',e=>{
 if(!memorySession)return;
 if(['Escape','ArrowLeft','ArrowRight'].includes(e.key)){e.preventDefault();e.stopImmediatePropagation();if(e.key==='Escape')exitMemory();else nextMemory(e.key==='ArrowLeft'?-1:1);}
},true);
let memoryTouch=null;
$('#memoryViewport').addEventListener('pointerdown',e=>{if(e.pointerType==='touch'&&!memoryZoom)memoryTouch=[e.clientX,e.clientY];});
$('#memoryViewport').addEventListener('pointerup',e=>{if(!memoryTouch)return;const dx=e.clientX-memoryTouch[0],dy=e.clientY-memoryTouch[1];memoryTouch=null;if(Math.abs(dx)>65&&Math.abs(dx)>Math.abs(dy)*1.7)nextMemory(dx<0?1:-1);});
$('#memoryViewport').addEventListener('pointercancel',()=>memoryTouch=null);
window.addEventListener('resize',layoutMemoryImage);
window.__observerMemoryDebug={session:()=>memorySession?structuredClone(memorySession):null,coverage:()=>memoryCoverage(memoryIndex,bindings.map(p=>p.id)),edition:()=>structuredClone(memoryIndex.source)};
