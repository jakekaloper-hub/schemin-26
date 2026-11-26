/* Candidate-only place history from exact World Memory location IDs. */
const {historyForLocation,openPlaceHistory,closePlaceHistory}=PlaceHistory;
const historyDialog=$('#historyDialog');
const historyEntries=$('#historyEntries');
let historySession=null,historyPreviousFocus=null;
function updateHistoryEntry(){
  const items=selected?historyForLocation(catalog,selected.id):[];
  $('#openHistory').hidden=items.length===0;
  $('#historyAvailability').hidden=items.length>0;
  $('#openHistory').textContent=items.length?`RECORDED PLACE HISTORY · ${items.length} ${items.length===1?'ENTRY':'ENTRIES'}`:'';
}
function appendLine(parent,label,values){
  if(!values?.length)return;
  const section=document.createElement('section'),heading=document.createElement('h3'),list=document.createElement('ul');
  heading.textContent=label;
  for(const v of values){const li=document.createElement('li');li.textContent=v;list.append(li);}
  section.append(heading,list);parent.append(section);
}
function enterHistory(){
  if(!selected||!canControl())return;
  historyPreviousFocus=document.activeElement;
  historySession=openPlaceHistory(catalog,selected.id,camera);target=structuredClone(camera);
  cancelWorldGesture();
  $('#historyPlace').textContent=selected.name;
  $('#historyBoundary').textContent=`World Memory · ${catalog.history.status.replaceAll('_',' ')} · recorded as ${catalog.stateAsOf.replaceAll('_',' ')}. Historical source descriptions are not verified present-day conditions, official released folios or approved physical geometry.`;
  historyEntries.replaceChildren();
  for(const event of historySession.entries){
    const card=document.createElement('article'),title=document.createElement('h2'),note=document.createElement('p');
    title.textContent=`${event.year} · Week ${event.week} · ${event.id}`;
    note.textContent='Historical candidate record · read-only';card.append(title,note);
    for(const [key,label] of [['physical','Recorded physical effects'],['social','Recorded social effects'],['reputation','Recorded reputation effects'],['institutional','Recorded institutional effects']])appendLine(card,label,event.effects[key]);
    if(event.expiryCondition){const exp=document.createElement('p');exp.textContent=`Source expiry condition: ${event.expiryCondition}`;card.append(exp);}
    if(event.supersededBy){const note2=document.createElement('p');note2.textContent=`Source supersession: ${event.supersededBy}`;card.append(note2);}
    appendLine(card,'Source receipt paths (not public links)',event.sourceReceipts);
    historyEntries.append(card);
  }
  document.body.classList.add('history-open');historyDialog.showModal();$('#historyBack').focus();
}
function exitHistory(){
  if(!historySession)return;
  const restore=closePlaceHistory(historySession);historySession=null;
  camera=structuredClone(restore.camera);target=structuredClone(restore.camera);
  historyDialog.close();document.body.classList.remove('history-open');
  lastTime=performance.now();if(!restoreFallbackPlace(restore.locationId,true)&&historyPreviousFocus?.isConnected)historyPreviousFocus.focus();
}
$('#openHistory').onclick=enterHistory;$('#historyBack').onclick=exitHistory;
historyDialog.addEventListener('cancel',e=>{e.preventDefault();exitHistory();});
document.addEventListener('keydown',e=>{if(historySession&&e.key==='Escape'){e.preventDefault();e.stopImmediatePropagation();exitHistory();}},true);
window.__observerHistoryDebug={session:()=>historySession?structuredClone(historySession):null,entries:id=>historyForLocation(catalog,id)};
