import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(atlas.locations)});
const snapshot=JSON.stringify(bindings);
const crossingId='LOC-TDS-CHILI-SHARED-MARCH';
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
function smoothstep(a,b,x){const u=Math.max(0,Math.min(1,(x-a)/(b-a)));return u*u*(3-2*u);}
function crest(x,y,time){
 const interior=1-smoothstep(.58,.95,Math.hypot(x,y));
 const wave=Math.sin(y*18.8-time*2.1+Math.sin(x*5)*.55);
 return interior*smoothstep(.38,.90,wave);
}

test('source-gated optical crest reuses the original displaced watercourse and one mesh',()=>{
 const world=build();
 const crossing=world.locations.find(s=>s.id===crossingId);
 const active=world.water.filter(w=>w.material.uniforms.uCrossing.value===1);
 assert.ok(crossing);
 assert.equal(world.locations.length,20);
 assert.equal(world.water.length,4);
 assert.equal(active.length,1);
 const water=active[0];
 assert.equal(water.kind,'watercourse crossing');
 assert.ok(crossing.group.children.includes(water.mesh));
 assert.equal(water.mesh.children.length,0);
 assert.equal(water.mesh.geometry.getAttribute('position').count,393);
 assert.equal(water.mesh.geometry.index.count,2184);
 assert.equal(water.material.depthWrite,false);
 for(const w of world.water)assert.equal(w.material.uniforms.uCrossing.value,w===water?1:0);
 assert.deepEqual(world.principalCharacters,[]);
 assert.equal(world.worldMutationAllowed,false);
 assert.equal(world.weatherMutationAllowed,false);
 assert.equal(JSON.stringify(bindings),snapshot);
 world.dispose();
});

test('GLSL optical crest is tied to physical crossing phase, not weather or another site',()=>{
 const world=build(),water=world.water.find(w=>w.kind==='watercourse crossing');
 const vs=water.material.vertexShader,fs=water.material.fragmentShader;
 assert.match(vs,/varying float vCrossCrest;/);
 assert.match(fs,/varying float vCrossCrest;/);
 assert.ok(vs.includes('vCrossCrest=uCrossing*interior*smoothstep(.38,.90,crossingWave);'));
 assert.ok(vs.includes('p.z+=uCrossing*uAmplitude*.34*interior*crossingWave;'));
 assert.ok(fs.includes('vec3 crossingKey=normalize(vec3(.43,.74,.51));'));
 assert.ok(fs.includes('float crossingSpark=pow(max(dot(reflect(-crossingKey,crossingNormal),eyeRay),0.),10.);'));
 assert.ok(fs.includes('float crossingCrest=vCrossCrest*(.35+.65*crossingSpark);'));
 assert.ok(fs.includes('c=clamp(c+vec3(.032,.048,.045)*crossingCrest,0.,1.);'));
 assert.ok(!fs.includes('uStorm')&&!fs.includes('uGlobalCalm'));
 assert.ok(!Object.hasOwn(water.material.uniforms,'uCrossCrest'),'one varying, zero new uniforms');
 for(const w of world.water.filter(w=>w!==water))assert.equal(w.material.uniforms.uCrossing.value,0);
 world.dispose();
});

test('optical crest advances under global calm, stays inside shoreline, freezes on explicit pause',()=>{
 const world=build();
 let varying=0,peak=0;
 for(let xi=-9;xi<=9;xi++)for(let yi=-9;yi<=9;yi++){
  const x=xi/10,y=yi/10,a=crest(x,y,1.2),b=crest(x,y,3.7);
  assert.ok(Number.isFinite(a)&&Number.isFinite(b));
  assert.ok(a>=0&&a<=1&&b>=0&&b<=1,'bounded optical highlight');
  if(Math.hypot(x,y)>=.95)assert.ok(a<1e-12&&b<1e-12,'old shoreline unchanged');
  varying=Math.max(varying,Math.abs(a-b));
  peak=Math.max(peak,a,b);
 }
 assert.ok(peak>.5,'moving wave has eligible crests');
 assert.ok(varying>.5,'ordinary water phase moves crest illumination');
 world.tick(1.2,{globalCalm:true,storm:0});
 world.tick(3.7,{globalCalm:true,storm:0});
 assert.ok(world.water.every(w=>w.material.uniforms.uTime.value===3.7));
 world.tick(8,{paused:true});
 assert.ok(world.water.every(w=>w.material.uniforms.uTime.value===3.7));
 assert.equal(JSON.stringify(bindings),snapshot);
 world.dispose();
});
