import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,mkdtempSync,writeFileSync,rmSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {WETLAND_TEMPORAL_SITES,verifyWetlandsTemporalSequences} from '../tools/temporal-evidence.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const three=[
 'LOC-COUNTRY-CLUB-JACKSON','LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP'
];
const synthetic=()=>WETLAND_TEMPORAL_SITES.flatMap(({placeId},site)=>[
 {placeId,motionState:'MOVING',waterTime:1,width:1440,height:900,bytes:Buffer.alloc(64,10+site)},
 {placeId,motionState:'MOVING',waterTime:2.5,width:1440,height:900,bytes:Buffer.alloc(64,20+site)},
 {placeId,motionState:'PAUSED',waterTime:2.5,width:1440,height:900,bytes:Buffer.alloc(64,30+site)},
 {placeId,motionState:'PAUSED',waterTime:2.5,width:1440,height:900,bytes:Buffer.alloc(64,30+site)}
]);

test('exact source-only Southern Wetlands site names and coordinates are preserved',()=>{
 assert.deepEqual(WETLAND_TEMPORAL_SITES.map(s=>s.placeId),three);
 for(const {placeId,title} of WETLAND_TEMPORAL_SITES){
  const record=source.locations.find(x=>x.id===placeId);
  assert.ok(record,'no speculative new site');
  assert.equal(record.name,title);
  assert.equal(record.physical_zone_id,'REG-SOUTHERN-WETLANDS');
 }
});
test('three separately keyed moving/paused real-frame sequences validate without borrowing a site',()=>{
 const input=synthetic(),before=input.map(s=>({...s,bytes:Buffer.from(s.bytes)}));
 const result=verifyWetlandsTemporalSequences(input);
 assert.deepEqual(result.map(x=>x.placeId),three);
 assert.ok(result.every(x=>x.movingSceneChanged&&x.pausedSceneHashesEqual));
 assert.deepEqual(input,before,'verification must never mutate evidence');
});
test('fail closed on missing frames, swapped site, absent GPU dimensions or paused pixel drift',()=>{
 assert.throws(()=>verifyWetlandsTemporalSequences(synthetic().slice(0,11)),/twelve physical-GPU frames/);
 const swap=synthetic();swap[4].placeId=three[0];
 assert.throws(()=>verifyWetlandsTemporalSequences(swap),/borrowed a different Atlas location/);
 const dims=synthetic();dims[8].width=0;
 assert.throws(()=>verifyWetlandsTemporalSequences(dims),/viewport dimensions/);
 const unstable=synthetic();unstable[11].bytes=Buffer.alloc(64,99);
 assert.throws(()=>verifyWetlandsTemporalSequences(unstable),/PAUSED_SCENE_VISUAL_DRIFT/);
 const staticFrames=synthetic();staticFrames[1].bytes=staticFrames[0].bytes;
 assert.throws(()=>verifyWetlandsTemporalSequences(staticFrames),/Moving GPU scene frames were identical/);
});
test('GPU capture option refuses an existing Wetlands directory, malformed and mixed modes before Chrome',()=>{
 const script=new URL('../tools/webgl2-journey-smoke.mjs',import.meta.url).pathname;
 const dir=mkdtempSync(join(tmpdir(),'wetlands-temporal-guard-'));
 try{
  const protectedFile=join(dir,'original.txt');writeFileSync(protectedFile,'PRESERVE');
  const command=(...args)=>spawnSync(process.execPath,[script,script,...args],{encoding:'utf8',timeout:6000});
  const protectedRun=command('--wetlands-temporal-dir',dir);
  assert.notEqual(protectedRun.status,0);
  assert.match(protectedRun.stderr,/WETLANDS_DIRECTORY_EXISTS/);
  assert.equal(readFileSync(protectedFile,'utf8'),'PRESERVE');
  for(const args of [['--wetlands-temporal-dir'],['--wetlands-temporal-dir',dir,'--capture-dir',dir],['--temporal-dir',dir,'--wetlands-temporal-dir',dir]]){
   const check=command(...args);assert.notEqual(check.status,0);
   assert.match(check.stderr,/Optional capture argument/);
  }
 }finally{rmSync(dir,{recursive:true,force:true});}
});
