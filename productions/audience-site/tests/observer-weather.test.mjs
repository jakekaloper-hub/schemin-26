import test from 'node:test';
import assert from 'node:assert/strict';
import {existsSync} from 'node:fs';
const target=new URL('../src/observer-weather.mjs',import.meta.url);
const api=existsSync(target)?await import(target.href):null;
const present=()=>assert.ok(api,'Observer weather implementation is missing');
// Synthetic result data: not a report of El Nino's actual results.
const now='2026-11-15T20:00:00Z';
const regions=[{id:'WX-EASTERN-STORM',propagation_order:['REG-EAST','REG-SEA','REG-BASIN','REG-VALLEY'],effects:['wind','road washout']}];
const envelope=(outcomes=['LOSS'])=>({characterId:'CHAR-MANNING-WELTY',season:2026,latestCompletedWeek:9,
 checkedAt:'2026-11-15T19:00:00Z',validUntil:'2026-11-15T21:00:00Z',sourceReceipts:['fixture://verified-result'],
 matches:outcomes.map((outcome,i)=>({season:2026,week:9-i,completion:'FINAL',evidenceStatus:'VERIFIED',outcome}))});
const resolve=(overrides={})=>{present();return api.resolveObserverWeather({mode:'LIVE',now,resultEvidence:envelope(),weatherRegions:regions,baseline:{effects:['rain','wind','fog','lightning']},...overrides});};

test('verified loss suppresses all baseline weather globally',()=>{const x=resolve();assert.equal(x.status,'GLOBAL_CALM');assert.deepEqual(x.effects,[]);assert.deepEqual(x.affectedZoneIds,[]);assert.equal(x.appliesTo,'ALL_LOCATIONS');assert.equal(x.dayNightCycleContinues,true);});
test('one verified win creates a bounded storm presence',()=>{const x=resolve({resultEvidence:envelope(['WIN','LOSS'])});assert.equal(x.status,'EL_NINO_STORM');assert.deepEqual(x.affectedZoneIds,['REG-EAST']);assert.equal(x.consecutiveWins,1);assert.equal(x.streakComplete,true);});
test('verified winning streak increases extent in source-defined order',()=>{const x=resolve({resultEvidence:envelope(['WIN','WIN','WIN','LOSS'])});assert.deepEqual(x.affectedZoneIds,['REG-EAST','REG-SEA','REG-BASIN']);assert.equal(x.consecutiveWins,3);});
test('storm coverage is capped by supplied geography and does not invent zones',()=>{const x=resolve({resultEvidence:envelope(['WIN','WIN','WIN','WIN','WIN'])});assert.equal(x.affectedZoneIds.length,4);assert.equal(x.streakComplete,false);});
test('a missing earlier week gives a known lower bound, never an invented streak',()=>{const e=envelope(['WIN']);e.matches.push({season:2026,week:7,completion:'FINAL',evidenceStatus:'VERIFIED',outcome:'WIN'});const x=resolve({resultEvidence:e});assert.equal(x.consecutiveWins,1);assert.equal(x.streakComplete,false);});
test('projection cannot overrule latest finalized loss',()=>{const e=envelope();e.matches.push({season:2026,week:10,completion:'PROJECTED',evidenceStatus:'PROVISIONAL',outcome:'WIN'});assert.equal(resolve({resultEvidence:e}).status,'GLOBAL_CALM');});
test('a newer unverified final blocks falling back to an older verified result',()=>{const e=envelope(['LOSS','WIN']);e.matches[0].evidenceStatus='PROVISIONAL';const x=resolve({resultEvidence:e});assert.equal(x.status,'UNRESOLVED');assert.equal(x.reason,'LATEST_NOT_VERIFIED');});
test('latest completed week must actually match the envelope',()=>{const e=envelope();e.latestCompletedWeek=8;assert.equal(resolve({resultEvidence:e}).reason,'LATEST_WEEK_MISMATCH');});
test('expired source cannot produce fresh storms or calm claims',()=>{const e=envelope(['WIN']);e.validUntil='2026-11-15T19:59:59Z';assert.equal(resolve({resultEvidence:e}).status,'UNRESOLVED');});
test('future checked-at and inverted validity interval fail closed',()=>{for(const patch of [{checkedAt:'2026-11-15T20:01:00Z'},{validUntil:'2026-11-15T18:00:00Z'}]){const e={...envelope(),...patch};assert.equal(resolve({resultEvidence:e}).status,'UNRESOLVED');}});
test('ties are not silently treated as wins or losses',()=>{assert.equal(resolve({resultEvidence:envelope(['TIE'])}).reason,'NO_WIN_LOSS_DECISION');});
test('missing data and missing source receipts remain unresolved',()=>{assert.equal(resolve({resultEvidence:null}).status,'UNRESOLVED');assert.equal(resolve({resultEvidence:{...envelope(),sourceReceipts:[]}}).status,'UNRESOLVED');});
test('wrong character and another season cannot control El Nino weather',()=>{assert.equal(resolve({resultEvidence:{...envelope(),characterId:'CHAR-OTHER'}}).status,'UNRESOLVED');const e=envelope();e.matches[0].season=2025;assert.equal(resolve({resultEvidence:e}).status,'UNRESOLVED');});
test('duplicate final records and invalid outcomes fail closed',()=>{let e=envelope();e.matches.push({...e.matches[0]});assert.equal(resolve({resultEvidence:e}).status,'UNRESOLVED');e=envelope(['VAGUE']);assert.equal(resolve({resultEvidence:e}).status,'UNRESOLVED');});
test('win cannot invent an absent propagation region',()=>{assert.equal(resolve({resultEvidence:envelope(['WIN']),weatherRegions:[]}).reason,'MISSING_STORM_GEOGRAPHY');});
test('historical presentation is unaffected by todays loss and baseline weather',()=>{const snapshot={period:'2026-W03',evidenceStatus:'VERIFIED',sourceReceipts:['fixture://historical-scene'],effects:['rain'],affectedZoneIds:['REG-EAST']};const a=resolve({mode:'HISTORICAL',historicalSnapshot:snapshot});const b=resolve({mode:'HISTORICAL',historicalSnapshot:snapshot,resultEvidence:envelope(['WIN'])});assert.deepEqual(a,b);assert.equal(a.status,'HISTORICAL_LOCK');assert.deepEqual(a.effects,['rain']);});
test('missing or unverified historical presentation never borrows live conditions',()=>{assert.equal(resolve({mode:'HISTORICAL'}).reason,'HISTORICAL_SNAPSHOT_REQUIRED');assert.equal(resolve({mode:'HISTORICAL',historicalSnapshot:{evidenceStatus:'PROVISIONAL'}}).status,'UNRESOLVED');});
test('weather plans cannot assert damage, route closure or world writes',()=>{const x=resolve({resultEvidence:envelope(['WIN','WIN'])});assert.deepEqual(x.persistentOperations,[]);assert.equal(x.worldMutationAllowed,false);assert.ok(!x.effects.includes('road washout'));assert.ok(!x.effects.includes('lightning'));});
test('weather resolution preserves input objects and source receipts',()=>{const e=envelope(['WIN','LOSS']),before=JSON.stringify(e);const x=resolve({resultEvidence:e});assert.equal(JSON.stringify(e),before);assert.deepEqual(x.sourceReceipts,e.sourceReceipts);x.sourceReceipts.push('other');assert.equal(e.sourceReceipts.length,1);});
test('clock is shared Eastern time and handles seasonal offset without visitor timezone',()=>{present();assert.equal(api.observerClock('2026-11-15T20:00:00Z').hour,15);assert.equal(api.observerClock('2026-07-15T20:00:00Z').hour,16);assert.equal(api.observerClock(now).timeZone,'America/New_York');});
test('ambiguous or invalid instants are rejected, not interpreted in machine local time',()=>{present();for(const input of ['yesterday','2026-11-15T20:00:00',null,'invalid'])assert.throws(()=>api.observerClock(input),/INSTANT/);});
