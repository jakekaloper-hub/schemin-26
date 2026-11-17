import test from 'node:test';
import assert from 'node:assert/strict';
import {existsSync,readFileSync} from 'node:fs';
const url=new URL('../place-history.mjs',import.meta.url);
const api=existsSync(url)?await import(url.href):null;
const sample={history:{status:'RELEASE_CANDIDATE',publicationAuthorized:false,events:[{id:'EVT-A',locationId:'LOC-CLUB',year:2026,week:3,publicationAuthorized:false,effects:{physical:['chili residue']},sourceReceipts:['memo-os/a.md']} ]},locations:[{id:'LOC-CLUB'},{id:'LOC-SWAMP'}],stateAsOf:'end_of_week_3_2026'};
const camera={target:[3,4,5],yaw:.1,pitch:.2,distance:30};
test('history returns only exact source-bound place records, never nearby interpretations',()=>{
 assert.ok(api,'place-history module missing');
 assert.equal(api.historyForLocation(sample,'LOC-CLUB').length,1);
 assert.deepEqual(api.historyForLocation(sample,'LOC-SWAMP'),[]);
 assert.throws(()=>api.historyForLocation(sample,'LOC-FAKE'),/UNKNOWN_LOCATION/);
});
test('history reader retains the camera and is spectator-only with no live weather',()=>{
 assert.ok(api,'place-history module missing');const original=structuredClone(sample);
 const session=api.openPlaceHistory(sample,'LOC-CLUB',camera);
 assert.equal(session.inputOwner,'HISTORY');assert.equal(session.worldMutationAllowed,false);
 assert.equal(session.liveWeatherAllowed,false);
 camera.target[0]=99;
 assert.deepEqual(api.closePlaceHistory(session).camera.target,[3,4,5]);
 assert.deepEqual(sample,original);
 assert.throws(()=>api.openPlaceHistory(sample,'LOC-SWAMP',camera),/NO_HISTORY/);
});
test('host explicitly closes its source-bound history reader before world input resumes',()=>{
 const host=readFileSync(new URL('../app.mjs',import.meta.url),'utf8');
 const layout=readFileSync(new URL('../index.template.html',import.meta.url),'utf8');
 assert.match(host,/updateHistoryEntry\(\)/);
 assert.match(host,/historySession/);
 assert.match(layout,/id="historyDialog"/);
 assert.match(layout,/id="openHistory"/);
});
test('long source receipt paths wrap within narrow mobile history overlay',()=>{
 const layout=readFileSync(new URL('../index.template.html',import.meta.url),'utf8');
 assert.match(layout,/\.history-dialog li\s*,\s*\.history-dialog h2\s*\{[^}]*overflow-wrap:\s*anywhere/);
});
