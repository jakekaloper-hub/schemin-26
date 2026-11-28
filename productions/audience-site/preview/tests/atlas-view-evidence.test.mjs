import test from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {mkdtempSync,writeFileSync,readFileSync,rmSync} from 'node:fs';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {atlasViewPlan,verifyAtlasCandidateCaptures,atlasContactSheetHtml} from '../tools/atlas-view-evidence.mjs';

const source=Array.from({length:23},(_,i)=>({id:'LOC-TEST-'+(i+1),name:'Read-only place '+(i+1),zoneId:'REG-SOUTHERN-WETLANDS'}));
const png=i=>{
 const b=Buffer.alloc(80+i,i+1);
 Buffer.from('89504e470d0a1a0a','hex').copy(b,0);
 b.writeUInt32BE(1440,16);b.writeUInt32BE(813,20);return b;
};
const frames=plan=>plan.map((place,i)=>({...place,bytes:png(i),width:1440,height:813,frames:1,
 camera:{target:[i,0,1],distance:20,yaw:.4,pitch:.6}}));
test('all 23 source identities map to one ordered unique candidate filename without new place invention',()=>{
 const plan=atlasViewPlan(source);
 assert.equal(plan.length,23);assert.equal(plan[0].file,'01-loc-test-1.png');
 assert.equal(plan.at(-1).file,'23-loc-test-23.png');
 assert.deepEqual(verifyAtlasCandidateCaptures(plan,frames(plan)),
  {sourcePlaces:23,uniqueIds:23,uniquePngHashes:23,complete:true});
 assert.throws(()=>atlasViewPlan(source.slice(1)),/ATLAS_SOURCE_COUNT_DRIFT/);
 assert.throws(()=>atlasViewPlan([...source.slice(0,22),source[0]]),/DUPLICATE_SOURCE_PLACE/);
});
test('GPU evidence verifier rejects absent places, spoofed identity, duplicated frames and false PNG dimensions',()=>{
 const plan=atlasViewPlan(source),valid=frames(plan);
 assert.throws(()=>verifyAtlasCandidateCaptures(plan,valid.slice(1)),/INCOMPLETE_ATLAS_GPU_COVERAGE/);
 const wrong=frames(plan);wrong[4].placeId='LOC-NOT-SOURCE';
 assert.throws(()=>verifyAtlasCandidateCaptures(plan,wrong),/ATLAS_SOURCE_ORDER_MISMATCH/);
 const duplicate=frames(plan);duplicate[1].bytes=duplicate[0].bytes;
 assert.throws(()=>verifyAtlasCandidateCaptures(plan,duplicate),/DUPLICATE_GPU_VIEW_PIXELS/);
 const corrupt=frames(plan);corrupt[0].width=5;
 assert.throws(()=>verifyAtlasCandidateCaptures(plan,corrupt),/INVALID_CAPTURE_DIMENSIONS/);
});
test('offline contact sheet safely escapes source names without scripts or external resources',()=>{
 const plan=atlasViewPlan(source);
 plan[0].name='<script>bad()</script>';
 const html=atlasContactSheetHtml(plan,{sourceRevision:'a'.repeat(40),stateAsOf:'end_of_week_3_2026',gpu:'Apple M3 Pro',renderer:'three-webgl2'});
 assert.match(html,/&lt;script&gt;bad\(\)&lt;\/script&gt;/);
 assert.doesNotMatch(html,/<script[ >]/);
 assert.doesNotMatch(html,/https?:\/\//);
 assert.equal((html.match(/<figure>/g)||[]).length,23);
});
test('new atlas-wide mode rejects destination overwrite and mixed options before launching Chrome',()=>{
 const script=new URL('../tools/webgl2-journey-smoke.mjs',import.meta.url).pathname;
 const dir=mkdtempSync(join(tmpdir(),'cw-atlas-guard-'));
 try{
  writeFileSync(join(dir,'original.txt'),'DO NOT REPLACE');
  const p=spawnSync(process.execPath,[script,script,'--atlas-views-dir',dir],{encoding:'utf8',timeout:6000});
  assert.notEqual(p.status,0);assert.match(p.stderr,/ATLAS_DIRECTORY_EXISTS/);
  assert.equal(readFileSync(join(dir,'original.txt'),'utf8'),'DO NOT REPLACE');
  const mixed=spawnSync(process.execPath,[script,script,'--atlas-views-dir',dir,'--capture-dir',dir],{encoding:'utf8',timeout:6000});
  assert.notEqual(mixed.status,0);assert.match(mixed.stderr,/Optional capture argument/);
 }finally{rmSync(dir,{recursive:true,force:true});}
});
