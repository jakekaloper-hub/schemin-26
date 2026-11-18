import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';
const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)});
const original=JSON.stringify(bindings);
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
const smooth=(a,b,v)=>{const t=Math.max(0,Math.min(1,(v-a)/(b-a)));return t*t*(3-2*t);};
const fract=v=>v-Math.floor(v);
const hash=(x,y)=>fract(Math.sin(x*127.1+y*311.7)*43758.5453);
function noise(x,y){
 const ix=Math.floor(x),iy=Math.floor(y),fx=fract(x),fy=fract(y),sx=fx*fx*(3-2*fx),sy=fy*fy*(3-2*fy);
 const lo=hash(ix,iy)*(1-sx)+hash(ix+1,iy)*sx,hi=hash(ix,iy+1)*(1-sx)+hash(ix+1,iy+1)*sx;
 return lo*(1-sy)+hi*sy;
}
function smokeOpacity(u,v,t){
 const rise=Math.max(0,Math.min(1,v)),a=u*4.2,b=v*3.9-t*.39;
 const coarse=noise(a*1.8,b*1.8),fine=noise(a*4.1+11.7,b*4.1-t*.12);
 const drift=.075*Math.sin(rise*5.7-t*.61)+.034*Math.sin(rise*13.1-t*.27);
 const spread=.11+(.36-.11)*rise,across=Math.abs(u-.5-drift),body=1-smooth(spread*.52,spread,across);
 const breakup=Math.max(0,Math.min(1,.64+.52*(coarse-.5)+.36*(fine-.5)));
 return Math.min(.22,.22*body*breakup*smooth(0,.12,rise)*(1-smooth(.72,1,rise)));
}
test('existing Chili pit smoke is source-exact, isolated, and has no additional draw geometry',()=>{
 const a=build(),chili=a.locations.find(x=>x.id==='LOC-CHILI-STABLE');
 assert.ok(chili);
 assert.ok(source.locations.find(x=>x.id==='LOC-CHILI-STABLE').persistent_landmarks.includes('pit smoke'));
 const smoke=chili.group.children.filter(x=>x.name==='Authored pit smoke');
 assert.equal(smoke.length,2);
 assert.equal(smoke[0].material,smoke[1].material);
 assert.ok(Math.abs(smoke[1].rotation.y-smoke[0].rotation.y-Math.PI/2)<1e-12,'the two original crossed smoke faces remain orthogonal');
 assert.ok(smoke.every(x=>x.geometry.type==='PlaneGeometry'&&x.geometry.getAttribute('position').count===4));
 assert.ok(a.locations.filter(x=>x!==chili).every(x=>!x.group.children.some(o=>o.name==='Authored pit smoke')));
 assert.equal(a.locations.length,20);assert.equal(a.water.length,4);
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);assert.equal(JSON.stringify(bindings),original);a.dispose();
});
test('shader has layered advected wisps, soft base/top edges and bounded alpha',()=>{
 const a=build(),chili=a.locations.find(x=>x.id==='LOC-CHILI-STABLE'),smoke=chili.group.children.find(x=>x.name==='Authored pit smoke'),shader=smoke.material.fragmentShader;
 for(const term of ['float hash(vec2 p)','float noise(vec2 p)','float coarse=noise(adv*1.8)','fine=noise(adv*4.1+vec2(11.7,-uTime*.12))','float drift=.075*sin(rise*5.7-uTime*.61)+.034*sin(rise*13.1-uTime*.27)','float birth=smoothstep(0.,.12,rise);','float fade=1.-smoothstep(.72,1.,rise);','float a=min(.22,.22*body*breakup*birth*fade);'])assert.ok(shader.includes(term),term);
 let moving=0,max=0;for(let yi=0;yi<=24;yi++)for(let xi=0;xi<=24;xi++){
  const u=xi/24,v=yi/24,p=smokeOpacity(u,v,1.3),q=smokeOpacity(u,v,3.7);
  assert.ok(Number.isFinite(p)&&Number.isFinite(q)&&p>=0&&q>=0&&p<=.22+1e-12&&q<=.22+1e-12);
  max=Math.max(max,p,q);moving=Math.max(moving,Math.abs(p-q));
  if(yi===0||yi===24)assert.ok(p<1e-12&&q<1e-12,'no hard start/end cut');
 }
 assert.ok(max>.07,'visible smoke body');assert.ok(moving>.015,'not a static alpha ribbon');
 assert.equal(JSON.stringify(bindings),original);a.dispose();
});
test('smoke advances through synthetic calm, freezes on pause, and disposes once',()=>{
 const a=build(),chili=a.locations.find(x=>x.id==='LOC-CHILI-STABLE'),smoke=chili.group.children.find(x=>x.name==='Authored pit smoke'),material=smoke.material;
 a.tick(1,{storm:0,globalCalm:true});assert.equal(material.uniforms.uTime.value,1);
 a.tick(3,{storm:0,globalCalm:true});assert.equal(material.uniforms.uTime.value,3);
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3));
 a.tick(7,{paused:true,storm:0,globalCalm:true});assert.equal(material.uniforms.uTime.value,3);
 let disposed=0;material.addEventListener('dispose',()=>disposed++);
 a.dispose();a.dispose();assert.equal(disposed,1);a.tick(20);assert.equal(material.uniforms.uTime.value,3);
 assert.equal(JSON.stringify(bindings),original);
});
