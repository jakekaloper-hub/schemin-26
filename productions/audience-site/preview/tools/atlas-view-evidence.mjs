/** Read-only physical-GPU Atlas-wide evidence validation and offline viewer.
 * Does not authorize publication, canon mutation, or visual approval. */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';

export const ATLAS_VIEW_COUNT=23;
const validId=id=>typeof id==='string'&&/^LOC-[A-Z0-9-]+$/.test(id);
const safe=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;')
 .replaceAll('>','&gt;').replaceAll('"','&quot;').replaceAll("'",'&#39;');

export function atlasViewPlan(bindings){
 assert.ok(Array.isArray(bindings)&&bindings.length===ATLAS_VIEW_COUNT,'ATLAS_SOURCE_COUNT_DRIFT');
 const seen=new Set();
 return bindings.map((place,index)=>{
  assert.ok(place&&validId(place.id)&&typeof place.name==='string'&&place.name.trim().length>0
   &&typeof place.zoneId==='string'&&/^REG-[A-Z0-9-]+$/.test(place.zoneId),'INVALID_SOURCE_PLACE');
  assert.ok(!seen.has(place.id),'DUPLICATE_SOURCE_PLACE');
  seen.add(place.id);
  const file=String(index+1).padStart(2,'0')+'-'+place.id.toLowerCase()+'.png';
  return {file,placeId:place.id,name:place.name,zoneId:place.zoneId};
 });
}
export function verifyAtlasCandidateCaptures(plan,captures){
 assert.ok(Array.isArray(plan)&&plan.length===ATLAS_VIEW_COUNT,'INVALID_ATLAS_PLAN');
 assert.ok(Array.isArray(captures)&&captures.length===ATLAS_VIEW_COUNT,'INCOMPLETE_ATLAS_GPU_COVERAGE');
 const seenFiles=new Set(),seenHashes=new Set();
 for(let i=0;i<ATLAS_VIEW_COUNT;i++){
  const expected=plan[i],shot=captures[i];
  assert.ok(expected&&validId(expected.placeId)&&typeof expected.file==='string','INVALID_ATLAS_PLAN_ITEM');
  assert.ok(shot&&shot.file===expected.file&&shot.placeId===expected.placeId,'ATLAS_SOURCE_ORDER_MISMATCH');
  assert.ok(!seenFiles.has(shot.file),'DUPLICATE_ATLAS_CAPTURE');
  seenFiles.add(shot.file);
  assert.ok(Buffer.isBuffer(shot.bytes)&&shot.bytes.length>=24
   &&shot.bytes.subarray(0,8).toString('hex')==='89504e470d0a1a0a','INVALID_PHYSICAL_PNG');
  assert.ok(shot.width>=1000&&shot.height>=600
   &&shot.bytes.readUInt32BE(16)===shot.width
   &&shot.bytes.readUInt32BE(20)===shot.height,'INVALID_CAPTURE_DIMENSIONS');
  assert.ok(Number.isInteger(shot.frames)&&shot.frames>0,'NO_GPU_FRAMES');
  assert.ok(shot.camera&&Array.isArray(shot.camera.target)&&shot.camera.target.length===3
   &&[...shot.camera.target,shot.camera.distance,shot.camera.yaw,shot.camera.pitch].every(Number.isFinite),'INVALID_CAMERA_EVIDENCE');
  const digest=createHash('sha256').update(shot.bytes).digest('hex');
  assert.ok(!seenHashes.has(digest),'DUPLICATE_GPU_VIEW_PIXELS');
  seenHashes.add(digest);
 }
 return {sourcePlaces:ATLAS_VIEW_COUNT,uniqueIds:ATLAS_VIEW_COUNT,uniquePngHashes:seenHashes.size,complete:true};
}
export function atlasContactSheetHtml(plan,{sourceRevision,stateAsOf,gpu,renderer}={}){
 assert.ok(Array.isArray(plan)&&plan.length===ATLAS_VIEW_COUNT,'INVALID_ATLAS_PLAN');
 assert.ok(typeof sourceRevision==='string'&&/^[0-9a-f]{40}$/.test(sourceRevision),'INVALID_SOURCE_REVISION');
 const cards=plan.map(place=>`<figure><a href="${safe(place.file)}"><img src="${safe(place.file)}" alt="${safe(place.name)} candidate physical GPU scene" loading="lazy"></a><figcaption><strong>${safe(place.name)}</strong><small>${safe(place.placeId)} · ${safe(place.zoneId)}</small></figcaption></figure>`).join('\n');
 return `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Commonwealth · Atlas physical-GPU candidate review</title>
<style>*,*::before,*::after{box-sizing:border-box}body{margin:0;padding:1.5rem;background:#121b1b;color:#e6ece7;font:15px/1.55 system-ui,sans-serif}main{max-width:1680px;margin:auto}h1{font-size:clamp(1.5rem,2.5vw,2.5rem)}p{max-width:80ch;color:#b7c4c1}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,350px),1fr));gap:1.1rem;margin-top:2rem}figure{margin:0;padding:.6rem;background:#21302e;border:1px solid #3e5350;border-radius:.55rem}img{width:100%;aspect-ratio:1440/813;object-fit:contain;display:block;background:#17201f}a:focus-visible{outline:3px solid #b0e8d6}figcaption{padding:.5rem .15rem .1rem}small{display:block;overflow-wrap:anywhere;color:#b6c9c1}code{overflow-wrap:anywhere}</style></head><body><main>
<h1>Commonwealth Atlas · 23 source places</h1>
<p><strong>Unpublished candidate inspection, not approved cinematic artwork.</strong> Actual opt-in physical-WebGL2 screenshots, one frame per existing Atlas place. This contact sheet is offline and read-only. It does not claim a water-only motion proof, canonical geometry, current live weather, creator acceptance, or a release.</p>
<p>Source revision: <code>${safe(sourceRevision)}</code> · state as recorded: ${safe(stateAsOf)} · renderer: ${safe(renderer)} · observed GPU: ${safe(gpu)}</p>
<div class="grid">${cards}</div></main></body></html>\n`;
}
