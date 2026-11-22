import test from 'node:test';
import assert from 'node:assert/strict';
import {verifyTemporalSceneSequence} from '../tools/temporal-evidence.mjs';

const sample=()=>[
 {motionState:'MOVING',waterTime:1,bytes:Buffer.alloc(64,1)},
 {motionState:'MOVING',waterTime:2,bytes:Buffer.alloc(64,2)},
 {motionState:'PAUSED',waterTime:2,bytes:Buffer.alloc(64,2)},
 {motionState:'PAUSED',waterTime:2,bytes:Buffer.alloc(64,2)}
];
test('moving then visually frozen GPU frame sequence produces bounded proof',()=>{
 assert.deepEqual(verifyTemporalSceneSequence(sample()),{movingSceneChanged:true,pausedSceneHashesEqual:true});
});
test('rejects falsified moving-frame change despite clock progression',()=>{
 const s=sample();s[1].bytes=s[0].bytes;
 assert.throws(()=>verifyTemporalSceneSequence(s),/Moving GPU scene frames were identical/);
});
test('rejects paused visual drift even when water clock is frozen',()=>{
 const s=sample();s[3].bytes=Buffer.alloc(64,3);
 assert.throws(()=>verifyTemporalSceneSequence(s),/PAUSED_SCENE_VISUAL_DRIFT/);
});
test('rejects paused clock drift and reordered phase claims',()=>{
 const s=sample();s[3].waterTime=2.01;
 assert.throws(()=>verifyTemporalSceneSequence(s),/Paused water clock advanced/);
 s[3].waterTime=2;s[3].motionState='MOVING';
 assert.throws(()=>verifyTemporalSceneSequence(s),/Invalid temporal phase ordering/);
});
test('rejects absent frames and made-up water measurements',()=>{
 assert.throws(()=>verifyTemporalSceneSequence(sample().slice(0,3)),/Expected two moving and two paused/);
 const s=sample();s[0].waterTime=NaN;
 assert.throws(()=>verifyTemporalSceneSequence(s),/Missing ordinary water-clock sample/);
});
