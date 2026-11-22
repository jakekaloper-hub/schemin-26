/** Strict, dependency-free proof of moving and paused scene capture behavior.
 * Compares whole-frame GPU PNGs; this is NOT isolated waterfall-pixel attribution.
 */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';

export function verifyTemporalSceneSequence(captures){
 assert.equal(captures.length,4,'Expected two moving and two paused Temple frames');
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
