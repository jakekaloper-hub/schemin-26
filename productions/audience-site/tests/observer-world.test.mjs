import test from 'node:test';
import assert from 'node:assert/strict';
import {existsSync} from 'node:fs';
const target=new URL('../src/observer-world.mjs',import.meta.url);
const api=existsSync(target)?await import(target.href):null;

// Synthetic fixtures. These are not geographic assertions or approved artwork.
const locations=[
 {id:'LOC-ONE',name:'One',canon_status:'PERMANENT_CANON',physical_zone_id:'REG-ONE',abstract_position:[1,2],persistent_landmarks:['gate'],open_questions:['private']},
 {id:'LOC-TWO',name:'Two',canon_status:'PROVISIONAL_CANON',physical_zone_id:'REG-TWO',abstract_position:[3,4]},
 {id:'LOC-THREE',name:'Three',canon_status:'INTERPRETIVE_CANON',physical_zone_id:'REG-TWO',abstract_position:[5,6]},
 {id:'CAND-FOUR',name:'Unauthored',canon_status:'EDITORIAL_ONLY',physical_zone_id:'REG-TWO',abstract_position:[7,8]},
];
const present=()=>assert.ok(api,'Observer-world implementation is missing');
const fresh=(extra={})=>{present();return api.createObserver({locationIds:['LOC-ONE','LOC-TWO'],criticalAssetIds:['world','first-frame'],...extra});};
const ready=(extra={})=>{let s=fresh(extra);for(const id of ['world','first-frame'])s=api.transitionObserver(s,{type:'asset_ready',id});return s;};
const exploring=()=>api.transitionObserver(ready(),{type:'reveal_finished'});

test('all source-defined places exist before personal visits',()=>{present();const a=api.projectAtlas(locations,[]),b=api.projectAtlas(locations,['LOC-ONE']);assert.deepEqual(a.map(x=>x.id),b.map(x=>x.id));assert.equal(a.length,3);assert.ok(a.every(x=>x.visible));assert.equal(a[0].visited,false);assert.equal(b[0].visited,true);});
test('atlas keeps interpretive/provisional status without canon promotion',()=>{present();const p=api.projectAtlas(locations);assert.equal(p[1].canonStatus,'PROVISIONAL_CANON');assert.equal(p[2].canonStatus,'INTERPRETIVE_CANON');assert.ok(p.every(x=>x.publicationAuthorized===false));});
test('atlas does not leak editorial questions or mutate source records',()=>{present();const before=JSON.stringify(locations),p=api.projectAtlas(locations);assert.equal(JSON.stringify(locations),before);assert.equal(JSON.stringify(p).includes('private'),false);p[0].position[0]=100;assert.equal(locations[0].abstract_position[0],1);});
test('duplicate active location IDs and nonfinite positions are rejected',()=>{present();assert.throws(()=>api.projectAtlas([locations[0],locations[0]]),/DUPLICATE/);assert.throws(()=>api.projectAtlas([{...locations[0],abstract_position:[NaN,2]}]),/POSITION/);});
test('opening remains loading until every critical resource is ready',()=>{let s=fresh();assert.equal(s.phase,'LOADING');s=api.transitionObserver(s,{type:'asset_ready',id:'world'});assert.equal(s.phase,'LOADING');assert.equal(s.labels,'NONE');assert.equal(s.avatar,null);});
test('readiness reveals once then yields control without exposing labels',()=>{let s=ready();assert.equal(s.phase,'REVEALING');s=api.transitionObserver(s,{type:'reveal_finished'});assert.equal(s.phase,'EXPLORING');assert.equal(s.labels,'NONE');assert.equal(s.worldMutationAllowed,false);});
test('reduced motion and returning visits bypass cinematic reveal after readiness',()=>{assert.equal(ready({reducedMotion:true}).phase,'EXPLORING');assert.equal(ready({returning:true}).phase,'EXPLORING');assert.equal(fresh({returning:true}).phase,'LOADING');});
test('failed critical asset does not masquerade as a ready world',()=>{let s=fresh();s=api.transitionObserver(s,{type:'asset_failed',id:'world'});assert.equal(s.phase,'FALLBACK');for(const id of ['world','first-frame'])s=api.transitionObserver(s,{type:'asset_ready',id});assert.equal(s.phase,'FALLBACK');s=api.transitionObserver(s,{type:'retry'});assert.equal(s.phase,'LOADING');assert.equal(s.readyAssets.length,0);});
test('unknown asset and premature reveal cannot bypass readiness',()=>{const s=fresh();assert.throws(()=>api.transitionObserver(s,{type:'asset_ready',id:'made-up'}),/UNKNOWN_ASSET/);assert.throws(()=>api.transitionObserver(s,{type:'reveal_finished'}),/NOT_REVEALING/);});
test('inspection identifies only chosen existing place and has no inhabitant effect',()=>{const s=exploring(),before=JSON.stringify(s);const n=api.transitionObserver(s,{type:'inspect',id:'LOC-TWO'});assert.equal(n.locationId,'LOC-TWO');assert.equal(n.labels,'ON_INSPECTION');assert.equal(n.phase,'EXPLORING');assert.equal(n.inhabitantInteractionAllowed,false);assert.equal(JSON.stringify(s),before);assert.throws(()=>api.transitionObserver(s,{type:'inspect',id:'CAND-MADE-UP'}),/UNKNOWN_LOCATION/);});
test('camera views remain spectator perspectives',()=>{for(const mode of ['AERIAL','OVERHEAD','PANORAMIC','GROUND']){const n=api.transitionObserver(exploring(),{type:'camera',mode});assert.equal(n.cameraMode,mode);assert.equal(n.avatar,null);}assert.throws(()=>api.transitionObserver(exploring(),{type:'camera',mode:'PLAYER'}),/CAMERA/);});
test('reader capture blocks camera scrolling and closes to same location',()=>{let s=api.transitionObserver(exploring(),{type:'inspect',id:'LOC-TWO'});s=api.transitionObserver(s,{type:'open_reader',publicationId:'MEMO-TEST',eligible:true});assert.equal(s.inputOwner,'READER');assert.throws(()=>api.transitionObserver(s,{type:'camera',mode:'GROUND'}),/INPUT_OWNER/);s=api.transitionObserver(s,{type:'close_reader'});assert.equal(s.locationId,'LOC-TWO');assert.equal(s.inputOwner,'WORLD');});
test('unreleased reader request never becomes readable by selection alone',()=>{assert.throws(()=>api.transitionObserver(exploring(),{type:'open_reader',publicationId:'MEMO-TEST',eligible:false}),/NOT_ELIGIBLE/);});
test('spectator actions cannot mutate world or speak to inhabitants',()=>{for(const type of ['change_weather','talk_to_character','unlock_location','mutate_world'])assert.throws(()=>api.transitionObserver(exploring(),{type}),/ACTION_NOT_ALLOWED/);});
test('zero critical assets and duplicate asset IDs cannot create false readiness',()=>{present();assert.throws(()=>fresh({criticalAssetIds:[]}),/CRITICAL_ASSETS/);assert.throws(()=>fresh({criticalAssetIds:['world','world']}),/DUPLICATE/);});
