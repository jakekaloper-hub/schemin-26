/** Presentation-only El Nino policy. Consumes upstream evidence; never verifies league truth.
 * No provider is called. Caller must provide authoritative, fresh source receipts.
 * Founder rule applies only to LIVE observer mode, not historical canon or damage.
 */
const CHAR='CHAR-MANNING-WELTY';
const ALLOWED_EFFECTS=new Set(['rain','snow','wind','fog','cloud','lightning','thunder']);
const strings=x=>Array.isArray(x)&&x.length>0&&x.every(v=>typeof v==='string'&&v.trim().length>0);
function instant(value){
  if(typeof value!=='string'||!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$/.test(value))return NaN;
  return Date.parse(value);
}
function base(mode){return {mode,policyVersion:'OBSERVER-2026-11-15',worldMutationAllowed:false,persistentOperations:[],sourceReceipts:[],effects:[],affectedZoneIds:[],dayNightCycleContinues:mode==='LIVE'};}
function unresolved(mode,reason){return {...base(mode),status:'UNRESOLVED',reason};}

/** Shared wall-clock time only; this is not a solar-position/weather-provider calculation. */
export function observerClock(value){
  const ms=instant(value);if(!Number.isFinite(ms))throw new Error('INVALID_INSTANT');
  const timeZone='America/New_York';
  const parts=new Intl.DateTimeFormat('en-US',{timeZone,year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit',hourCycle:'h23'}).formatToParts(new Date(ms));
  const values=Object.fromEntries(parts.filter(p=>p.type!=='literal').map(p=>[p.type,p.value]));
  return {timeZone,date:`${values.year}-${values.month}-${values.day}`,hour:Number(values.hour),minute:Number(values.minute),second:Number(values.second)};
}

/**
 * @param {object} input Source evidence is supplied, not fetched or promoted by this module.
 * `baseline` is deliberately suppressed on LOSS; a live southeastern-US provider adapter
 * is not implemented here. On WIN this returns the El Nino overlay only.
 */
export function resolveObserverWeather({mode,now,resultEvidence,weatherRegions=[],historicalSnapshot}){
  if(mode==='HISTORICAL'){
    const s=historicalSnapshot;
    if(!s||s.evidenceStatus!=='VERIFIED'||!strings(s.sourceReceipts)||typeof s.period!=='string'||!s.period.trim()||!Array.isArray(s.effects)||s.effects.some(x=>!ALLOWED_EFFECTS.has(x))||!Array.isArray(s.affectedZoneIds)||!s.affectedZoneIds.every(x=>typeof x==='string'&&x.startsWith('REG-')))return unresolved(mode,'HISTORICAL_SNAPSHOT_REQUIRED');
    return {...base(mode),status:'HISTORICAL_LOCK',period:s.period,sourceReceipts:[...s.sourceReceipts],effects:[...s.effects],affectedZoneIds:[...s.affectedZoneIds]};
  }
  if(mode!=='LIVE')return unresolved(mode,'INVALID_MODE');
  const e=resultEvidence,t=instant(now);
  if(!e||e.characterId!==CHAR||!Number.isInteger(e.season)||!Number.isInteger(e.latestCompletedWeek)||e.latestCompletedWeek<1||e.latestCompletedWeek>18||!strings(e.sourceReceipts)||!Array.isArray(e.matches))return unresolved(mode,'RESULT_EVIDENCE_REQUIRED');
  const checked=instant(e.checkedAt),until=instant(e.validUntil);
  if(![t,checked,until].every(Number.isFinite)||checked>t||until<=t||until<=checked)return unresolved(mode,'STALE_OR_INVALID_RESULT_EVIDENCE');
  const finals=e.matches.filter(x=>x?.completion==='FINAL');
  if(!finals.length)return unresolved(mode,'NO_FINAL_RESULTS');
  if(finals.some(x=>x.season!==e.season||!Number.isInteger(x.week)||x.week<1||x.week>18||!['WIN','LOSS','TIE'].includes(x.outcome)))return unresolved(mode,'INVALID_FINAL_RESULT');
  if(new Set(finals.map(x=>x.week)).size!==finals.length)return unresolved(mode,'DUPLICATE_FINAL_WEEK');
  const latest=Math.max(...finals.map(x=>x.week));
  if(latest!==e.latestCompletedWeek)return unresolved(mode,'LATEST_WEEK_MISMATCH');
  const byWeek=new Map(finals.map(x=>[x.week,x]));
  const last=byWeek.get(latest);
  if(last.evidenceStatus!=='VERIFIED')return unresolved(mode,'LATEST_NOT_VERIFIED');
  const result={...base(mode),resultWeek:latest,sourceReceipts:[...e.sourceReceipts]};
  if(last.outcome==='LOSS')return {...result,status:'GLOBAL_CALM',appliesTo:'ALL_LOCATIONS',consecutiveWins:0,streakComplete:true};
  if(last.outcome!=='WIN')return unresolved(mode,'NO_WIN_LOSS_DECISION');
  let wins=0,complete=false;
  for(let week=latest;week>=1;week--){
    const match=byWeek.get(week);
    if(!match||match.evidenceStatus!=='VERIFIED')break;
    if(match.outcome!=='WIN'){complete=true;break;}
    wins++;
    if(week===1)complete=true;
  }
  const regions=Array.isArray(weatherRegions)?weatherRegions:[];
  const storms=regions.filter(x=>x?.id==='WX-EASTERN-STORM');
  const order=storms[0]?.propagation_order;
  if(storms.length!==1||!strings(order)||order.some(x=>!x.startsWith('REG-'))||new Set(order).size!==order.length)return unresolved(mode,'MISSING_STORM_GEOGRAPHY');
  // Candidate tuning: one more source-defined zone per verified consecutive win.
  // Never creates geography, route closures, flood damage, or cinematic lightning.
  return {...result,status:'EL_NINO_STORM',consecutiveWins:wins,streakComplete:complete,
    affectedZoneIds:order.slice(0,Math.min(wins,order.length)),effects:['cloud','rain','wind'],
    baselineWeather:'NOT_CONNECTED',coverageRule:'ONE_ORDERED_ZONE_PER_KNOWN_WIN_CAPPED'};
}
