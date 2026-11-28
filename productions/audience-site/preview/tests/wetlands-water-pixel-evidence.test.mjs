import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,existsSync,mkdtempSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {decodePng,roiDifference,encodeRegionDifference,produceWaterEvidence,reviewRegions} from '../tools/water-pixel-evidence.mjs';

const captureDir=fileURLToPath(new URL('../evidence/gpu-wetlands-exact-0736e071-20261123/',import.meta.url));
const resultDir=fileURLToPath(new URL('../evidence/gpu-wetlands-water-region-motion-20261123/',import.meta.url));
const source=JSON.parse(readFileSync(join(captureDir,'manifest.json'),'utf8'));
const result=JSON.parse(readFileSync(join(resultDir,'manifest.json'),'utf8'));
const sha=b=>createHash('sha256').update(b).digest('hex');

test('diagnostic only reads verified historic hardware WebGL2 captures and never elevates authority',()=>{
 assert.equal(source.sourceRevision,'0736e071e4fcd3c70deea60e565293ccfde2230b');
 assert.equal(source.renderer,'three-webgl2');
 assert.match(source.gpu,/Apple M3 Pro/);
 assert.equal(source.weatherStatus,'GLOBAL_CALM');
 assert.equal(source.pausedSceneHashesEqual,true);
 assert.equal(source.ordinaryWaterAdvanced,true);
 assert.equal(source.publicationAuthorized,false);
 assert.equal(result.status,'CANDIDATE_NOT_APPROVED');
 assert.equal(result.publicationAuthorized,false);
 assert.equal(result.sourceRevision,source.sourceRevision);
 assert.equal(result.weatherStatus,'GLOBAL_CALM');
 assert.equal(result.sites.length,3);
 assert.match(result.purpose,/NOT_WATER_ONLY_SEGMENTATION/);
});
test('three exact-source water-focused regions change while controls and paused captures do not',()=>{
 const expected={temple:33,jackson:114,'mud-dogs':311};
 for(const [slug,roi] of Object.entries(reviewRegions)){
  const captures=['01-moving','02-moving','03-paused-a','04-paused-b'].map(s=>source.captures.find(c=>c.file===slug+'-'+s+'.png'));
  assert.ok(captures.every(c=>c&&c.placeId===roi.placeId));
  const frames=captures.map(c=>{
   const filename=join(captureDir,c.file),bytes=readFileSync(filename),img=decodePng(filename);
   assert.equal(img.width,1440);assert.equal(img.height,813);
   assert.equal(bytes.length,c.bytes);assert.equal(img.sha256,c.sha256);
   return img;
  });
  assert.ok(captures[1].waterTime>captures[0].waterTime);
  assert.equal(captures[2].waterTime,captures[3].waterTime);
  const moving=roiDifference(frames[0],frames[1],roi.water);
  const stable=roiDifference(frames[0],frames[1],roi.static);
  const paused=roiDifference(frames[2],frames[3],roi.water);
  assert.equal(moving.changed,expected[slug]);
  assert.equal(stable.changed,0);assert.equal(paused.changed,0);
  const record=result.sites.find(x=>x.slug===slug);
  assert.ok(record);assert.deepEqual(record.waterRegion,roi.water);
  assert.deepEqual(record.stableControlRegion,roi.static);
  assert.equal(record.moving.changed,moving.changed);
  assert.equal(record.staticControl.changed,0);
  assert.equal(record.paused.changed,0);
  const derived=readFileSync(join(resultDir,record.derivedFile));
  assert.equal(sha(derived),record.derivedSha256);
  assert.deepEqual(derived,encodeRegionDifference(frames[0],frames[1],roi.water));
  assert.deepEqual([derived.readUInt32BE(16),derived.readUInt32BE(20)],record.derivedDimensions);
  assert.ok(decodePng(join(resultDir,record.derivedFile)).pixels.length>0);
 }
});
test('diagnostic fails closed on bad regions, altered captures, and preexisting output folders',()=>{
 const f=decodePng(join(captureDir,'temple-01-moving.png'));
 assert.throws(()=>roiDifference(f,f,[0,0,9999,4]),/INVALID_ROI/);
 assert.throws(()=>roiDifference(f,f,[-1,0,4,4]),/INVALID_ROI/);
 const tmp=mkdtempSync(join(tmpdir(),'cw-roi-negative-'));
 try{
  assert.throws(()=>produceWaterEvidence(captureDir,tmp),/EVIDENCE_FOLDER_ALREADY_EXISTS/);
  const bad=join(tmp,'tampered.png');
  const bytes=Buffer.from(readFileSync(join(captureDir,'temple-01-moving.png')));
  bytes[0]=0;writeFileSync(bad,bytes);
  assert.throws(()=>decodePng(bad),/NOT_PNG/);
 }finally{rmSync(tmp,{recursive:true,force:true});}
});
test('visual inspection page links only actual local artifacts with no remote dependencies',()=>{
 const html=readFileSync(join(resultDir,'inspection.html'),'utf8');
 assert.match(html,/CANDIDATE_NOT_APPROVED/);
 assert.match(html,/not water-only/i);
 for(const slug of Object.keys(reviewRegions)){
  assert.ok(html.includes('data-place="'+slug+'"'));
  assert.ok(existsSync(join(resultDir,slug+'-water-region-rgb-difference.png')));
 }
 assert.match(html,/gpu-wetlands-exact-0736e071-20261123/);
 assert.doesNotMatch(html,/(?:src|href)\s*=\s*["']https?:/i);
 assert.doesNotMatch(html,/\b(?:fetch|XMLHttpRequest|sendBeacon|WebSocket)\s*\(/);
 const script=html.match(/<script>([\s\S]*?)<\/script>/)?.[1];
 assert.ok(script);assert.doesNotThrow(()=>new Function(script));
});
