import test from 'node:test';
import assert from 'node:assert/strict';
import {parseRoute,routeHash} from '../src/routes.js';

test('direct memo deep link resolves exact requested week',()=>{
  assert.deepEqual(parseRoute('#memo/week-9'),{page:'memo',id:'week-9'});
});

test('unknown memo id is preserved for unavailable-state handling and never falls back',()=>{
  assert.deepEqual(parseRoute('#memo/week-404'),{page:'memo',id:'week-404'});
});

test('encoded ids decode deterministically',()=>{
  assert.deepEqual(parseRoute('#character/CHAR-JAKE-KALOPER'),{page:'character',id:'CHAR-JAKE-KALOPER'});
  assert.equal(routeHash('memo','week-9'),'#memo/week-9');
});

test('invalid percent encoding fails closed to missing route',()=>{
  assert.deepEqual(parseRoute('#memo/%E0%A4%A'),{page:'missing',id:null});
});

test('empty and root hashes resolve home',()=>{
  assert.deepEqual(parseRoute(''),{page:'home',id:null});
  assert.deepEqual(parseRoute('#home'),{page:'home',id:null});
});
