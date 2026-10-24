import test from 'node:test';
import assert from 'node:assert/strict';
import {loadProgress,saveProgress} from '../src/progress.js';
function reset(){const values=new Map();globalThis.localStorage={getItem:k=>values.get(k)??null,setItem:(k,v)=>values.set(k,v)};return values;}
test('progress survives reload-equivalent reads for the same accepted source',()=>{reset();saveProgress('chapter-1',.55,'sha-a');assert.equal(loadProgress('chapter-1','sha-a'),.55);});
test('progress cannot cross publication or source-version boundaries',()=>{reset();saveProgress('chapter-1',.7,'sha-a');assert.equal(loadProgress('chapter-1','sha-b'),0);assert.equal(loadProgress('chapter-2','sha-a'),0);});
test('corrupt and blocked storage do not prevent reading',()=>{const values=reset();saveProgress('chapter-1',.5,'sha-a');for(const k of values.keys())values.set(k,'{corrupt');assert.equal(loadProgress('chapter-1','sha-a'),0);globalThis.localStorage={getItem(){throw new Error('denied')},setItem(){throw new Error('denied')}};assert.equal(loadProgress('chapter-1','sha-a'),0);assert.doesNotThrow(()=>saveProgress('chapter-1',.2,'sha-a'));});
test('invalid saved values never escape the normalized position range',()=>{reset();saveProgress('chapter-1',NaN,'sha-a');assert.equal(loadProgress('chapter-1','sha-a'),0);saveProgress('chapter-1',4,'sha-a');assert.equal(loadProgress('chapter-1','sha-a'),1);});
