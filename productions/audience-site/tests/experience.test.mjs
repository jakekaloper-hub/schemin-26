import test from 'node:test';
import assert from 'node:assert/strict';
import {projectPoint,readRoute,chooseMemo,clampPage,loadPreference,savePreference,relatedRecords} from '../src/experience.js';
test('north stays above south in the canonical abstract coordinate system',()=>{assert.ok(projectPoint({x:50,y:80}).y<projectPoint({x:50,y:20}).y);assert.equal(projectPoint({x:0,y:0}).x,90);});
test('deep links decode identity and page without crashing on malformed encodings',()=>{assert.deepEqual(readRoute('#memo/week-3?page=7'),{page:'memo',id:'week-3',query:'page=7'});assert.equal(readRoute('#character/%E0%A4%A').page,'missing');});
test('featured release never silently promotes a source edition',()=>{const a=[{id:'week-6',releaseState:'SOURCE_VERIFIED_NOT_RELEASE_PROMOTED'},{id:'week-3',releaseState:'RELEASED'}];assert.equal(chooseMemo(a,'week-3').id,'week-3');assert.equal(chooseMemo(a,'missing'),null);assert.equal(chooseMemo(a,null),null);});
test('page indexes reject non-finite and fractional input and stay in range',()=>{assert.equal(clampPage('abc',14),1);assert.equal(clampPage(100,14),14);assert.equal(clampPage(0,14),1);assert.equal(clampPage(3.7,14),3);});
test('corrupt or unavailable preference storage never blocks the experience',()=>{const s={getItem:()=>'{broken',setItem:()=>{throw Error('blocked')}};assert.equal(loadPreference('x',7,s),7);assert.doesNotThrow(()=>savePreference('x',8,s));});
test('relationships expose only explicit ids, never generic recommendations as evidence',()=>{assert.deepEqual(relatedRecords([{id:'a',characterIds:['x']},{id:'b'}],'characterIds','x').map(x=>x.id),['a']);});
