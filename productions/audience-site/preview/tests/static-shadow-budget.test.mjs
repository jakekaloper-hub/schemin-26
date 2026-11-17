import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {shadowCoverage} from '../three-world.mjs';

const camera=(x=0,z=0,distance=100)=>({target:[x,4,z],distance,yaw:.2,pitch:.8});

test('shadow coverage follows the established camera target and bounded distance',()=>{
 const a=shadowCoverage(camera(3,7,100));
 assert.equal(a.span,65);
 assert.equal(a.key,shadowCoverage({...camera(3,7,100),yaw:1.9,pitch:1.1}).key,
  'orbit alone must reuse a fixed-location light shadow map');
 assert.equal(a.key,shadowCoverage({...camera(3,7,100),target:[3,999,7]}).key,
  'vertical look-at value does not alter the fixed-y sun target');
 assert.notEqual(a.key,shadowCoverage(camera(4,7,100)).key);
 assert.notEqual(a.key,shadowCoverage(camera(3,7,115)).key);
 assert.equal(shadowCoverage(camera(0,0,3)).span,20);
 assert.equal(shadowCoverage(camera(0,0,500)).span,140);
 assert.throws(()=>shadowCoverage(camera(0,0,Number.NaN)),/INVALID_SHADOW_COVERAGE/);
});

test('static shadow map invalidation is keyed to coverage, not moving water or light intensity',()=>{
 const src=readFileSync(new URL('../three-world.mjs',import.meta.url),'utf8');
 const anchor=src.indexOf('const {span,key:shadowKey}=shadowCoverage(c);');
 const branch=src.slice(anchor,src.indexOf('lastShadowKey=shadowKey;',anchor)+'lastShadowKey=shadowKey;'.length);
 assert.ok(anchor>0,'renderer applies fixed-source shadow coverage after camera setup');
 assert.match(branch,/if\(shadowKey!==lastShadowKey\)\{/);
 assert.match(branch,/sun\.shadow\.camera\.updateProjectionMatrix\(\);renderer\.shadowMap\.needsUpdate=true;/);
 assert.match(branch,/lastShadowKey=shadowKey;/);
 assert.ok(!/uTime|lastTime|strength|storm/.test(branch),'ambient, storm, and river motion cannot force a shadow-map redraw');
});
