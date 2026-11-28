/** Strict, dependency-free proof of moving and paused scene capture behavior.
 * Compares whole-frame GPU PNGs; this is NOT isolated waterfall-pixel attribution.
 */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';

export function verifyTemporalSceneSequence(captures){
 assert.equal(captures.length,4,'Expected two moving and two paused scene frames');
 const [m0,m1,p0,p1]=captures;
 assert.deepEqual(captures.map(c=>c.motionState),['MOVING','MOVING','PAUSED','PAUSED'],
  'Invalid temporal phase ordering');
 for(const c of captures){
  assert.ok(Buffer.isBuffer(c.bytes)&&c.bytes.length>24,'Missing physical GPU PNG bytes');
  assert.ok(Number.isFinite(c.waterTime),'Missing ordinary water-clock sample');
 }
 assert.ok(m1.waterTime>m0.waterTime+.2,'Moving water time failed to advance');
 assert.equal(p0.waterTime,p1.waterTime,'Paused water clock advanced');
 const hash=c=>createHash('sha256').update(c.bytes).digest('hex');
 assert.notEqual(hash(m0),hash(m1),'Moving GPU scene frames were identical');
 assert.equal(hash(p0),hash(p1),'PAUSED_SCENE_VISUAL_DRIFT: GPU scene changed while water was paused');
 return {movingSceneChanged:true,pausedSceneHashesEqual:true};
}

/** Exact published Atlas identifiers; three existing Southern Wetlands candidate sites.
 * This verifies observed whole-frame motion, not isolation of moving-water pixels.
 * It does not grant scene/canon/publication approval.
 */
export const WETLAND_TEMPORAL_SITES=Object.freeze([
 Object.freeze({placeId:'LOC-COUNTRY-CLUB-JACKSON',title:'Country Club of Jackson',slug:'jackson'}),
 Object.freeze({placeId:'LOC-TDS-WATERFALL-TEMPLE',title:'Podium Shadow Waterfall Temple',slug:'temple'}),
 Object.freeze({placeId:'LOC-MUD-DOGS-SWAMP',title:'Mud Dogs Swamp',slug:'mud-dogs'})
]);

export function verifyWetlandsTemporalSequences(captures){
 assert.equal(captures.length,WETLAND_TEMPORAL_SITES.length*4,'Expected twelve physical-GPU frames across three Southern Wetlands places');
 return WETLAND_TEMPORAL_SITES.map((site,index)=>{
  const group=captures.slice(index*4,index*4+4);
  for(const shot of group){
   assert.equal(shot.placeId,site.placeId,'Temporal capture borrowed a different Atlas location');
   assert.ok(Number.isInteger(shot.width)&&shot.width>=1000&&Number.isInteger(shot.height)&&shot.height>=600,'Missing physical GPU viewport dimensions');
   assert.equal(shot.width,group[0].width,'Temporal site viewport width changed');
   assert.equal(shot.height,group[0].height,'Temporal site viewport height changed');
  }
  return {placeId:site.placeId,...verifyTemporalSceneSequence(group)};
 });
}
