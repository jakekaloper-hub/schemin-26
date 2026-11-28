import test from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFileSync,readdirSync} from 'node:fs';

const evidence=new URL('../evidence/gpu-atlas-material-response-20261122/',import.meta.url);
const baseline=new URL('../evidence/gpu-atlas-views-20261122-1528/',import.meta.url);
const json=(root,file)=>JSON.parse(readFileSync(new URL(file,root),'utf8'));
const after=json(evidence,'manifest.json');
const before=json(baseline,'manifest.json');
const comparison=json(evidence,'comparison-manifest.json');
const catalog=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
const cameraNumbers=c=>[...c.target,c.distance,c.yaw,c.pitch];

test('material response evidence is source-pinned, full-coverage and cryptographically intact',()=>{
 assert.equal(before.sourceRevision,'8ae8615fad190af2a4308438d04270bdf4c76eef');
 assert.equal(after.sourceRevision,'7a03257e0bf745a18819a0aa97506b988c6f149a');
 assert.equal(comparison.baselineRevision,before.sourceRevision);
 assert.equal(comparison.candidateRevision,after.sourceRevision);
 assert.equal(after.status,'CANDIDATE_NOT_APPROVED');
 assert.equal(comparison.status,'CANDIDATE_NOT_APPROVED');
 assert.equal(after.publicationAuthorized,false);
 assert.equal(comparison.publicationAuthorized,false);
 assert.equal(after.renderer,'three-webgl2');
 assert.match(after.gpu,/Apple M3 Pro/);
 assert.doesNotMatch(after.gpu,/SwiftShader|Software Rasterizer|llvmpipe/i);
 assert.equal(after.stateAsOf,'end_of_week_3_2026');
 assert.equal(after.originalHistoryJourneyPassed,true);
 assert.equal(after.ordinaryWaterAdvanced,true);
 assert.equal(after.sourceUnchanged,true);
 const locations=catalog.locations;
 assert.equal(locations.length,23);
 const expected=new Set(locations.map(x=>x.id));
 assert.equal(expected.size,23);
 for(const shots of [before.captures,after.captures,comparison.pairs]){
  assert.equal(shots.length,23);
  assert.deepEqual(new Set(shots.map(x=>x.placeId)),expected);
 }
 const names=new Map(locations.map(x=>[x.id,x.name]));
 for(let i=0;i<23;i++){
  const b=before.captures[i],a=after.captures[i],p=comparison.pairs[i];
  assert.equal(a.placeId,b.placeId);
  assert.equal(a.file,b.file);
  assert.equal(p.file,a.file);
  assert.equal(p.placeId,a.placeId);
  assert.equal(p.sourceName,names.get(a.placeId));
  for(const [root,shot] of [[baseline,b],[evidence,a]]){
   assert.match(shot.file,/^\d{2}-loc-[a-z0-9-]+\.png$/);
   const bytes=readFileSync(new URL(shot.file,root));
   assert.equal(bytes.subarray(0,8).toString('hex'),'89504e470d0a1a0a');
   assert.equal(bytes.readUInt32BE(16),1440);
   assert.equal(bytes.readUInt32BE(20),813);
   assert.equal(shot.bytes,bytes.length);
   assert.equal(hash(bytes),shot.sha256);
  }
  assert.equal(p.baselineSha256,b.sha256);
  assert.equal(p.candidateSha256,a.sha256);
  const o=cameraNumbers(b.camera),n=cameraNumbers(a.camera);
  assert.ok([...o,...n].every(Number.isFinite));
  const delta=Math.max(...o.map((v,j)=>Math.abs(v-n[j])));
  assert.ok(delta<.01,'Camera not comparable: '+p.placeId);
  assert.ok(Math.abs(delta-p.cameraMaxAbsDelta)<1e-7);
 }
 assert.deepEqual(new Set(readdirSync(evidence).filter(x=>x.endsWith('.png'))),
  new Set(after.captures.map(x=>x.file)));
});

test('offline before/after inspection links every source frame without private or remote assets',()=>{
 const html=readFileSync(new URL('comparison.html',evidence),'utf8');
 const contact=readFileSync(new URL('inspection.html',evidence),'utf8');
 assert.match(html,/CANDIDATE_NOT_APPROVED/);
 assert.match(html,/cannot establish isolated pixel-causal changes/);
 assert.doesNotMatch(html,/https?:\/\/|<script|\.jpe?g\b|<iframe/i);
 for(const shot of after.captures){
  assert.ok(html.includes('src="'+shot.file+'"'));
  assert.ok(html.includes('src="../gpu-atlas-views-20261122-1528/'+shot.file+'"'));
  assert.ok(contact.includes(shot.file));
 }
 assert.equal((html.match(/class="place"/g)||[]).length,23);
});
